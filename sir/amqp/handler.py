#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2014 Wieland Hoffmann
# License: MIT, see LICENSE for details
from . import message
from ..schema import SCHEMA
from ..indexing import send_data_to_solr
from ..util import (create_amqp_connection,
                    db_session,
                    db_session_ctx,
                    solr_connection,
                    solr_version_check)
from amqp.exceptions import AMQPError
from functools import partial, wraps
from logging import getLogger
from retrying import retry
from socket import error as socket_error
from sqlalchemy import and_
from urllib2 import URLError


logger = getLogger("sir")


_DEFAULT_MB_RETRIES = 4
_RETRY_WAIT_SECS = 30


def callback_wrapper(f):
    """
    Wraps a function ``f`` to provide basic exception handling around it.

    The following wrapper function is returned:

    .. py:function:: wrapper(self, msg, queue)

        :param sir.amqp.handler.Handler self:
        :param sir.amqp.message.Message msg:
        :param str queue:

        Calls ``f`` with ``self`` and  an instance of
        :class:`~sir.amqp.message.Message`.
        If an exception gets raised by ``f``, it will be caught and the
        message will be :meth:`rejected
        <amqp:amqp.channel.Channel.basic_reject>` and sent to the
        ``search.failed`` queue (cf. :ref:`queue_setup`).
        Then the exception will not be reraised.

        If no exception is raised, the message will be :meth:`acknowledged
        <amqp:amqp.channel.Channel.basic_ack>`.

    """
    @wraps(f)
    def wrapper(self, msg, queue):
        try:
            parsed_message = message.Message.from_amqp_message(queue, msg)
            f(self=self, parsed_message=parsed_message)
        except Exception as exc:
            logger.error(exc)

            msg.channel.basic_reject(msg.delivery_tag, requeue=False)

            retries_remaining = msg.application_headers.get("mb-retries",
                                                            _DEFAULT_MB_RETRIES)
            routing_key = msg.delivery_info["routing_key"]
            if retries_remaining:
                msg.application_headers["mb-retries"] = retries_remaining - 1
                msg.application_headers["mb-exception"] = str(exc)
                msg.channel.basic_publish(msg, exchange="search.retry",
                                          routing_key=routing_key)
            else:
                msg.channel.basic_publish(msg, exchange="search.failed",
                                          routing_key=routing_key)
        else:
            msg.channel.basic_ack(msg.delivery_tag)

    return wrapper


class Handler(object):
    """
    This class is used to provide callbacks for AMQP messages and access to
    Solr cores.
    """
    def __init__(self):
        self.cores = {}  #: Maps entity type names to Solr cores
        for corename in SCHEMA.keys():
            self.cores[corename] = solr_connection(corename)
            solr_version_check(corename)

        self.session = db_session()  #: The database session used by this handler

    @callback_wrapper
    def index_callback(self, parsed_message):
        entity = SCHEMA[parsed_message.entity_type]
        converter = entity.query_result_to_dict
        query = entity.query

        condition = and_(entity.model.id.in_(parsed_message.ids))

        with db_session_ctx(self.session) as session:
            query = query.filter(condition).with_session(session)
            send_data_to_solr(self.cores[parsed_message.entity_type],
                              map(lambda obj: converter(obj), query.all()))

    @callback_wrapper
    def delete_callback(self, parsed_message):
        logger.debug("Deleting {entity_type}: {ids}".format(
            entity_type=parsed_message.entity_type,
            ids=parsed_message.ids))
        self.cores[parsed_message.entity_type].delete_many(parsed_message.ids)


def _should_retry(exc):
    logger.exception(exc)
    if isinstance(exc, AMQPError) or isinstance(exc, socket_error):
        logger.info("Retrying in %i seconds", _RETRY_WAIT_SECS)
        return True

    return False


@retry(wait_fixed=_RETRY_WAIT_SECS * 1000, retry_on_exception=_should_retry)
def _watch_impl():
    conn = create_amqp_connection()
    logger.info("Connection to RabbitMQ established")
    ch = conn.channel()

    handler = Handler()

    def add_handler(queue, f):
        logger.info("Adding a callback to %s", queue)
        handler = partial(f, queue=queue)
        ch.basic_consume(queue, callback=handler)

    add_handler("search.index", handler.index_callback)
    add_handler("search.delete", handler.delete_callback)

    while ch.callbacks:
        ch.wait()


def watch(args):
    """
    Watch AMQP queues for messages.

    :param args: will be ignored
    """
    try:
        create_amqp_connection()
    except socket_error as e:
        logger.error("Couldn't connect to RabbitMQ, check your settings")
        logger.error("The error was: %s", e)
        return

    try:
        _watch_impl()
    except URLError as e:
        logger.info("Connecting to Solr failed: %s", e)
        return
