import emoji
import utils
import loader

possible_enchants = loader.load_yaml('content/enchants.yaml')

if possible_enchants is None:
    possible_enchants = [""]
else:
    possible_enchants = possible_enchants.get('enchants', [""])

class Item:
    def __init__(self):
        self.handle = None
        self.name = ''
        self.enchant = ''
        self.enchanted = False
        self.chance = 1
        self.public = True
        self.possible_names = ['nothing']
        self.given_name = 'nothing'
        self.tier = 0
        self.slot = 'trinket'
        self.verb = 'swing'
        self.behaviors = ['']

        self.strength = 0
        self.dexterity = 0
        self.intellect = 0
        self.charisma = 0
        self.luck = 0
        self.affinity = 'none'

        self.evaluate = None

        self.events = {}

    class Event:
        def __init__(self):
            self.trigger = None
            self.trigger_execute = None
            self.trigger_message = None

    def parse(self, content):
        self.handle = content.get('handle', None)
        self.name = content.get('name', '')
        self.chance = content.get('chance', 1)
        self.enchanted = content.get('enchanted', False)
        self.public = content.get('public', True)
        self.possible_names = content.get('possible_names', ['nothing'])

        self.behaviors = content.get('behaviors', [''])
        self.tier = content.get('tier', 0)
        self.slot = content.get('slot', 'trinket')
        self.verb = content.get('verb', 'swing')

        self.strength = content.get('strength', 0)
        self.dexterity = content.get('dexterity', 0)
        self.intellect = content.get('intellect', 0)
        self.charisma = content.get('charisma', 0)
        self.luck = content.get('luck', 0)
        self.affinity = content.get('affinity', 'none')

        self.evaluate = content.get('evaluate', None)

    def get_tag(self):
        return self.name + " of " + self.enchant

    def get_replace_text(self):
        if self.slot == 'title':
            return ""
        else:
            return "You leave your " + self.get_tag() + " behind."

    def get_reject_text(self):
        if self.slot == 'title':
            return ""
        else:
            return "You leave the " + self.get_tag() + " behind."

    def on_equip(self):
        if self.slot == 'pet':
            self.given_name = utils.select(self.possible_names)

    def roll(self):
        # random rolls this template or items random props
        if self.enchanted:
            self.enchant = utils.select(possible_enchants)

    def get_equip_text(self):
        if self.slot == 'pet':
            return "You **adopt the " + self.get_tag() + "** " + emoji.pet + "! You decide to name it *" + self.given_name + "*."
        elif self.slot == 'title':
            return "**You shall henceforth be known as the " + self.get_tag() + "!**"
        else:
            return "You **equip the " + self.get_tag() + "** " + emoji.item + "."

    def get_attack_text(self):
        return "You " + self.verb + " with your " + self.get_tag() + "!"

    def get_price(self):
        return (self.tier * (5 + utils.randint(0, 10))) + utils.randint(1, 5)

    def get_behavior_text(self):
        # for pets
        return self.get_tag() + ', *' + self.given_name + '*. *' + self.given_name + '* ' + utils.select(self.behaviors)
