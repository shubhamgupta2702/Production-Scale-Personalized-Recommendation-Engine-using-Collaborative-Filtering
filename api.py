from fastapi import FastAPI, HTTPException
from src.pipeline.prediction_pipeline import RecommendationRequest, RecommendationResponse
import time
import os
import pickle
from src.logger.logger import logger
from src.utils.utils import load_object

latency_history = []

MODEL_VERSION = "1.0.0"
app = FastAPI(title="Personalized Book Recommender API", version=MODEL_VERSION)

ARTIFACTS_DIR = "artifacts"

FINAL_RATING_PATH = os.path.join(
    ARTIFACTS_DIR,
    "serialized_objects",
    "final_rating.pkl"
)

BOOK_PIVOT_PATH = os.path.join(
    ARTIFACTS_DIR,
    "transformed_data",
    "book_pivot.pkl"
)

BOOK_NAMES_PATH = os.path.join(
    ARTIFACTS_DIR,
    "transformed_data",
    "book_names.pkl"
)

MODEL_PATH = os.path.join(
    ARTIFACTS_DIR,
    "trained_model",
    "model.pkl"
)

try:
  final_rating = load_object(FINAL_RATING_PATH)
  book_pivot = load_object(BOOK_PIVOT_PATH)
  book_names = load_object(BOOK_NAMES_PATH)
  model = load_object(MODEL_PATH)
  
  if final_rating is None or book_pivot is None or book_names is None or model is None:
    raise Exception("Artifacts not found")
  
  logger.info("Artifacts loaded successfully")
  
except Exception as e:
  logger.error(f"Failed to load artifacts: {e}")
  raise HTTPException(status_code=500, detail=f"Failed to load artifacts: {e}")



@app.get('/')
def hello():
    return {"message": "Welcome to Personalized Book Recommender API"}
  
@app.get('/health')
def health_check():
    return {"status": "ok",
            "version": MODEL_VERSION,
            "model_loaded": model is not None
            }
    
@app.get('/books')
def get_books():
    return {
        "books": list(book_names)
    }
    
@app.post('/recommend', response_model=RecommendationResponse)
def recommend_books(request: RecommendationRequest):
  start_time = time.time()
  try:
    
    if model is None or final_rating is None or book_names is None or book_pivot is None:
      raise HTTPException(status_code=500, detail="Model not loaded")
    
    
    book_name = request.book_name
    top_n = request.top_n

    if book_name not in book_pivot.index:
      raise HTTPException(status_code=404,detail=f"Book '{book_name}' not found")

    book_id = book_pivot.index.get_loc(book_name)

    distances, suggestions = model.kneighbors(
            book_pivot.iloc[
                book_id, :
            ].values.reshape(1, -1),
            n_neighbors=top_n + 1
        )

    recommendations = []

    for i in suggestions[0]:
      title = book_pivot.index[i]

      temp_df = final_rating[final_rating["title"] == title]

      temp_df = temp_df.drop_duplicates("title")

      if not temp_df.empty:
        recommendations.append(
                    {
                        "title": temp_df[
                            "title"
                        ].values[0],
                        "author": temp_df[
                            "author"
                        ].values[0],
                        "image_url": temp_df[
                            "image_url"
                        ].values[0]
                    }
                )

    recommendations = recommendations[1:]

    latency = round((time.time() - start_time) * 1000, 4)
    latency_history.append(latency)
    
    average_latency = round((sum(latency_history)/ len(latency_history)), 4)

    logger.info(
            f"Recommendation generated in "
            f"{latency} ms"
        )

    return RecommendationResponse(
            input_book=book_name,
            total_recommendations=len(
                recommendations
            ),
            recommendations=recommendations,
            latency=latency,
            average_latency=average_latency
        )
    
    
  except Exception as e:
    logger.error(f"Recommendation failed: {e}")
    raise HTTPException(status_code=500,detail=f"Internal Server Error: {e}")