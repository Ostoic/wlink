from enum import Enum
from typing import Optional

import construct

from wlink.utility.construct import PackEnum, GuidConstruct
from .headers import ClientHeader, ServerHeader
from .opcode import Opcode
from wlink.guid import Guid, GuidType

class Language(Enum):
    universal = 0
    orcish = 1
    darnassian = 2
    taurahe = 3
    dwarvish = 6
    common = 7
    demonic = 8
    tita = 9
    thalassian = 10
    draconic = 11
    kalimag = 12
    gnomish = 13
    troll = 14
    gutterspeak = 33
    draenai = 35
    zombie = 36
    gnomish_binary = 37
    goblin_binary = 38
    worgen = 39
    goblin = 40
    addon = -1

class MessageType(Enum):
    system = 0x00
    say = 0x01
    party = 0x02
    raid = 0x03
    guild = 0x04
    officer = 0x05
    yell = 0x06
    whisper = 0x07
    whisper_foreign = 0x08
    whisper_inform = 0x09
    emote = 0x0a
    text_emote = 0x0b
    monster_say = 0x0c
    monster_party = 0x0d
    monster_yell = 0x0e
    monster_whisper = 0x0f
    monster_emote = 0x10
    channel = 0x11
    channel_join = 0x12
    channel_leave = 0x13
    channel_list = 0x14
    channel_notice = 0x15
    channel_notice_user = 0x16
    afk = 0x17
    dnd = 0x18
    ignored = 0x19
    skill = 0x1a
    loot = 0x1b
    money = 0x1c
    opening = 0x1d
    tradeskills = 0x1e
    pet_info = 0x1f
    combat_misc_info = 0x20
    combat_xp_gain = 0x21
    combat_honor_gain = 0x22
    combat_faction_change = 0x23
    bg_system_neutral = 0x24
    bg_system_alliance = 0x25
    bg_system_horde = 0x26
    raid_leader = 0x27
    raid_warning = 0x28
    raid_boss_emote = 0x29
    raid_boss_whisper = 0x2a
    filtered = 0x2b
    battleground = 0x2c
    battleground_leader = 0x2d
    restricted = 0x2e
    battlenet = 0x2f
    achievement = 0x30
    guild_achievement = 0x31
    arena_points = 0x32
    party_leader = 0x33
    addon = 0xFFFFFFFF

CMSG_MESSAGECHAT = construct.Struct(
    'header' / ClientHeader(Opcode.CMSG_MESSAGECHAT, 0),
    'message_type' / PackEnum(MessageType, construct.Int32sl),
    'language' / PackEnum(Language, construct.Int32sl),
    'channel' / construct.If(
        construct.this.message_type == MessageType.channel,
        construct.CString('utf-8')
    ),
    'receiver' / construct.If(
        construct.this.message_type == MessageType.whisper,
        construct.CString('utf-8')
    ),
    'text' / construct.CString('utf-8')
)

def make_CMSG_MESSAGECHAT(
    text: str, message_type,
    language, recipient: Optional[str] = None,
    channel: Optional[str] = None
):
    size = 4 + 4 + len(text)
    if message_type in (MessageType.whisper, MessageType.channel):
        size += max(len(channel) if channel else 0, len(recipient))

    return CMSG_MESSAGECHAT.build(dict(
        header={'size': size + 5},
        text=text, message_type=message_type, language=language,
        receiver=recipient, channel=channel
    ))

MonsterMessage = construct.Struct(
    'sender' / construct.Prefixed(construct.Int32ul, construct.CString('ascii')),
    'receiver_guid' / GuidConstruct(Guid),
    'receiver' / construct.If(
        construct.this.receiver_guid != Guid() and construct.this.receiver_guid.type not in (GuidType.player, GuidType.pet),
        construct.Prefixed(construct.Int32ul, construct.CString('ascii'))
    ),
)

WhisperForeign = construct.Struct(
    'sender' / construct.Prefixed(construct.Int32ul, construct.CString('ascii')),
    'receiver_guid' / GuidConstruct(Guid),
)

BGMessage = construct.Struct(
    'receiver_guid' / GuidConstruct(Guid),
    'receiver' / construct.If(
        construct.this.receiver_guid != Guid() and construct.this.receiver_guid.type != GuidType.player,
        construct.Prefixed(construct.Int32ul, construct.CString('ascii'))
    ),
)

AchievementMessage = construct.Struct(
    'receiver_guid' / GuidConstruct(Guid),
)


def ChannelMessage(gm_chat=False):
    if gm_chat:
        return construct.Struct(
            'sender' / construct.Prefixed(construct.Int32ul, construct.CString('ascii')),
            'channel' / construct.CString('ascii'),
            'receiver_guid' / GuidConstruct(Guid),
        )
    else:
        return construct.Struct(
            'channel' / construct.CString('ascii'),
            'receiver_guid' / GuidConstruct(Guid),
        )

