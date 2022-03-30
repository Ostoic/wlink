from wlink.world.packets import SMSG_CHARACTER_LOGIN_FAILED, LoginFailureReason

async def test_SMSG_CHARACTER_LOGIN_FAILED():
    data = b'\x00\x03A\x00\x02'
    packet = SMSG_CHARACTER_LOGIN_FAILED.parse(data)
    print(packet)

    assert packet.header.size == 2 + 1
    assert packet.reason == LoginFailureReason.duplicate_character
