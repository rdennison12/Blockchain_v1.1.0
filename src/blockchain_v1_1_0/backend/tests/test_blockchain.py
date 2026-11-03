import pytest
from blockchain_v1_1_0.backend.blockchain.blockchain import Blockchain


def test_blockchain_init():
    blockchain = Blockchain(difficulty=1)
    assert len(blockchain.chain) == 1
    assert blockchain.latest_block.index == 0
    assert blockchain.latest_block.previous_hash == "0"
    assert blockchain.is_chain_valid() is True


def test_blockchain_add_block():
    blockchain = Blockchain(difficulty=1)
    blockchain.add_block("First Block")
    blockchain.add_block("Second Block")

    assert len(blockchain.chain) == 3
    assert blockchain.chain[1].data == "First Block"
    assert blockchain.chain[1].index == 1
    assert blockchain.chain[1].previous_hash == blockchain.chain[0].hash
    assert blockchain.chain[2].data == "Second Block"
    assert blockchain.chain[2].index == 2
    assert blockchain.chain[2].previous_hash == blockchain.chain[1].hash
    assert blockchain.is_chain_valid() is True


def test_blockchain_invalid_block_hash():
    blockchain = Blockchain(difficulty=1)
    blockchain.add_block("First Block")
    blockchain.add_block("Second Block")

    # Tamper with block data without updating hash
    blockchain.chain[1].data = "Tampered Data"
    assert blockchain.is_chain_valid() is False


def test_blockchain_invalid_link():
    blockchain = Blockchain(difficulty=1)
    blockchain.add_block("First Block")
    blockchain.add_block("Second Block")

    # Tamper with previous_hash
    blockchain.chain[2].previous_hash = "corrupted_hash"
    assert blockchain.is_chain_valid() is False