def DefaultMessage(gm_chat=False):
    if gm_chat:
        return construct.Struct(
            'sender' / construct.Prefixed(construct.Int32ul, construct.CString('ascii')),
            'receiver_guid' / GuidConstruct(Guid),
        )
    else:
        return construct.Struct(
            'receiver_guid' / GuidConstruct(Guid),
        )

def make_messagechat_packet(gm_chat=False):
    return construct.Struct(
        'header' / ServerHeader(Opcode.SMSG_GM_MESSAGECHAT if gm_chat else Opcode.SMSG_MESSAGECHAT, 0),
        'message_type' / PackEnum(MessageType, construct.Int8sl),
        'language' / PackEnum(Language, construct.Int32sl),
        'sender_guid' / GuidConstruct(Guid),
        'flags' / construct.Default(construct.Int32ul, 0),
        'info' / construct.Switch(
            construct.this.message_type, {
                MessageType.monster_say: MonsterMessage,
                MessageType.monster_emote: MonsterMessage,
                MessageType.monster_party: MonsterMessage,
                MessageType.monster_yell: MonsterMessage,
                MessageType.monster_whisper: MonsterMessage,
                MessageType.raid_boss_emote: MonsterMessage,
                MessageType.raid_boss_whisper: MonsterMessage,

                MessageType.whisper_foreign: WhisperForeign,

                MessageType.bg_system_alliance: BGMessage,
                MessageType.bg_system_horde: BGMessage,
                MessageType.bg_system_neutral: BGMessage,

                MessageType.achievement: AchievementMessage,
                MessageType.guild_achievement: AchievementMessage,

                MessageType.channel: ChannelMessage(gm_chat=gm_chat),

            }, default=DefaultMessage(gm_chat=gm_chat)
        ),

        'text' / construct.Prefixed(construct.Int32ul, construct.CString('utf-8')),
        'chat_tag' / construct.Byte, # 4 appears when a GM has their chat tag visible
        'achievement_id' / construct.Switch(
            construct.this.message_type, {
                MessageType.achievement: construct.Int32ul,
                MessageType.guild_achievement: construct.Int32ul,
            }
        )
    )

SMSG_GM_MESSAGECHAT = make_messagechat_packet(gm_chat=True)
SMSG_MESSAGECHAT = make_messagechat_packet(gm_chat=False)

# def make_SMSG_MESSAGECHAT() -> SMSG_MESSAGECHAT:
# 	return SMSG_MESSAGECHAT.build(dict())

SMSG_EMOTE = construct.Struct(
    'header' / ServerHeader(Opcode.SMSG_EMOTE),
    'emote_id' / construct.Int32ul,
    'guid' / GuidConstruct(Guid),
)


class ChannelFlags(Enum):
    CHANNEL_FLAG_NONE       = 0x00
    CHANNEL_FLAG_CUSTOM     = 0x01
    # // 0x02
    CHANNEL_FLAG_TRADE      = 0x04
    CHANNEL_FLAG_NOT_LFG    = 0x08
    CHANNEL_FLAG_GENERAL    = 0x10
    CHANNEL_FLAG_CITY       = 0x20
    CHANNEL_FLAG_LFG        = 0x40
    CHANNEL_FLAG_VOICE      = 0x80
    # // General                  0x18 = 0x10 | 0x08
    # // Trade                    0x3C = 0x20 | 0x10 | 0x08 | 0x04
    # // LocalDefence             0x18 = 0x10 | 0x08
    # // GuildRecruitment         0x38 = 0x20 | 0x10 | 0x08
    # // LookingForGroup          0x50 = 0x40 | 0x10

