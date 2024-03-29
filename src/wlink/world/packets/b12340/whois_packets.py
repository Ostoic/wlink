from typing import List

import construct

from .opcode import Opcode
from .character_enum_packets import CombatClass, Race, Gender
from .headers import ClientHeader, ServerHeader, is_large_server_packet
from wlink.utility.construct import PackEnum

CMSG_WHOIS = construct.Struct(
    "header" / ClientHeader(Opcode.CMSG_WHOIS), "name" / construct.CString("ascii")
)


def make_CMSG_WHOIS(name: str):
    return CMSG_WHOIS.build(dict(header=dict(size=4 + len(name) + 1), name=name))


SMSG_WHOIS = construct.Struct(
    "header" / ServerHeader(Opcode.SMSG_WHOIS), "message" / construct.CString("utf8")
)


def make_SMSG_WHOIS(name: str):
    is_large = is_large_server_packet(len(name) + 1)
    return SMSG_WHOIS.build(
        dict(header=dict(size=(3 if is_large else 2) + len(name) + 1), name=name)
    )


# WHO is a non-privileged ingame character query
CMSG_WHO = construct.Struct(
    "header"
    / ClientHeader(
        Opcode.CMSG_WHO, body_size=4 + 4 + 0 + 1 + 4 + 4 + 4 + 4 * 0 + 4 + (0 + 1) * 0
    ),
    "min_level" / construct.Default(construct.Int32ul, 1),
    "max_level" / construct.Default(construct.Int32ul, 80),
    "name" / construct.CString("utf8"),
    "guild_name" / construct.Default(construct.CString("utf8"), ""),
    "race" / construct.Default(construct.Int32ul, 0),
    "combat_class" / construct.Default(construct.Int32ul, 0),
    "zones"
    / construct.Default(  # max length is 10 (TODO: check overflow)
        construct.PrefixedArray(construct.Int32ul, construct.Int32ul), []
    ),
    "search_terms"
    / construct.Default(  # max num of strings is 4 (TODO: check overflow)
        construct.PrefixedArray(construct.Int32ul, construct.CString("utf8")), []
    ),
)


def make_CMSG_WHO(
    name: str = "",
    guild_name: str = "",
    race=None,
    combat_class=None,
    min_level=1,
    max_level=80,
    zones=(),
    search_terms=(),
):
    size = len(name) + 1
    size += len(guild_name) + 1
    size += 4 * 4  # min level, max level, race, combat_class

    size += 4
    for zone in zones:
        size += len(zone) + 1

    size += 4
    for term in search_terms:
        size += len(term) + 1

    return CMSG_WHO.build(
        dict(
            header=dict(size=4 + size),
            name=name,
            race=race,
            combat_class=combat_class,
            min_level=min_level,
            max_level=max_level,
            guild_name=guild_name,
            zones=zones,
            search_terms=search_terms,
        )
    )


WhoMatchInfo = construct.Struct(
    "name" / construct.CString("utf8"),
    "guild" / construct.CString("utf8"),
    "level" / construct.Int32ul,
    "combat_class" / PackEnum(CombatClass),
    "race" / PackEnum(Race),
    "gender" / PackEnum(Gender),
    "zone_id" / construct.Int32ul,
)

SMSG_WHO = construct.Struct(
    "header" / ServerHeader(Opcode.SMSG_WHO),
    # 'total_num_matches' / construct.Int32ul,
    "matches" / construct.PrefixedArray(construct.Int32ul, WhoMatchInfo),
)


def make_SMSG_WHO(matches: list):
    is_large = is_large_server_packet(len(matches) + 1)
    return SMSG_WHO.build(
        dict(
            header=dict(size=(3 if is_large else 2) + len(matches) + 1), matches=matches
        )
    )


__all__ = [
    "SMSG_WHO",
    "SMSG_WHOIS",
    "CMSG_WHOIS",
    "CMSG_WHO",
    "WhoMatchInfo",
    "make_CMSG_WHO",
    "make_CMSG_WHOIS",
    "make_SMSG_WHOIS",
]
