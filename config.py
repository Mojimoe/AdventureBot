import loader

delay_min = 40 # in minutes
delay_max = 60 # in minutes
keep_online = 80 # in minutes

discord_admins = ['---']
discord_channel = '---'
discord_server = '---'
discord_token = '---'
discord_description = 'A lovely robot that serves adventures.'

sftp_host = "---"
sftp_username = "---"
sftp_password = "---"

item_affinity_weight = 1
item_level_difference = 2

def load_config():
    global delay_min
    global delay_max
    global keep_online
    global discord_admins
    global discord_channel
    global discord_server
    global discord_token
    global discord_description
    global sftp_host
    global sftp_username
    global sftp_password
    global item_level_difference

    content = loader.load_yaml('credentials.yaml', {}).get('config', {})

    delay_min = content.get('delay_min', None)
    delay_max = content.get('delay_max', 60)
    keep_online = content.get('keep_online', 80)

    discord_admins = content.get('discord_admins', ['---'])
    discord_channel = content.get('discord_channel', '---')
    discord_server = content.get('discord_server', '---')
    discord_token = content.get('discord_token', '---')
    discord_description = content.get('discord_description', 'A lovely bot that serves adventures')
    sftp_host = content.get('sftp_host', '---')
    sftp_username = content.get('sftp_username', '---')
    sftp_password = content.get('sftp_password', '---')
    item_level_difference = content.get('item_level_difference', 2)

load_config()
