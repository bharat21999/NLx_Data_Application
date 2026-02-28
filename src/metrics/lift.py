import pandas as pd
import os

CITY_MATRIX_PATH = "data/processed/city_skill_matrix.parquet"
ANALYSIS_PATH = "data/processed/analysis_ready.parquet"
OUTPUT_PATH = "data/processed/city_skill_lift.parquet"

def build_lift_matrix():

    city_df = pd.read_parquet(CITY_MATRIX_PATH)
    analysis_df = pd.read_parquet(ANALYSIS_PATH)

    # Total unique jobs statewide
    total_state_jobs = analysis_df["system_job_id"].nunique()

    # 1️⃣ Compute true statewide skill frequency
    statewide = (
        analysis_df.groupby("Taxonomy Skill")
        .agg(
            total_skill_weight=("skill_weight", "sum"),
            job_count=("system_job_id", "nunique")
        )
        .reset_index()
    )

    # Filter rare skills
    MIN_STATE_JOBS = 100
    statewide = statewide[statewide["job_count"] >= MIN_STATE_JOBS]

    # Compute statewide skill share
    statewide["state_skill_share"] = (
        statewide["total_skill_weight"] / total_state_jobs
    )

    # 2️⃣ Merge into city matrix
    merged = city_df.merge(
        statewide[["Taxonomy Skill", "state_skill_share"]],
        on="Taxonomy Skill"
    )

    # 3️⃣ Compute lift
    merged["lift"] = (
        merged["skill_share"] / merged["state_skill_share"]
    )

    # 4️⃣ Remove weak city-skill signals
    MIN_CITY_SKILL_WEIGHT = 5
    merged = merged[merged["skill_weight"] >= MIN_CITY_SKILL_WEIGHT]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    merged.to_parquet(OUTPUT_PATH, index=False)

    print(f"Saved lift matrix to {OUTPUT_PATH}")

    return merged


if __name__ == "__main__":
    build_lift_matrix()