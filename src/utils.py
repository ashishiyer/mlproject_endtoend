import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
import dill
def save_object(path:str,obj):
    try:
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path,exist_ok=True)
        with open(path,"wb") as f:
            dill.dump(obj,f)
    except Exception as e:
        raise CustomException(e,sys)