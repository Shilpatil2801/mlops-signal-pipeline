import argparse
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


def setup_logger(log_file: str):
    logger = logging.getLogger("mlops_pipeline")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def load_config(config_path: str):
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    if config is None:
        raise ValueError("Config file is empty or invalid YAML")

    required_keys = ["seed", "window", "version"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing config key: {key}")

    return config



def load_data(input_path: str):
    from pathlib import Path
    import pandas as pd

    if not Path(input_path).exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        # Read raw lines
        with open(input_path, "r") as f:
            lines = f.readlines()

        if not lines:
            raise ValueError("Input CSV is empty")

        # Remove quotes and strip
        lines = [line.strip().replace('"', '') for line in lines]

        # Split header
        header = lines[0].split(",")

        # Split data rows
        data = [line.split(",") for line in lines[1:]]

        # Create DataFrame
        df = pd.DataFrame(data, columns=header)

        # Normalize column names
        df.columns = df.columns.str.strip().str.lower()

    except Exception as e:
        raise ValueError(f"Invalid CSV format: {str(e)}")

    if df.empty:
        raise ValueError("Input CSV is empty after parsing")

    if "close" not in df.columns:
        raise ValueError("Missing required column: 'close'")

    # Convert close to numeric
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    df = df.dropna(subset=["close"])

    if df.empty:
        raise ValueError("No valid numeric data in 'close' column")

    return df

def compute_signals(df: pd.DataFrame, window: int, logger):
    logger.info("Computing rolling mean")
    df["rolling_mean"] = df["close"].rolling(window=window).mean()

    logger.info("Generating signals")
    df = df.dropna(subset=["rolling_mean"])

    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

    return df


def write_metrics(output_path: str, data: dict):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="MLOps Signal Pipeline")
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    logger = setup_logger(args.log_file)

    start_time = time.time()

    try:
        logger.info("Job started")

        # Load config
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        logger.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        # Set seed
        np.random.seed(seed)

        # Load data
        df = load_data(args.input)
        logger.info(f"Rows loaded: {len(df)}")

        # Process
        df = compute_signals(df, window, logger)

        rows_processed = len(df)
        signal_rate = float(df["signal"].mean())

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        write_metrics(args.output, metrics)

        logger.info(f"Metrics: {metrics}")
        logger.info("Job completed successfully")

        print(json.dumps(metrics, indent=2))

        sys.exit(0)

    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)

        error_metrics = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        write_metrics(args.output, error_metrics)

        logger.error(f"Error occurred: {str(e)}")
        logger.info("Job failed")

        print(json.dumps(error_metrics, indent=2))

        sys.exit(1)


if __name__ == "__main__":
    main()