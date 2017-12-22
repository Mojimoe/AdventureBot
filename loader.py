import glob
import yaml
import pickle

import world
import utils

import adventure
import category
import item


def load_pickle(filename, default=None):
    try:
        file = open(filename, 'rb')
        content = pickle.load(file)
        file.close()
        if content is None:
            return default
        else:
            return content
    except Exception as e:
        utils.log_exception(e)
        return default


def save_pickle(content, filename):
    try:
        file = open(filename, 'wb')
        pickle.dump(content, file)
        file.close()
    except Exception as e:
        utils.log_exception(e)


def load_yaml(filename, default=None):
    try:
        file = open(filename, 'r')
        content = yaml.load(file)
        file.close()
        if content is None:
            return default
        else:
            return content
    except Exception as e:
        utils.log_exception(e)
        return default


def save_yaml(content, filename):
    if content is None:
        return

    try:
        file = open(filename, 'w')
        yaml.dump_all(content, file, default_flow_style=False)
        file.close()
    except Exception as e:
        utils.log_exception(e)


def convert_yaml_to_objects(template, globpath):

    data = {}

    fileset = glob.glob(globpath, recursive=True)

    if len(fileset) == 0:
        return

    for filename in fileset:
        try:
            file = open(filename)
            content = yaml.load(file)
            file.close()

            new_object = template() # I literally can't believe python lets me do this
            new_object.parse(content)

            handle = new_object.handle

            if handle is None:
                utils.log("[!] Couldn't register object at filepath " + filename + ", because it has no handle.")
            elif handle in data:
                utils.log(
                    "[!] Couldn't register object at filepath " + filename + ", because its handle is already in use by another object of the same type.")
            else:
                data[handle] = new_object
        except Exception as e:
            utils.log('[!] Exception when parsing file: ' + filename)
            utils.log_exception(e)

    return data
