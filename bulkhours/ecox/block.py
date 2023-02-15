import hashlib
import time


class Block:
    def __init__(self, index, prev_hash, data, timestamp=None):
        """A block refers to a transaction between 2 people. It is characterised by"""

        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def content(self):
        # Get the content info
        return "{}/{}/{}/{}".format(self.index, self.prev_hash, self.data, self.timestamp)

    @property
    def calculate_hash(self):
        """Calculates the cryptographic hash of every block"""
        return hashlib.sha256(self.content.encode()).hexdigest()

    def __repr__(self):
        return self.content


class BlockCoin(Block):
    @staticmethod
    def get_reward_data(miner):
        return {"sender": "MINER_REWARD_!!!!!", "recipient": miner, "quantity": 1}


class BlockMsg(Block):
    @staticmethod
    def get_reward_data(miner):
        return {
            "sender": "MINER_REWARD_!!!!!",
            "recipient": miner,
            "message": "Thanks to check the message thread integrity",
        }
