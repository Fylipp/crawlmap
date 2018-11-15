import configparser


class Config:
    @staticmethod
    def load(path):
        cfg = configparser.ConfigParser()
        cfg.read(path)
        return Config(cfg)

    def __init__(self, cfg):
        self.db_uri = cfg.get('Database', 'uri')
        self.db_user = cfg.get('Database', 'user')
        self.db_password = cfg.get('Database', 'password')
        self.db_autoclear = cfg.get('Database', 'autoclear')
        self.web_timeout = cfg.getint('Web', 'timeout')
        self.crawl_max_depth = cfg.getint('Crawl', 'max_depth')
