import yaml

def get_config(config_file): # -> dict # can be moved to utils
    """
    read configuration from file
    """
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)
            raise Exception("{}: Unable to parse config file!".format(sys.argv[0]))
