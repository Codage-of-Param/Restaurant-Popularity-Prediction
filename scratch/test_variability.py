import sys
from pathlib import Path
import pandas as pd
sys.path.append(str(Path("backend").resolve()))

from predictor import load_artifacts, build_feature_row, predict_rating

artifacts = load_artifacts("backend/model.pkl", "backend/encoders.pkl")

test_cases = [
    {"city": "New Delhi", "cuisines": "North Indian", "cost": 500},
    {"city": "Mumbai", "cuisines": "Italian", "cost": 2000},
    {"city": "Kolkata", "cuisines": "Bengali", "cost": 800},
]

for case in test_cases:
    features, warnings = build_feature_row(
        artifacts=artifacts,
        city=case["city"],
        cuisines=case["cuisines"],
        country="India",
        avg_cost_for_two=case["cost"],
        price_range=2 if case["cost"] < 1000 else 4,
        service_score=2
    )
    rating = predict_rating(artifacts=artifacts, features=features)
    print(f"City: {case['city']}, Cuisines: {case['cuisines']}, Cost: {case['cost']} => Predicted Rating: {rating}")
