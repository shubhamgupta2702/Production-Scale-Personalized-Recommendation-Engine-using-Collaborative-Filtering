import os
import zipfile
import sys
from src.logger.logger import logger
from src.exception.exception import CustomException
from dataclasses import dataclass
from src.constant import *
import urllib
from urllib.request import urlretrieve



@dataclass
class DataIngestionConfig:
  artifacts_dir: str = 'artifacts'
  dataset_url:str = DATASET_URL
  dataset_zip_path: str = os.path.join('artifacts', "books_data.zip")
  raw_data_dir: str = os.path.join('artifacts', "raw_data")
  ingested_data_dir: str = os.path.join('artifacts', "ingested_data")
  
  
  
class DataIngestion:
  def __init__(self):
    self.ingestion_config = DataIngestionConfig()
    
  def create_directories(self):
    """
    Create required directories for data ingestion.
    """
    try:
      os.makedirs(self.ingestion_config.artifact_dir, exist_ok=True)
      os.makedirs(self.ingestion_config.raw_data_dir, exist_ok=True)
      os.makedirs(self.ingestion_config.ingested_data_dir, exist_ok=True)

      logger.info("Required directories created successfully")

    except Exception as e:
      logger.error("Failed while creating directories")
      raise CustomException(e, sys)
    
  def download_data(self):
    """Download dataset zip from source URL"""
    try:
      logger.info("Downloading data from source URL")
      zip_path = self.ingestion_config.dataset_zip_path
      
      if os.path.exists(zip_path):
        logger.info("Data already downloaded")
        return zip_path
      
      urllib.request.urlretrieve(self.ingestion_config.dataset_url, zip_path)
      logger.info("Data downloaded successfully")
      return zip_path
    
    except Exception as e:
      logger.error("Failed while downloading data")
      raise CustomException(e, sys)
    
  def extract_data(self):
    """Extracting the downloaded zip file"""
    try:
      logger.info("Extracting data")
      zip_path = self.ingestion_config.dataset_zip_path
      
      if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Zip file not found at {zip_path}")
      
      logger.info("Unzipping data")
      
      with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(self.ingestion_config.raw_data_dir)

      logger.info("Dataset extracted successfully")

      return self.ingestion_config.raw_data_dir
    
    except Exception as e:
      logger.error("Failed while extracting dataset")
      raise CustomException(e, sys)
    
  def initiate_data_ingestion(self):
    """Complete Data Ingestion Pipeline"""
    try:
      logger.info("Data ingestion started")

      self.create_directories()
      self.download_data()
      raw_data_path = self.extract_data()

      logger.info("Data ingestion completed successfully")

      return raw_data_path

    except Exception as e:
      logger.error("Data ingestion pipeline failed")
      raise CustomException(e, sys)

