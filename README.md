# AllocationSocialGoods

This repository contains code for paper "Strategic allocation of social goods in the evolution of cooperation".

Repository: https://github.com/yaomeng1/AllocationSocialGoods

The code includes MATLAB implementations of (i) gradient-based optimization of donation structures, (ii) exact optimization for single-recipient donation structures, and (iii) calculation of critical benefit-to-cost ratios for asymmetric interaction networks. 

## Repository contents

### Main MATLAB scripts and functions

| File | Purpose |
|---|---|
| `opt_RMSprop_single_recipient.mlx` | Runs RMSprop-style gradient-based optimization for the single-recipient donation case. |
| `opt_RMSprop_multiple_recipient.mlx` | Runs RMSprop-style gradient-based optimization for the multiple-recipient donation case. |
| `gradient_single_recipient.mlx` | Calculates the objective and gradient used by the single-recipient optimization routine (used in `opt_RMSprop_single_recipient.mlx`). |
| `gradient_multiple_recipients.mlx` | Calculates the objective and gradient used by the multiple-recipient optimization routine (used in `opt_RMSprop_multiple_recipient.mlx`). |
| `opt_bcr_exact_single_recipient.mlx` | Exact optimization solution for the single-recipient case under the DB update rule (applied in the main text). |
| `opt_bcr_exact_single_recipient_pc.mlx` | Exact optimization solution for the single-recipient case under the PC update rule. |
| `opt_bcr_exact_single_recipient_im.mlx` | Exact optimization solution for the single-recipient case under the IM update rule. |
| `opt_bcr_exact_test.mlx` | Demo script that loads an example network, calculates remeeting times, and calls `opt_bcr_exact_single_recipient`. |
| `getBCratioAsymInteract.m` | Calculates the critical benefit-to-cost ratio for a replacement graph and a potentially different interaction graph. This function supports asymmetric interaction structures and allows isolated nodes in the interaction graph. It is used to generate the results shown in **Fig. 2c and Fig. 4e**. |
| `findRemeetingTimes.m` | Calculates random-walk remeeting times from the replacement-network adjacency matrix (supplied files for the above programs) |
|                                         | product graph used by `findRemeetingTimes.m`.                |
| `normalizedLaplacian.m` | Calculates the normalized graph Laplacian used in the remeeting-time and threshold calculations. |

Some `.mlx` files define functions called by other scripts; they are not necessarily intended to be run directly.

### Data files

| File | Contents |
|---|---|
| `BA_n20_k6_idx2.mat` | Example network adjacency matrix, stored in variable `mAdj` (`20 × 20`). |
| `BA_n100_k6_idx0.mat` | Example network adjacency matrix, stored in variable `mAdj` (`100 × 100`). |

## Software requirements

### MATLAB

- **MATLAB:** Use a MATLAB release that supports Live Scripts (`.mlx`) and the syntax used in the code. MATLAB R2023b or later is a reasonable starting point; the code has not been tested here across MATLAB releases, so the exact minimum supported version should be confirmed by running the scripts in the target environment.
- **Operating system:** MATLAB-compatible operating systems should be suitable.

## Setup

1. Clone or download the repository.
2. For MATLAB analyses, open MATLAB and set the repository directory as the Current Folder, or add it to the MATLAB path.
3. Ensure the relevant `.mat` file is in the current working directory when running a script that loads it by filename.

Example MATLAB setup:

```matlab
cd('path/to/AllocationSocialGoods')
addpath(pwd)
```

## Reproducing selected results

### 1. Exact single-recipient optimization

The demo `opt_bcr_exact_test.mlx` provides an example of how to calculate an exact single-recipient solution.

1. Open `opt_bcr_exact_test.mlx` in MATLAB.
2. Make sure `BA_n20_k6_idx2.mat` is in the current working directory.
3. Run the Live Script.

The main calculation follows this pattern:

```matlab
load('BA_n20_k6_idx2.mat')
Rem = findRemeetingTimes(mAdj);
[opt_bcr, opt_mInt, alpha_i, gamma_ij] = ...
    opt_bcr_exact_single_recipient(mAdj, Rem);
```

The returned variables are:

- `opt_bcr`: critical benefit-to-cost ratio for the exact solution;
- `opt_mInt`: optimized single-recipient donation structure;
- `alpha_i` and `gamma_ij`: intermediate quantities used by the calculation.

The results in Fig. 3a and b then can be reproduced. Note that the exact optimization results(Fig. 3d and Fig.4c,d) can be reproduced using `opt_bcr_exact_single_recipient`. 

### 2. Gradient-based optimization: single recipient

1. Open `opt_RMSprop_single_recipient.mlx`.
2. Ensure `BA_n100_k6_idx0.mat` is in the current working directory.
3. Run the Live Script.

The settings currently shown in the script include:

