import time

from ...backend.util.crypto_hash import crypto_hash
from ...backend.util.hex_to_binary import hex_to_binary
from ..config import MINE_RATE

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    """
    Block: is a unit of storage.

    Stores transactions in a blockchain that supports a cryptocurrency.
    """

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}), '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serializes the block into a dictionary of its attributes.

        :return:
        """
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data, until a block hash
        is found that meets the leading 0's proof of work requirement.
        :param last_block:
        :param data:
        :return:
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to the MINE_RATE.
            - Increase the difficulty for quickly mined blocks.
            - Decrease the difficulty for slowly mined blocks.
        :param last_block:
        :param new_timestamp:
        :return:
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validates a given block according to the following rules:
            - The block must have the proper last_hash reference
            - The block must meet the proof of work requirement
            - The difficulty must only adjust by 1
            - The block hash must be a valid combination of the block fields
        :param last_block:
        :param block:
        :return:
        """
        
    @staticmethod
    def genesis():
        """Generates the genesis block of the blockchain."""
        return Block(**GENESIS_DATA)


    def _payload(self):
        """Returns the payload representation of the block for hashing."""
        return {
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }


    def _meets_difficulty(self, difficulty):
        """Checks if the block's hash satisfies the given difficulty target."""
        return self.hash.startswith("0" * difficulty)


    def _increment_nonce(self):
        """Increments the nonce by 1 and recalculates the hash."""
        self.nonce += 1


def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    print(f'genesis_block: {genesis_block}')
    print(f'block: {block}')


if __name__ == "__main__":
    main()
