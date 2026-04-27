import sys
from pathlib import Path
import pandas as pd
sys.path.append(str(Path("backend").resolve()))

from predictor import load_artifacts, build_feature_row, predict_rating

artifacts = load_artifacts("backend/model.pkl", "backend/encoders.pkl")

# dummy fast API data
features, warnings = build_feature_row(
    artifacts=artifacts,
    city="New Delhi",
    cuisines="North Indian, Mughlai",
    country="India",
    avg_cost_for_two=1500,
    price_range=3,
    service_score=2
)

if warnings:
    print("Warnings:", warnings)

rating = predict_rating(artifacts=artifacts, features=features)
print(f"Predicted Rating: {rating}")
