# AllocationSocialGoods

Code repository for the computational study of optimized donation structures and cooperation thresholds in networked social dilemmas.

Repository: https://github.com/yaomeng1/AllocationSocialGoods

## Overview

This repository contains MATLAB implementations of two complementary approaches for finding donation structures:

1. **Gradient-based optimization**, implemented with an RMSprop-style update rule, for the single-recipient and multiple-recipient cases.
2. **Exact optimization solutions** for the single-recipient case under three variants of the calculation.

The supplied example network is stored in `BA_n20_k6_idx2.mat` and `BA_n100_k6_idx0.mat`. Its variable `mAdj` is a `N × N` adjacency matrix. The scripts use this matrix to calculate random-walk remeeting times and then evaluate or optimize donation structures.

## Repository contents

| File | Type | Purpose |
|---|---|---|
| `opt_RMSprop_single_recipient.mlx` | MATLAB Live Script | Runs gradient-based optimization for the single-recipient donation case using an RMSprop-style update. It loads the example network, calculates remeeting times, initializes the donation variables, and iteratively updates the optimization variables. |
| `opt_RMSprop_multiple_recipient.mlx` | MATLAB Live Script | Runs gradient-based optimization for the multiple-recipient donation case using an RMSprop-style update. |
| `gradient_single_recipient.mlx` | MATLAB function in Live Script format | Evaluates the critical benefit-to-cost ratio and penalized objective, and computes the gradient for the single-recipient optimization routine. |
| `gradient_multiple_recipients.mlx` | MATLAB function in Live Script format | Evaluates the critical benefit-to-cost ratio and penalized objective, and computes the gradient for the multiple-recipient optimization routine. |
| `opt_bcr_exact_test.mlx` | MATLAB Live Script / demo | Demonstrates the exact single-recipient optimization using `opt_bcr_exact_single_recipient`. It loads the example network, calculates remeeting times, and calls the exact solver. |
| `opt_bcr_exact_single_recipient.mlx` | MATLAB function in Live Script format | Computes the exact single-recipient solution corresponding to the DB update (analysed in the main text). |
| `opt_bcr_exact_single_recipient_pc.mlx` | MATLAB function in Live Script format | Computes an exact single-recipient solution corresponding to the PC update. |
| `opt_bcr_exact_single_recipient_im.mlx` | MATLAB function in Live Script format | Computes an exact single-recipient solution corresponding to the IM update. |
| `findRemeetingTimes.m` | MATLAB function | Calculates random-walk remeeting times from the network adjacency matrix. |
| `cartProd.m` | MATLAB function | Constructs the Cartesian product of two weighted graphs; used by `findRemeetingTimes.m`. |
| `normalizedLaplacian.m` | MATLAB function | Calculates the normalized graph Laplacian used in the remeeting-time and optimization calculations. |
| `BA_n20_k6_idx2.mat` | MATLAB data file | Example network input. Contains the variable `mAdj`, a `20 × 20` adjacency matrix. |
| `BA_n100_k6_idx0.mat` | MATLAB data file | Example network input. Contains the variable `mAdj`, a `100 × 100` adjacency matrix. |



The `.mlx` files are MATLAB Live Scripts. Some of them define functions and are called by other scripts, rather than being run directly as standalone demonstrations.

## Software requirements

- **MATLAB:** Use a MATLAB release that supports Live Scripts (`.mlx`) and the syntax used in the code. MATLAB R2023b or later is a reasonable starting point; the code has not been tested here across MATLAB releases, so the exact minimum supported version should be confirmed by running the scripts in the target environment.
- **Operating system:** MATLAB-compatible operating systems should be suitable.

## Setup

1. Download or clone this repository.
2. Open MATLAB.
3. Set MATLAB's **Current Folder** to the repository directory, or add the directory to the MATLAB path.
4. Confirm that `BA_n20_k6_idx2.mat` and `BA_n100_k6_idx0.mat` is in the current working directory, because the example scripts load it by filename.

No separate compilation step is required.

## Reproducing the example exact solution

The repository includes a small example network so that the exact single-recipient routine can be called without preparing another dataset.

1. Open `opt_bcr_exact_test.mlx` in MATLAB.
2. Ensure the repository directory is the current folder.
3. Run the Live Script.

The demo performs the following operations:

