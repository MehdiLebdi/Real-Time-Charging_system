import configparser
import os

class Properties:
    #APP_HOME is a mandatory env variable where configuration files will be present
    config_dir = os.environ.get('APP_HOME')
    config_fileName = ('config.ini')
    config_file = config_dir + os.sep + config_fileName

    @staticmethod
    def load_properties():
        config = configparser.ConfigParser()
        config.read(Properties.config_file)
        DB_INPUT_URI = 'mongodb://' + config['DATABASE']['USERNAME'] + ':' + config['DATABASE']['PASSWORD'] + '@' + config['DATABASE']['SERVER_IP'] \
                        + ':' + config['DATABASE']['SERVER_PORT'] + '/' + config['DATABASE']['DB_NAME']

        DB_OUTPUT_URI =  'mongodb://' + config['DATABASE']['USERNAME'] + ':' + config['DATABASE']['PASSWORD'] + '@' + config['DATABASE']['SERVER_IP'] \
                          + ':' + config['DATABASE']['SERVER_PORT'] + '/' + config['DATABASE']['DB_NAME']

        config.set("DATABASE","DB_INPUT_URI",DB_INPUT_URI)
        config.set("DATABASE","DB_OUTPUT_URI",DB_OUTPUT_URI)

        return config