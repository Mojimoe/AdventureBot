import utils
import datetime
import emoji
import config
import world

class Player:
    def __init__(self):
        self.level = 1
        self.id = '0'
        self.name = 'UNDEFINED'

        self.scheduled_adventure = None
        self.paused = False

        self.race = "human"
        self.alignment = "lawful"
        self.horoscope = "scorpio"

        self.gold = 0
        self.exp = 0
        self.loot = 0
        self.wounded = False

        self.strength = 0
        self.dexterity = 0
        self.intellect = 0
        self.charisma = 0
        self.luck = 0

        self.strength_affinity = 0
        self.dexterity_affinity = 0
        self.intellect_affinity = 0
        self.charisma_affinity = 0

        self.highest_stat = 'strength'

        self.strength_roll = 0
        self.dexterity_roll = 0
        self.intellect_roll = 0
        self.charisma_roll = 0
        self.luck_roll = 0
        self.attack_roll = 0

        self.visits = {}
        self.items = {}
        self.flags = {}
        self.counters = {}

        self.next = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return

    # == PLAYER EVENTS ==

    def create(self):
        self.level = 1
        self.race = utils.select(['human', 'elf', 'dwarf', 'orc', 'gnome'])
        self.alignment = utils.select(['lawful', 'chaotic'])
        self.horoscope = utils.select(['aquarius', 'pisces', 'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn'])

        stats = [1, 2, 3, 4]
        utils.shuffle(stats)

        self.strength = stats[0]
        self.dexterity = stats[1]
        self.intellect = stats[2]
        self.charisma = stats[3]

        affinities = [1, 2, 3, 4]
        utils.shuffle(affinities)

        self.strength_affinity = affinities[0]
        self.dexterity_affinity = affinities[1]
        self.intellect_affinity = affinities[2]
        self.charisma_affinity = affinities[3]

    # == PLAYER DATA MANIPULATORS ==

    def get_tag(self, should_use_title=False):
        text = "<@" + self.id + ">"

        if should_use_title and self.get_slot_filled('title'):
            text += ", " + self.get_item_name('title')

        return text

    def schedule_next_adventure(self):
        minimum = config.delay_min
        maximum = config.delay_max
        minutes = utils.randfloat(minimum, maximum)

        self.scheduled_adventure = utils.get_future_timestamp(minutes=minutes)

    def get_item_instance(self, slot):
        return self.items.get(slot, None)

    def get_item_name(self, slot):
        item = self.get_item_instance(slot)
        if item is not None:
            return item.name
        else:
            return 'nothing'

    def get_item_handle(self, slot):
        item = self.get_item_instance(slot)
        if item is not None:
            return item.handle
        else:
            return 'nothing'

    def get_slot_tier(self, slot):
        item = self.get_item_instance(slot)
        if item is not None:
            return item.handle
        else:
            return 0

    def get_slot_filled(self, slot):
        item = self.get_item_instance(slot)
        if item is None:
            return False
        else:
            return True

    def has_item(self, item_handle):
        for key, value in self.items.items():
            if value.handle == item_handle:
                return True

        return False

    def wants_item(self, in_item):
        if isinstance(in_item, str):
            # if we passed in a handle, get the item by handle.
            new_item = world.get_item(in_item)
        else:
            new_item = in_item

        if new_item is None:
            utils.log('[!] Could not find an item specified by a string... ignoring it.')
            return False

        slot = new_item.slot

        old_item = self.get_item_instance(slot)

        if old_item is None:
            return True

        if slot == 'pet':
            return False  # Never trade pets if you already have one!

        new_desirability = new_item.tier
        old_desirability = old_item.tier

        new_affinity = new_item.affinity
        old_affinity = old_item.affinity

        if new_affinity == 'strength':
            new_desirability += self.strength_affinity - 2
        elif new_affinity == 'dexterity':
            new_desirability += self.dexterity_affinity - 2
        elif new_affinity == 'intellect':
            new_desirability += self.intellect_affinity - 2
        elif new_affinity == 'charisma':
            new_desirability += self.charisma_affinity - 2

        if old_affinity == 'strength':
            old_desirability += self.strength_affinity - 2
        elif old_affinity == 'dexterity':
            old_desirability += self.dexterity_affinity - 2
        elif old_affinity == 'intellect':
            old_desirability += self.intellect_affinity - 2
        elif old_affinity == 'charisma':
            old_desirability += self.charisma_affinity - 2

        if new_desirability > old_desirability:
            return True
        else:
            return False

    def equip_item(self, new_item):
        slot = new_item.slot
        old_item = self.get_item_instance(slot)

        text = ""

        new_instance = utils.clone(new_item) # We have to clone the item so we don't reference the template.

        self.items[slot] = new_instance
        new_instance.on_equip()

        text += new_instance.get_equip_text() + " "

        if old_item is not None:
            text += old_item.get_replace_text() + " "

        return text

    def reject_item(self, new_item):
        return new_item.get_reject_text()

    def offer_item(self, new_item):
        if self.wants_item(new_item):
            text = self.equip_item(new_item)
        else:
            text = self.reject_item(new_item)
        return text

    def get_flag(self, flag_handle):
        return self.flags.get(flag_handle, False)

    def set_flag(self, flag_handle, value=True):
        self.flags[flag_handle] = value

    def toggle_flag(self, flag_handle):
        self.flags[flag_handle] = not self.get_flag(flag_handle)

    def get_counter(self, counter_handle):
        return self.counters.get(counter_handle, 0)

    def set_counter(self, counter_handle, value):
        self.counters[counter_handle] = value

    def increment_counter(self, counter_handle):
        self.counters[counter_handle] = self.get_counter(counter_handle) + 1

    def get_visits(self, adventure_handle):
        return self.visits.get(adventure_handle, 0)

    def increment_visits(self, adventure_handle):
        self.visits[adventure_handle] = self.get_visits(adventure_handle) + 1

    def wants_to_visit_shop(self):
        if self.loot > 10 or self.gold >= (10*self.level + 5):
            return True
        else:
            return False

    # == TEXT HELPERS ==

    def get_item_behavior(self, slot):
        inst = self.get_item_instance(slot)
        if inst is not None:
            return inst.get_behavior_text()
        else:
            return ''

    def get_inspect_text(self):
        message = self.get_tag(True) + ": "
        message += "You are a level " + str(self.level) + " " + self.race + "."
        message += "\nYou have " + str(self.gold) + " gold."
        message += "\n"

        str_adjectives = ["You are emaciated and thin. ",
                          "",
                          "You are remarkably strong. ",
                          "You are capable of great feats of strength. ",
                          "Your strength is legendary. "]

        dex_adjectives = ["You are clumsy and uncoordinated. ",
                          "",
                          "You are graceful and nimble. ",
                          "You are exceptionally agile. ",
                          "You are lightning quick. "]

        int_adjectives = ["You are dim-witted. ",
                          "",
                          "You are sharp and aware. ",
                          "You are remarkably smart. ",
                          "You are purveyor of lost knowledge. ",
                          "Your knowledge of the arcane is known throughout the land. "]

        cha_adjectives = ["You are frequently at a loss for words. ",
                          "",
                          "You are keen and likable. ",
                          "You are fabulously witty and charming. ",
                          "You have legions of admirers. "]

        str_index = int(utils.clamp(utils.floor(self.strength / 2), 0, 4))
        dex_index = int(utils.clamp(utils.floor(self.dexterity / 2), 0, 4))
        int_index = int(utils.clamp(utils.floor(self.intellect / 2), 0, 4))
        cha_index = int(utils.clamp(utils.floor(self.charisma / 2), 0, 4))

        message += str_adjectives[str_index]
        message += dex_adjectives[dex_index]
        message += int_adjectives[int_index]
        message += cha_adjectives[cha_index]

        # Affinities

        message += "\n"

        if self.strength_affinity >= 3:
            if self.dexterity_affinity >= 3:
                if self.alignment == 'chaotic':
                    message += "You are outgoing. "  # Str-Dex-Chaotic
                if self.alignment == 'lawful':
                    message += "You are enthusiastic. "  # Str-Dex-Lawful
            if self.intellect_affinity >= 3:
                if self.alignment == 'chaotic':
                    message += "You are determined. "  # Str-Int-Chaotic
                if self.alignment == 'lawful':
                    message += "You are disciplined. "  # Str-Int-Lawful
            if self.charisma_affinity >= 3:
                if self.alignment == 'chaotic':
                    message += "You are energetic. "  # Str-Cha-Chaotic
                if self.alignment == 'lawful':
                    message += "You think before you speak. "  # Str-Cha-Lawful
        elif self.dexterity_affinity >= 3:
            if self.intellect_affinity >= 3:
                if self.alignment == 'chaotic':
                    message += "You are wily. "  # Dex-Int-Chaotic
                if self.alignment == 'lawful':
                    message += "You are a problem-solver. "  # Dex-Int-Lawful
            if self.charisma_affinity >= 3:
                if self.alignment == 'chaotic':
                    message += "You are a show-off. "  # Dex-Cha-Chaotic
                if self.alignment == 'lawful':
                    message += "You are confident. "  # Dex-Cha-Lawful
        elif self.intellect_affinity >= 3:
            if self.charisma_affinity >= 3:
                if self.alignment == 'chaotic':
                    message += "You like puns. "  # Int-Cha-Chaotic
                if self.alignment == 'lawful':
                    message += "You appreciate a good joke. "  # Int-Cha-Lawful

        message += "You were born under the sign of " + self.horoscope + ". "

        if self.intellect - self.charisma >= 3:
            message += "(You're pretty sure that doesn't mean anything.) "
        elif self.intellect - self.charisma <= -3:
            message += "(You're pretty sure that's your most important trait.) "

        message += "\n"
        # items

        if self.get_slot_filled('armor'):
            name = self.get_item_name('armor')
            message += "You are wearing " + name + ". "

        if self.get_slot_filled('weapon'):
            name = self.get_item_name('weapon')
            message += "You wield a " + name + ". "

        if self.get_slot_filled('trinket'):
            name = self.get_item_name('trinket')
            message += "You carry a " + name + ". "

        if self.get_slot_filled('pet'):
            name = self.get_item_name('pet')
            given_name = self.get_item_instance('pet').given_name
            message += "You own a pet " + name + ", named *" + given_name + "*!"

        return message

    # == EMBARK HELPERS ==

    def get_valid_shop_item(self):
        # SET UP FOR EVALUATE
        player = self

        valid_items = []
        item_chances = []
        for handle, item in world.items.items():
            this = item
            if item.slot not in ['weapon', 'armor', 'trinket']:
                continue
            if not item.public:
                continue
            if abs(item.tier-self.level) > config.item_level_difference:
                continue
            if item.evaluate is not None and not eval(item.evaluate):
                continue
            valid_items.append(item)
            item_chances.append(item.chance)

        if len(valid_items) == 0:
            utils.log('[!] No valid shop items found for player. ' + self.id)
            return None

        return utils.select_with_weight(valid_items, item_chances)

    def get_valid_category(self):
        # Alias for eval.
        player = self

        valid_categories = []
        category_chances = []
        for handle, category in world.categories.items():
            this = category # for eval
            if category.public:
                if category.evaluate is None or eval(category.evaluate):
                    valid_categories.append(category)
                    category_chances.append(category.chance)

        if len(valid_categories) == 0:
            utils.log('[!] No valid categories found for player ' + self.id)
            return None

        return utils.select_with_weight(valid_categories, category_chances)

    def get_valid_adventure_from_category(self, category):
        if category is None:
            utils.log('[!] Cannot find adventures in None category for player ' + self.id)
            return None

        if category.first is not None and self.get_visits(category.first) == 0:
            return world.get_adventure(category.first)

        if len(category.adventures) == 0:
            utils.log('[!] category ' + category.handle + ' has no adventures.')
            return None

        # Some setup
        player = self  # This aliases self to player, for exec and eval syntax.

        valid_adventures = []
        adventure_chances = []
        for handle, adventure in category.adventures.items():
            this = adventure
            if not adventure.public:
                continue
            if adventure.evaluate is not None and not eval(adventure.evaluate):
                continue
            if adventure.once and self.get_visits(adventure.handle) > 0:
                continue
            valid_adventures.append(adventure)
            adventure_chances.append(adventure.chance)

        if len(valid_adventures) == 0:
            utils.log('[!] No valid adventures found for player ' + self.id + ' in category ' + category.handle)
            return None

        return utils.select_with_weight(valid_adventures, adventure_chances)

    def roll(self):
        self.strength_roll = utils.randint(0, 10) + self.strength
        self.dexterity_roll = utils.randint(0, 10) + self.dexterity
        self.intellect_roll = utils.randint(0, 10) + self.intellect
        self.charisma_roll = utils.randint(0, 10) + self.charisma

    # == EMBARK LOGIC CHUNKS ==
    def check_level_up(self):
        xp_to_next_level = (self.level - 1) * 10 + 20

        text = ""

        if self.exp >= xp_to_next_level:
            self.exp += -xp_to_next_level
            self.level += 1

            text += "You **LEVELED UP!** " + emoji.level + " You are now **level " + str(self.level) + "!** "

            probability_list = [self.strength_affinity, self.dexterity_affinity, self.intellect_affinity, self.charisma_affinity]
            stat_list = ['s', 'd', 'i', 'c']

            stat_gains = utils.multiselect_with_weight(stat_list, probability_list, 2)

            if 's' in stat_gains:
                self.strength += 1
                text += "You feel **stronger**! "
            if 'd' in stat_gains:
                self.dexterity += 1
                text += "You feel **quicker**! "
            if 'i' in stat_gains:
                self.intellect += 1
                text += "You feel **smarter**! "
            if 'c' in stat_gains:
                self.charisma += 1
                text += "You feel **wittier**! "

        return text

    # == EMBARK AND BLOCK READ ==
    def embark(self):

        message = ""
        self.roll()
        try:
            if self.next is not None:
                # QUEST CHAIN
                adventure_instance = world.get_adventure(self.next)
                self.next = None
                message = self.run_adventure(adventure_instance)
            elif self.wounded:
                # Handle wounded
                message = self.run_hospital()
            elif self.wants_to_visit_shop() and utils.chance(1/3):
                # Handle shop
                message = self.run_shop()
            else:
                # Handle default.
                category = self.get_valid_category()
                adventure_instance = self.get_valid_adventure_from_category(category)
                message = self.run_adventure(adventure_instance)

            self.schedule_next_adventure()
            return message
        except Exception as e:
            utils.log_exception(e)
            return None

    def run_adventure(self, root_block):
        if root_block is None:
            utils.log('[!] Cannot run NONE adventure for player ' + self.id)
            return None

        try:
            # Tag
            message = self.get_tag(True) + ": "

            # Preambles
            if root_block.public:
                category_data = world.get_category(root_block.category)
                if category_data is not None:
                    preambles = category_data.preambles
                    message += utils.select(preambles) + '\n'

            # Iterate through the blocks!
            message += self.run_adventure_block(root_block)

            # Increment Visits
            self.increment_visits(root_block.handle)

            # Calc Level up
            message += self.check_level_up()

            # Broadcast message
            return message

        except Exception as e:
            utils.log('[!] Encountered an exception in adventure ' + root_block.handle)
            utils.log_exception(e)
            return None

    def run_adventure_block(self, block):
        # Runs a chunk of adventure logic

        # Some setup
        player = self  # This aliases self to player, for exec and eval syntax.
        this = block

        block_message = ""

        # Text
        block_message += block.text + " "

        # Execute
        if block.execute is not None:
            exec(block.execute)  # Runs arbitrary code. Tremendously unsafe.

        # Pytext
        if block.pytext is not None:
            block_message += eval(block.pytext)

        # Battle
        if block.battle:
            item_inst = self.get_item_instance('weapon')
            if item_inst is not None:
                block_message += item_inst.get_attack_text() + " "
            else:
                block_message += "You swing with your fists! "

        # Wounds
        if block.wound:
            self.wounded = True
            block_message += "**You have been wounded!** " + emoji.wound + " "

        # Item
        if block.item is not None:
            target_item = world.get_item(block.item)

            if target_item is not None:
                block_message += self.offer_item(target_item)
            else:
                utils.log('[!] Could not find target item handle.')

        # Give Exp, Gold, Loot
        exp = block.exp
        gold = block.gold
        loot = block.loot

        if exp > 0 and gold > 0:
            block_message += "\nYou gained **" + str(exp) + " experience** " + emoji.exp + " and **" + str(
                gold) + " gold** " + emoji.gold + "! "
        elif exp > 0:
            block_message += "\nYou gained **" + str(exp) + " experience** " + emoji.exp + "! "
        elif gold > 0:
            block_message += "\nYou gained **" + str(gold) + " gold** " + emoji.gold + "! "

        self.exp = max(self.exp + exp, 0)
        self.gold = max(self.gold + gold, 0)
        self.loot = max(self.loot + loot, 0)

        # Quest Chains
        self.next = block.next

        # Select a sub-block and run it, if it meets our criteria.
        # This method runs *every* block in sequence.
        if len(block.sequence) > 0:
            for sub_block in block.sequence:
                this = sub_block
                if sub_block.evaluate is None or eval(sub_block.evaluate):
                    if sub_block.public is True and utils.chance(sub_block.chance):
                        block_message += self.run_adventure_block(sub_block)

        # Select a sub-block and run it, if it meets our criteria.
        # This method runs *the first* block in select.
        elif len(block.select) > 0:
            for sub_block in block.select:
                this = sub_block
                if sub_block.evaluate is None or eval(sub_block.evaluate):
                    if sub_block.public is True and utils.chance(sub_block.chance):
                        block_message += self.run_adventure_block(sub_block)
                        break

        # Select a sub-block and run it, if it meets our criteria.
        # This method runs *a random* block in random.
        elif len(block.random) > 0:
            possible_blocks = []
            block_chance = []
            for sub_block in block.random:
                this = sub_block
                if sub_block.evaluate is None or eval(sub_block.evaluate):
                    if sub_block.public is True:
                        possible_blocks.append(sub_block)
                        block_chance.append(sub_block.chance)
            if len(possible_blocks) > 0:
                target_block = utils.select_with_weight(possible_blocks, block_chance)
                block_message += self.run_adventure_block(target_block)

        return block_message

    def run_hospital(self):
        self.wounded = False
        message = self.get_tag(True) + ": "
        message += "You visit a healer in town. Your wounds are cured! " + emoji.heal
        return message

    def run_shop(self):
        rand_item = self.get_valid_shop_item()

        message = self.get_tag(True) + ": "
        message += "You visit a shop in town. "

        if self.loot > 0:
            message += "You sell your adventuring loot. **You gain " + str(
                self.loot) + " gold** " + emoji.gold + " !\n"
            self.gold += self.loot
            self.loot = 0

        if rand_item is not None:
            price = rand_item.get_price()

            message += "The shopkeeper offers you a " + rand_item.name + " for " + str(price) + " gold."

            if self.gold < price:
                message += ".. but you are unable to afford it."
            elif self.wants_item(rand_item):
                message += " You purchase it! You **lose " + str(price) + " gold**, but you **gain the " + rand_item.name + "** " + emoji.item + "!"
                self.gold += -price

                old_item = self.items.get(rand_item.slot, None)

                self.equip_item(rand_item)

                if old_item is not None:
                    message += " " + old_item.get_replace_text()
            else:
                message += " You politely decline the shopkeeper."

        return message
