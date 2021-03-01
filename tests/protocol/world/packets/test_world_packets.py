from prowl.guid import Guid, GuidType
from prowl.protocol.world.packets import SMSG_LOGIN_VERIFY_WORLD, SMSG_LOGOUT_RESPONSE, SMSG_NOTIFICATION, \
	SMSG_CLIENTCACHE_VERSION, SMSG_TUTORIAL_FLAGS, SMSG_ADDON_INFO, SMSG_CHAR_ENUM, Race, Gender, CombatClass, \
	CMSG_CHAR_ENUM, CMSG_PLAYER_LOGIN, SMSG_TIME_SYNC_REQ, CMSG_TIME_SYNC_RESP, CMSG_NAME_QUERY, \
	SMSG_NAME_QUERY_RESPONSE, Opcode, SMSG_INIT_WORLD_STATES, SMSG_BIND_POINT_UPDATE, SMSG_MOTD


def test_SMSG_LOGIN_VERIFY_WORLD():
	data = b'\x00\x166\x02\x01\x00\x00\x00ke\xb7E\x7f\xb3\x82\xc5D\xb7\xceD\xa0\xf8E@'
	packet = SMSG_LOGIN_VERIFY_WORLD.parse(data)
	print(packet)

	assert packet.map == 1
	assert packet.position.x == 1653.72705078125
	assert packet.position.y == -4182.43701171875
	assert packet.position.z == 5868.67724609375
	assert packet.rotation == 3.0932998657226562

def test_SMSG_LOGOUT_RESPONSE():
	data = b'\x00\x07L\x00\x00\x00\x00\x00\x01'
	packet = SMSG_LOGOUT_RESPONSE.parse(data)

	assert packet.header.size == 7
	assert packet.reason == 0
	assert packet.instant_logout is True

def test_SMSG_NOTIFICATION():
	data = b'\x00\x13\xcb\x01Unknown language\x00'
	packet = SMSG_NOTIFICATION.parse(data)
	assert packet.message == "Unknown language"

def test_SMSG_CLIENTCACHE_VERSION():
	data = bytes.fromhex('0006AB0403000000')
	packet = SMSG_CLIENTCACHE_VERSION.parse(data)
	assert packet.version == 3
	print(packet)

def test_SMSG_TUTORIAL_FLAGS():
	data = bytes.fromhex('0022FD00F7BFEFFCE3A3F503000000000000000000000000000000000000000000000000')
	packet = SMSG_TUTORIAL_FLAGS.parse(data)
	print(packet)

	assert packet.tutorials == [0, 0, 0, 0, 0, 0, 66429923, 4243570679]

def test_SMSG_ADDON_INFO():
	data = b'\x00\xbe\xef\x02\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

	packet = SMSG_ADDON_INFO.parse(data)
	print(packet)
	# raise False

