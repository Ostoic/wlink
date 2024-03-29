from typing import Dict
from . import *


class WorldPacketParser:
    def __init__(self):
        self._parsers: Dict[Opcode, Optional[construct.Construct]] = {}

    def set_parser(self, opcode: Opcode, parser: construct.Construct):
        self._parsers[opcode] = parser

    def parse_header(self, data: bytes) -> ServerHeader:
        raise NotImplemented()

    def parse(self, data: bytes, header):
        raise NotImplemented

    def parser(self, opcode):
        return self._parsers[opcode]


class WorldServerPacketParser(WorldPacketParser):
    def __init__(self, backend=""):
        parsers = {
            Opcode.SMSG_ADDON_INFO: SMSG_ADDON_INFO,
            Opcode.SMSG_AUCTION_LIST_RESULT: SMSG_AUCTION_LIST_RESULT,
            Opcode.SMSG_AUTH_RESPONSE: SMSG_AUTH_RESPONSE,
            Opcode.SMSG_AUTH_CHALLENGE: SMSG_AUTH_CHALLENGE,
            Opcode.SMSG_BIND_POINT_UPDATE: SMSG_BIND_POINT_UPDATE,
            Opcode.SMSG_CHAR_ENUM: SMSG_CHAR_ENUM,
            Opcode.SMSG_CHAR_CREATE: SMSG_CHAR_CREATE,
            Opcode.SMSG_CHAR_RENAME: SMSG_CHAR_RENAME,
            Opcode.SMSG_CLIENTCACHE_VERSION: SMSG_CLIENTCACHE_VERSION,
            Opcode.SMSG_GUILD_QUERY_RESPONSE: SMSG_GUILD_QUERY_RESPONSE,
            Opcode.SMSG_GUILD_ROSTER: SMSG_GUILD_ROSTER,
            Opcode.SMSG_GUILD_INVITE: SMSG_GUILD_INVITE,
            Opcode.SMSG_GUILD_EVENT: SMSG_GUILD_EVENT,
            Opcode.SMSG_GUILD_INFO: SMSG_GUILD_INFO,
            Opcode.SMSG_TIME_SYNC_REQ: SMSG_TIME_SYNC_REQ,
            Opcode.SMSG_MESSAGECHAT: SMSG_MESSAGECHAT,
            Opcode.SMSG_GM_MESSAGECHAT: SMSG_GM_MESSAGECHAT,
            Opcode.SMSG_LOGIN_VERIFY_WORLD: SMSG_LOGIN_VERIFY_WORLD,
            Opcode.SMSG_MOTD: SMSG_MOTD,
            Opcode.SMSG_NAME_QUERY_RESPONSE: SMSG_NAME_QUERY_RESPONSE,
            Opcode.SMSG_PONG: SMSG_PONG,
            Opcode.SMSG_QUERY_TIME_RESPONSE: SMSG_QUERY_TIME_RESPONSE,
            Opcode.SMSG_TUTORIAL_FLAGS: SMSG_TUTORIAL_FLAGS,
            Opcode.SMSG_WARDEN_DATA: SMSG_WARDEN_DATA,
            Opcode.SMSG_INIT_WORLD_STATES: SMSG_INIT_WORLD_STATES,
            Opcode.SMSG_LOGOUT_RESPONSE: SMSG_LOGOUT_RESPONSE,
            Opcode.SMSG_LOGOUT_CANCEL_ACK: SMSG_LOGOUT_CANCEL_ACK,
            Opcode.SMSG_LOGOUT_COMPLETE: SMSG_LOGOUT_COMPLETE,
            Opcode.SMSG_GROUP_INVITE: SMSG_GROUP_INVITE,
            Opcode.SMSG_GROUP_LIST: SMSG_GROUP_LIST,
            Opcode.SMSG_GROUP_DESTROYED: SMSG_GROUP_DESTROYED,
            Opcode.SMSG_GROUP_UNINVITE: SMSG_GROUP_UNINVITE,
            Opcode.SMSG_GROUP_DECLINE: SMSG_GROUP_DECLINE,
            Opcode.SMSG_GROUP_JOINED_BATTLEGROUND: SMSG_GROUP_JOINED_BATTLEGROUND,
            Opcode.SMSG_INVALIDATE_PLAYER: SMSG_INVALIDATE_PLAYER,
            Opcode.SMSG_SERVER_MESSAGE: SMSG_SERVER_MESSAGE,
            Opcode.SMSG_NOTIFICATION: SMSG_NOTIFICATION,
            Opcode.SMSG_DUEL_REQUESTED: SMSG_DUEL_REQUESTED,
            Opcode.SMSG_DUEL_WINNER: SMSG_DUEL_WINNER,
            Opcode.SMSG_DUEL_COMPLETE: SMSG_DUEL_COMPLETE,
            # Opcode.SMSG_UPDATE_OBJECT: SMSG_UPDATE_OBJECT,
            # Opcode.SMSG_COMPRESSED_UPDATE_OBJECT: SMSG_COMPRESSED_UPDATE_OBJECT,
            Opcode.SMSG_DESTROY_OBJECT: SMSG_DESTROY_OBJECT,
            Opcode.SMSG_MAIL_LIST_RESULT: SMSG_MAIL_LIST_RESULT,
            Opcode.SMSG_SEND_MAIL_RESULT: SMSG_SEND_MAIL_RESULT,
            Opcode.SMSG_RECEIVED_MAIL: SMSG_RECEIVED_MAIL,
            Opcode.SMSG_SHOW_MAILBOX: SMSG_SHOW_MAILBOX,
            Opcode.SMSG_WHOIS: SMSG_WHOIS,
            Opcode.SMSG_WHO: SMSG_WHO,
            Opcode.SMSG_PLAY_SOUND: SMSG_PLAY_SOUND,
            Opcode.SMSG_TRANSFER_PENDING: SMSG_TRANSFER_PENDING,
            Opcode.SMSG_TRANSFER_ABORTED: SMSG_TRANSFER_ABORTED,
            Opcode.SMSG_NEW_WORLD: SMSG_NEW_WORLD,
            Opcode.SMSG_HEALTH_UPDATE: SMSG_HEALTH_UPDATE,
        }
        super().__init__()

        for opcode, parser in parsers.items():
            self.set_parser(opcode, parser)

    def parse(self, data: bytes, header):
        return self._parsers[header.opcode].parse(data)


