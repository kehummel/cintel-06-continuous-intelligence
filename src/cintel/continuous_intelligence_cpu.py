"""
continuous_intelligence_case.py - Project script (example).

Author: Denise Case, Kim Hummel
Date: 2026-03

System Metrics Data

- Data represents recent observations from a monitored system.
- Each row represents one observation of system activity.

- The CSV file includes these columns:
  - requests: number of requests handled
  - errors: number of failed requests
  - total_latency_ms: total response time in milliseconds

Purpose

- Read system metrics from a CSV file.
- Apply multiple continuous intelligence techniques learned earlier:
  - anomaly detection
  - signal design
  - simple drift-style reasoning
- Summarize the system's current state.
- Save the resulting system assessment as a CSV artifact.
- Log the pipeline process to assist with debugging and transparency.

Questions to Consider

- What signals best summarize the health of a system?
- When multiple indicators change at once, how should we interpret the system's state?
- How can monitoring data support operational decisions?

Paths (relative to repo root)

    INPUT FILE: data/cpu_metrics_hummel.csv
    OUTPUT FILE: artifacts/system_assessment_cpu.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.continuous_intelligence_cpu
"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P6", level="DEBUG")

# === DEFINE GLOBAL PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "cpu_metrics_hummel.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "cpu_assessment_hummel.csv"
ANOMALY_FILE: Final[Path] = ARTIFACTS_DIR / "cpu_anomalies_hummel.csv"

# === DEFINE THRESHOLDS ===

# Analysts need to know their data and
# choose thresholds that make sense for their specific use case.

MAX_CPS_USAGE: Final[float] = 100.0
MAX_CPU_TEMP: Final[float] = 110.0
MAX_MISS_RATE: Final[float] = 9.0
MAX_POWER: Final[float] = 110.0

# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the pipeline.

    log_header() logs a standard run header.
    log_path() logs repo-relative paths (privacy-safe).
    """
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    # Ensure artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ----------------------------------------------------
    # STEP 1: READ SYSTEM METRICS
    # ----------------------------------------------------
    df = pl.read_csv(DATA_FILE)

    LOG.info(f"STEP 1. Loaded {df.height} system records")

    df = df.sort("time")

    LOG.info("Sorted Records by time")

    WINDOW_SIZE: int = 102

    # ----------------------------------------------------
    # STEP 2: SET UP ROLLING MEAN
    # ----------------------------------------------------
    # This step connects to Module 4: Rolling Mean
    # Sets up a rolling mean to see if CPU usage stays consistent over time.
    # Checking the average per hour.

    cpu_usage_rolling_mean_recipe: pl.Expr = (
        pl.col("cpu_usage _%")
        .rolling_mean(WINDOW_SIZE)
        .round(2)
        .alias("cpu_usage_rolling_mean")
    )

    # ----------------------------------------------------
    # STEP 3: DESIGN SIGNALS
    # ----------------------------------------------------
    # This step connects to Module 3: Signal Design.
    # Create useful signals derived from raw system metrics.

    LOG.info("STEP 3. Designing signals from raw metrics...")

    df = df.with_columns(
        [
            (pl.col("power_consumption_W") / pl.col("cpu_usage _%"))
            .round(2)
            .alias("power_per_usage"),
            (pl.col("cpu_temperature_C") / pl.col("cpu_usage _%"))
            .round(2)
            .alias("temp_per_usage"),
            (pl.col("cache_miss_rate_%") / pl.col("cpu_usage _%"))
            .round(2)
            .alias("miss_rate_per_usage"),
            cpu_usage_rolling_mean_recipe,
        ]
    )
    LOG.info("Step 3 complete. Signals created.")

    LOG.info("Rolling mean per hour of CPU Usage")

    if len(df) > 102:
        for i, row in enumerate(df.iter_rows(named=True)):
            if row["cpu_usage_rolling_mean"] is not None and (i + 1) % 102 == 0:
                LOG.info(
                    f"Row {i + 1}: "
                    f"mean for last hour={row['cpu_usage_rolling_mean']:.2f}, "
                )

    # ----------------------------------------------------
    # STEP 4: DETECT ANOMALIES
    # ----------------------------------------------------
    # This step connects to Module 2: Anomaly Detection.
    # Check whether signal values exceed reasonable thresholds.

    LOG.info("STEP 4. Checking for anomalies in system signals...")

    anomalies_df = df.filter(
        (pl.col("cpu_usage _%") > MAX_CPS_USAGE)
        | (pl.col("cpu_temperature_C") > MAX_CPU_TEMP)
        | (pl.col("cache_miss_rate_%") > MAX_MISS_RATE)
        | (pl.col("power_consumption_W") > MAX_POWER)
    )

    LOG.info(
        f"STEP 4. Using thresholds: MAX_CPS_USAGE={MAX_CPS_USAGE}, "
        f"MAX_CPU_TEMP={MAX_CPU_TEMP}, "
        f"MAX_MISS_RATE={MAX_MISS_RATE}, "
        f"MAX_POWER={MAX_POWER}"
    )

    LOG.info(f"STEP 4. Anomalies detected: {anomalies_df.height}")

    # Save anomalies with their corresponding time column
    if anomalies_df.height > 0:
        anomalies_df.write_csv(ANOMALY_FILE)
        LOG.info(f"STEP 4. Wrote anomalies file: {ANOMALY_FILE}")
    else:
        LOG.info("STEP 4. No anomalies detected. Anomaly file not written.")

    # ----------------------------------------------------
    # STEP 4: SUMMARIZE CURRENT SYSTEM STATE
    # ----------------------------------------------------
    # This step brings together ideas from earlier modules:
    # - Module 3: Signal Design
    # - Module 2: Anomaly Detection
    # It then adds the main goal of Module 6:
    # assess the overall state of the system.

    # NOTE: recipes for column creation and filtering
    # can be done in place as we add signals and logic to a DataFrame.
    # When logic is more complex, it can be helpful to
    # break it into multiple steps/recipes
    # for readability and debugging as shown previously.

    LOG.info("STEP 5. Summarizing system state from monitored signals...")

    summary_df = df.select(
        [
            pl.col("cpu_usage _%").mean().round(3).alias("avg_cpu_usage _%"),
            pl.col("cpu_temperature_C").mean().round(3).alias("avg_cpu_temperature_C"),
            pl.col("cache_miss_rate_%").mean().round(3).alias("avg_cache_miss_rate_%"),
            pl.col("power_consumption_W")
            .mean()
            .round(3)
            .alias("avg_power_consumption_W"),
            pl.col("power_per_usage").mean().round(3).alias("avg_power_per_usage"),
            pl.col("temp_per_usage").mean().round(3).alias("avg_temp_per_usage"),
            pl.col("miss_rate_per_usage")
            .mean()
            .round(3)
            .alias("avg_miss_rate_per_usage"),
        ]
    )

    # display summary
    summary_dict = summary_df.to_dicts()[0]

    LOG.info("Summary (one field per line):")
    for field_name, field_value in summary_dict.items():
        LOG.info(f"{field_name}: {field_value}")

    # Add a simple assessment label
    summary_df = summary_df.with_columns(
        pl.when(
            (pl.col("avg_power_per_usage") > MAX_POWER)
            | (pl.col("avg_temp_per_usage") > MAX_CPU_TEMP)
            | (pl.col("avg_miss_rate_per_usage") > MAX_MISS_RATE)
        )
        .then(pl.lit("DEGRADED"))
        .otherwise(pl.lit("STABLE"))
        .alias("system_state")
    )

    LOG.info("STEP 5. System assessment completed")

    # ----------------------------------------------------
    # STEP 6: SAVE SYSTEM ASSESSMENT
    # ----------------------------------------------------
    summary_dict = summary_df.to_dicts()[0]

    summary_df = pl.DataFrame(
        {
            "field_name": list(summary_dict.keys()),
            "field_value": [str(value) for value in summary_dict.values()],
        }
    )

    summary_df.write_csv(OUTPUT_FILE)

    LOG.info(f"STEP 6. Wrote system assessment file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
