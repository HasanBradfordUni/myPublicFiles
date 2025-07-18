import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
import joblib
import numpy as np

# Load the training data
data = pd.read_csv('trainingData.csv', delimiter=';')

# Check class distribution
print("Class distribution:")
class_distribution = data['python'].value_counts()
print(class_distribution)

# Filter out classes with only one sample
min_samples_per_class = 2
print(f"\nRemoving classes with fewer than {min_samples_per_class} samples...")
valid_classes = class_distribution[class_distribution >= min_samples_per_class].index
filtered_data = data[data['python'].isin(valid_classes)]

print(f"Original dataset size: {len(data)}")
print(f"Filtered dataset size: {len(filtered_data)}")
print(f"Removed {len(data) - len(filtered_data)} samples")

# Preprocess the filtered data
X = filtered_data['code']
y = filtered_data['python']

# Train a simpler model without cross-validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with reasonable default parameters
model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 3), max_features=5000),
    RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
)

print("\nTraining model without cross-validation...")
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print("\nDetailed classification report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'trained_model.pkl')

# Show a few examples of predictions vs actual
print("\nSample predictions:")
for i in range(min(5, len(X_test))):
    print(f"Input: {X_test.iloc[i]}")
    print(f"Predicted: {y_pred[i]}")
    print(f"Actual: {y_test.iloc[i]}")
    print("-" * 50)