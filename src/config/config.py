import yaml


class Config:
    def __init__(self):
        self.configs = Config.load_configs(config_file="./config.yaml")

    @staticmethod
    def load_configs(config_file="./src/config/config.yaml"):
        with open(config_file) as conf:
            data = yaml.load(conf, Loader=yaml.FullLoader)
            print(f"Config Loaded {data}")
        return data


if __name__ == '__main__':
    conf = Config()
    print(conf.configs.get("site").get("url"))
