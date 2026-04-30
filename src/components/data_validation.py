from dataclasses import dataclass
from src.exception.exception import CustomException
from src.logger.logger import logger
import os
import sys
import pandas as pd 
import numpy as np 
import pickle


@dataclass
class DataValidationConfig:
  ingested_data_dir: str = os.path.join("artifacts", "ingested_data")
  clean_data_dir: str = os.path.join("artifacts", "clean_data")
  books_csv_file: str = os.path.join(ingested_data_dir, "BX-Books.csv")
  ratings_csv_file: str = os.path.join(ingested_data_dir, "BX-Book-Ratings.csv")
  serialized_object_dir:str = os.path.join('artifacts', "serialized_objects")
  
  
class DataValidation:
  def __init__(self):
    self.data_validation_config = DataValidationConfig()
    
  def data_preprocessing(self):
    try:
      logger.info("Data preprocessing started")
      
      books = pd.read_csv(self.data_validation_config.books_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1', dtype={"Year-Of-Publication": str})
      
      ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1')
      
      logger.info(f"Shape of books dataframe: {books.shape}")
      logger.info(f"Shape of ratings dataframe: {ratings.shape}")
      
      #selecting columns
      books = books[['ISBN','Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher','Image-URL-L']]
      
      #renaming columns
      books.rename(columns={"Book-Title":'title',
                      'Book-Author':'author',
                     "Year-Of-Publication":'year',
                     "Publisher":"publisher",
                     "Image-URL-L":"image_url"},inplace=True)
      
      ratings.rename(columns={"User-ID":'user_id',
                      'Book-Rating':'rating'},inplace=True)
      
      x = ratings['user_id'].value_counts() > 200
      
      y= x[x].index
      
      ratings = ratings[ratings['user_id'].isin(y)]
      
      
      # join ratings with books based on ISBN column
      ratings_with_books = ratings.merge(books, on='ISBN')
      number_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
      
      #renaming columns
      number_rating.rename(columns={'rating':'num_of_rating'},inplace=True)
      final_rating = ratings_with_books.merge(number_rating, on='title')
      
      logger.info("Filter out the final rating which have at least 50 ratings")
      final_rating = final_rating[final_rating['num_of_rating'] >= 50]
      
      # lets drop the duplicates
      final_rating.drop_duplicates(['user_id','title'],inplace=True)
      logger.info(f"Shape of final_rating dataframe: {final_rating.shape}")
      
      os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
      final_rating.to_csv(os.path.join(self.data_validation_config.clean_data_dir, 'clean_data.csv'), index=False)
      logger.info(f"Saved cleaned data to {self.data_validation_config.clean_data_dir}")
      
      #saving final rating object for web app
      os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
      
      pickle.dump(final_rating, open(os.path.join(self.data_validation_config.serialized_object_dir, 'final_rating.pkl'), 'wb'))
      
      logger.info(f"Saved final rating object to {self.data_validation_config.serialized_object_dir}")
      
    except Exception as e:
      logger.error("Failed while preprocessing data")
      raise CustomException(e, sys)
    
  def initiate_data_validation(self):
    try:
      self.data_preprocessing()
    except Exception as e:
      logger.error("Failed while initiating data validation")
      raise CustomException(e, sys)