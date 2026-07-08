# SPDX-FileCopyrightText:  PyPSA-Earth and PyPSA-Eur Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-


import logging
import os
import shutil

import country_converter as coco
import numpy as np
import pandas as pd
import pypsa
from helpers import configure_logging, harmonize_carrier_names, read_csv_nafix

logger = logging.getLogger(__name__)


def compile_health_status(snakemake):
    # Year: handle single value or list
    year = snakemake.params.year
    if isinstance(year, list):
        year = year[0]

    # Networks dictionary
    networks = snakemake.params.networks
    if not networks:
        logger.warning("No networks defined in configuration networks list.")
        return

    cc = coco.CountryConverter()

    # Resolve datasets configuration from snakemake params
    datasets = snakemake.params.datasets
    demand_source = datasets.get("demand", ["ember"])[0].lower()
    capacity_source = datasets.get("installed_capacity", ["ember"])[0].lower()
    generation_source = datasets.get("generation", ["ember"])[0].lower()

    # Load Demand Reference dynamically
    if demand_source == "ourworldindata":
        ref_demand_df = read_csv_nafix(snakemake.input.demand_owid)
        ref_demand_df = ref_demand_df.rename(
            columns={"year": "Year", "electricity_demand": "demand"}
        )
    elif demand_source == "ember":
        ref_demand_df = read_csv_nafix(snakemake.input.demand_ember)
    else:
        raise ValueError(f"Unknown demand reference source: {demand_source}")
    ref_demand_df = ref_demand_df[ref_demand_df["Year"] == year]

    # Load Capacity Reference dynamically
    if capacity_source == "irena":
        ref_capacity_df = read_csv_nafix(snakemake.input.cap_irena)
    elif capacity_source == "ember":
        ref_capacity_df = read_csv_nafix(snakemake.input.cap_ember)
    else:
        raise ValueError(f"Unknown capacity reference source: {capacity_source}")
    ref_capacity_df = ref_capacity_df[ref_capacity_df["Year"] == year].rename(
        columns={"Technology": "carrier"}
    )
    ref_capacity_df["carrier"] = harmonize_carrier_names(ref_capacity_df["carrier"])

    # Load Generation Reference dynamically
    if generation_source == "ember":
        ref_generation_df = read_csv_nafix(snakemake.input.gen_ember)
    else:
        raise ValueError(f"Unknown generation reference source: {generation_source}")
    ref_generation_df = ref_generation_df[ref_generation_df["Year"] == year].rename(
        columns={"Technology": "carrier"}
    )
    ref_generation_df["carrier"] = harmonize_carrier_names(ref_generation_df["carrier"])

    carriers = [
        "pv",
        "wind",
        "hydro",
        "ccgt",
        "coal",
        "nuclear",
        "oil",
        "biomass",
        "geothermal",
        "other",
    ]

    records = []

    for scenario_key, network_info in networks.items():
        if isinstance(network_info, str):
            network_path = network_info
            explicit_countries = None
        else:
            network_path = network_info.get("path")
            explicit_countries = network_info.get("countries")

        logger.info(f"Processing scenario {scenario_key}...")
        logger.info(f"  Using solved network: {network_path}")

        if not network_path or not os.path.exists(network_path):
            logger.warning(
                f"  Warning: Solved network path for {scenario_key} does not exist: {network_path}. Skipping."
            )
            continue

        try:
            n = pypsa.Network(network_path)
        except Exception as e:
            logger.error(f"  Error loading network for {scenario_key}: {e}. Skipping.")
            continue

        # Resolve target countries for this scenario
        if explicit_countries is not None:
            target_countries = explicit_countries
        else:
            if "country" in n.buses.columns:
                target_countries = n.buses["country"].dropna().unique().tolist()
                target_countries = [
                    c
                    for c in target_countries
                    if c and isinstance(c, str) and c.strip()
                ]
            else:
                target_countries = []

        target_countries = [c.strip().upper() for c in target_countries]

        if not target_countries:
            logger.warning(
                f"  No target countries resolved for scenario {scenario_key}. Skipping."
            )
            continue

        # Extract common stats for all countries in this network (we will filter per country)
        gen_cap = n.generators[["carrier", "p_nom", "bus"]].copy()
        if "country" in n.buses.columns:
            gen_cap["region"] = (
                n.buses.loc[gen_cap["bus"], "country"].fillna("").astype(str).values
            )
        else:
            gen_cap["region"] = ""

        if not n.storage_units.empty:
            store_cap = n.storage_units[["carrier", "p_nom", "bus"]].copy()
            if "country" in n.buses.columns:
                store_cap["region"] = (
                    n.buses.loc[store_cap["bus"], "country"]
                    .fillna("")
                    .astype(str)
                    .values
                )
            else:
                store_cap["region"] = ""
            installed_capacity = pd.concat([gen_cap, store_cap], axis=0)
        else:
            installed_capacity = gen_cap

        installed_capacity = installed_capacity[
            ~installed_capacity["carrier"].str.lower().isin(["load", "load shedding"])
        ]
        installed_capacity["carrier"] = harmonize_carrier_names(
            installed_capacity["carrier"]
        )

        gen_p_t = n.generators_t.p.multiply(n.snapshot_weightings.objective, axis=0)
        gen_gen_sum = gen_p_t.sum() * 1e-6
        df_gen = pd.DataFrame(
            {
                "generation": gen_gen_sum,
                "carrier": n.generators.carrier,
                "bus": n.generators.bus,
            }
        )
        if "country" in n.buses.columns:
            df_gen["region"] = (
                n.buses.loc[df_gen["bus"], "country"].fillna("").astype(str).values
            )
        else:
            df_gen["region"] = ""

        if not n.storage_units.empty:
            store_p_t = n.storage_units_t.p.multiply(
                n.snapshot_weightings.objective, axis=0
            )
            store_gen_sum = store_p_t.sum() * 1e-6
            df_store = pd.DataFrame(
                {
                    "generation": store_gen_sum,
                    "carrier": n.storage_units.carrier,
                    "bus": n.storage_units.bus,
                }
            )
            if "country" in n.buses.columns:
                df_store["region"] = (
                    n.buses.loc[df_store["bus"], "country"]
                    .fillna("")
                    .astype(str)
                    .values
                )
            else:
                df_store["region"] = ""
            generation = pd.concat([df_gen, df_store], axis=0)
        else:
            generation = df_gen

        generation = generation[
            ~generation["carrier"].str.lower().isin(["load", "load shedding"])
        ]
        generation["carrier"] = harmonize_carrier_names(generation["carrier"])

        # Now loop through target countries
        for country in target_countries:
            country_name = cc.convert(names=country, to="name")
            logger.info(f"  Comparing country {country_name} ({country})...")

            # 1. Demand comparison
            ref_dem_row = ref_demand_df[ref_demand_df["region"] == country]
            ref_demand = ref_dem_row["demand"].sum() if not ref_dem_row.empty else 0.0

            if "country" in n.buses.columns:
                loads_country = n.loads.bus.map(n.buses.country)
                country_loads = n.loads.index[loads_country == country]
            else:
                country_loads = n.loads.index

            pypsa_demand = (
                n.loads_t.p_set.reindex(columns=country_loads, fill_value=0.0)
                .multiply(n.snapshot_weightings.objective, axis=0)
                .sum()
                .sum()
                * 1e-6
            )

            demand_error_pct = (
                (pypsa_demand - ref_demand) / ref_demand * 100.0
                if ref_demand > 0
                else np.nan
            )

            # 2. Installed capacity comparison
            ref_cap_rows = ref_capacity_df[ref_capacity_df["region"] == country]
            ref_cap_grouped = ref_cap_rows.groupby("carrier")["p_nom"].sum()
            total_installed_capacity_ref = ref_cap_grouped.reindex(
                carriers, fill_value=0.0
            ).sum()

            installed_capacity_country = installed_capacity[
                installed_capacity["region"].str.upper() == country
            ]
            pypsa_cap_grouped = installed_capacity_country.groupby("carrier")[
                "p_nom"
            ].sum()
            total_installed_capacity_pypsa = pypsa_cap_grouped.reindex(
                carriers, fill_value=0.0
            ).sum()

            # Calculate capacity MAE as a percentage of total reference capacity
            df_cap = pd.DataFrame(index=carriers)
            df_cap["pypsa"] = pypsa_cap_grouped.reindex(carriers, fill_value=0.0)
            df_cap["ref"] = ref_cap_grouped.reindex(carriers, fill_value=0.0)
            capacity_difference_mae = (df_cap["pypsa"] - df_cap["ref"]).abs().mean()
            capacity_mae_pct = (
                (capacity_difference_mae / total_installed_capacity_ref * 100.0)
                if total_installed_capacity_ref > 0
                else 0.0
            )

            # 3. Generation comparison
            ref_gen_rows = ref_generation_df[ref_generation_df["region"] == country]
            ref_gen_grouped = ref_gen_rows.groupby("carrier")["generation"].sum()
            total_generation_ref = ref_gen_grouped.reindex(
                carriers, fill_value=0.0
            ).sum()

            generation_country = generation[generation["region"].str.upper() == country]
            pypsa_gen_grouped = generation_country.groupby("carrier")[
                "generation"
            ].sum()
            total_generation_pypsa = pypsa_gen_grouped.reindex(
                carriers, fill_value=0.0
            ).sum()

            # Calculate generation MAE as a percentage of total reference generation
            df_gen_comp = pd.DataFrame(index=carriers)
            df_gen_comp["pypsa"] = pypsa_gen_grouped.reindex(carriers, fill_value=0.0)
            df_gen_comp["ref"] = ref_gen_grouped.reindex(carriers, fill_value=0.0)
            generation_difference_mae = (
                (df_gen_comp["pypsa"] - df_gen_comp["ref"]).abs().mean()
            )
            generation_mae_pct = (
                (generation_difference_mae / total_generation_ref * 100.0)
                if total_generation_ref > 0
                else 0.0
            )

            # Append record
            records.append(
                {
                    "scenario_key": scenario_key,
                    "country_code": country,
                    "country_name": country_name,
                    "pypsa_earth_version": "v0.4.0",
                    "total_installed_capacity_ref": total_installed_capacity_ref,
                    "total_installed_capacity_pypsa": total_installed_capacity_pypsa,
                    "capacity_mae_pct": capacity_mae_pct,
                    "total_generation_ref": total_generation_ref,
                    "total_generation_pypsa": total_generation_pypsa,
                    "generation_mae_pct": generation_mae_pct,
                    "demand_ref": ref_demand,
                    "demand_pypsa": pypsa_demand,
                    "demand_error_pct": demand_error_pct,
                }
            )

    # Save to CSV
    health_status_df = pd.DataFrame(records)
    output_path = snakemake.output.health_status
    health_status_df.to_csv(output_path, index=False)
    logger.info(f"Successfully compiled health_status.csv to {output_path}!")

    # Copy to parent folder as requested
    try:
        shutil.copyfile(output_path, "../health_status.csv")
        logger.info("Successfully copied health_status.csv to ../health_status.csv!")
    except Exception as e:
        logger.error(f"Failed to copy health_status.csv to ../health_status.csv: {e}")


if __name__ == "__main__":
    if "snakemake" not in globals():
        from helpers import mock_snakemake

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        snakemake = mock_snakemake("build_health_status")
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    configure_logging(snakemake)
    compile_health_status(snakemake)