class WorldClientPacketParser(WorldPacketParser):
    def __init__(self):
        super().__init__()
        parsers = [
            (Opcode.CMSG_PING, CMSG_PING),
            (Opcode.CMSG_GET_MAIL_LIST, CMSG_GET_MAIL_LIST),
            (Opcode.CMSG_SEND_MAIL, CMSG_SEND_MAIL),
            (Opcode.MSG_AUCTION_HELLO, MSG_AUCTION_HELLO(server=False)),
            # (Opcode.CMSG_AUCTION_LIST_BIDDER_ITEMS, CMSG_AUCTION_LIST_BIDDER_ITEMS),
            (Opcode.CMSG_AUCTION_LIST_OWNER_ITEMS, CMSG_AUCTION_LIST_OWNER_ITEMS),
            (Opcode.CMSG_AUCTION_LIST_PENDING_SALES, CMSG_AUCTION_LIST_PENDING_SALES),
            (Opcode.CMSG_AUCTION_LIST_ITEMS, CMSG_AUCTION_LIST_ITEMS),
            (Opcode.CMSG_AUCTION_PLACE_BID, CMSG_AUCTION_PLACE_BID),
            (Opcode.CMSG_AUCTION_SELL_ITEM, CMSG_AUCTION_SELL_ITEM),
            (Opcode.CMSG_GUILD_INFO_TEXT, CMSG_GUILD_INFO_TEXT),
            (Opcode.CMSG_GUILD_ROSTER, CMSG_GUILD_ROSTER),
            (Opcode.CMSG_GUILD_INFO, CMSG_GUILD_INFO),
            (Opcode.CMSG_GUILD_MOTD, CMSG_GUILD_MOTD),
            (Opcode.CMSG_GUILD_ACCEPT, CMSG_GUILD_ACCEPT),
            (Opcode.CMSG_GUILD_CREATE, CMSG_GUILD_CREATE),
            (Opcode.CMSG_GROUP_UNINVITE, CMSG_GROUP_UNINVITE),
            (Opcode.CMSG_GROUP_UNINVITE_GUID, CMSG_GROUP_UNINVITE_GUID),
            (Opcode.CMSG_GROUP_INVITE, CMSG_GROUP_INVITE),
            (Opcode.CMSG_GROUP_ACCEPT, CMSG_GROUP_ACCEPT),
            (Opcode.CMSG_GROUP_DECLINE, CMSG_GROUP_DECLINE),
            (Opcode.CMSG_GROUP_CANCEL, CMSG_GROUP_CANCEL),
            (Opcode.CMSG_GROUP_DISBAND, CMSG_GROUP_DISBAND),
            (Opcode.CMSG_CHAR_RENAME, CMSG_CHAR_RENAME),
            (Opcode.CMSG_CHAR_CREATE, CMSG_CHAR_CREATE),
            (Opcode.CMSG_WHOIS, CMSG_WHOIS),
            (Opcode.CMSG_WHO, CMSG_WHO),
            (Opcode.CMSG_WARDEN_DATA, CMSG_WARDEN_DATA),
        ]

        for opcode, parser in parsers:
            self.set_parser(opcode, parser)

    def parse(self, data: bytes, header, large=False):
        return self._parsers[header.opcode].parse(data)


__all__ = ["WorldClientPacketParser", "WorldServerPacketParser", "WorldPacketParser"]
