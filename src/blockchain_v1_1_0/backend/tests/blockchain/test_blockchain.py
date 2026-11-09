from blockchain_v1_1_0.backend.blockchain.block import GENESIS_DATA
from blockchain_v1_1_0.backend.blockchain.blockchain import Blockchain


def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA["hash"]


def test_add_block():
    blockchain = Blockchain()
    data = "test_data"
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data
