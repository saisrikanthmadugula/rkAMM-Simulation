# rkAMM-Simulation

Technical implementation framework and Monte Carlo simulation architecture for **Dynamic Interest Rate Discovery in Decentralized Finance: A Reverse Kelly Automated Market Maker for Risk-Adjusted Lending**.

## Repository Architecture
* `.dvc/` & `data/*.dvc` - Versioning pointer arrays identifying underlying SME corporate loan matrices.
* `ReverseKellyAMM.sol` - WAD-arithmetic contract performing runtime dynamic interest calculations on EVM rails.
* `simulate_rkamm.py` - Complete multi-scenario stress verification engine analyzing system solvency.
* `generate_rwa_dataset.py` - Baseline transactional data array setup configuration.
* `requirements.txt` - System package dependencies.

## Local Execution Flow
1. Install requirements: `pip install -r requirements.txt`
2. Initialize underlying data arrays: `python generate_rwa_dataset.py`
3. Execute the full Monte Carlo suite: `python simulate_rkamm.py`
