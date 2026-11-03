import hashlib
import json
import time

GENESIS_PREVIOUS_HASH = "0"


class Block:
    """Represents a block in the blockchain."""

    def __init__(self, index, timestamp=None, data="", previous_hash="", nonce=0):
        self.index = index
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculates the hash of the block."""
        block_string = json.dumps(self._payload(), sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def _payload(self):
        """Returns the payload representation of the block for hashing."""
        return {
            "index": self.index,
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
        self.hash = self.calculate_hash()

    def mine(self, difficulty):
        while not self._meets_difficulty(difficulty):
            self._increment_nonce()
        print(f"Block {self.index} successfully mined: {self.hash}")

    @classmethod
    def create_genesis_block(cls, difficulty=0):
        """Creates the genesis block of the blockchain."""
        block = cls(0, time.time(), "Genesis Block", GENESIS_PREVIOUS_HASH)
        if difficulty > 0:
            block.mine(difficulty)
        return block


def create_genesis_block():
    """Creates the genesis block of the blockchain."""
    return Block.create_genesis_block()


def main():
    difficulty = 4
    chain = [create_genesis_block()]
    chain[0].mine(difficulty)

    for i in range(1, 5):
        previous = chain[-1]
        block = Block(i, time.time(), f"Block {i} data", previous.hash)
        block.mine(difficulty)
        chain.append(block)


if __name__ == "__main__":
    main()
