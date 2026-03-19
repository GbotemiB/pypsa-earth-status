# Quick start

This guide shows how to run **PyPSA-Earth-Status** for the first time using the built-in example workflow.

In just a few minutes, you will:
- Create a small example PyPSA network
- Validate it against real-world reference data
- Generate tables and visualizations for inspection

---

## 1. Activate the Conda environment and location

Make sure the PyPSA-Earth environment is active:

```bash
conda activate pypsa-earth
```

## 2. Navigate to the project folder

Then, navigate to the PyPSA-Earth-Status project folder:

```bash
cd pypsa-earth-status
```

## 3. Run the example validation workflow

From the project root directory, run the default workflow target:

```bash
snakemake -j 1 visualize_data
```

> Tip: The -j 1 option runs one job at a time and is recommended for first-time users. You can increase this number later to speed up execution; beyond 4 limited improvements apply.

Wait until the workflow finishes successfully. If the command completes without errors, the example validation has been executed correctly.

This command will automatically:
- Create the example PyPSA network scigrid_de
- Save it as resources/example_DE.nc with minimal modifications
- Execute the full validation workflow
- Generate tables and visualizations in the results/ directory

## 4. Inspect the results

After the workflow completes, you can inspect the results in the `results/` folder.
The folder contains tables and visualizations comparing the example network against reference data.

In particular:
- `results/figures/` contains plots for visual inspection
- `results/tables/` contains CSV files with numerical comparisons
- `network_comparison.geojson` contains geographic data for comparing the network layout and capacities

You can open the figures using any image viewer and the CSV files using spreadsheet software or a text editor.

## 5. Next steps: test with your own networks

Now that you have successfully run the example workflow, you can test it with your own PyPSA networks!

To do so, you just need to edit the `config.yaml` file to point to your network file.

1. Specify the path of the file to your network:
    ```yaml
    network_validation:
        network_path: "{your network file}" # File to the PyPSA network file to validate
    ```

2. Edit the list of countries in the `config.yaml` file to match your network's coverage.
    ```yaml
    network_validation:
        countries: ["DE", "FR"] # ISO-3166 alpha-2 country codes for the countries in the network
    ```
   > At least 2 countries must be specified and they shall have at least a network line connecting them. Adding more countries than the necessary ones is possible and is not affecting the validation. For example, you can just keep ["DE", "FR"] in countries list while adding countries which belong to your region of interests.
