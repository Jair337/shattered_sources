import json
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, confusion_matrix, accuracy_score, precision_score, \
    recall_score, f1_score


def ML_demo_random_forest():
    ## Load the JSON Data
    with open('ml_test_data.json', 'r') as f:
        json_data = json.load(f)

    df = pd.DataFrame(json_data)

    ## Define inputs (X) using ONLY text-based keys, and target (y)
    feature_columns = ['title', 'description', 'event_type', 'category', 'country', 'region', 'city']
    X = df[feature_columns]
    y = df['severity']

    ## Split the data using sklearn train_test_split, with 20 rows reserved for validation.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=20, random_state=67)

    ## Processes the data so it can be used
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(ngram_range=(1, 2), max_features=3500, stop_words='english', sublinear_tf=True),
             'title'),
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['event_type', 'category', 'country', 'region', 'city'])
        ]
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        ))
    ])

    ## Execute Training
    model.fit(X_train, y_train)

    ## List of predicted severities
    predictions = model.predict(X_test)

    ## Round the predictions to the nearest integer to match the severity levels, needed for the metrics to work
    integer_predictions = np.round(predictions).astype(int)

    ## Calculate error metrics
    mae = mean_absolute_error(y_test, integer_predictions)
    r2 = r2_score(y_test, integer_predictions)
    residuals = y_test.values - integer_predictions
    cm = confusion_matrix(y_test, integer_predictions)
    accuracy = accuracy_score(y_test, integer_predictions)
    precision = precision_score(y_test, integer_predictions, average='weighted')
    recall = recall_score(y_test, integer_predictions, average='weighted')
    f1 = f1_score(y_test, integer_predictions, average='weighted')

    return mae, r2, residuals, cm, accuracy, precision, recall, f1, predictions, y_test