from main import *


class TestBlockChain():
    def test_encoding(self):
        expected = '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069'
        assert encode_string('Hello World!') == expected

    def test_compute_block_hash(self):
        content = 'Hello'
        expected_hash = '80878c5b013ba72c0d2b7e8f65868649cbdb1e7e7a8c8a07537d6b3619e4e32f'
        test_block = Block(content)
        assert test_block.hash == expected_hash

    def test_block_validation(self):
        myBlockChain = BlockChain(5)
        difficulty = myBlockChain.difficulty
        new_block = Block('sample content')
        myBlockChain.addBlock(new_block)
        assert new_block.hash[:difficulty] == '0'*difficulty

    def test_multiple_blocks(self):
        difficulty = 5
        myBlockChain = BlockChain(difficulty)
        contents = ['This is an example of content. Our first block',
                    'Blockchain is cool! This will be our second block',
                    'Hello World. Third block!',
                    '42. Fourth and final block']
        for content in contents:
            new_block = Block(content)
            myBlockChain.addBlock(new_block)

        assert myBlockChain.check_integrity()
