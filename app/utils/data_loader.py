import argparse
import sys
from pathlib import Path
from typing import Any, Dict, Union

import pandas as pd
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Ticket


def load_clean_tickets(csv_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load the tickets CSV, clean the data and add derived columns.

    Steps:
    - Drop rows without a description.
    - Fill missing priority with 'medium'.
    - Normalize channel to lowercase.
    - Convert created_at to datetime.
    - Add:
        * short_description: first 140 characters of description.
        * is_urgent: True if priority is 'high' or 'urgent'.

    Parameters
    ----------
    csv_path : str | Path
        Path to the tickets CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame ready to be loaded into the database.
    """
    csv_path = Path(csv_path)

    # 1. Load CSV
    # na_values ensures empty cells are treated as NaN (e.g. empty priority)
    df = pd.read_csv(csv_path, na_values=["", " "])

    # 2. Basic cleaning

    # 2.1 Remove rows without description
    df = df.dropna(subset=["description"])

    # 2.2 Fill missing priority with 'medium'
    df["priority"] = df["priority"].fillna("medium")

    # 2.3 Normalize channel to lowercase (chat, email, phone, etc.)
    df["channel"] = df["channel"].str.lower()

    # 2.4 Convert created_at to datetime
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Optional: drop rows where date could not be parsed
    df = df.dropna(subset=["created_at"])

    # 3. Derived columns

    # 3.1 short_description: first 140 characters
    df["short_description"] = df["description"].str.slice(0, 140)

    # 3.2 is_urgent: True if priority is 'high' or 'urgent'
    df["is_urgent"] = df["priority"].str.lower().isin(["high", "urgent"])

    return df


def bulk_insert_tickets(df):
    session: Session = SessionLocal()
    try:
        tickets = [
            Ticket(
                ticket_id=int(row["ticket_id"]),
                customer_id=int(row["customer_id"]),
                created_at=row["created_at"],
                channel=str(row["channel"]),
                subject=str(row["subject"]),
                description=str(row["description"]),
                status=str(row["status"]),
                priority=str(row["priority"]),
                short_description=str(row["short_description"]),
                is_urgent=bool(row["is_urgent"]),
                agent=str(row["agent"]) if not pd.isna(row["agent"]) else None,
            )
            for _, row in df.iterrows()
        ]
        session.bulk_save_objects(tickets)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def load_csv_to_db(csv_path: str) -> bool:
    df_cleaned = load_clean_tickets(csv_path)
    bulk_insert_tickets(df_cleaned)
    return True


def get_parameters() -> Dict[str, Any]:
    """
    Parse command line arguments and return parameters for the script.

    Returns:
        Dict[str, Any]: Dictionary containing script parameters
    """
    parser = argparse.ArgumentParser(
        description="Data loader script for CSV to database operations"
    )

    parser.add_argument(
        "--csv_path", type=str, required=True, help="Path to the CSV file to load"
    )

    args = parser.parse_args()

    return {
        "csv_path": args.csv_path,
    }


def main():
    """
    Main function to execute the data loader script.
    """
    try:
        # Get parameters from command line
        params = get_parameters()

        print(f"Starting data loader with parameters: {params}")

        # Load CSV file
        csv_path = params["csv_path"]
        print(f"Loading CSV file: {csv_path}")

        # Here you would implement the actual loading logic
        # For now, just call the existing function
        success = load_csv_to_db(csv_path)

        if success:
            print(f"Successfully loaded data from {csv_path}")
        else:
            print(f"Failed to load data from {csv_path}")
            sys.exit(1)

    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
