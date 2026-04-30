import yaml
import pickle
import sys
from src.exception.exception import CustomException
from src.logger.logger import logger


def read_yaml(file_path:str) -> dict:
  """
  reads a YAML file and returns the contents as a dictionary
  """
  try:
    logger.info(f"Reading YAML file: {file_path}")
    with open(file_path, 'r') as yaml_file:
      return yaml.safe_load(yaml_file)
  except Exception as e:
    logger.error(f"Error occurred while reading YAML file: {file_path}")
    raise CustomException(e, sys)
  
  
def load_object(file_path:str):
  try:
    with open(file_path, "rb") as file_obj:
      model = pickle.load(file_obj)
      logger.info("Succesfully loaded the object in utils.py")
      return model
      
  except Exception as e:
    logger.info("Error in load_object function in utils.py")
    raise CustomException(e, sys)