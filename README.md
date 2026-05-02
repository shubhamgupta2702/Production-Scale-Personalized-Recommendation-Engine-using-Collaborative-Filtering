📚 Production-Scale Personalized Book Recommendation Engine

A production-grade personalized book recommendation system built using **Collaborative Filtering**, designed with modular ML pipelines, experiment tracking, API serving, containerization, and CI/CD automation.

This project demonstrates how to take a recommendation model from raw data ingestion to production deployment using modern MLOps practices.

---

## 🚀 Project Overview

This system recommends books based on user-book interaction history using **Item-Based Collaborative Filtering** with **K-Nearest Neighbors (KNN)**.

The pipeline:

- Ingests raw book-rating data
- Cleans and validates user-book interactions
- Builds a sparse user-item matrix
- Trains a nearest-neighbor recommendation model
- Tracks experiments with MLflow + DagsHub
- Serves recommendations via FastAPI
- Provides an interactive Streamlit UI
- Containerized with Docker
- Automated with GitHub Actions CI/CD

---

## 🏗️ Production Architecture

```text
Raw Dataset
    │
    ▼
Data Ingestion
    │
    ▼
Data Validation
    │
    ▼
Data Transformation
    │
    ▼
Model Training
    │
    ▼
Serialized Artifacts
    │
    ├── FastAPI API Layer
    │
    ├── Streamlit Frontend
    │
    └── Docker Container
```

---

## 📂 Project Structure

```text
.
├── artifacts/
│   ├── raw_data/
│   ├── ingested_data/
│   ├── clean_data/
│   ├── transformed_data/
│   ├── serialized_objects/
│   └── trained_model/
│
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── pipeline/
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   │
│   ├── logger/
│   ├── exception/
│   ├── utils/
│   └── constant/
│
├── tests/
├── logs/
├── app.py
├── api.py
├── main.py
├── requirements.txt
├── Dockerfile
└── .github/workflows/
```

---

## ⚙️ Tech Stack

### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn
- SciPy

### Backend
- FastAPI
- Pydantic
- Uvicorn

### Frontend
- Streamlit

### MLOps
- MLflow
- DagsHub
- Docker
- GitHub Actions

---

## 🧠 Recommendation Logic

This project uses:

### Item-Based Collaborative Filtering

Books are recommended based on similarity in user interaction patterns.

### Algorithm

KNN with:

- brute-force nearest neighbors
- cosine similarity metric

### Why this approach?

- Simple
- Interpretable
- Effective for sparse recommendation datasets
- Scales well with sparse matrix representation

---

## 📊 Dataset

Dataset used:

Book-Crossing Dataset

Contains:

- Books metadata
- User ratings
- User information

Files:

- BX-Books.csv
- BX-Book-Ratings.csv
- BX-Users.csv

---

## 🔄 Training Pipeline

Run complete training pipeline:

```bash
python main.py
```

Pipeline stages:

### 1. Data Ingestion
- Downloads dataset
- Extracts ZIP
- Stores raw files

### 2. Data Validation
- Cleans data
- Filters active users (>200 interactions)
- Filters popular books (>50 ratings)

### 3. Data Transformation
- Creates pivot matrix
- Serializes transformed artifacts

### 4. Model Training
- Converts pivot to sparse matrix
- Trains KNN model
- Saves model artifacts
- Tracks experiment with MLflow

---

## 📈 Experiment Tracking

Integrated with:

- MLflow
- DagsHub

Tracked:

### Parameters
- algorithm
- metric
- number of books
- number of users

### Metrics
- training time
- dataset dimensions

### Artifacts
- trained model
- pivot matrix
- book names

---

## 🌐 FastAPI Backend

Run API:

```bash
uvicorn api:app --reload
```

Swagger docs:

```text
http://localhost:8000/docs
```

### Endpoints

#### Health Check

```http
GET /health
```

#### Get Books

```http
GET /books
```

#### Recommend Books

```http
POST /recommend
```

Request:

```json
{
  "book_name": "Harry Potter and the Sorcerer's Stone (Book 1)",
  "top_n": 5
}
```

Response:

```json
{
  "input_book": "Harry Potter and the Sorcerer's Stone (Book 1)",
  "total_recommendations": 5,
  "recommendations": [],
  "latency": 45.92
}
```

---

## 🎨 Streamlit Frontend

Run UI:

```bash
streamlit run app.py
```

Features:

- Book dropdown selection
- Recommendation display
- Book cover previews
- Author information

---

## 🐳 Docker Support

Build:

```bash
docker build -t book-recommender .
```

Run:

```bash
docker run -p 8000:8000 book-recommender
```

Pull from Docker Hub:

```bash
docker pull shubhamgupta2702/book-recommender
```

---

## 🔁 CI/CD Pipeline

Automated with GitHub Actions.

Pipeline includes:

- Dependency installation
- Training pipeline execution
- MLflow experiment logging
- Docker image build
- Docker image push

Triggered on:

```text
push to main branch
```

---

## 📌 Performance Metrics

### API Latency

Average latency:

```text
45.92 ms
```

### Recommendation Strategy

KNN + Cosine Similarity

### Sparse Matrix Optimization

Used CSR matrix for memory efficiency.

---

## 🛠 Installation

Clone repository:

```bash
git clone https://github.com/shubhamgupta2702/Production-Scale-Personalized-Recommendation-Engine-using-Collaborative-Filtering.git
```

Move into project:

```bash
cd Production-Scale-Personalized-Recommendation-Engine-using-Collaborative-Filtering
```

Create virtual environment:

```bash
python -m venv env
```

Activate:

Windows:

```bash
env\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create `.env`

```env
MLFLOW_TRACKING_USERNAME=your_username
MLFLOW_TRACKING_PASSWORD=your_token
```

---

## 📷 Application Preview

Add screenshots here.

Suggested:

- Streamlit UI
- <img width="1811" height="805" alt="image" src="https://github.com/user-attachments/assets/761fe469-1575-41ed-8cb0-d1d19db6102e" />

- Swagger docs
- <img width="1904" height="817" alt="image" src="https://github.com/user-attachments/assets/3ab2ab31-8c86-44c8-95fc-c2eb605e0389" />

- MLflow dashboard
- <img width="1608" height="775" alt="image" src="https://github.com/user-attachments/assets/4bba8865-b109-40b9-8484-93e62f021f39" />
<img width="1905" height="600" alt="image" src="https://github.com/user-attachments/assets/a31b02b5-0bf9-4c96-8460-eb3c12a2acc1" />


- Docker image
- <img width="1894" height="762" alt="image" src="https://github.com/user-attachments/assets/08740cb9-debf-41d8-879f-662c9d2536e1" />

---

## 📬 Contact

Shubham Gupta

GitHub:
https://github.com/shubhamgupta2702

LinkedIn:
https://www.linkedin.com/in/shubhamg2702/

Gmail:
shubhamgupta43567@gmail.com

---
