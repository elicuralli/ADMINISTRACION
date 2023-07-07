from decouple import config

class Settings:
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')

class DevelopmentConfig(Settings):
    DEBUG = True

settings = {
    'development': DevelopmentConfig
}
