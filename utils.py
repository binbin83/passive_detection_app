import yaml
import pandas as pd

def load_config(file_path: str = "config_evaluation.yaml") -> dict :
    """
    load config file into dict python oject
    """
    try :
        with open(file_path, 'r') as file :
            config = yaml.safe_load(file)
    except Exception as e:
        print(f"Fail to load config file because of {e}")
        config = {}
    return config