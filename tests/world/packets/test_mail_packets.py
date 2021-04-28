from wlink.world.packets import CMSG_GET_MAIL_LIST, MailType, SMSG_MAIL_LIST_RESULT, SMSG_RECEIVED_MAIL, \
	SMSG_SEND_MAIL_RESULT, MailResponseType, MailResponse
from wlink.guid import Guid
from wlink.world.packets.parse import WorldServerPacketParser


def test_CMSG_GET_MAIL_LIST():
	# header=Container(size=0, opcode= <Opcode.CMSG_GET_MAIL_LIST: 570>), mailbox = 215099663085715459)
	data = b'\x00\x00:\x02\x00\x00\x03\xc0\x87\x01\x010\xfc\x02'
	packet = CMSG_GET_MAIL_LIST.parse(data)

	assert packet.mailbox == Guid(value=0x2fc30010187c003)

def test_SMSG_MAIL_LIST_RESULT():
	data = b'\x008;\x02\x01\x00\x00\x00\x015\x00\x19\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)\x00\x00\x00\x87\xd6\x12\x00\x04\x00\x00\x00a\xff\xb3B\x00\x00\x00\x00asd\x00\x00\x00'
	packet = SMSG_MAIL_LIST_RESULT.parse(data)

	message = packet.mail[0]
	assert len(packet.mail) == 1
	assert packet.total_num_mail == 1
	assert message.size == 53
	assert message.id == 25
	assert message.type == MailType.normal
	assert message.sender == Guid(0x1)
	assert message.cod == 0
	assert message.stationery == 41
	assert message.money == 1234567
	assert message.checked == 4
	assert message.timestamp == 89.99878692626953
	assert message.mail_template == 0
	assert message.subject == 'asd'
	assert message.body == ''
	print(packet)

	data = b'\x02E;\x02\x04\x00\x00\x00\x04\xb3\x00\x1c\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)\x00\x00\x00\x87\xd6\x12\x00\x10\x00\x00\x00\xb5\xf6\xb3B\x00\x00\x00\x00ay\x00there man\x00\x01\x00\x01\r\x00\x00\xbc\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xba\x00\x1b\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)\x00\x00\x00\x87\xd6\x12\x00\x10\x00\x00\x00\xc6\xe7\xb3B\x00\x00\x00\x00hi\x00there\n\n\n\nogngour\x00\x01\x00\x00\r\x00\x00\xbc\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xac\x00\x1a\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xd2\x04\x00\x00\x00\x00\x00\x00)\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x8d\xf9;@\x00\x00\x00\x00haee\x00\x00\x01\x00\xba\x04\x00\x00 \n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x005\x00\x19\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)\x00\x00\x00\x87\xd6\x12\x00\x04\x00\x00\x00~\xc5\xb3B\x00\x00\x00\x00asd\x00\x00\x00'
	packet = SMSG_MAIL_LIST_RESULT.parse(data)
	mail = packet.mail

	# message 1
	assert mail[0].size == 179
	assert mail[0].id == 28
	assert mail[0].type == MailType.normal
	assert mail[0].sender == Guid(0x1)
	assert mail[0].cod == 0
	assert mail[0].stationery == 41
	assert mail[0].money == 1234567
	assert mail[0].checked == 16
	assert mail[0].timestamp == 89.98184967041016
	assert mail[0].mail_template == 0
	assert mail[0].subject == 'ay'
	assert mail[0].body == 'there man'
	assert mail[0].sent_items[0].index == 0
	assert mail[0].sent_items[0].guid_low == 3329
	assert mail[0].sent_items[0].entry == 4540
	assert mail[0].sent_items[0].property_id == 0
	assert mail[0].sent_items[0].suffix_factor == 0
	assert mail[0].sent_items[0].count == 1
	assert mail[0].sent_items[0].charges == 4294967295
	assert mail[0].sent_items[0].max_durability == 0
	assert mail[0].sent_items[0].durability == 0

	# message 3
	assert mail[2].size == 172
	assert mail[2].id == 26
	assert mail[2].type == MailType.normal
	assert mail[2].sender == Guid(0x1)
	assert mail[2].cod == 1234
	assert mail[2].stationery == 41
	assert mail[2].money == 0
	assert mail[2].checked == 4
	assert mail[2].timestamp == 2.9371063709259033
	assert mail[2].mail_template == 0
	assert mail[2].subject == 'haee'
	assert mail[2].body == ''
	assert mail[2].sent_items[0].index == 0
	assert mail[2].sent_items[0].guid_low == 1210
	assert mail[2].sent_items[0].entry == 2592
	assert mail[2].sent_items[0].property_id == 0
	assert mail[2].sent_items[0].suffix_factor == 0
	assert mail[2].sent_items[0].count == 1
	assert mail[2].sent_items[0].charges == 0
	assert mail[2].sent_items[0].max_durability == 0
	assert mail[2].sent_items[0].durability == 0
	print(packet)

def test_SMSG_RECEIVED_MAIL():
	data = b'\x00\x06\x85\x02\x00\x00\x00\x00'
	packet = SMSG_RECEIVED_MAIL.parse(data)
	print(packet)

	assert packet.unk == 0

def test_SMSG_SEND_MAIL_RESULT():
	data = b'\x00\x0e9\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	packet = SMSG_SEND_MAIL_RESULT.parse(data)
	print(packet)

	assert packet.mail_id == 0
	assert packet.mail_action == MailResponseType.send
	assert packet.mail_response == MailResponse.ok
