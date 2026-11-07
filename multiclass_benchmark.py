# ==========================================
# 1. IMPORTING REQUIRED LIBRARIES
# ==========================================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Importing train_test_split to divide data into training and testing sets
from sklearn.model_selection import train_test_split

# Importing StandardScaler for feature scaling
from sklearn.preprocessing import StandardScaler

# Importing classification algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# Importing evaluation metrics
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)


# ==========================================
# 2. LOADING THE DATASET
# ==========================================

# Reading the Iris dataset using pandas
df = pd.read_csv("ml_project/iris.csv")

# Displaying the first five rows
print(df.head())


# ==========================================
# 3. EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================

# Checking the number of rows and columns
print("Dataset Shape:", df.shape)

# Checking column names, data types and non-null values
print(df.info())

# Checking missing values in each column
print(df.isnull().sum())

# Generating statistical summary of the dataset
print(df.describe(include='all'))

# Visualizing relationships between features
# hue='species' assigns different colors to different flower classes
sns.pairplot(df, hue='species')
plt.show()


# ==========================================
# 4. SEPARATING FEATURES AND TARGET
# ==========================================

# X contains all input features
# Removing the target column 'species' from the dataset
x = df.drop('species', axis=1)

# y contains the target variable that we want to predict
y = df['species']


# ==========================================
# 5. SPLITTING DATA INTO TRAINING AND TESTING SETS
# ==========================================

# 80% data is used for training and 20% for testing
# random_state ensures reproducible results
# stratify maintains the same class distribution in both sets
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================================
# 6. FEATURE SCALING
# ==========================================

# Creating a StandardScaler object
scaler = StandardScaler()

# Learning scaling parameters from training data and transforming it
x_train = scaler.fit_transform(x_train)

# Applying the same scaling parameters to test data
# We use transform() instead of fit_transform() to avoid data leakage
x_test = scaler.transform(x_test)


# ==========================================
# 7. MODEL TRAINING
# ==========================================

# Creating Logistic Regression model
model_lr = LogisticRegression()

# Training Logistic Regression using training data
model_lr.fit(x_train, y_train)


# Creating Decision Tree model
# random_state ensures reproducible results
model_tree = DecisionTreeClassifier(random_state=42)

# Training Decision Tree using training data
model_tree.fit(x_train, y_train)


# ==========================================
# 8. MAKING PREDICTIONS
# ==========================================

# Predicting flower species using Logistic Regression
y_pred_lr = model_lr.predict(x_test)

# Predicting flower species using Decision Tree
y_pred_tree = model_tree.predict(x_test)


# ==========================================
# 9. MODEL EVALUATION
# ==========================================

# Calculating accuracy for both models
accuracy_lr = accuracy_score(y_test, y_pred_lr)
accuracy_tree = accuracy_score(y_test, y_pred_tree)

# Calculating weighted precision
precision_lr = precision_score(y_test, y_pred_lr, average='weighted')
precision_tree = precision_score(y_test, y_pred_tree, average='weighted')

# Calculating weighted recall
recall_lr = recall_score(y_test, y_pred_lr, average='weighted')
recall_tree = recall_score(y_test, y_pred_tree, average='weighted')

# Calculating weighted F1-score
f1_lr = f1_score(y_test, y_pred_lr, average='weighted')
f1_tree = f1_score(y_test, y_pred_tree, average='weighted')


# ==========================================
# 10. PRINTING CLASSIFICATION REPORTS
# ==========================================

# Classification report provides precision, recall, F1-score and support
print("\nLogistic Regression Classification Report:")
print(classification_report(y_test, y_pred_lr))

print("\nDecision Tree Classification Report:")
print(classification_report(y_test, y_pred_tree))


# ==========================================
# 11. CONFUSION MATRICES
# ==========================================

# Creating confusion matrices for both models
cm_lr = confusion_matrix(y_test, y_pred_lr)
cm_tree = confusion_matrix(y_test, y_pred_tree)

print("\nLogistic Regression Confusion Matrix:")
print(cm_lr)

print("\nDecision Tree Confusion Matrix:")
print(cm_tree)


# ==========================================
# 12. MODEL COMPARISON
# ==========================================

# Creating a DataFrame to compare model performance
comparison = pd.DataFrame({
    'Model': ['Logistic Regression', 'Decision Tree'],
    'Accuracy': [accuracy_lr, accuracy_tree],
    'Precision': [precision_lr, precision_tree],
    'Recall': [recall_lr, recall_tree],
    'F1 Score': [f1_lr, f1_tree]
})

# Displaying model comparison results
print("\nModel Performance Comparison:")
print(comparison.round(4))


# ==========================================
# 13. CONFUSION MATRIX VISUALIZATION
# ==========================================

# Creating two plots side by side
plt.figure(figsize=(12, 5))

# First subplot for Logistic Regression
plt.subplot(1, 2, 1)

sns.heatmap(
    cm_lr,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=model_lr.classes_,
    yticklabels=model_lr.classes_
)

plt.title('Logistic Regression Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')


# Second subplot for Decision Tree
plt.subplot(1, 2, 2)

sns.heatmap(
    cm_tree,
    annot=True,
    fmt='d',
    cmap='Greens',
    xticklabels=model_tree.classes_,
    yticklabels=model_tree.classes_
)

