import time

import construct

from wlink.utility.construct import UpperPascalString, IPv4Address, PaddedStringByteSwapped, \
	VersionString
from .header import ResponseHeader
from ..opcode import Opcode
from ..response import Response

ChallengeRequest = construct.Struct(
	'header' / ResponseHeader(Opcode.login_challenge, Response.db_busy),
	'size' / construct.ByteSwapped(construct.Default(construct.Short, 30 + construct.len_(construct.this.account_name))),
	'game' / construct.Default(construct.PaddedString(4, 'ascii'), 'WoW'),
	'version' / construct.Default(VersionString(num_bytes=3), '3.3.5'),
	'build' / construct.Default(construct.Int16ul, 12340),
	'architecture' / construct.Default(PaddedStringByteSwapped(4), 'x86'),
	'os' / construct.Default(PaddedStringByteSwapped(4), 'OSX'),
	'country' / construct.Default(PaddedStringByteSwapped(4), 'enUS'),
	'timezone_bias' / construct.Default(construct.ByteSwapped(construct.Int32sb), int(-time.timezone / 60)),
	'ip' / construct.Default(IPv4Address, '127.0.0.1'),
	'account_name' / UpperPascalString('ascii'),
)
