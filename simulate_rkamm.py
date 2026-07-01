import os
import numpy as np
import mlflow
import dagshub

# Initialize Decentralized Data Tracking via DagsHub
dagshub.init(repo_owner='madugula', repo_name='rkAMM-Simulation', mlflow=True)

def simulate_scenario(scenario_name, epochs=10000, initial_liquidity=10000000, 
                      base_pd_alpha=2, base_pd_beta=38, target_yield=0.12, static_rate=0.085):
    
    rkamm_liquidity = initial_liquidity
    static_liquidity = initial_liquidity
    np.random.seed(42)
    
    with mlflow.start_run(run_name=scenario_name):
        mlflow.log_param("scenario", scenario_name)
        mlflow.log_param("target_yield", target_yield)
        mlflow.log_param("pd_alpha", base_pd_alpha)
        mlflow.log_param("pd_beta", base_pd_beta)
        
        # Draw PDs from Beta distribution reflecting specific market shocks
        pds = np.random.beta(base_pd_alpha, base_pd_beta, epochs)
        
        # Calculate fixed loan size so total volume equals 1x pool liquidity
        loan_fraction = 1.0 / epochs
        loan_amount = initial_liquidity * loan_fraction
        
        approved_loans = 0
        defaults = 0
        total_rkamm_rate = 0
        
        for pd in pds:
            # 1. Static Utilization Model 
            static_default = np.random.binomial(1, pd)
            if static_default == 0:
                static_liquidity += loan_amount * static_rate
            else:
                static_liquidity -= loan_amount
                
            # 2. rkAMM Model 
            if pd > 0.30: continue # Cap risk to acceptable threshold
            
            approved_loans += 1
            rkamm_rate = (target_yield + pd) / (1 - pd) # Reverse Kelly Formula
            total_rkamm_rate += rkamm_rate
            
            rkamm_default = np.random.binomial(1, pd)
            if rkamm_default == 0:
                rkamm_liquidity += loan_amount * rkamm_rate 
            else:
                rkamm_liquidity -= loan_amount
                defaults += 1
                
        # Metric Calculations
        approval_rate = approved_loans / epochs
        avg_rkamm_rate = total_rkamm_rate / approved_loans if approved_loans > 0 else 0
        npl_ratio = defaults / approved_loans if approved_loans > 0 else 0
        
        rkamm_net_yield = (rkamm_liquidity - initial_liquidity) / initial_liquidity
        static_net_yield = (static_liquidity - initial_liquidity) / initial_liquidity
        
        # Dashboard Logging
        mlflow.log_metric("rkamm_approval_rate", approval_rate)
        mlflow.log_metric("rkamm_avg_interest_rate", avg_rkamm_rate)
        mlflow.log_metric("rkamm_npl_ratio", npl_ratio)
        mlflow.log_metric("rkamm_net_yield", rkamm_net_yield)
        mlflow.log_metric("static_net_yield", static_net_yield)
        
        print(f"--- {scenario_name} ---")
        print(f"rkAMM Avg Interest Rate: {avg_rkamm_rate:.2%}")
        print(f"rkAMM Net Yield: {rkamm_net_yield:.2%}")
        print(f"Static Net Yield: {static_net_yield:.2%}")
        print(f"Approval Rate: {approval_rate:.1%}")
        print(f"NPL Ratio: {npl_ratio:.1%}\n")
        
        return rkamm_net_yield

if __name__ == "__main__":
    # Execute full macroeconomic stress testing suite
    simulate_scenario("Normal Market", base_pd_alpha=2, base_pd_beta=38, static_rate=0.085)
    simulate_scenario("Macroeconomic Shock", base_pd_alpha=3, base_pd_beta=17, static_rate=0.092)
    simulate_scenario("Adverse Selection", base_pd_alpha=5, base_pd_beta=15, static_rate=0.095)
