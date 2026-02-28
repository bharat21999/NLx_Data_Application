import pandas as pd
import os

INPUT_PATH = "data/processed/analysis_ready.parquet"
OUTPUT_PATH = "data/processed/city_skill_matrix.parquet"

def build_city_skill_matrix(input_path=INPUT_PATH, output_path=OUTPUT_PATH):
    df = pd.read_parquet(input_path)

    df["city"] = df["city"].str.strip().str.upper()
    
    # 1️⃣ Count total unique jobs per city
    total_jobs = (
        df.groupby("city")["system_job_id"]
        .nunique()
        .reset_index(name="total_jobs")
    )

    MIN_JOBS = 20

# Filter cities with sufficient job counts
    total_jobs = total_jobs[total_jobs["total_jobs"] >= MIN_JOBS]

    # 2️⃣ Sum weighted skill counts per city + skill
    skill_counts = (
        df.groupby(["city", "Taxonomy Skill"])["skill_weight"]
        .sum()
        .reset_index()
    )

    # 3️⃣ Merge to compute normalized share
    merged = skill_counts.merge(total_jobs, on="city")

    merged["skill_share"] = (
        merged["skill_weight"] / merged["total_jobs"]
    )

    # Save result
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.to_parquet(output_path, index=False)

    print(f"Saved city skill matrix to {output_path}")

    return merged


if __name__ == "__main__":
    build_city_skill_matrix()