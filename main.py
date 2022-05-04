import hashlib
import time
from tqdm import tqdm
from texttable import Texttable


def encode_string(message: str) -> str:
    """
    Takes a string and outputs the corresponding sha256 encoded string
    """

    if not isinstance(message, str):
        raise TypeError
    return hashlib.sha256(message.encode('utf-8')).hexdigest()


class BlockChain:
    """
    A BlockChain is composed of a sequence of Blocks, which are referenced 
    to each other based on the previous_block_hash attribute. 
    """

    def __init__(self, difficulty=2):
        """
        Initializes the BlockChain by generating the Genesis Block
        """
        self.difficulty = difficulty
        self.blocks = []
        self.create_genesis()

    def validate_block(self, block):
        """
        Difficulty is defined as the number of zeros needed at the
        beginning of an hash so that it's considered valid.
        The Node will mine the new block by bruteforcing the Nonce
        until the hash satisfies the validity condition (# of zeros
        at the beggining of the hash, depending on the difficulty)
        """
        print('Validating new block...')
        t0 = time.time()

        if block.idx == 0:
            block.previous_block_hash = '(genesis has no previous block)'
        else:
            previous_block = self.blocks[(block.idx-1)]
            block.previous_block_hash = previous_block.hash

        while block.hash[:self.difficulty] != '0'*self.difficulty:
            block.nonce += 1
            block.compute_hash()

        t1 = time.time()
        print(f'Block #{block.idx} validated in {round(t1-t0, 2)} sec')

        self.blocks.append(block)

    def create_genesis(self):
        """
        Creates the first block of the chain. When it's added, it fires
        a special case in addBlock() thanks to its index, so that it
        accounts for the fact that the Genesis Block has no predecessor
        """
        genesis_block = Block(content='this is the genesis')
        genesis_block.idx = 0
        self.addBlock(genesis_block)

    def addBlock(self, new_block):
        """
        Adds a new Block by validating it (brute forcing of the Nonce)
        """
        new_block.idx = len(self.blocks)
        self.validate_block(new_block)

    def __repr__(self):
        return self.blocks

    def visualize(self):
        """
        For visualizing the sequence of blocks in tabular view
        """

        for block in self.blocks:
            t = Texttable()
            rows = [['Index', block.idx],
                    ['Nonce', block.nonce],
                    ['Previous', block.previous_block_hash],
                    ['Hash', block.hash],
                    ['Content', block.content]]

            t.add_rows(rows)
            print(t.draw())

    def check_integrity(self):
        """
        Goes through all the blocks and checks that:
        1) the predecessor's has matches with the block's information
        2) the hash of the block was computed correctly
        3) the hash was validated (it starts with zeros, based on
           the difficulty of the blockchain)
        """
        t0 = time.time()
        print('Checking integrity of the BlockChain...')
        for i in tqdm(range(1, len(self.blocks))):
            block = self.blocks[i]
            previous_block = self.blocks[i-1]

            # check predecessor match
            assert previous_block.hash == block.previous_block_hash

            # recompute hash and check if it's legit
            content_to_hash = block.content + str(block.nonce)
            assert block.hash == encode_string(content_to_hash)

            # check proof of work
            assert block.hash[:self.difficulty] == '0'*self.difficulty
        t1 = time.time()
        print(
            f'The BlockChain is valid. Validation took {round(t1-t0, 2)} sec')

        return True  # if the asserts didn't fire, return True


class Block:
    """
    Individual component of the Chain. It contains:
    1) a reference to the previous block
    2) a content
    3) a Nonce (used for validation of the block) 
    4) a hash, which is computed with the Content and the Nonce
    """

    def __init__(self, content):
        """
        initializes the block
        """
        self.idx = None  # not yet assigned to a chain
        self.nonce = 0
        self.content = content
        self.compute_hash()

    def compute_hash(self):
        """
        Updates the hash based on the Block's content and nonce.
        This function is called at every iteration of the bruteforce
        """
        content_to_hash = self.content + str(self.nonce)
        assert type(content_to_hash) == str
        self.hash = encode_string(content_to_hash)

    def __repr__(self):
        if self.idx == 0:
            return 'Genesis'
        else:
            return f'Block #{self.idx}'


if __name__ == '__main__':
    difficulty = 5
    myBlockChain = BlockChain(difficulty)
    contents = ['This is an example of content. Our first block',
                'Blockchain is cool! This will be our second block',
                'Hello World. Third block!',
                '42. Fourth and final block']
    for content in contents:
        new_block = Block(content)
        myBlockChain.addBlock(new_block)

    myBlockChain.visualize()
    assert myBlockChain.check_integrity()