plt.title('Decision Tree Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')

# Adjusting spacing between plots
plt.tight_layout()
plt.show()


# ==========================================
# 14. SELECTING TWO FEATURES FOR DECISION BOUNDARY
# ==========================================

# Selecting only two features because decision boundary
# visualization is easier to understand in a 2D graph
x_2d = df[['petal_length', 'petal_width']]

# Target variable
y_2d = df['species']


# ==========================================
# 15. SPLITTING THE TWO-FEATURE DATA
# ==========================================

# Splitting the selected two features into training and testing sets
x_train_2d, x_test_2d, y_train_2d, y_test_2d = train_test_split(
    x_2d,
    y_2d,
    test_size=0.2,
    random_state=42,
    stratify=y_2d
)


# ==========================================
# 16. SCALING TWO-FEATURE DATA
# ==========================================

# Creating a separate scaler for the two-feature dataset
scaler_2d = StandardScaler()

# Fitting scaler on training data and transforming it
x_train_2d = scaler_2d.fit_transform(x_train_2d)

# Applying the same scaling parameters to testing data
x_test_2d = scaler_2d.transform(x_test_2d)


# ==========================================
# 17. TRAINING TWO-FEATURE MODELS
# ==========================================

# Training Logistic Regression using only two features
model_lr_2d = LogisticRegression()
model_lr_2d.fit(x_train_2d, y_train_2d)

# Training Decision Tree using only two features
model_tree_2d = DecisionTreeClassifier(random_state=42)
model_tree_2d.fit(x_train_2d, y_train_2d)


# ==========================================
# 18. CREATING A MESHGRID
# ==========================================

# Finding minimum and maximum values of the first feature
x_min = x_train_2d[:, 0].min() - 1
x_max = x_train_2d[:, 0].max() + 1

# Finding minimum and maximum values of the second feature
y_min = x_train_2d[:, 1].min() - 1
y_max = x_train_2d[:, 1].max() + 1

# Creating coordinate points across the graph
xx, yy = np.meshgrid(
    np.arange(x_min, x_max, 0.02),
    np.arange(y_min, y_max, 0.02)
)

# Combining the coordinates into a two-column array
# Each row represents one point on the graph
grid = np.c_[xx.ravel(), yy.ravel()]


# ==========================================
# 19. PREDICTING GRID POINTS
# ==========================================

# Getting the class names learned by Logistic Regression
classes = model_lr_2d.classes_

# Mapping each flower species to a numeric value
# Numeric values are required for contour plotting
class_mapping = {
    label: index for index, label in enumerate(classes)
}

# Predicting the class for every point in the grid using Logistic Regression
Z_lr = model_lr_2d.predict(grid)

# Converting predicted class names into numeric values
# Reshaping predictions to match the meshgrid dimensions
Z_lr = np.array([
    class_mapping[label] for label in Z_lr
]).reshape(xx.shape)


# Predicting the class for every point using Decision Tree
Z_tree = model_tree_2d.predict(grid)

# Converting predicted class names into numeric values
# Reshaping predictions to match the meshgrid dimensions
Z_tree = np.array([
    class_mapping[label] for label in Z_tree
]).reshape(xx.shape)


# ==========================================
# 20. DECISION BOUNDARY VISUALIZATION
# ==========================================

# Creating two plots side by side
fig, axes = plt.subplots(1, 2, figsize=(14, 6))


# Logistic Regression Decision Boundary
# contourf colors the regions according to predicted classes
axes[0].contourf(
    xx,
    yy,
    Z_lr,
    levels=np.arange(-0.5, 3.5, 1),
    alpha=0.3,
    cmap='viridis'
)

# Plotting actual training data points
axes[0].scatter(
    x_train_2d[:, 0],
    x_train_2d[:, 1],
    c=y_train_2d.map(class_mapping),
    cmap='viridis',
    edgecolors='black'
)

axes[0].set_title("Logistic Regression Decision Boundary")
axes[0].set_xlabel("Petal Length (Scaled)")
axes[0].set_ylabel("Petal Width (Scaled)")


# Decision Tree Decision Boundary
axes[1].contourf(
    xx,
    yy,
    Z_tree,
    levels=np.arange(-0.5, 3.5, 1),
    alpha=0.3,
    cmap='viridis'
)

# Plotting actual training data points
axes[1].scatter(
    x_train_2d[:, 0],
    x_train_2d[:, 1],
    c=y_train_2d.map(class_mapping),
    cmap='viridis',
    edgecolors='black'
)

axes[1].set_title("Decision Tree Decision Boundary")
axes[1].set_xlabel("Petal Length (Scaled)")
axes[1].set_ylabel("Petal Width (Scaled)")


# Adjusting layout and displaying both graphs
plt.tight_layout()
plt.show()


# ==========================================
# 21. FINAL CONCLUSION
# ==========================================

print("\nFinal Model Comparison:")

# Comparing the accuracy of both models
if accuracy_lr > accuracy_tree:

    print("Logistic Regression performed better.")

elif accuracy_tree > accuracy_lr:

    print("Decision Tree performed better.")

else:

    print("Both models achieved the same accuracy.")

print("Logistic Regression Accuracy:", round(accuracy_lr * 100, 2), "%")
print("Decision Tree Accuracy:", round(accuracy_tree * 100, 2), "%")
