# 🌫️👕 Machine Learning Mini-Project 3: SVM & Dimensionality Reduction

This repository contains the **third mini-project** for the **Machine Learning (Spring 2025)** course at **K. N. Toosi University of Technology**.  
It is divided into two main parts:

1. **Support Vector Machines (SVM) for Air Quality Analysis**  
2. **Dimensionality Reduction on Fashion-MNIST**

---

## 📁 Project Structure

├── Part1_SVM_for_Air_Quality/
│ └── Implementation & analysis of SVM models on Beijing PM2.5 dataset
├── Part2_Dimensionality_Reduction/
│ └── PCA, LDA, and t-SNE experiments on Fashion-MNIST
└── README.md

---

## 🌫️ Part 1: SVM for Beijing PM2.5 Air Quality Analysis

This section tackles a **real-world regression and classification problem** using the **Beijing PM2.5 dataset**.  
It covers the full ML pipeline: **EDA → Feature Engineering → Model Implementation → Optimization**.

### 🔍 Key Steps

#### 📊 EDA & Feature Engineering
- Cleaned dataset: handled **missing values** & **outliers**.  
- Engineered new features to boost performance:
  - **Lag features** (e.g., PM2.5 two hours ago, one day ago).  
  - **Rolling statistics** (moving averages & std. devs).  
  - **Cyclical encoding** of periodic features (hour, month).  

#### 🧠 SVM for Classification
- Converted continuous PM2.5 into **Air Quality Index (AQI) categories**.  
- Implemented **Linear, Polynomial, and RBF kernel SVMs**:
  - From scratch  
  - Using **Scikit-learn**  
- Compared performance across models.  
- Tuned hyperparameters with **GridSearchCV** and **RandomizedSearchCV**.  

#### 📉 SVM for Regression
- Built an **SVR (Support Vector Regressor)** to predict exact PM2.5 values.  
- Evaluated using standard regression metrics (e.g., MSE, R²).  

#### ⚡ Advanced Optimizations (Bonus)
- **Particle Swarm Optimization (PSO)** for SVM hyperparameters.  
- Implemented concepts from *"Innovative SVM optimization with differential gravitational fireworks for superior air pollution classification (2024)"*.  

---

## 👕 Part 2: Dimensionality Reduction on Fashion-MNIST

This section explores **dimensionality reduction** techniques on the **Fashion-MNIST dataset** (28×28 grayscale clothing images).

### 🔍 Key Steps

#### 🧹 Data Preparation
- Loaded Fashion-MNIST dataset.  
- Added **Gaussian noise** to create noisy samples for denoising tasks.  

#### 📉 Principal Component Analysis (PCA)
- Implemented **PCA from scratch**.  
- Plotted **explained variance ratio** to determine optimal components (e.g., 90% retained variance).  
- Reduced dataset to **2D components** with `scikit-learn` and visualized clusters.  
- Used PCA for **denoising autoencoding**: project → reconstruct → remove noise.  

#### 📐 Linear Discriminant Analysis (LDA)
- Applied **LDA** (via `scikit-learn`) for supervised dimensionality reduction.  
- Projected data into 2D space, maximizing **class separability**.  
- Compared PCA vs. LDA projections.  

#### 🌌 t-SNE (Bonus)
- Implemented **t-SNE** from scratch for advanced visualization.  
- Compared **strengths & weaknesses** against PCA and LDA.  

---

## 📌 Summary

This project provides hands-on experience in:
- Building **SVMs from scratch** and with libraries.  
- Performing **feature engineering** on real-world datasets.  
- Using **dimensionality reduction techniques** for visualization, denoising, and class separation.  
- Exploring **advanced optimization algorithms** for model tuning.  

---

## 🧑‍💻 Contributors
- [Your Name Here]

---

## 📄 License
This project is licensed under the **MIT License** — see the `LICENSE` file for details.
