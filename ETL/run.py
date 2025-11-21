import argparse
from ETL.pipeline import digital_data_etl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Digital Data ETL pipeline.")
    parser.add_argument(
        "--user",
        dest="user_full_name",
        type=str,
        default="Moetez Fradi",
        help="Full name of the user (e.g., 'Jane Doe')",
    )
    parser.add_argument(
        "--links",
        nargs="*",
        default=[
            "https://github.com/Moetez-Fradi/Galery-Classifier",
            "https://github.com/Moetez-Fradi/HaAf",
            "https://github.com/Moetez-Fradi/PosePal-Seneca-Hackathon",
            "https://github.com/Moetez-Fradi/Everyday-Agent",
        ],
        help="Space-separated list of links to crawl",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    digital_data_etl(
        user_full_name=args.user_full_name,
        links=args.links,
    )