# 🧬 Data Preprocessing Pipeline on AWS Lambda with Docker

This repository contains a lightweight data pipeline for AWS, containerized with Docker and executed via **AWS Lambda**.  
The function reads CSV files from **Amazon S3**, applies feature transformations and splits using `scikit-learn`, and saves the resulting datasets back to S3.

---

## 🚀 Features

- Executed as an AWS Lambda function using a custom **Python Docker image**
- Reads multiple CSV files from **Amazon S3**
- Combines raw data into a single DataFrame
- Applies column-wise preprocessing (imputation, scaling, encoding)
- Performs data splits: train, validation, test
- Saves processed datasets back to **S3**
- Fully compatible with `scikit-learn` and `category-encoders`

---

## ⚙️ Lambda Execution Flow

### 1. Trigger

Lambda is invoked via HTTP API Gateway with query parameters:

```bash
GET /?year=2025&month=06
```

### 2. Inside the Lambda

- Downloads the following files from S3:

```bash
source_data/2025_06/credit_risk_1.csv
source_data/2025_06/credit_risk_2.csv
source_data/2025_06/credit_risk_3.csv
```

- Combines them into a single DataFrame  
- Applies preprocessing and feature engineering  
- Splits the data into:

- `X_train`, `y_train`
- `X_val`, `y_val`
- `X_test`, `y_test`

- Saves each result to:

```bash
datasets/2025_06/X_train.csv
datasets/2025_06/y_train.csv
datasets/2025_06/X_val.csv
datasets/2025_06/y_val.csv
datasets/2025_06/X_test.csv
datasets/2025_06/y_test.csv
```

---

## 📦 Preprocessing Logic

- **Categorical features (strings)**:
- Imputed with `"UNKNOWN"` and encoded via `JamesSteinEncoder`

- **Categorical features (one-hot)**:
- Imputed and one-hot encoded

- **Numerical features**:
- Some filled with mean
- Others filled with constant (e.g., 0) and flagged with binary indicators

- **Scaling**:
- All numerical values are standardized using `StandardScaler`

---

## 🐳 Docker Build & Deploy

### Build Docker Image

```bash
docker build -t lambda-data-pipeline .
```

---
