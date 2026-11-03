import time
from blockchain_v1_1_0.backend.blockchain.block import Block, GENESIS_PREVIOUS_HASH


def test_block_init_and_payload():
    timestamp = time.time()
    block = Block(
        index=0,
        timestamp=timestamp,
        data="genesis_data",
        previous_hash=GENESIS_PREVIOUS_HASH,
        nonce=0
    )
    expected_payload = {
        "index": 0,
        "timestamp": timestamp,
        "data": "genesis_data",
        "previous_hash": GENESIS_PREVIOUS_HASH,
        "nonce": 0
    }
    assert block._payload() == expected_payload
    assert block.hash == block.calculate_hash()


def test_meets_difficulty():
    block = Block(0, 1234567890, "data", GENESIS_PREVIOUS_HASH, nonce=0)
    # Target difficulty 0 should always be met
    assert block._meets_difficulty(0) is True

    # Manually check with a known hash pattern
    block.hash = "000abc123"
    assert block._meets_difficulty(1) is True
    assert block._meets_difficulty(2) is True
    assert block._meets_difficulty(3) is True
    assert block._meets_difficulty(4) is False


def test_increment_nonce():
    block = Block(0, 1234567890, "data", GENESIS_PREVIOUS_HASH, nonce=0)
    initial_nonce = block.nonce
    initial_hash = block.hash

    block._increment_nonce()
    assert block.nonce == initial_nonce + 1
    assert block.hash != initial_hash
    assert block.hash == block.calculate_hash()


def test_mine():
    block = Block(0, 1234567890, "data", GENESIS_PREVIOUS_HASH, nonce=0)
    difficulty = 2
    block.mine(difficulty)
    assert block.hash.startswith("0" * difficulty)
    assert block.hash == block.calculate_hash()
