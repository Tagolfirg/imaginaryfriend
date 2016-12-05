import configparser
from src.redis_c import Redis
from src.service import *

# Config
sections = {
    'bot': ['token', 'name', 'anchors', 'messages', 'purge_interval', 'default_chance', 'spam_stickers'],
    'grammar': ['end_sentence', 'all'],
    'logging': ['level'],
    'updates': ['mode'],
    'media_checker': ['lifetime', 'stickers'],
    'redis': ['host', 'port', 'db'],
    'db': []
}


def getlist(self, section, option, type=str):
    return list(map(lambda o: type(o), config.get(section, option).split(',')))

configparser.ConfigParser.getlist = getlist

config = configparser.ConfigParser()
config.read('./main.cfg', encoding='utf-8')

for section, options in sections.items():
    if not config.has_section(section):
        raise ValueError("Config is not valid! Section '{}' is missing!".format(section))
    for option in options:
        if not config.has_option(section, option):
            raise ValueError("Config is not valid! Option '{}' in section '{}' is missing!".format(option, section))


# IOC
redis = Redis(config)
chance_manager = ChanceManager()
media_checker = MediaUniquenessChecker()
data_learner = DataLearner()
reply_generator = ReplyGenerator()
chat_purge_queue = ChatPurgeQueue()
