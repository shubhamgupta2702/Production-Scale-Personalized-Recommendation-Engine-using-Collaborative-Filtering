from src.exception.exception import CustomException
from src.logger.logger import logger
import os
import sys
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle
from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
  transformed_data_dir = os.path.join("artifacts", "transformed_data")
  book_pivot = os.path.join(transformed_data_dir, "book_pivot.pkl")
  book_names = os.path.join(transformed_data_dir, "book_names.pkl")
  trained_model_dir = os.path.join("artifacts", "trained_model")
  trained_model_name = os.path.join(trained_model_dir, "model.pkl")
  
  
class ModelTrainer:
  def __init__(self):
    self.model_trainer_config = ModelTrainerConfig()
    
  def model_trainer(self):
    try:
      logger.info("Model trainer started")
      
      book_pivot = pickle.load(open(self.model_trainer_config.book_pivot, 'rb'))
      book_names = pickle.load(open(self.model_trainer_config.book_names, 'rb'))
      logger.info("Pickle files loaded")
      
      book_sparse = csr_matrix(book_pivot)
      logger.info(f"Sparse matrix created. type(book_sparse): {type(book_sparse)}")
      
      model = NearestNeighbors(algorithm= 'brute', metric='cosine')
      model.fit(book_sparse)
      logger.info("Model trained")
      
      os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
      pickle.dump(model, open(self.model_trainer_config.trained_model_name, 'wb'))
      logger.info("Model saved")
      
      logger.info("Model trainer completed")
      
      
    except Exception as e:
      logger.error("Failed while initiating model trainer")
      raise CustomException(e, sys)
      
  
  def initiate_model_trainer(self):
    try:
      self.model_trainer()
    except Exception as e:
      logger.error("Failed while initiating model trainer")
      raise CustomException(e, sys)