class ChatNotifyType(Enum):
    CHAT_JOINED_NOTICE                = 0x00           #  "%s joined channel.";
    CHAT_LEFT_NOTICE                  = 0x01           #  "%s left channel.";
    # CHAT_SUSPENDED_NOTICE             = 0x01         # "%s left channel.";
    CHAT_YOU_JOINED_NOTICE            = 0x02           #  "Joined Channel: [%s]"; -- You joined
    # CHAT_YOU_CHANGED_NOTICE           = 0x02         # "Changed Channel: [%s]";
    CHAT_YOU_LEFT_NOTICE              = 0x03           #  "Left Channel: [%s]"; -- You left
    CHAT_WRONG_PASSWORD_NOTICE        = 0x04           #  "Wrong password for %s.";
    CHAT_NOT_MEMBER_NOTICE            = 0x05           #  "Not on channel %s.";
    CHAT_NOT_MODERATOR_NOTICE         = 0x06           #  "Not a moderator of %s.";
    CHAT_PASSWORD_CHANGED_NOTICE      = 0x07           #  "[%s] Password changed by %s.";
    CHAT_OWNER_CHANGED_NOTICE         = 0x08           #  "[%s] Owner changed to %s.";
    CHAT_PLAYER_NOT_FOUND_NOTICE      = 0x09           #  "[%s] Player %s was not found.";
    CHAT_NOT_OWNER_NOTICE             = 0x0A           #  "[%s] You are not the channel owner.";
    CHAT_CHANNEL_OWNER_NOTICE         = 0x0B           #  "[%s] Channel owner is %s.";
    CHAT_MODE_CHANGE_NOTICE           = 0x0C           #
    CHAT_ANNOUNCEMENTS_ON_NOTICE      = 0x0D           #  "[%s] Channel announcements enabled by %s.";
    CHAT_ANNOUNCEMENTS_OFF_NOTICE     = 0x0E           #  "[%s] Channel announcements disabled by %s.";
    CHAT_MODERATION_ON_NOTICE         = 0x0F           #  "[%s] Channel moderation enabled by %s.";
    CHAT_MODERATION_OFF_NOTICE        = 0x10           #  "[%s] Channel moderation disabled by %s.";
    CHAT_MUTED_NOTICE                 = 0x11           #  "[%s] You do not have permission to speak.";
    CHAT_PLAYER_KICKED_NOTICE         = 0x12           # "[%s] Player %s kicked by %s.";
    CHAT_BANNED_NOTICE                = 0x13           #  "[%s] You are bannedStore from that channel.";
    CHAT_PLAYER_BANNED_NOTICE         = 0x14           # "[%s] Player %s bannedStore by %s.";
    CHAT_PLAYER_UNBANNED_NOTICE       = 0x15           # "[%s] Player %s unbanned by %s.";
    CHAT_PLAYER_NOT_BANNED_NOTICE     = 0x16           #  "[%s] Player %s is not bannedStore.";
    CHAT_PLAYER_ALREADY_MEMBER_NOTICE = 0x17           #  "[%s] Player %s is already on the channel.";
    CHAT_INVITE_NOTICE                = 0x18           #  "%2$s has invited you to join the channel '%1$s'.";
    CHAT_INVITE_WRONG_FACTION_NOTICE  = 0x19           #  "Target is in the wrong alliance for %s.";
    CHAT_WRONG_FACTION_NOTICE         = 0x1A           #  "Wrong alliance for %s.";
    CHAT_INVALID_NAME_NOTICE          = 0x1B           #  "Invalid channel name";
    CHAT_NOT_MODERATED_NOTICE         = 0x1C           #  "%s is not moderated";
    CHAT_PLAYER_INVITED_NOTICE        = 0x1D           #  "[%s] You invited %s to join the channel";
    CHAT_PLAYER_INVITE_BANNED_NOTICE  = 0x1E           #  "[%s] %s has been bannedStore.";
    CHAT_THROTTLED_NOTICE             = 0x1F           #  "[%s] The number of messages that can be sent to this channel is limited, please wait to send another message.";
    CHAT_NOT_IN_AREA_NOTICE           = 0x20           #  "[%s] You are not in the correct area for this channel."; -- The user is trying to send a chat to a zone specific channel, and they're not physically in that zone.
    CHAT_NOT_IN_LFG_NOTICE            = 0x21           #  "[%s] You must be queued in looking for group before joining this channel."; -- The user must be in the looking for group system to join LFG chat channels.
    CHAT_VOICE_ON_NOTICE              = 0x22           #  "[%s] Channel voice enabled by %s.";
    CHAT_VOICE_OFF_NOTICE             = 0x23            #  "[%s] Channel voice disabled by %s.";

JoinedNotice = construct.Struct(
    'guid' / GuidConstruct(Guid),
)

YouJoinedNotice = construct.Struct(
    'flags' / construct.Byte,
    'channel_id' / construct.Int32ul,
    construct.Padding(4),
)

NotifyInfo = construct.Struct(
    'type' / PackEnum(ChatNotifyType),
    'name' / construct.CString('ascii'),
    construct.Switch(
        construct.this.type, {
            ChatNotifyType.CHAT_JOINED_NOTICE: JoinedNotice,
            ChatNotifyType.CHAT_YOU_LEFT_NOTICE: YouJoinedNotice,
        }
    )
)

SMSG_CHANNEL_NOTIFY = construct.Struct(
    'header' / ServerHeader(Opcode.SMSG_CHANNEL_NOTIFY),
    'notification' / NotifyInfo
)

__all__ = [
    'SMSG_EMOTE', 'SMSG_MESSAGECHAT', 'SMSG_GM_MESSAGECHAT', 'MessageType', 'CMSG_MESSAGECHAT', 'ChannelMessage',
    'AchievementMessage', 'BGMessage', 'MonsterMessage', 'DefaultMessage', 'WhisperForeign', 'Language'
]