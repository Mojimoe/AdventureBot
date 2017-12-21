class Category:
    def __init__(self):
        self.handle = "UNDEFINED"
        self.public = True
        self.evaluate = None
        self.first = None
        self.chance = 1
        self.adventures = {}
        self.preambles = ['']

    def parse(self, content):
        self.handle = content.get('handle', None)
        self.public = content.get('public', True)
        self.evaluate = content.get('evaluate', None)
        self.first = content.get('first', None)
        self.chance = content.get('chance', 1)
        self.adventures = {}  # Blank. We'll fill this later.
        self.preambles = content.get('preambles', [''])

    def add_adventure(self, adventure):
        handle = adventure.handle
        self.adventures[handle] = adventure
