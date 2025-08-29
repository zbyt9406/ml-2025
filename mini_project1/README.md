# 🌦️⚙️ Machine Learning Mini-Project 1: Weather Forecasting & Fault Diagnosis

This repository contains the first mini-project for the **Machine Learning** course (Spring 2025) at **K. N. Toosi University of Technology**. The project is divided into two distinct parts:

1. **Weather Forecasting** (Regression)
2. **Bearing Fault Diagnosis** (Classification)

---

## Part 1: Machine Learning-Based Weather Forecasting 🌤️

This part focuses on building regression models to predict weather conditions, inspired by the paper:

> *"A real-time collaborative machine learning based weather forecasting system with multiple predictor locations."*

The core idea is to use **collaborative learning**—leveraging data from multiple nearby cities—to enhance prediction accuracy for a target city.

### 🔧 Key Components

#### 📊 Data Preprocessing
- Utilizes weather data from several cities in France.
- Data from **2009** is reserved as the **test set**.
- Input data is structured into **sliding time windows** (e.g., from time *t-n* to *t-1* to predict *t*).

#### 🤝 Collaborative Learning Framework
- For each target city, models are trained using features from **all available cities**.
- This approach captures **spatial correlations** to boost model performance.

#### 🧠 Model Implementation
- **Polynomial Regression from Scratch**: Built manually with full training logic (predictions, gradients, updates).
- **Scikit-learn Models**: Implements and compares 3 types of linear regression from the `scikit-learn` library.

#### 📈 Evaluation
- Models are trained and evaluated for multiple cities.
- The best model is selected based on performance metrics.
- Repeated across 3 different cities to assess **robustness**.

---

## Part 2: Hierarchical Classification for Bearing Fault Diagnosis ⚙️

This section focuses on identifying mechanical faults in rotating machinery using vibration data from the **MaFaulDa** dataset, based on a reference thesis.

### 🧩 Problem Overview
- The dataset includes vibrational signals under various fault conditions: **imbalance**, **misalignment**, **bearing defects**, etc.
- Understanding of the fault types and data acquisition setup is provided.

### 🔍 Preprocessing & Feature Extraction
- Raw time-series signals undergo normalization and noise filtering.
- Features are extracted to train classification models.
- Dataset is split into **training** and **test** sets.

### 🧠 Model Design & Implementation

Two classification strategies are explored:

#### 1. **Flat Classification**
- A single model directly classifies all fault types.

#### 2. **Hierarchical Classification**
- Multi-level approach:
  - First level: broad categories (e.g., *Normal* vs. *Fault*).
  - Next levels: fine-grained sub-classes (e.g., *Horizontal vs. Vertical Misalignment*).

Balanced training is ensured using **upsampling/downsampling** techniques.

### 📊 Evaluation
- Evaluated using **confusion matrices** and **classification reports** on both training and test sets.
- Performance comparison between flat and hierarchical approaches.

---

## 🛠️ Final Deliverable

The final product is a Python program that:
- Takes a data sample as input,
- Runs it through the **trained hierarchical model structure**,
- Outputs the **predicted fault class**.

---



