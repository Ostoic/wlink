from enum import Enum

import construct

from .headers import ServerHeader
from wlink.world.opcode import Opcode
from ...utility.construct import PackEnum


class ServerCommand(Enum):
	module_use = 0
	module_cache = 1
	cheat_checks_request = 26
	module_initialize = 3
	memory_check_request = 4
	hash_request = 5

class ClientCommand(Enum):
	module_missing = 0
	module_ok = 1
	cheat_check_result = 2
	memory_check_result = 3
	hash_result = 4
	module_failed = 5

ServerModuleInfoRequest = construct.Struct(
	'id' / construct.BytesInteger(length=16, swapped=True),
	'key' / construct.BytesInteger(length=16, swapped=True),
	'size' / construct.Int32ul
)

ServerModuleTransferRequest = construct.Struct(
	'data' / construct.FixedSized(500, construct.PrefixedArray(construct.Int16ul, construct.Byte))
)

InitModuleRequest = construct.Struct(
	'command1' / construct.Byte,
	'size1' / construct.Int16ul,
	'checksum1' / construct.Int32ul,
	'unk1' / construct.Bytes(2),
	'type' / construct.Byte,
	'string_library1' / construct.Byte,
	'function1' / construct.Array(4, construct.Int32ul),

	'command2' / construct.Byte,
	'size2' / construct.Int16ul,
	'checksum2' / construct.Int32ul,
	'unk2' / construct.Bytes(2),
	'string_library2' / construct.Byte,
	'function2' / construct.Int32ul,
	'function2_set' / construct.Byte,

	'command3' / construct.Byte,
	'size3' / construct.Int16ul,
	'checksum3' / construct.Int32ul,
	'unk3' / construct.Bytes(2),
	'string_library3' / construct.Byte,
	'function3' / construct.Int32ul,
	'function3_set' / construct.Byte,
)

ServerHashRequest = construct.Struct(
	'seed' / construct.BytesInteger(length=16, swapped=True)
)

ClientModule = construct.Struct(
	'id' / construct.BytesInteger(length=16, swapped=True),
	'key' / construct.BytesInteger(length=16, swapped=True),
	'data' / construct.PrefixedArray(construct.Int32ul, construct.Byte)
)

SMSG_WARDEN_DATA = construct.Struct(
	'header' / ServerHeader(Opcode.SMSG_WARDEN_DATA, size=39),
	'command' / construct.Byte,
	# 'command' / PackEnum(ServerCommand),
	# 'request' / construct.Switch(
	# 	construct.this.command, {
	# 		warden.ServerCommand.module_use: warden.ServerModuleInfoRequest,
	# 		warden.ServerCommand.module_cache: warden.ServerModuleTransferRequest,
	# 		warden.ServerCommand.cheat_checks_request: warden.CheatChecksRequest,
	# 		warden.ServerCommand.module_initialize: warden.InitModuleRequest,
	# 		warden.ServerCommand.hash_request: warden.ServerHashRequest
	# 	}
	# )
)
