from wlink.world.packets import SMSG_GROUP_INVITE, Opcode, SMSG_GROUP_LIST


def test_group_invite():
	data = b'\x00\x10o\x00\x01Act\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	packet = SMSG_GROUP_INVITE.parse(data)
	print(packet)

	assert packet.header.opcode == Opcode.SMSG_GROUP_INVITE
	assert packet.in_group == True
	assert packet.inviter == 'Act'

def test_group_list():
	data = b'\x00>}\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00P\x1fC\x00\x00\x00\x01\x00\x00\x00Imbued\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00'
	packet = SMSG_GROUP_LIST.parse(data)
	print(packet)
