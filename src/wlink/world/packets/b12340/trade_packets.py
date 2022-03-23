import construct

from wlink.world.packets import ClientHeader, Opcode

CMSG_INITIATE_TRADE = construct.Struct(
	'header' / ClientHeader(Opcode.CMSG_INITIATE_TRADE)
)
# CMSG_BEGIN_TRADE = 0x117
# CMSG_BUSY_TRADE = 0x118
# CMSG_IGNORE_TRADE = 0x119
# CMSG_ACCEPT_TRADE = 0x11A
# CMSG_UNACCEPT_TRADE = 0x11B
# CMSG_CANCEL_TRADE = 0x11C
# CMSG_SET_TRADE_ITEM = 0x11D
# CMSG_CLEAR_TRADE_ITEM = 0x11E
# CMSG_SET_TRADE_GOLD = 0x11F
# SMSG_TRADE_STATUS = 0x120
# SMSG_TRADE_STATUS_EXTENDED = 0x121

__all__ = [
	'CMSG_INITIATE_TRADE'
]