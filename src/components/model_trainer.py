from src.exception.exception import CustomException
from src.logger.logger import logger
import os
import sys
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle
from dataclasses import dataclass
import mlflow
import dagshub
import time
from dotenv import load_dotenv

load_dotenv()

mlflow.set_tracking_uri(
    "https://dagshub.com/shubhamgupta43567/Production-Scale-Personalized-Recommendation-Engine-using-Collaborative-Filtering.mlflow"
)

if os.getenv("MLFLOW_TRACKING_USERNAME") and os.getenv("MLFLOW_TRACKING_PASSWORD"):
    dagshub.init(
        repo_owner="shubhamgupta43567",
        repo_name="Production-Scale-Personalized-Recommendation-Engine-using-Collaborative-Filtering",
        mlflow=True
    )
mlflow.set_experiment(
    "book_recommender_training"
)

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

        book_pivot = pickle.load(
            open(
                self.model_trainer_config.book_pivot,
                'rb'
            )
        )

        book_names = pickle.load(
            open(
                self.model_trainer_config.book_names,
                'rb'
            )
        )

        logger.info("Pickle files loaded")

        start_time = time.time()

        book_sparse = csr_matrix(
            book_pivot
        )

        logger.info(
            f"Sparse matrix created. "
            f"type(book_sparse): {type(book_sparse)}"
        )

        with mlflow.start_run():

            mlflow.log_param(
                "algorithm",
                "brute"
            )

            mlflow.log_param(
                "metric",
                "cosine"
            )

            mlflow.log_param(
                "num_books",
                book_pivot.shape[0]
            )

            mlflow.log_param(
                "num_users",
                book_pivot.shape[1]
            )


            model = NearestNeighbors(
                algorithm='brute',
                metric='cosine'
            )

            model.fit(book_sparse)

            logger.info("Model trained")

            training_time = round(
                time.time() - start_time,
                4
            )

            mlflow.log_metric(
                "training_time_sec",
                training_time
            )

            mlflow.log_metric(
                "dataset_rows",
                book_pivot.shape[0]
            )

            mlflow.log_metric(
                "dataset_columns",
                book_pivot.shape[1]
            )

            os.makedirs(
                self.model_trainer_config.trained_model_dir,
                exist_ok=True
            )

            pickle.dump(
                model,
                open(
                    self.model_trainer_config.trained_model_name,
                    'wb'
                )
            )

            logger.info("Model saved")

            mlflow.log_artifact(
                self.model_trainer_config.trained_model_name
            )

            mlflow.log_artifact(
                self.model_trainer_config.book_pivot
            )

            mlflow.log_artifact(
                self.model_trainer_config.book_names
            )

            mlflow.sklearn.log_model(
                sk_model=model,
                name="book_recommender_model"
                )

            logger.info(
                "MLflow tracking completed"
            )

        logger.info(
            "Model trainer completed"
        )

    except Exception as e:
        logger.error(
            "Failed while initiating model trainer"
        )
        raise CustomException(e, sys)
      
  def initiate_model_trainer(self):
    try:
      self.model_trainer()
    except Exception as e:
      logger.error("Failed while initiating model trainer")
      raise CustomException(e, sys)
