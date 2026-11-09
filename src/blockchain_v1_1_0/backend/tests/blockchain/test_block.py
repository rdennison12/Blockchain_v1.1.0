import time

from blockchain_v1_1_0.backend.blockchain.block import Block, GENESIS_DATA
from blockchain_v1_1_0.backend.config import MINE_RATE
from blockchain_v1_1_0.backend.util.hex_to_binary import hex_to_binary


def test_genesis():
    genesis = Block.genesis()
    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value


def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_adjust_difficulty_quickly_mined():
    last_block = Block.genesis()
    adjusted_difficulty = Block.adjust_difficulty(last_block, last_block.timestamp + MINE_RATE - 100)
    assert adjusted_difficulty == last_block.difficulty + 1


def test_adjust_difficulty_slowly_mined():
    last_block = Block.genesis()
    adjusted_difficulty = Block.adjust_difficulty(last_block, last_block.timestamp + MINE_RATE + 100)
    assert adjusted_difficulty == last_block.difficulty - 1


def test_adjust_difficulty_lower_limit():
    last_block = Block(
        timestamp=time.time_ns(),
        last_hash='test_last_hash',
        hash='test_hash',
        data='test_data',
        difficulty=1,
        nonce=0
    )
    adjusted_difficulty = Block.adjust_difficulty(last_block, last_block.timestamp + MINE_RATE + 100)
    assert adjusted_difficulty == 1
