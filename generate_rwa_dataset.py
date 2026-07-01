import os
import numpy as np
import pandas as pd

def generate_dataset(output_path="data/sme_invoice_risk_features.csv", num_records=12000):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.random.seed(42)
    
    # Generate realistic SME invoice fields matching our research distributions
    invoice_amounts = np.random.lognormal(mean=10.5, sigma=0.75, size=num_records)
    base_pds = np.random.beta(a=2, b=38, size=num_records)
    
    df = pd.DataFrame({
        "invoice_id": [f"INV-{i:06d}" for i in range(num_records)],
        "amount_usd": np.round(invoice_amounts, 2),
        "base_probability_default": np.round(base_pds, 4),
        "repayment_duration_days": np.random.choice([30, 60, 90], size=num_records, p=[0.5, 0.4, 0.1]),
        "sector_risk_multiplier": np.random.uniform(0.8, 1.3, size=num_records)
    })
    
    df.to_csv(output_path, index=False)
    print(f"Successfully generated dataset with {num_records} samples at {output_path}")

if __name__ == "__main__":
    generate_dataset()
