from setuptools import find_packages, setup

setup(
    name="Personalized Recommendation System",
    version="0.0.1",
    author="Shubham Gupta",
    author_email="shubhamgupta43567@gmail.com",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "fastapi",
        "uvicorn",
        "python-dotenv", 
        "scikit-learn",
        "joblib",
        "pydantic"
    ]
)