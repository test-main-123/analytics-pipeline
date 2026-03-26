"""Main entry point for the analytics pipeline."""

import argparse
import logging
import sys

from pipeline import Pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the analytics pipeline.")
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to the pipeline configuration file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run extract and transform without loading.",
    )
    args = parser.parse_args()

    logger.info("Starting pipeline with config: %s", args.config)
    pipeline = Pipeline(args.config)

    logger.info("Extracting data...")
    data = pipeline.extract()
    logger.info("Extracted %d rows.", len(data))

    logger.info("Transforming data...")
    data = pipeline.transform()
    logger.info("Transformed data has %d rows.", len(data))

    if args.dry_run:
        logger.info("Dry run complete. Skipping load.")
        return

    logger.info("Loading data...")
    output_path = pipeline.load()
    logger.info("Data written to %s", output_path)


if __name__ == "__main__":
    main()
