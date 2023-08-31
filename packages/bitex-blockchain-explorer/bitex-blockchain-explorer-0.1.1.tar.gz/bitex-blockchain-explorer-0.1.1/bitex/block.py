class Block:
    def __init__(self, height, position, mempool=None):
        self.position = position
        self.height = height
        self.mempool = mempool

    def __repr__(self):
        return f'<Block {self.height}:{self.position}>'