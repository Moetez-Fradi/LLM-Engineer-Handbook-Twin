import argparse
from Feature.pipeline import feature_engineering

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Digital Data ETL pipeline.")
    parser.add_argument(
        "--user",
        dest="user_full_name",
        type=str,
        default="Moetez Fradi",
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    feature_engineering(author_full_names=[args.user_full_name])
