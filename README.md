# Colorado Workforce Intelligence Platform

A production‑ready workforce analytics dashboard for analyzing job demand, skill specialization, and regional opportunity gaps across Colorado.

Built as a lightweight Workforce Intelligence Engine for economic development professionals, policy planners, and workforce boards.

## Executive Summary

The Colorado Workforce Intelligence Platform transforms structured labor market data into actionable insights for workforce strategy and economic planning.

The platform enables:

- Statewide skill demand analysis
- City‑level specialization insights
- Opportunity gap identification
- Workforce investment recommendations
- Regional skill archetype clustering

The system is designed to simulate a modern workforce intelligence SaaS tool while maintaining a clean, reproducible, and scalable architecture.

## Key Features

### 1. State Overview
- Total jobs analyzed
- Unique skills identified
- Cities covered
- Top 10 most demanded skills statewide

### 2. City Intelligence
- Skill specialization using Lift metrics
- Top specialized skills by city
- Comparative performance indicators

### 3. Regional Clusters
- KMeans clustering of cities by skill composition
- Identification of workforce archetypes
- Cluster‑level skill profiles

### 4. Opportunity Gaps
- Detection of underdeveloped but high‑demand skills
- City vs. statewide skill share comparison

### 5. Training Strategy
- Suggested workforce investment tracks
- High‑impact skill pathway recommendations

## Architecture Overview

The project follows a production‑oriented architecture:

### Data Layers
**Raw Data (Excluded from Repo)**
- Large ingestion datasets
- Not committed due to size constraints
- For complete data ingestion and feature engineering add colorado.csv and colorado_processed.csv to the data/raw folder.

**Analytical Layer**
- city_skill_lift.parquet
- Precomputed specialization and skill metrics
- Optimized for dashboard performance

**Presentation Layer**
- Streamlit UI
- Interactive visualizations via Plotly
- Cached data loading for performance

### Repository Structure

```
NLx_Data_Application/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── processed/
│       └── city_skill_lift.parquet
│
└── src/
    └── metrics/
        ├── lift.py
        ├── city_matrix.py
        └── quality.py
```

## Installation & Local Deployment

### 1. Clone Repository
```bash
git clone https://github.com/bharat21999/NLx_Data_Application.git
cd NLx_Data_Application
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

Then open: http://localhost:8501


## Technology Stack

- Python 3.11
- Streamlit
- Pandas
- Plotly
- Scikit‑learn
- Parquet (PyArrow backend)

## Performance Design

- Precomputed lift metrics prevent heavy runtime calculations
- Streamlit caching reduces reload latency
- Lightweight analytical dataset enables fast UI rendering
- No raw pipeline dependencies required for UI execution

## Intended Users

- Economic Development Agencies
- Workforce Planning Boards
- State Labor Departments
- Policy Analysts
- Workforce Strategy Consultants

## Future Enhancements

- Cloud deployment with auto‑scaling
- Real‑time data refresh pipeline
- Interactive policy scenario modeling
- Skill demand forecasting
- Cross‑state benchmarking
- API endpoint for workforce intelligence queries

## Version

Current Release: v1.0 (MVP)

## Authors

Bharat Khandelwal, Vaijayanti Deshmukh  
Workforce Intelligence & Labor Market Analytics