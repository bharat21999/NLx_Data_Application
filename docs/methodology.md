# Workforce Intelligence Methodology

## Colorado Workforce Intelligence Platform

### 1. Introduction

This document outlines the methodology used to construct the Colorado Workforce Intelligence Platform. The goal of the system is to transform structured job posting data into actionable workforce strategy insights for policymakers, economic development agencies, and labor market analysts.

The platform translates raw job and skill data into:
- City-level specialization metrics
- Statewide skill demand indicators
- Opportunity gap analysis
- Regional workforce archetypes
- Training investment recommendations

All analytical decisions were made with statistical robustness, interpretability, and policy usability in mind.

### 2. Data Overview

The platform is built on structured job posting data containing:
- Unique job identifiers
- City location
- Standardized skill taxonomy labels
- Skill weights per job

Raw ingestion files are excluded from the public repository due to size constraints. The dashboard operates on a precomputed analytical dataset:
```
data/processed/city_skill_lift.parquet
```

This file contains city-level skill metrics derived from the full dataset.

### 3. Skill Demand Aggregation

#### 3.1 Job-Level to City-Level Aggregation

Each job posting may contain multiple skills. To construct city-level skill profiles:
- Jobs are grouped by city.
- Skill weights are aggregated across all jobs in the city.
- Skill shares are computed:

$$\text{Skill Share}_{city,skill} = \frac{\text{Skill Weight}_{city,skill}}{\text{Total Skill Weight}_{city}}$$

This produces a normalized skill distribution per city.

### 4. Specialization via Lift Metric

#### 4.1 Why Lift?

We selected the Lift metric to measure specialization because it allows comparison between local and statewide skill prevalence.

Lift answers:
> "Is this skill more concentrated in this city than in the state overall?"

It is defined as:

$$\text{Lift}_{city,skill} = \frac{\text{Skill Share}_{city,skill}}{\text{Skill Share}_{state,skill}}$$

#### 4.2 Interpretation

- **Lift > 1** → Skill is overrepresented in the city
- **Lift = 1** → Skill aligns with state average
- **Lift < 1** → Skill is underrepresented

This approach is widely used in economic geography and market basket analysis and provides an intuitive measure for policymakers.

### 5. Statistical Stability Controls

Labor market data often contains sparsity issues. We implemented multiple safeguards to prevent misleading results.

#### 5.1 Minimum Job Threshold

Cities with extremely small job counts (e.g., 1–2 postings) can produce unstable specialization ratios.

We applied:
- A minimum job count threshold
- Exclusion or down-weighting of statistically insignificant cities

This prevents artificial inflation of lift scores.

#### 5.2 Skill Frequency Threshold

Rare skills can produce exaggerated lift values due to small denominators.

We filtered:
- Skills below a minimum statewide occurrence threshold

This ensures that reported specialization reflects meaningful labor market signals rather than noise.

#### 5.3 Share Normalization

Skill shares are computed relative to total city skill weight to prevent:
- Larger cities dominating rankings
- Small cities appearing artificially extreme

This normalization ensures comparability across geographic areas.

### 6. Opportunity Gap Analysis

Opportunity gaps identify skills that:
- Have strong statewide demand
- Are underrepresented in a given city

We compute:

$$\text{Gap}_{city,skill} = \text{State Skill Share} - \text{City Skill Share}$$

Positive gaps indicate underdeveloped but high-demand skill areas, useful for workforce investment planning.

### 7. Regional Clustering

#### 7.1 Objective

To identify workforce archetypes across Colorado cities.

#### 7.2 Method

1. Construct a city × skill lift matrix.
2. Apply KMeans clustering.
3. Group cities with similar specialization patterns.

#### 7.3 Rationale for KMeans

- Interpretable cluster assignment
- Scalable to multiple cities
- Computationally efficient
- Suitable for policy segmentation

Cluster outputs help identify:
- Tech-driven cities
- Healthcare-specialized regions
- Logistics/manufacturing corridors

### 8. Workforce Investment Recommendations

Training recommendations are derived from:
- High lift skills (existing strengths)
- High opportunity gap skills (future growth areas)

This dual approach supports both:
- Economic competitiveness
- Strategic workforce diversification

### 9. Design Principles

The system was built with five core principles:

1. **Interpretability** over algorithmic opacity
2. **Statistical robustness**
3. **Policy usability**
4. **Performance efficiency**
5. **Reproducibility**

The dashboard operates on a precomputed analytical dataset to ensure fast, reliable execution without requiring raw pipeline dependencies.

### 10. Limitations

- Job postings reflect demand, not supply.
- Lift does not measure wage or economic impact.
- Temporal trends are not yet incorporated.
- Clustering depends on chosen parameters.

Future versions may incorporate:
- Time-series forecasting
- Wage weighting
- Industry controls
- Confidence intervals for lift stability

### 11. Conclusion

The Colorado Workforce Intelligence Platform provides a structured, statistically grounded approach to understanding regional labor market dynamics.

By combining normalization, specialization metrics, clustering, and gap analysis, the system transforms raw job data into actionable workforce strategy insights suitable for economic development planning.

#### Why This Is Powerful

Adding this document:
- Makes your project look policy-grade
- Shows statistical rigor
- Demonstrates awareness of methodological limitations
- Signals senior-level thinking
