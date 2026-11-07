import hashlib
import json
import time

try:
    from backend.util.crypto_hash import crypto_hash
    from backend.util.hex_to_binary import hex_to_binary
except ImportError:
    try:
        from blockchain_v1_1_0.backend.util.crypto_hash import crypto_hash
        from blockchain_v1_1_0.backend.util.hex_to_binary import hex_to_binary
    except ImportError:
        try:
            from .crypto_hash import crypto_hash
            from .hex_to_binary import hex_to_binary
        except ImportError:
            from crypto_hash import crypto_hash # type: ignore[import-not-found] # noqa: F811
            from hex_to_binary import hex_to_binary # type: ignore[import-not-found] # noqa: F811

GENESIS_PREVIOUS_HASH = "0"
GENESIS_DATA = {
    'index': 0,
    'data': 'Genesis Block',
    'previous_hash': GENESIS_PREVIOUS_HASH,
}

class Block:
    """Represents a block in the blockchain."""

    def __init__(self, index, timestamp=None, data="", previous_hash="", nonce=0):
        self.index = index
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def __repr__(self):
        return (
            f"Block(index={self.index}, timestamp={self.timestamp}, "
            f"data={self.data}, previous_hash={self.previous_hash}, "
            f"hash={self.hash}, nonce={self.nonce})"
        )

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

    def mine_block(self, difficulty):
        """Mines a block by incrementing nonce until the hash satisfies difficulty."""
        while not self._meets_difficulty(difficulty):
            self._increment_nonce()
        print(f"Block {self.index} successfully mined: {self.hash}")

    mine = mine_block

    @classmethod
    def genesis(cls, difficulty=0):
        """Generates the genesis block of the blockchain."""
        block = cls(
            index=0,
            timestamp=time.time(),
            data="Genesis Block",
            previous_hash=GENESIS_PREVIOUS_HASH,
        )
        if difficulty > 0:
            block.mine_block(difficulty)
        return block

    create_genesis_block = genesis


def create_genesis_block(difficulty=0):
    """Creates the genesis block of the blockchain."""
    return Block.genesis(difficulty)


def main():
    difficulty = 4
    chain = [create_genesis_block()]
    chain[0].mine_block(difficulty)

    for i in range(1, 5):
        previous = chain[-1]
        block = Block(i, time.time(), f"Block {i} data", previous.hash)
        block.mine_block(difficulty)
        chain.append(block)


if __name__ == "__main__":
    main()
