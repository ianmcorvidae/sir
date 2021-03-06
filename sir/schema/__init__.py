# Copyright (c) 2014 Wieland Hoffmann
# License: MIT, see LICENSE for details
from . import modelext
from .searchentities import SearchEntity as E, SearchField as F
from ..wscompat import convert
from mbdata import models


SearchLabel = E(modelext.CustomLabel, [
    F("mbid", "gid"),
    F("label", "name"),
    F("alias", "aliases.name"),
    F("area", "area.name"),
    #F("begin", "begin_data"),
    #F("end", "end_date")
    F("comment", "comment"),
    F("ipi", "ipis.ipi"),
    F("type", "type.name")
],
    1.2,
    convert.convert_label,
)


SearchRecording = E(modelext.CustomRecording, [
    # F("date", "tracks.medium.release.country_dates.country.date"),
    F("arid", "artist_credit.artists.artist.gid"),
    F("artist", "artist_credit.name"),
    F("artistname", "artist_credit.artists.artist.name"),
    F("comment", "comment"),
    F("country", "tracks.medium.release.country_dates.country.area.name"),
    F("creditname", "artist_credit.artists.name"),
    F("dur", "length"),
    F("format", "tracks.medium.format.name"),
    F("isrc", "isrcs.isrc"),
    F("mbid", "gid"),
    F("number", "tracks.number"),
    F("position", "tracks.medium.position"),
    F("primarytype", "tracks.medium.release.release_group.type.name"),
    F("recording", "name"),
    F("reid", "tracks.medium.release.gid"),
    F("release", "tracks.medium.release.name"),
    F("rgid", "tracks.medium.release.release_group.gid"),
    F("secondarytype",
      "tracks.medium.release.release_group.secondary_types.secondary_type.name"),
    F("status", "tracks.medium.release.status.name"),
    F("tid", "tracks.gid"),
    F("tnum", "tracks.position"),
    F("tracks", "tracks.medium.track_count"),
    F("tracksrelease", "tracks.medium.release.mediums.track_count",
        transformfunc=lambda values: reduce(lambda x, y: x+y, values, 0)),
    F("video", "video")
],
    1.2,
    convert.convert_recording,
    extrapaths=["artist_credit.artists.artist.aliases.begin_date_day",
                "artist_credit.artists.artist.aliases.begin_date_month",
                "artist_credit.artists.artist.aliases.begin_date_year",
                "artist_credit.artists.artist.aliases.end_date_day",
                "artist_credit.artists.artist.aliases.end_date_month",
                "artist_credit.artists.artist.aliases.end_date_year",
                "artist_credit.artists.artist.aliases.locale",
                "artist_credit.artists.artist.aliases.name",
                "artist_credit.artists.artist.aliases.primary_for_locale",
                "artist_credit.artists.artist.aliases.sort_name",
                "artist_credit.artists.artist.aliases.type.id",
                "artist_credit.artists.artist.aliases.type.name",
                "artist_credit.artists.artist.comment",
                "artist_credit.artists.artist.gid",
                "artist_credit.artists.artist.name",
                "artist_credit.artists.artist.sort_name",
                "artist_credit.artists.join_phrase",
                "artist_credit.artists.name",
                "artist_credit.name",
                "tags.count",
                "tags.tag.name",
                "tracks.length",
                "tracks.medium.cdtocs.id",
                "tracks.medium.release.artist_credit.artists.artist.aliases.begin_date_day",
                "tracks.medium.release.artist_credit.artists.artist.aliases.begin_date_month",
                "tracks.medium.release.artist_credit.artists.artist.aliases.begin_date_year",
                "tracks.medium.release.artist_credit.artists.artist.aliases.end_date_day",
                "tracks.medium.release.artist_credit.artists.artist.aliases.end_date_month",
                "tracks.medium.release.artist_credit.artists.artist.aliases.end_date_year",
                "tracks.medium.release.artist_credit.artists.artist.aliases.locale",
                "tracks.medium.release.artist_credit.artists.artist.aliases.name",
                "tracks.medium.release.artist_credit.artists.artist.aliases.primary_for_locale",
                "tracks.medium.release.artist_credit.artists.artist.aliases.sort_name",
                "tracks.medium.release.artist_credit.artists.artist.aliases.type.id",
                "tracks.medium.release.artist_credit.artists.artist.aliases.type.name",
                "tracks.medium.release.artist_credit.artists.artist.comment",
                "tracks.medium.release.artist_credit.artists.artist.gid",
                "tracks.medium.release.artist_credit.artists.artist.name",
                "tracks.medium.release.artist_credit.artists.artist.sort_name",
                "tracks.medium.release.artist_credit.artists.join_phrase",
                "tracks.medium.release.artist_credit.artists.name",
                "tracks.medium.release.artist_credit.name",
                "tracks.medium.release.comment",
                "tracks.medium.release.country_dates.country.area.gid",
                "tracks.medium.release.country_dates.country.area.iso_3166_1_codes.code",
                "tracks.medium.release.country_dates.country.area.name",
                "tracks.medium.release.country_dates.date_day",
                "tracks.medium.release.country_dates.date_month",
                "tracks.medium.release.country_dates.date_year",
                "tracks.medium.release.release_group.comment",
                "tracks.medium.release.release_group.name",
                "tracks.name"
    ]
)


