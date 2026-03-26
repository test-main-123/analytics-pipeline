# Analytics Pipeline

A sample data analytics pipeline built with Python.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Run the full pipeline
python main.py --config config.yaml

# Dry run (no output written)
python main.py --dry-run
```

## Configuration

Edit `config.yaml` to configure data sources, transformations, and output settings.

## Project Structure

- `main.py` - CLI entry point
- `pipeline.py` - Core ETL pipeline logic
- `config.yaml` - Pipeline configuration
- `requirements.txt` - Python dependencies
