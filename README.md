# Data-Driven Real Estate Valuation and Recommendation Engine

### Project Links
* **Live Application:** [View Streamlit App](http://65.2.172.23/)
* **Developer Profile:** [LinkedIn](https://www.linkedin.com/in/rajeshxdatascience/)

---

## Executive Summary
This project provides an end-to-end data science solution for the real estate market in Gurgaon. It addresses the lack of transparency in property valuation by providing a machine learning-based price predictor and a hybrid recommendation system. The application is built using a dataset self-scraped from 99acres and processed through a rigorous pipeline involving feature engineering, outlier detection, and model optimization.

## Core Modules

### 1. Price Prediction Engine
A machine learning pipeline designed to estimate the market value of residential properties. 
* **Model:** Random Forest Regressor (optimized for minimum Mean Absolute Error).
* **Validation:** Implements logical constraints (e.g., BHK-to-Area ratios) to ensure realistic inputs and high prediction confidence.

### 2. Interactive Market Analytics
A visual intelligence module that offers geographical and statistical insights into market trends.
* **Geospatial Mapping:** Sector-wise price heatmaps using Plotly Mapbox.
* **Property Distribution:** Analysis of BHK mix, property age, and configuration preferences.
* **Correlation Studies:** Visualizing the impact of built-up area and amenities on final valuation.

### 3. Hybrid Recommendation System
A multi-factor recommendation engine that suggests properties based on the similarity of three distinct features:
* **Facilities & Amenities:** Matching properties with similar luxury scores and internal features.
* **Price Segment:** Finding options within the same financial bracket.
* **Geographic Location:** Prioritizing properties within a similar radius or sector.

## Technical Methodology

### Data Acquisition & Preprocessing
* **Source:** Self-scraped data from property listing portals (99acres).
* **Cleaning:** Handled missing values through median imputation and removed statistical outliers using the IQR method.
* **Feature Engineering:** Developed new metrics including age-based possession categories and simplified floor classifications.

### Feature Selection
* Utilized Correlation Analysis, Random Forest Feature Importance, and Recursive Feature Elimination (RFE) to identify the most predictive variables.

### Model Benchmarking
A comparative study was conducted across various regressors:
* Linear Regression, Ridge, and LASSO.
* Support Vector Regression (SVR).
* Random Forest and Gradient Boosting (Selected Model).
* Multi-layer Perceptron (MLP).

## Installation & Usage
To run the application locally:

1. Clone the repository:
   ```bash
   git clone [https://github.com/rajeshxdatascience/Data-Driven-Real-Estate-Valuation-Recommendation-Engine.git](https://github.com/rajeshxdatascience/Data-Driven-Real-Estate-Valuation-Recommendation-Engine.git)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Launch the Streamlit application:
   ```bash
   streamlit run Home.py

## Developed by Rajesh | Data Science Portfolio 2026