SearchRelease = E(models.Release, [
    F("mbid", "gid"),
    F("release", "name"),
    F("arid", "artist_credit.artists.artist.gid"),
    F("country", "country_dates.country.area.name"),
    #F("data", "country_dates.date")
    F("comment", "comment"),
    F("lang", "language.name"),
    F("script", "script.name")
],
    1.2,
    convert.convert_release,
    extrapaths=["artist_credit.artists.name",
                "artist_credit.artists.join_phrase",
                "artist_credit.name",
                "artist_credit.artists.artist.aliases.begin_date_day",
                "artist_credit.artists.artist.aliases.begin_date_month",
                "artist_credit.artists.artist.aliases.begin_date_year",
                "artist_credit.artists.artist.aliases.end_date_day",
                "artist_credit.artists.artist.aliases.end_date_month",
                "artist_credit.artists.artist.aliases.end_date_year",
                "artist_credit.artists.artist.aliases.locale",
                "artist_credit.artists.artist.aliases.name",
                "artist_credit.artists.artist.aliases.primary_for_locale",
                "artist_credit.artists.artist.aliases.sort_name",
                "artist_credit.artists.artist.aliases.type.id",
                "artist_credit.artists.artist.aliases.type.name",
                "artist_credit.artists.artist.gid",
                "artist_credit.artists.artist.name",
                "artist_credit.artists.artist.sort_name",
                "barcode",
                "country_dates.country.area.gid",
                "country_dates.country.area.name",
                "country_dates.country.area.iso_3166_1_codes.code",
                "country_dates.date_day",
                "country_dates.date_month",
                "country_dates.date_year",
                "labels.catalog_number",
                "labels.label.gid",
                "labels.label.name",
                "mediums.format.name",
                "mediums.cdtocs.id",
                "mediums.track_count",
                "packaging.name",
                "release_group.comment",
                "release_group.gid",
                "release_group.name",
                "release_group.secondary_types.secondary_type.name",
                "release_group.type.name",
                "status.name",
                "language.iso_code_3",
                "script.iso_code",
                "tags.count",
                "tags.tag.name"]
)


SearchReleaseGroup = E(modelext.CustomReleaseGroup, [
    F("mbid", "gid"),
    F("release-group", "name"),
    # F("release", "releases.name"),
    F("reid", "releases.gid"),
    F("releases", "releases.gid", transformfunc=len),
    F("credit-name", "artist_credit.artists.artist.name")
],
    1.2,
    convert.convert_release_group,
    extrapaths = ["artist_credit.artists.name",
                  "artist_credit.artists.join_phrase", "artist_credit.name",
                  "artist_credit.artists.artist.aliases.begin_date_day",
                  "artist_credit.artists.artist.aliases.begin_date_month",
                  "artist_credit.artists.artist.aliases.begin_date_year",
                  "artist_credit.artists.artist.aliases.end_date_day",
                  "artist_credit.artists.artist.aliases.end_date_month",
                  "artist_credit.artists.artist.aliases.end_date_year",
                  "artist_credit.artists.artist.aliases.locale",
                  "artist_credit.artists.artist.aliases.name",
                  "artist_credit.artists.artist.aliases.primary_for_locale",
                  "artist_credit.artists.artist.aliases.sort_name",
                  "artist_credit.artists.artist.aliases.type.id",
                  "artist_credit.artists.artist.aliases.type.name",
                  "artist_credit.artists.artist.gid",
                  "artist_credit.artists.artist.name",
                  "artist_credit.artists.artist.sort_name",
                  "type.name", "secondary_types.secondary_type.name",
                  "tags.count",
                  "tags.tag.name",
                  "releases.name",
                  "releases.status.name"
]
)

SearchArtist = E(modelext.CustomArtist, [
    F("mbid", "gid"),
    F("name", "name"),
    F("alias", "aliases.name"),
    F("area", ["area.name", "area.aliases.name"]),
    F("beginarea", ["begin_area.name", "begin_area.aliases.name"]),
    F("endarea", ["end_area.name", "end_area.aliases.name"]),
    F("comment", "comment"),
    F("ipi", "ipis.ipi"),
    F("type", "type.name")
],
    1.2,
    convert.convert_artist,
    extrapaths=["area.iso_3166_1_codes.code", "tags.count", "tags.tag.name",
                "aliases.type.name", "aliases.type.id", "aliases.sort_name",
                "aliases.locale", "aliases.primary_for_locale",
                "begin_area.gid", "area.gid", "end_area.gid"]

)


SearchWork = E(modelext.CustomWork, [
    F("mbid", "gid"),
    F("name", "name"),
    F("alias", "aliases.name"),
    F("arid", "artist_links.artist.gid"),
    F("artist", "artist_links.artist.name"),
    F("comment", "comment"),
    F("iswc", "iswcs.iswc"),
    F("language", "language.name"),
],
    1.2,
    convert.convert_work,
    extrapaths=["aliases.type.name", "aliases.type.id",
                "aliases.sort_name", "aliases.locale",
                "aliases.primary_for_locale",
                "artist_links.link.link_type.name",
                "artist_links.link.attributes.attribute_type.name"]
)


SCHEMA = {
    "artist": SearchArtist,
    "label": SearchLabel,
    "recording": SearchRecording,
    "release": SearchRelease,
    "release-group": SearchReleaseGroup,
    "work": SearchWork,
}