- `epoch = 100000`: maximum number of iterations;
- `eta = 0.01`: step-size parameter;
- `alpha = 0.9`: moving-average parameter for squared gradients;
- `epsilon = 1e-6`: numerical stabilizer;
- `rho = 1.01`: growth factor for penalty parameters;
- initial `sigma = 1` and `gamma = 10^-2`.

The script stops early when the average absolute update falls below its convergence threshold. It creates variables including `bcr_array`, `f_penalty_array`, `hidden_t`, `mInt_process`, and `mInt_opt`. 

### 3. Gradient-based optimization: multiple recipients

1. Open `opt_RMSprop_multiple_recipient.mlx`.
2. Ensure `BA_n100_k6_idx0.mat` is in the current working directory.
3. Run the Live Script.

The settings currently shown in the script include:

- `epoch = 100000`: maximum number of iterations;
- `eta = 0.1`: step-size parameter;
- `alpha = 0.9`;
- `epsilon = 1e-6`;
- `rho = 1.01`;
- initial `sigma = 1` and `gamma = 10^-2`.

The script stops early when the average absolute update falls below its convergence threshold. It creates variables including `bcr_array`, `f_penalty_array`, `hidden_t`, `mInt_process`, and `mInt_opt`. 

The results in Fig. 6a-d then can be reproduced. 

### 4. Critical benefit-to-cost ratio for strategic allocation of social goods

The function `getBCratioAsymInteract.m` calculates the critical benefit-to-cost ratio when the replacement graph and interaction graph may differ. Its first input is the adjacency matrix of the replacement graph. The interaction graph and a precomputed remeeting-time matrix can be supplied as optional inputs.

Function signature:

```matlab
bcr = getBCratioAsymInteract(mAdj)
bcr = getBCratioAsymInteract(mAdj, mInt)
bcr = getBCratioAsymInteract(mAdj, mInt, Rem)
```

Arguments:

- `mAdj`: adjacency matrix of the replacement graph;
- `mInt` (optional): adjacency matrix of the interaction graph. If omitted, the function uses `mAdj` as the interaction graph;
- `Rem` (optional): precomputed remeeting-time matrix. If omitted, the function calculates it from `mAdj` using `findRemeetingTimes`.

The function returns `bcr`, the calculated critical benefit-to-cost ratio. 

Example:

```matlab
load('BA_n20_k6_idx2.mat')
bcr = getBCratioAsymInteract(mAdj);
```

This minimal example uses the same adjacency matrix for replacement and interaction. To reproduce Fig. 2c and Fig. 4e, use the replacement matrix, interaction matrix, and parameter settings used for those panels in the manuscript.

## Input-data notes

The MATLAB `.mat` files contain an adjacency matrix named `mAdj`. For the example files, its dimensions are `20 × 20` or `100 × 100`. The helper function `normalizedLaplacian.m` symmetrizes its input using `max(mAdj, mAdj')`, so the replacement graph is treated as undirected by these calculations.

## Outputs 

- The exact-solution demo leaves its returned variables in the MATLAB workspace.
- The RMSprop scripts create optimization histories and optimized donation-structure variables in the MATLAB workspace. Saving commands in the supplied scripts may be commented out.
- `getBCratioAsymInteract` returns a scalar critical benefit-to-cost ratio.

## Mapping code to manuscript results

| Manuscript result | Main code | Notes |
|---|---|---|
| Fig. 2c | `getBCratioAsymInteract.m` | Critical benefit-to-cost ratio for asymmetric interaction structure. |
| Fig. 3a,b | `opt_bcr_exact_test.mlx`, `opt_bcr_exact_single_recipient.mlx` | Exact single-recipient optimization demo file. |
| Fig. 3d and Fig. 4c,d | `opt_bcr_exact_single_recipient.mlx` | Exact single-recipient solution. |
| Fig. 4e | `getBCratioAsymInteract.m` | Critical benefit-to-cost ratio for strategic allocations of social goods. |
| Fig. 6a–d | `opt_RMSprop_multiple_recipient.mlx` `opt_RMSprop_single_recipient.mlx` | Single and multiple-recipient gradient-based optimization, according to the current README. |
| Gradient-based single-recipient optimization | `opt_RMSprop_single_recipient.mlx`, `gradient_single_recipient.mlx` | RMSprop-style update and penalty terms. |
| Gradient-based multiple-recipient optimization | `opt_RMSprop_multiple_recipient.mlx`, `gradient_multiple_recipients.mlx` | RMSprop-style update and penalty terms. |
| PC exact solution | `opt_bcr_exact_single_recipient_pc.mlx` | Exact single-recipient optimization under the PC update rule. |
| IM exact solution | `opt_bcr_exact_single_recipient_im.mlx` | Exact single-recipient optimization under the IM update rule. |

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

## Contact

For questions about the code or reproducing the computational results, please contact the corresponding author listed in the associated manuscript.
