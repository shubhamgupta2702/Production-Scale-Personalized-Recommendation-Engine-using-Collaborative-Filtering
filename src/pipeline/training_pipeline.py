from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation



class TrainingPipeline:
  def __init__(self):
    self.data_ingestion = DataIngestion()
    self.data_validation = DataValidation()
    self.data_transformation = DataTransformation()
    
  def start_training_pipeline(self):
    """Start the training pipeline and return none"""
    self.data_ingestion.initiate_data_ingestion()
    self.data_validation.initiate_data_validation()
    self.data_transformation.initiate_data_transformation()