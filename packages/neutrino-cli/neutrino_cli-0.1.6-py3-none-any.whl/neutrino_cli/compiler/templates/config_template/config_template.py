from neutrino_cli.compiler.templates.template import Template


template = """
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    CORS_HEADERS = 'Content-Type'
    API_PORT = int(os.getenv("API_PORT", 8080))


class ProductionConfig(Config):
    DEBUG = False
    CORS_ORIGIN_WHITELIST = os.getenv("CORS_ORIGIN_WHITELIST", '*')
    ENV = "prod"


class DevConfig(Config):
    DEBUG = True
    ENV = os.getenv("ENV", "dev")
    CORS_ORIGIN_WHITELIST = '*'  # any origin


def load_config(mode=os.getenv('ENV', 'prod')):
    '''Load config.'''
    if mode == 'prod':
        print('Loading production config')
        return ProductionConfig()
    else:
        print('Loading dev config')
        return DevConfig()


config = load_config()
"""


class ConfigTemplate(Template):
    def __init__(self):
        template_vars = {}
        super().__init__(template_str=template, template_vars=template_vars)

