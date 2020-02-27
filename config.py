from os.path import join, dirname
import yaml
cfgFile = open(join(dirname(__file__), "private/config.yml"))
cfg = yaml.load(cfgFile.read(), Loader=yaml.SafeLoader)

class ProductionConfig():
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SECRET_KEY = cfg['production']['secret'].encode()
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/api/token-refresh/'
    JWT_COOKIE_CSRF_PROTECT = False
    TEMPLATES_AUTO_RELOAD = False

class DevelopmentConfig():
    DEBUG = True
    TESTING = True
    ENV = 'development'
    SECRET_KEY = cfg['dev']['secret'].encode()
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/api/token-refresh/'
    JWT_COOKIE_CSRF_PROTECT = False
    TEMPLATES_AUTO_RELOAD = True

