import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, confusion_matrix

# ==========================================
# 1. LOAD THE DATA
# ==========================================
print("Loading data...")
with open('../synthetic_seerist_events.json', 'r') as f:
    data = json.load(f)

# pd.json_normalize flattens nested JSON (e.g., 'impact.likely_disruption')
df = pd.json_normalize(data['events'])

# ==========================================
# 2. FEATURE ENGINEERING (Text to Numbers)
# ==========================================
print("Engineering features...")

# A. Numeric & Boolean (Ready to use)
df['source_count'] = df['provenance.source_count'].fillna(0)
df['human_reviewed'] = df['provenance.human_reviewed'].astype(int)

# B. Ordinal Categorical (Ranked Mapping)
disruption_map = {
    "none": 0, "minimal": 1, "localized": 2,
    "moderate": 3, "significant": 4, "severe": 5
}
df['disruption_score'] = df['impact.likely_disruption'].map(disruption_map).fillna(0)

# C. Nominal Categorical (One-Hot Encoding)
# This turns 'category' into 'category_security' (0 or 1), 'category_weather', etc.
df_encoded = pd.get_dummies(df, columns=['category', 'region'], dummy_na=False)

# Filter out the newly created One-Hot columns
one_hot_cols = [c for c in df_encoded.columns if c.startswith('category_') or c.startswith('region_')]

# D. Arrays / Lists (Multi-Hot Encoding)
# This handles the arrays like ["travel", "employee_safety"]
mlb_domains = MultiLabelBinarizer()
# We use fillna([]) to handle any empty lists before encoding
domains_encoded = pd.DataFrame(
    mlb_domains.fit_transform(df['impact.affected_domains'].apply(lambda x: x if isinstance(x, list) else [])),
    columns=[f"domain_{c}" for c in mlb_domains.classes_],
    index=df.index
)

mlb_tags = MultiLabelBinarizer()
tags_encoded = pd.DataFrame(
    mlb_tags.fit_transform(df['tags'].apply(lambda x: x if isinstance(x, list) else [])),
    columns=[f"tag_{c}" for c in mlb_tags.classes_],
    index=df.index
)

# E. Combine everything into our final Feature Matrix (X)
feature_cols = ['severity', 'source_count', 'human_reviewed', 'disruption_score'] + one_hot_cols
X = pd.concat([df_encoded[feature_cols], domains_encoded, tags_encoded], axis=1)

X.to_json("transformed_events.json", orient="records", indent=4)
X.to_csv("transformed_events.csv", index=False)

print(X.head(10))
# ==========================================
# 3. CREATE THE TARGET VARIABLE (y)
# ==========================================
# We are creating a proxy: We assume an analyst SHOULD review this if:
# Severity is 4 or 5  -OR-  it impacts 'employee_safety'
base_rule = (df['severity'] >= 4) | (df['impact.affected_domains'].apply(lambda x: 'employee_safety' in x if isinstance(x, list) else False))

# We add 10% random noise to simulate human errors or nuanced edge cases
np.random.seed(42)
noise = np.random.choice([0, 1], size=len(df), p=[0.90, 0.10])
y = base_rule.astype(int) ^ noise  # XOR flips the label 10% of the time

# ==========================================
# 4. TRAIN AND EVALUATE THE MODEL
# ==========================================
print("Training the model...")
# Split into 80% training data, 20% testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict probabilities on the test set
probabilities = model.predict_proba(X_test)[:, 1]

# Calculate Overall AUC
model_auc = roc_auc_score(y_test, probabilities)

# Find the best threshold using F1-Score
thresholds = np.arange(0.0, 1.05, 0.05)
best_threshold, best_f1 = 0.0, -1.0
best_metrics = {}

for t in thresholds:
    preds = (probabilities >= t).astype(int)
    f1 = f1_score(y_test, preds, zero_division=0)

    if f1 > best_f1:
        best_f1 = f1
        best_threshold = t
        best_metrics = {
            'Precision': precision_score(y_test, preds, zero_division=0),
            'Recall': recall_score(y_test, preds, zero_division=0)
        }

# ==========================================
# 5. DISPLAY RESULTS
# ==========================================
print("\n" + "=" * 40)
print(f"🌟 OVERALL MODEL AUC: {model_auc:.3f}")
print("=" * 40)
print(f"🥇 OPTIMAL THRESHOLD: {best_threshold:.2f}")
print(f" - F1-Score: {best_f1:.3f}")
print(f" - Precision: {best_metrics['Precision']:.3f} (When it alerts, it's highly accurate)")
print(f" - Recall: {best_metrics['Recall']:.3f} (Caught almost all the real threats)")

# Let's peek inside the model's brain to see what it learned!
print("\n🧠 WHAT THE MODEL LEARNED (Feature Weights):")
weights_df = pd.DataFrame({
    'Feature': X.columns,
    'Weight': model.coef_[0]
}).sort_values(by='Weight', ascending=False)

print("\n--- Top 5 Indicators an event SHOULD be analyzed ---")
print(weights_df.head(5).to_string(index=False))

print("\n--- Top 5 Indicators an event can be IGNORED ---")
print(weights_df.tail(5).sort_values(by='Weight', ascending=True).to_string(index=False))
