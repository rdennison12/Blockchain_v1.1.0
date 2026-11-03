try:
    from backend.blockchain.block import Block
except ImportError:
    try:
        from blockchain_v1_1_0.backend.blockchain.block import Block
    except ImportError:
        from block import Block


class Blockchain:
    """
    Blockchain: a public ledger of transactions.

    Implemented as a list of blocks - data sets of transactions.
    """

    GENESIS_INDEX = 0
    GENESIS_PREVIOUS_HASH = "0"
    GENESIS_DATA = "Genesis Block Data"

    def __init__(self, difficulty: int) -> None:
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Generates the initial block in the blockchain."""
        genesis_block = Block.create_genesis_block(self.difficulty)
        self.chain.append(genesis_block)

    @property
    def latest_block(self) -> Block:
        """Returns the most recently added block."""
        return self.chain[-1]

    def add_block(self, data: str) -> None:
        """Creates, mines, and appends a new block to the chain."""
        new_block = Block(
            index=self.latest_block.index + 1,
            previous_hash=self.latest_block.hash,
            data=data,
        )
        self._mine_and_append(new_block)

    def is_chain_valid(self) -> bool:
        """Checks if the blockchain is valid."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if not self._is_block_hash_valid(current, i):
                return False
            if not self._is_link_valid(current, previous, i):
                return False
        return True

    def _mine_and_append(self, block: Block) -> None:
        """Mines and appends a block to the chain."""
        block.mine(self.difficulty)
        self.chain.append(block)

    def _is_block_hash_valid(self, block: Block, index: int) -> bool:
        """Checks if the block hash is valid."""
        if block.hash != block.calculate_hash():
            print(f"Error: Current hash of block {index} is invalid.")
            return False
        return True

    def _is_link_valid(self, current: Block, previous: Block, index: int) -> bool:
        """Checks if the block link is valid."""
        if current.previous_hash != previous.hash:
            print(f"Error: Previous hash of block {index} does not match computed hash.")
            return False
        return True

def main():
    blockchain = Blockchain(4)
    blockchain.add_block("First block")
    blockchain.add_block("Second block")
    blockchain.add_block("Third block")
    blockchain.add_block("Fourth block")
    print(f"Chain length: {len(blockchain.chain)}")
    print(f"Blockchain is valid: {blockchain.is_chain_valid()}")

if __name__ == "__main__":
    main()
