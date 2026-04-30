from dataclasses import dataclass
from src.exception.exception import CustomException
from src.logger.logger import logger
import os
import sys
import pandas as pd 
import numpy as np 
import pickle

@dataclass
class DataTransformationConfig:
  clean_data_dir = os.path.join("artifacts", "clean_data")
  clean_data_file = os.path.join(clean_data_dir, "clean_data.csv")
  transformed_data_dir = os.path.join("artifacts", "transformed_data")
  book_pivot = os.path.join(transformed_data_dir, "book_pivot.pkl")
  book_names = os.path.join(transformed_data_dir, "book_names.pkl")

class DataTransformation:
  def __init__(self):
    self.data_transformation_config = DataTransformationConfig
    
  def data_transformation(self):
    try:
      logger.info("Data transformation started")
      
      df = pd.read_csv(self.data_transformation_config.clean_data_file)
      
      # creating a pivot table
      book_pivot = df.pivot_table(columns='user_id', index='title', values= 'rating')
      logger.info(f"Pivot table created of shape: {book_pivot.shape}")
      
      book_pivot.fillna(0, inplace=True)
      logger.info("Missing values filled with 0")
      
      os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
      pickle.dump(book_pivot, open(self.data_transformation_config.book_pivot, 'wb'))
      logger.info("book_pivot saved")
      
      book_names = book_pivot.index
      logger.info(f"book_names: {book_names}")
      
      os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
      pickle.dump(book_names, open(self.data_transformation_config.book_names, 'wb'))
      logger.info("book_names saved")

      logger.info("Data transformation completed")
      
    except Exception as e:
      logger.error("Failed while initiating data transformation")
      raise CustomException(e, sys)
    

  def initiate_data_transformation(self):
    try:
      self.data_transformation()
    except Exception as e:
      logger.error("Failed while initiating data transformation")
      raise CustomException(e, sys)