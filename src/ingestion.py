import pandas as pd
import glob
import os
import sys

def get_latest_merged_data(data_dir='../data/'):
    """
    Automated merge with data validation (Data Contract).
    """
    # 1. Dynamic Discovery
    raw_files = glob.glob(os.path.join(data_dir, "*colorado.csv"))
    proc_files = glob.glob(os.path.join(data_dir, "*processed.csv"))
    
    if not raw_files or not proc_files:
        print(f"CRITICAL: No files found in {os.path.abspath(data_dir)}")
        sys.exit(1)

    # 2. Load & Validate Schema
    df_raw = pd.read_csv(raw_files[0])
    df_proc = pd.read_csv(proc_files[0])

    # Standardize Join Key
    if 'Research ID' in df_proc.columns:
        df_proc = df_proc.rename(columns={'Research ID': 'system_job_id'})

    # 3. The Merge (Inner Join)
    # Using inner join to ensure Bharat only gets 'complete' data
    merged_df = pd.merge(df_raw, df_proc, on='system_job_id', how='inner')

    # 4. Data Quality Gate (Senior Practice)
    # Drop rows without critical NLP text
    initial_count = len(merged_df)
    merged_df = merged_df.dropna(subset=['description', 'title'])
    
    print(f"LOG: Merged {initial_count} rows. Kept {len(merged_df)} after quality check.")
    
    return merged_df

if __name__ == "__main__":
    # Determine directory context
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, 'data')

    data = get_latest_merged_data(data_dir=data_path)
    output_file = os.path.join(data_path, 'merged_staging.csv')
    
    data.to_csv(output_file, index=False)
    print(f"SUCCESS: Gold-standard dataset ready at {output_file}")