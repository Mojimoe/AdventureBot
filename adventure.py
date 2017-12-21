import utils


class AdventureBlock:

    def __init__(self):
        self.handle = None
        self.category = None

        self.public = True
        self.evaluate = None
        self.once = False
        self.once_ever = False
        self.chance = 1
        self.run_all_blocks = True

        self.text = ""
        self.battle = False

        self.exp = 0
        self.gold = 0
        self.loot = 0
        self.wound = False
        self.item = None

        self.next = None  # The adventure to travel to next!

        self.execute = None
        self.pytext = None

        self.select = []
        self.sequence = []
        self.random = []

    def parse(self, content):
        self.handle = content.get('handle', None)
        self.category = content.get('category', None)

        self.public = content.get('public', True)
        self.evaluate = content.get('evaluate', None)
        self.once = content.get('once', False)
        self.once_ever = content.get('once_ever', False)
        self.chance = content.get('chance', 1)

        self.text = content.get('text', '')
        self.battle = content.get('battle', False)

        self.exp = content.get('exp', 0)
        self.gold = content.get('gold', 0)
        self.loot = content.get('loot', 0)
        self.wound = content.get('wound', False)
        self.item = content.get('item', None)

        self.next = content.get('next', None)

        self.execute = content.get('execute', None)
        self.pytext = content.get('pytext', None)

        for block_data in content.get('select', []):
            try:
                new_block = AdventureBlock()
                new_block.parse(block_data)
                self.select.append(new_block)
            except Exception as e:
                utils.log_exception(e)

        for block_data in content.get('sequence', []):
            try:
                new_block = AdventureBlock()
                new_block.parse(block_data)
                self.sequence.append(new_block)
            except Exception as e:
                utils.log_exception(e)

        for block_data in content.get('random', []):
            try:
                new_block = AdventureBlock()
                new_block.parse(block_data)
                self.random.append(new_block)
            except Exception as e:
                utils.log_exception(e)