```matlab
load('BA_n20_k6_idx2.mat')
Rem = findRemeetingTimes(mAdj);
[opt_bcr, opt_mInt, alpha_i, gamma_ij] = ...
    opt_bcr_exact_single_recipient(mAdj, Rem);
```

The returned variables are:

- `opt_bcr`: the critical benefit-to-cost ratio calculated for the exact solution.
- `opt_mInt`: the optimized single-recipient donation structure, represented as a matrix.
- `alpha_i` and `gamma_ij`: intermediate quantities used by the exact optimization calculation.

The results in Fig. 3a and b then can be reproduced. Note that the exact optimization results(Fig. 3d and Fig.4c,d) can be reproduced using `opt_bcr_exact_single_recipient`. 

## Running the gradient-based optimization

### Single recipient

1. Open `opt_RMSprop_single_recipient.mlx`.
2. Check that `BA_n100_k6_idx0.mat` is in the current folder.
3. Run the Live Script.

The current example settings in the script include:

- `epoch = 100000` (maximum number of iterations);
- `eta = 0.01` (step-size parameter);
- `alpha = 0.9` (squared-gradient moving-average parameter);
- `epsilon = 1e-6` (numerical stabilizer);
- `rho = 1.01` (growth factor for the penalty parameters);
- initial `sigma = 1` and `gamma = 10^-2`.

The script stops early when the average absolute update falls below its convergence threshold. It creates variables including `bcr_array`, `f_penalty_array`, `hidden_t`, `mInt_process`, and `mInt_opt`. Saving the results is currently commented out in the example script.

### Multiple recipients

1. Open `opt_RMSprop_multiple_recipient.mlx`.
2. Check that ``BA_n100_k6_idx0.mat`` is in the current folder.
3. Run the Live Script.

The current example settings include:

- `epoch = 100000` (maximum number of iterations);
- `eta = 0.1` (step-size parameter);
- `alpha = 0.9`;
- `epsilon = 1e-6`;
- `rho = 1.01`;
- initial `sigma = 1` and `gamma = 10^-2`.

As in the single-recipient script, the optimization can stop before the maximum number of iterations. The script creates the optimization history and the final donation-structure variables in the MATLAB workspace. The example save commands are commented out.

The results in Fig. 6a-d then can be reproduced. 

## Input data

### `BA_n20_k6_idx2.mat`(`BA_n100_k6_idx0.mat`)

This MAT-file contains one variable:

- `mAdj`: a `20 × 20`(`100 × 100` ) numeric adjacency matrix for the example network.

The helper function `normalizedLaplacian.m` symmetrizes its input using `max(mAdj, mAdj')`. The current example is therefore intended to be processed as an undirected network. If using another network, provide an adjacency matrix with dimensions `N × N` and check that its weights, symmetry, node ordering, and treatment of isolated nodes are consistent with the model assumptions.

The exact and gradient-based routines calculate remeeting times through `findRemeetingTimes.m`. That function calls `cartProd.m` and `normalizedLaplacian.m`.

## Outputs and interpretation



## Mapping scripts to manuscript results



| Manuscript figure/table/result | Script(s) | Notes |
|---|---|---|
| Exact single-recipient benchmark | `opt_bcr_exact_test.mlx`, `opt_bcr_exact_single_recipient.mlx` | Example demonstration on `BA_n20_k6_idx2.mat`. |
| Gradient-based single-recipient optimization | `opt_RMSprop_single_recipient.mlx` | Uses the RMSprop-style update and penalty terms. |
| Gradient-based multiple-recipient optimization | `opt_RMSprop_multiple_recipient.mlx`, | Uses the RMSprop-style update and penalty terms. |
| PC variant of exact single-recipient optimization | `opt_bcr_exact_single_recipient_pc.mlx` | Call directly with an adjacency matrix and, optionally, precomputed remeeting times. |
| IM variant of exact single-recipient optimization | `opt_bcr_exact_single_recipient_im.mlx` | Call directly with an adjacency matrix and, optionally, precomputed remeeting times. |



## License

**A software license must be selected and included in the repository before publication.** No license choice is inferred by this README. If you intend to permit broad reuse, modification, and redistribution with minimal restrictions, the MIT License is one common option; please confirm that this matches your intentions before adding an MIT `LICENSE` file. Until a license is added, users should not assume that the code is available for unrestricted reuse.

## Contact

For questions about the code or reproduction of the computational results, please contact the corresponding author listed in the associated manuscript.
