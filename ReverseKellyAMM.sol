// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title ReverseKellyAMM
 * @dev Dynamic interest rate discovery using inverted Kelly Criterion.
 */
contract ReverseKellyAMM is ReentrancyGuard {
    
    uint256 constant WAD = 1e18;
    uint256 public targetYieldWAD = 0.12 * 1e18; // 12% Target Yield Hyperparameter

    /**
     * @notice Calculates the required interest rate for a given Probability of Default.
     * @param pdWAD The Probability of Default scaled to 1e18 (e.g. 5% = 0.05 * 1e18).
     * @return rateWAD The precise interest rate scaled to 1e18.
     */
    function calculateReverseKellyRate(uint256 pdWAD) public view returns (uint256 rateWAD) {
        // Enforce strict upper bound to prevent division by zero or underflow
        require(pdWAD < WAD, "rkAMM: PD exceeds maximum risk threshold (100%)");
        
        // Formula: r = (y + PD) / (1 - PD)
        // Scaled: r_WAD = ((Y_WAD + PD_WAD) * WAD) / (WAD - PD_WAD)
        uint256 numerator = (targetYieldWAD + pdWAD) * WAD;
        uint256 denominator = WAD - pdWAD;
        
        rateWAD = numerator / denominator;
    }
}
