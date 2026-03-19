# Installation

This page describes how to install **PyPSA-Earth-Status** and its dependencies.

PyPSA-Earth-Status is designed to run within the **PyPSA-Earth Conda environment**, which ensures compatibility across operating systems and provides fully pinned dependencies.

## Prerequisites

Before installing PyPSA-Earth-Status, make sure you have:

- **Git**
- **Conda** (recommended: Miniconda)

## Clone the repository

First, clone the repository including all submodules:

```bash
git clone https://github.com/pypsa-meets-earth/pypsa-earth-status.git --recurse-submodules
cd pypsa-earth-status
```

## Create the Conda environment

1. Make sure you are in the project folder:
   ```bash
   cd pypsa-earth-status
   ```

2. Create the Conda environment using the lock file for your operating system:

    - Linux (x86_64)
    ```bash
    conda env create -f workflows/pypsa-earth/envs/linux-64.lock.yaml
    ```
    - macOS (Apple Silicon, arm64 / M1–M3)
    ```bash
    conda env create -f workflows/pypsa-earth/envs/osx-arm64.lock.yaml
    ```
    - macOS (Intel, x86_64)
    ```bash
    conda env create -f workflows/pypsa-earth/envs/osx-64.lock.yaml
    ```
    - Windows (x86_64)
    ```bash
    conda env create -f workflows/pypsa-earth/envs/win-64.lock.yaml
    ```

3. Activate the environment:
   ```bash
   conda activate pypsa-earth
   ```

4. Quick sanity check (optional):
   ```bash
   snakemake --help
   ```
   If you see the Snakemake help text, the environment is ready.
