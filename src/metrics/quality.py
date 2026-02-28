import pandas as pd
import os

INPUT_PATH = "data/processed/merged_staging.parquet"
OUTPUT_PATH = "data/processed/analysis_ready.parquet"

def load_data(path=INPUT_PATH):
    return pd.read_parquet(path)

def filter_by_corr(df, threshold=0.65):
    return df[df["Correlation Coefficient"] >= threshold]

def deduplicate(df):
    return df.drop_duplicates(
        subset=["system_job_id", "Taxonomy Skill"]
    )

def apply_weight(df):
    df["skill_weight"] = df["Correlation Coefficient"]
    return df

def select_columns(df):
    return df[
        [
            "system_job_id",
            "city",
            "Taxonomy Skill",
            "Taxonomy Source",
            "skill_weight",
        ]
    ]

def prepare_analysis_dataset(
    input_path=INPUT_PATH,
    output_path=OUTPUT_PATH,
    threshold=0.65
):
    df = load_data(input_path)
    df = filter_by_corr(df, threshold)
    df = deduplicate(df)
    df = apply_weight(df)
    df = select_columns(df)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)

    print(f"Saved analysis dataset to {output_path}")

    return df


if __name__ == "__main__":
    prepare_analysis_dataset()