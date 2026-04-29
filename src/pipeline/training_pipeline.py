from src.components.data_ingestion import DataIngestion,DataIngestionConfig



class TrainingPipeline:
  def __init__(self):
    self.data_ingestion = DataIngestion()
    
  def start_training_pipeline(self):
    """Start the training pipeline and return none"""
    self.data_ingestion.initiate_data_ingestion()