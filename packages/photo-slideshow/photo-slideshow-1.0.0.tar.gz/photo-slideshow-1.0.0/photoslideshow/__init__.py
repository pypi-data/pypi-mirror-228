# import configparser
from configparser import SafeConfigParser
from importlib.resources import files
import os

# przykłady do files: https://importlib-resources.readthedocs.io/en/latest/using.html
eml_config = files('config').joinpath('photoslideshow_config.ini').read_text()

# config = configparser.ConfigParser()
config = SafeConfigParser(os.environ)
config.read_string(eml_config)  # nie działa
# config.read("config/photoslideshow_config.ini")  # działa

# if config already exists for the user
if os.path.exists(config.get('path', 'userconfig')):
    config.read(config.get('path', 'userconfig'))

# zmienne do configa: https://stackoverflow.com/questions/26586801/configparser-and-string-interpolation-with-env-variable