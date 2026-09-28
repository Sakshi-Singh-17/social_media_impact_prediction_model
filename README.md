# 📱 Social Media Impact Prediction Using Machine Learning

**Author:** Sakshi Singh  
**Project Type:** Machine Learning Classification (Single-File Streamlit Application)  
**Dataset:** `Social_media_impact_on_life.csv` (https://www.kaggle.com/datasets/harishyadav0506/impact-of-social-media-on-life)
kaggle
---

## 📌 Project Overview

This project predicts the **Overall Impact** of social media on student life — classified as **Beneficial**, **Neutral**, or **Negative** — using a dataset of 4,500 student records. It is delivered as a single Python file that provides:

- Full Exploratory Data Analysis (EDA) with 13+ charts
- Data preprocessing with imputation, encoding, and scaling
- Training and evaluation of 3 classifiers (Logistic Regression, Decision Tree, Random Forest)
- Interactive prediction interface via Streamlit
- Automated generation of a comprehensive Word report (`.docx`)

---

## 📁 Project Structure

```
IBM_Intern_Proj/
│
├── SakshiSingh_SocialMediaImpactPredictionModel.py   ← Single-file application (run this)
├── Social_media_impact_on_life.csv                   ← Dataset (must be in same folder)
├── SakshiSingh_ProjectReport.docx                    ← Pre-generated project report
├── README.md                                         ← This file
└── report_charts/                                    ← Auto-created chart images for the report
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn streamlit python-docx
```

### 2. Place the dataset

Ensure `Social_media_impact_on_life.csv` is in the **same folder** as `SakshiSingh_SocialMediaImpactPredictionModel.py`.

### 3. Run the application

```bash
streamlit run SakshiSingh_SocialMediaImpactPredictionModel.py
```

The app will open automatically at `http://localhost:8501`.

---

## 🧭 Application Sections

| Section | Description |
|---|---|
| 🏠 **Dashboard** | Dataset overview, shape, descriptive statistics, target distribution |
| 📊 **EDA** | 13 interactive charts with insights — distributions, box plots, heatmaps |
| ⚙️ **Preprocessing** | Missing values, encoding details, train/test split, class distribution |
| 🤖 **Model Training** | Three classifiers with hyperparameters and CV scores |
| 📈 **Model Evaluation** | Accuracy, Precision, Recall, F1, confusion matrices, classification reports |
| 🔮 **Prediction** | Interactive form to predict Overall Impact for a new student |
| 📄 **Report** | Generate and download the full Word report (`.docx`) |

---

## 📊 Dataset Summary

| Property | Value |
|---|---|
| Records | 4,500 |
| Columns | 16 (15 features + 1 target) |
| Target Variable | `Overall_Impact` |
| Target Classes | Beneficial (82%), Neutral (15%), Negative (4%) |
| Missing Values | `Perceived_Stress_Score`: 46 · `Academic_Performance_GPA`: 85 |
| Duplicates | 0 |

---

## 🤖 Models & Results

All three models use the same 80/20 stratified train-test split with balanced class weights.

| Model | Accuracy | F1-Score (weighted) |
|---|---|---|
| Logistic Regression | ~97.1% | ~97.2% |
| Decision Tree | ~92.4% | ~92.9% |
| Random Forest | ~95.1% | ~95.3% |

> The best model is selected automatically based on the highest weighted F1-Score.

---

## 📄 Word Report

The auto-generated Word report (`Social_Media_Impact_Prediction_Report.docx`) is also available as `SakshiSingh_ProjectReport.docx` in the project folder. It contains:

- Cover page with project metadata
- Abstract and problem statement
- Dataset description with feature table
- All 13+ EDA charts embedded as images
- Preprocessing steps with imputation details
- Model descriptions and hyperparameters
- Evaluation metrics, confusion matrices, feature importance
- Prediction system explanation with code snippet
- **Complete Python source code** of the application
- Results, insights, limitations, and conclusion
- Requirements and execution instructions

To generate a fresh report: open the app → navigate to **📄 Report** → click **Generate Word Report** → click **Download**.

---

## ⚙️ Preprocessing Pipeline

```
Numerical features → SimpleImputer(median) → StandardScaler
Categorical features → OneHotEncoder(handle_unknown='ignore')
Target → LabelEncoder (Beneficial=0, Negative=1, Neutral=2)
Split → 80% train / 20% test (stratified)
Class imbalance → class_weight='balanced' on all models
```

---

## 🔮 Prediction Features

The prediction form accepts:

| Feature | Type |
|---|---|
| Age | Numeric (14–30) |
| Gender | Categorical |
| Academic Level | Categorical |
| Primary Platform | Categorical |
| Daily Usage Hours | Numeric slider |
| Weekend Extra Hours | Numeric slider |
| Device Type | Categorical |
| Sleep Duration Hours | Numeric slider |
| Sleep Quality Score | Numeric (1–5) |
| Late Night Usage | Boolean |
| Social Comparison Frequency | Categorical |
| Perceived Stress Score | Numeric slider |
| Mental Health Index | Numeric slider |
| Academic Performance GPA | Numeric slider |

---

## ⚠️ Disclaimer

All predictions are based on **statistical patterns** in historical data. They do **not** establish causation and **must not** be interpreted as medical or psychological diagnoses. Consult a qualified professional for personalized guidance.

---

## 🐍 Python Version

Python **3.9 or higher** is required.

---

## 📦 Dependencies

```
pandas
numpy
matplotlib
seaborn
scikit-learn
streamlit
python-docx
```

Install all at once:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn streamlit python-docx
```
