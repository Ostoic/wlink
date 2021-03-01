import construct

from prowl.world.opcode import Opcode
from .headers import ServerHeader

SMSG_UPDATE_OBJECT = construct.Struct(
	'header' / ServerHeader(Opcode.SMSG_UPDATE_OBJECT, 0),
	'data' / construct.Bytes(construct.this.header.size - 2),
)

SMSG_COMPRESSED_UPDATE_OBJECT = construct.Struct(
	'header' / ServerHeader(Opcode.SMSG_COMPRESSED_UPDATE_OBJECT, 0),
	'data' / construct.Bytes(construct.this.header.size - 2)
)
