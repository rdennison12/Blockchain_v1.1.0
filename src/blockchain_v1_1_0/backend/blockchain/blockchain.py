try:
    from backend.blockchain.block import Block
    from backend.util.crypto_hash import crypto_hash
except ImportError:
    try:
        from blockchain_v1_1_0.backend.blockchain.block import Block
        from blockchain_v1_1_0.backend.util.crypto_hash import crypto_hash
    except ImportError:
        try:
            from .block import Block
            from ..util.crypto_hash import crypto_hash
        except ImportError:
            from block import Block  # type: ignore[import-not-found] # noqa: F811
            from crypto_hash import crypto_hash  # type: ignore[import-not-found] # noqa: F811
from num2words import num2words


class Blockchain:
    """
    Blockchain: is a public ledger of transactions.

    Implemented as a list of blocks - data sets of transactions.
    """

    def __init__(self) -> None:
        self.chain: list[Block] = [Block.genesis()]

    def __repr__(self) -> str:
        return f"Blockchain: {self.chain}"

    def create_genesis_block(self) -> None:
        """Generates the initial block in the blockchain."""
        genesis_block = Block.genesis()
        self.chain.append(genesis_block)

    @property
    def latest_block(self) -> Block:
        """Returns the most recently added block."""
        return self.chain[-1]

    def add_block(self, data: str) -> None:
        """Creates, mines, and appends a new block to the chain."""
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def replace_chain(self, chain):
        """
        Replaces the local chain with the incoming one if the following conditions are met:
            - The incoming chain is longer than the local one.
            - The incoming chain is formatted properly.
        :param chain:
        :return:
        """
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace. The incoming chain must be longer.")
        try:
            Block.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f"Cannot replace. The incoming chain is invalid: {e}")

        self.chain = chain

    # TODO: Add a to JSON, and from JSON methods
    def to_json(self):
        """
        Serializes the chain into a list of dictionaries.
        :return:
        """
        return list(map(lambda block: block.to_json(), self.chain))
    @staticmethod
    def from_json(chain_json):
        """
        Deserializes a list of dictionary chains into a Blockchain instance.
        :param chain_json:
        :return:
        """
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json), chain_json)
        )
        return blockchain
    @staticmethod
    def is_chain_valid(self, chain: list[Block] | None = None) -> bool:
        """
        Validates the incoming chain.
        Enforces the following conditions:
            - The chain must start with the genesis block.
            - Blocks must be formatted correctly.
            - The block hash is valid.
            - The link between blocks is valid.
        :return:
        """
        target_chain = self.chain if chain is None else chain
        if not target_chain:
            return False

        if target_chain[0] != Block.genesis():
            return False

        for i in range(1, len(target_chain)):
            current = target_chain[i]
            previous = target_chain[i - 1]
            if not self._is_block_hash_valid(current):
                return False
            if not self._is_link_valid(current, previous):
                return False
        return True

    @staticmethod
    def _is_block_hash_valid(block: Block) -> bool:
        """Checks if the block hash is valid."""
        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce,
        )
        if block.hash != reconstructed_hash:
            print("Error: Current hash of block is invalid.")
            return False
        return True

    @staticmethod
    def _is_link_valid(current: Block, previous: Block) -> bool:
        """Checks if the block link is valid."""
        if current.last_hash != previous.hash:
            print("Error: Previous hash of block does not match computed hash.")
            return False
        return True


def main():
    blockchain = Blockchain()

    for i in range(1, 6):
        ordinal = num2words(i, to="ordinal")
        blockchain.add_block(f"{ordinal} block")
        print(f"{ordinal} block added.")

    print(f"Chain length: {len(blockchain.chain)}")
    print(f"Blockchain is valid: {blockchain.is_chain_valid()}")
    print(f"Blockchain: {blockchain}")


if __name__ == "__main__":
    main()
