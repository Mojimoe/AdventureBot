import emoji
import utils


class Item:
    def __init__(self):
        self.handle = None
        self.name = ''
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


    def get_replace_text(self):
        if self.slot == 'title':
            return ""
        else:
            return "You leave your " + self.name + " behind."

    def get_reject_text(self):
        if self.slot == 'title':
            return ""
        else:
            return "You leave the " + self.name + " behind."

    def on_equip(self):
        if self.slot == 'pet':
            self.given_name = utils.select(self.possible_names)

    def get_equip_text(self):
        if self.slot == 'pet':
            return "You **adopt the " + self.name + "** " + emoji.pet + "! You decide to name it *" + self.given_name + "*."
        elif self.slot == 'title':
            return "**You shall henceforth be known as the " + self.name + "!**"
        else:
            return "You **equip the " + self.name + "** " + emoji.item + "."

    def get_attack_text(self):
        return "You " + self.verb + " with your " + self.name + "!"

    def get_price(self):
        return (self.tier * (5 + utils.randint(0, 10))) + utils.randint(1, 5)

    def get_behavior_text(self):
        # for pets
        return self.name + ', *' + self.given_name + '*. *' + self.given_name + '* ' + utils.select(self.behaviors)