def test_SMSG_CHAR_ENUM():
	data = bytes.fromhex('03423B0003CC72330000000007537465616B6F000607000A04000106011100000001000000AA83B8C477C605C5ABC3BA42000000700000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000004A27000004000000000000000000000000000000000000000000004227000007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004A14000015000000002A4900000E0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000087EA4A000000000753646764666A676B6A000B0501010507060101C40D0000120200003D9A77C5CDAC59C6E13AC94200000070000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A609000004000000002A8D00001400000000000000000000000000BC0C00000700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000624800001100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000C2E14E0000000007526F676D6F6F000404010504030507097906000001000000D2211846F0672745E598A44400000070000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000B22600000400000000000000000000000000E32000000600000000374200000700000000BB26000008000000000000000000000000008F1E00000A00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000FA5000001100000000000000000000000000FB9C0000190000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
	char_enum = SMSG_CHAR_ENUM.parse(data)
	print(f'{char_enum}')

	steako = char_enum.characters[0]
	assert steako.name == 'Steako'
	assert steako.guid == Guid(value=0x7000000003372cc)
	assert steako.race == Race.tauren
	assert steako.gender == Gender.male
	assert steako.combat_class == CombatClass.shaman
	assert steako.skin == 10
	assert steako.face == 4
	assert steako.hair_style == 0
	assert steako.hair_color == 1
	assert steako.facial_hair == 6
	assert steako.level == 1
	assert steako.zone == 17
	assert steako.map == 1

	sdgdfjgkj = char_enum.characters[1]
	assert sdgdfjgkj.name == 'Sdgdfjgkj'
	assert sdgdfjgkj.race == Race.draenai
	assert sdgdfjgkj.combat_class == CombatClass.priest
	assert sdgdfjgkj.gender == Gender.female
	assert sdgdfjgkj.skin == 1
	assert sdgdfjgkj.face == 5
	assert sdgdfjgkj.hair_style == 7
	assert sdgdfjgkj.hair_color == 6
	assert sdgdfjgkj.level == 1
	assert sdgdfjgkj.zone == 3524
	assert sdgdfjgkj.map == 530
	assert sdgdfjgkj.position.x == 100.61499786376953
	assert sdgdfjgkj.position.y == -13931.2001953125
	assert sdgdfjgkj.position.z == -3961.639892578125

	rogmoo = char_enum.characters[2]
	assert rogmoo.name == 'Rogmoo'
	assert rogmoo.race == Race.night_elf
	assert rogmoo.combat_class == CombatClass.rogue
	assert rogmoo.gender == Gender.female
	assert rogmoo.skin == 5
	assert rogmoo.face == 4
	assert rogmoo.hair_style == 3
	assert rogmoo.hair_color == 5
	assert rogmoo.facial_hair == 7
	assert rogmoo.level == 9
	assert rogmoo.zone == 1657
	assert rogmoo.map == 1

	data2 = bytes.fromhex('01143B00010100000000000000416374000109010202080902506A020000010000006B65B7457FB382C544B7CE4401000000000000020000000000000000000000000000000000209E00000100000000000000000000000000EC9E00000300000000A81E00000400000000229E000014000000000000000000000000007601000007000000001256000008000000000000000000000000001F9E00000A000000000000000000000000000000000000000000000000000000000000000000000000000000007BF000001000000000000000000000000000000000000000000000000000000000000000000000000000000000B82C00001200000000000000000000000000000000000000000000000000000000000000')
	char_enum2 = SMSG_CHAR_ENUM.parse(data2)
	print(f'{char_enum2}')

	act = char_enum2.characters[0]
	assert act.name == 'Act'
	assert act.race == Race.human
	assert act.combat_class == CombatClass.warlock
	assert act.gender == Gender.female
	assert act.skin == 2
	assert act.face == 2
	assert act.hair_style == 8
	assert act.hair_color == 9
	assert act.facial_hair == 2
	assert act.level == 80
	assert act.zone == 618
	assert act.map == 1

def test_CMSG_CHAR_ENUM():
	data = bytes.fromhex('000437000000')
	char_enum_request = CMSG_CHAR_ENUM.parse(data)
	print(f'{char_enum_request}')

def test_CMSG_PLAYER_LOGIN():
	data = bytes.fromhex('000C3D0000000100000000000000')
	packet = CMSG_PLAYER_LOGIN.parse(data)

	assert packet.header.size == 12
	assert packet.player_guid == Guid(counter=1, type=GuidType.player)
	print(packet)

	data = b'\x00\x0c=\x00\x00\x000\x00\x00\x00\x00\x00\x00\x00'
	packet = CMSG_PLAYER_LOGIN.parse(data)

	assert packet.header.size == 12
	assert packet.player_guid == Guid(0x30)

def test_SMSG_TIME_SYNC_REQ():
	data = bytes.fromhex('000690033E010000')
	packet = SMSG_TIME_SYNC_REQ.parse(data)
	assert packet.header.size == 6
	assert packet.id == 318
	print(packet)

	data2 = b'\x00\x06\x90\x03\x19\x00\x00\x00'
	packet2 = SMSG_TIME_SYNC_REQ.parse(data2)
	assert packet2.header.size == 6
	assert packet2.id == 25
	print(packet2)

	data3 = b'\x00\x06\x90\x03g\x00\x00\x00'
	packet3 = SMSG_TIME_SYNC_REQ.parse(data3)
	assert packet3.header.size == 6
	print(packet3)

	data4 = b'\x00\x06\x90\x03h\x00\x00\x00'
	packet4 = SMSG_TIME_SYNC_REQ.parse(data4)
	assert packet4.header.size == 6
	assert packet3.id == packet4.id - 1
	print(packet4)

def test_CMSG_TIME_SYNC_REQ():
	data = bytes.fromhex('000A9103000005000000D5C30000')
	packet = CMSG_TIME_SYNC_RESP.parse(data)
	print(packet)

	assert packet.header.size == 10
	assert packet.id == 5
	assert packet.client_ticks == 50133

def test_CMSG_NAME_QUERY():
	data = b'\x00\x0cP\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00'
	packet = CMSG_NAME_QUERY.parse(data)
	print(packet)

	assert packet.header.size == 12
	assert packet.header.opcode == Opcode.CMSG_NAME_QUERY
	assert packet.guid == Guid(counter=0x1f)

def test_SMSG_NAME_QUERY():
	data = b'\x00\x0eQ\x00\x01\x1f\x00Eco\x00\x00\x01\x01\x04\x00'
	packet = SMSG_NAME_QUERY_RESPONSE.parse(data)
	print(packet)

	assert packet.found is True
	assert packet.info.name == 'Eco'
	assert packet.info.realm_name == ''
	assert packet.info.race == Race.human
	assert packet.info.gender == Gender.female

def test_SMSG_INIT_WORLD_STATES():
	data = bytes.fromhex('0050C20200000000EF050000EF0500000800D808000000000000D708000000000000D608000000000000D508000000000000D408000000000000D308000000000000770C0000010000003D0F000008000000')
	packet = SMSG_INIT_WORLD_STATES.parse(data)
	print(packet)

	assert packet.map_id == 0
	assert packet.zone_id == 1519
	assert packet.area_id == 1519

def test_SMSG_BIND_POINT_UPDATE():
	data = bytes.fromhex('00165501CDD70BC6357E04C3F90FA742000000000C000000')
	packet = SMSG_BIND_POINT_UPDATE.parse(data)
	print(packet)

	assert packet.header.size == 22
	assert packet.header.opcode == Opcode.SMSG_BIND_POINT_UPDATE
	assert packet.position.x == 83.53119659423828
	assert packet.position.y == -132.4929962158203
	assert packet.position.z == -8949.9501953125
	assert packet.map_id == 0
	assert packet.area_id == 12

def test_SMSG_MOTD():
	data = b'\x00t=\x03\x02\x00\x00\x00Welcome to an AzerothCore server.\x00|cffFF4A2DThis server runs on AzerothCore|r |cff3CE7FFwww.azerothcore.org|r\x00'
	packet = SMSG_MOTD.parse(data)

	assert packet.header.size == 116
	assert packet.lines == [
		'Welcome to an AzerothCore server.',
		'|cffFF4A2DThis server runs on AzerothCore|r |cff3CE7FFwww.azerothcore.org|r'
	]