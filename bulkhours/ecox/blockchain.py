import hashlib
import time
import random
import pandas as pd

from .block import Block, BlockCoin, BlockMsg

import hashlib
import time
import random

random.seed(42)

# https://dealancer.medium.com/how-to-using-bitcoin-key-pairs-to-for-encrypted-messaging-a0a980e627b1


class BlockChain:
    public_chain = []

    def __init__(self, reward_probability=0.1, miners_flops={"Aegon": 1.0}, data_type="Coins"):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.lottery_range = int(1.0 / reward_probability)
        self.miners_flops = miners_flops
        self.portfolios = {}
        self.start = time.time()
        self.transactions = []
        self.data_type = data_type

        # Construct the first block of the chain
        self.construct_block_and_add_it_to_blockchain({})

    def get_block_type(self):
        return BlockCoin if self.data_type == "Coins" else BlockMsg

    def construct_block_and_add_it_to_blockchain(self, data):
        # Construct a new block and adds it to the chain
        self.current_data.append(data)
        prev_hash = BlockChain.public_chain[-1] if len(BlockChain.public_chain) > 0 else 0

        block = self.get_block_type()(index=len(self.chain), prev_hash=prev_hash, data=data)

        self.chain.append(block)
        BlockChain.public_chain.append(block.calculate_hash)
        return block

    def is_valid_chain(self):
        """Check past transactions"""

        proof_no = 0

        def verifying_proof(last_proof, proof):
            guess = f"{last_proof}{proof}".encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            return guess_hash[:4] == "0000"

        return True
        while verifying_proof(proof_no, proof_no) is False:
            proof_no += 1

        return proof_no

    def add_block_to_chain(self, data, reward_probability=None):

        # Start clock
        self.start = time.time()

        # Get proof of work
        if not self.is_valid_chain():
            print(f"Error {data}")
            return

        # Add new block
        self.construct_block_and_add_it_to_blockchain(data)

        # Do I reward miner ?
        lottery_range = int(1.0 / reward_probability) if reward_probability is not None else self.lottery_range
        if random.randint(0, lottery_range) == 1:
            # Generate miner reward
            miner = self.get_block_type().get_reward_data(
                random.choices(list(self.miners_flops.keys()), weights=self.miners_flops.values(), k=1)[0]
            )
            self.construct_block_and_add_it_to_blockchain(miner)

        return time.time() - self.start
