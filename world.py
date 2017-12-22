import utils
import loader
import category
import adventure
import item


def add_player(player_instance):
    players[player_instance.id] = player_instance


def get_visits(adventure_handle):
    return visits.get(adventure_handle, 0)


def increment_visits(adventure_handle):
    visits[adventure_handle] = get_visits(adventure_handle) + 1


def get_counter(counter_handle):
    return counters.get(counter_handle, 0)


def increment_counter(counter_handle):
    counters[counter_handle] = get_counter(counter_handle) + 1


def set_counter(counter_handle, value):
    counters[counter_handle] = value


def get_flag(flag_handle):
    return flags.get(flag_handle, False)


def set_flag(flag_handle, value=True):
    flags[flag_handle] = value


def toggle_flag(flag_handle):
    flags[flag_handle] = not get_flag(flag_handle)


def get_adventure(adventure_handle):
    if adventures is None:
        utils.log('[!] Cannot get an adventure. No adventures exist.')
    return adventures.get(adventure_handle, None)


def get_category(category_handle):
    if categories is None:
        utils.log('[!] Cannot get a category. No categories exist.')
    return categories.get(category_handle, None)


def get_item(item_handle):
    if items is None:
        utils.log('[!] Cannot get a category. No items exist.')
    return items.get(item_handle, None)


def get_player(player_id):
    if players is None:
        return None
    return players.get(player_id, None)


def purge_saves():
    global players
    global visits
    global flags
    global counters

    players = {}
    visits = {}
    flags = {}
    counters = {}

    save_persistent_data()


def rebuild_content():
    global categories
    global adventures
    global items

    categories = loader.convert_yaml_to_objects(category.Category, "content/categories/**/*.yaml")
    adventures = loader.convert_yaml_to_objects(adventure.AdventureBlock, "content/adventures/**/*.yaml")
    items = loader.convert_yaml_to_objects(item.Item, "content/items/**/*.yaml")

    # Currently, each category has no adventures. Let's fix that.

    for handle, instance in adventures.items():
        map_to_category = instance.category
        target_category_instance = get_category(map_to_category)

        if target_category_instance is not None:
            target_category_instance.add_adventure(instance)
        else:
            utils.log("[!] Couldn't look up category for " + handle + ".")


def save_persistent_data():
    loader.save_pickle(players, 'saves/players.pickle')
    loader.save_pickle(visits, 'saves/visits.pickle')
    loader.save_pickle(counters, 'saves/counters.pickle')
    loader.save_pickle(flags, 'saves/flags.pickle')


categories = {}
adventures = {}
items = {}
rebuild_content()

players = loader.load_pickle('saves/players.pickle', {})
visits = loader.load_pickle('saves/visits.pickle', {})
counters = loader.load_pickle('saves/counters.pickle', {})
flags = loader.load_pickle('saves/flags.pickle', {})


