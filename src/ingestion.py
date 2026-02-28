import pandas as pd
import glob
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)

def get_latest_merged_data(data_dir='../data/raw'):
    """
    Automated merge with data validation (Data Contract).
    """
    # 1. Dynamic Discovery
    raw_files = glob.glob(os.path.join(data_dir, "*colorado.csv"))
    proc_files = glob.glob(os.path.join(data_dir, "*processed.csv"))
    
    if not raw_files or not proc_files:
        logging.info(f"CRITICAL: No files found in {os.path.abspath(data_dir)}")
        sys.exit(1)

    # 2. Load & Validate Schema
    df_raw = pd.read_csv(raw_files[0])
    df_proc = pd.read_csv(proc_files[0])

    # Standardize Join Key
    if 'Research ID' in df_proc.columns:
        df_proc = df_proc.rename(columns={'Research ID': 'system_job_id'})

    required_raw_cols = ['system_job_id', 'title', 'description', 'city']
    required_proc_cols = ['system_job_id','Raw Skill', 'Taxonomy Skill', 'Correlation Coefficient']

    for col in required_raw_cols:
        if col not in df_raw.columns:
            raise ValueError(f"Missing column in raw data: {col}")

    for col in required_proc_cols:
        if col not in df_proc.columns:
            raise ValueError(f"Missing column in processed data: {col}")

    

    # 3. The Merge (Inner Join)
    # Using inner join to ensure Bharat only gets 'complete' data
    merged_df = pd.merge(df_raw, df_proc, on='system_job_id', how='inner')

    # 4. Data Quality Gate (Senior Practice)
    # Drop rows without critical NLP text
    initial_count = len(merged_df)
    merged_df = merged_df.dropna(subset=['description', 'title'])
    
    logging.info(f"LOG: Merged {initial_count} rows. Kept {len(merged_df)} after quality check.")
    
    return merged_df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    raw_path = os.path.join(project_root, 'data', 'raw')
    processed_path = os.path.join(project_root, 'data', 'processed')

    os.makedirs(processed_path, exist_ok=True)

    data = get_latest_merged_data(data_dir=raw_path)

    output_file = os.path.join(processed_path, 'merged_staging.csv')
    output_file = os.path.join(processed_path, 'merged_staging.parquet')
    data.to_parquet(output_file, index=False)

    logging.info(f"SUCCESS: Gold-standard dataset ready at {output_file}")