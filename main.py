"""
Transaction analysis: time-based analysis, filtering, aggregations, and data cleaning.
"""
import csv
from collections import defaultdict
from datetime import datetime
from typing import Any

from app.database.db import Database
from app.services.math_service import multiply

CSV_PATH = "files/transactions.csv"
TIME_FMT = "%Y-%m-%d %H:%M:%S"


def load_transactions(path: str) -> list[dict[str, Any]]:
    """Load CSV and add total_amount to each row."""
    rows = []
    with open(path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        for row in reader:
            try:
                price = float(row["price"])
                qty = float(row["quantity"])
                row["total_amount"] = multiply(price, qty)
                rows.append(row)
            except (ValueError, KeyError):
                continue
    return rows


def is_valid_transaction_time(s: str) -> bool:
    """Return True if transaction_time is parseable and reasonable."""
    try:
        dt = datetime.strptime(s.strip(), TIME_FMT)
        return 2000 <= dt.year <= 2100
    except (ValueError, TypeError):
        return False


def clean_data(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Task 6 — Data engineering logic:
    - Remove rows where price <= 0
    - Remove duplicates (by transaction_id)
    - Ensure transaction_time is valid
    """
    seen_ids = set()
    cleaned = []
    for row in rows:
        try:
            price = float(row.get("price", 0))
            if price <= 0:
                continue
            if not is_valid_transaction_time(row.get("transaction_time", "")):
                continue
            tid = row.get("transaction_id")
            if tid in seen_ids:
                continue
            seen_ids.add(tid)
            cleaned.append(row)
        except (ValueError, TypeError, KeyError):
            continue
    return cleaned


def parse_time(row: dict[str, Any]) -> datetime:
    try:
        return datetime.strptime(row["transaction_time"].strip(), TIME_FMT)
    except (ValueError, KeyError, TypeError):
        return None


# --- Task 3 — Time-based analysis ---


def total_sales_per_day(rows: list[dict[str, Any]]) -> dict[str, float]:
    """Total sales per day (date string -> sum of total_amount)."""
    by_day: dict[str, float] = defaultdict(float)
    for row in rows:
        dt = parse_time(row)
        if dt is None:
            continue
        key = dt.date().isoformat()
        by_day[key] += float(row.get("total_amount", 0))
    return dict(by_day)


def total_sales_per_hour(rows: list[dict[str, Any]]) -> dict[int, float]:
    """Total sales per hour (hour 0–23 -> sum of total_amount)."""
    by_hour: dict[int, float] = defaultdict(float)
    for row in rows:
        dt = parse_time(row)
        if dt is None:
            continue
        by_hour[dt.hour] += float(row.get("total_amount", 0))
    return dict(by_hour)


def transactions_per_day_of_week(rows: list[dict[str, Any]]) -> dict[int, int]:
    """Number of transactions per day of week (0=Monday … 6=Sunday)."""
    by_weekday: dict[int, int] = defaultdict(int)
    for row in rows:
        dt = parse_time(row)
        if dt is None:
            continue
        by_weekday[dt.weekday()] += 1
    return dict(by_weekday)


# --- Task 4 — Filtering ---


def filter_after_12pm(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Transactions after 12 PM (hour >= 12)."""
    return [r for r in rows if (dt := parse_time(r)) is not None and dt.hour >= 12]


def filter_jan_11_to_13(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Transactions between Jan 11 and Jan 13 (inclusive)."""
    out = []
    for r in rows:
        dt = parse_time(r)
        if dt is None:
            continue
        if dt.year != 2025:
            continue
        if dt.month != 1:
            continue
        if 11 <= dt.day <= 13:
            out.append(r)
    return out


def filter_usa_only(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Transactions from USA only."""
    return [r for r in rows if r.get("country", "").strip().upper() == "USA"]


# --- Task 5 — Aggregations ---


def revenue_per_country(rows: list[dict[str, Any]]) -> dict[str, float]:
    """sum(total_amount) grouped by country."""
    by_country: dict[str, float] = defaultdict(float)
    for row in rows:
        c = (row.get("country") or "").strip() or "Unknown"
        by_country[c] += float(row.get("total_amount", 0))
    return dict(by_country)


def revenue_per_category(rows: list[dict[str, Any]]) -> dict[str, float]:
    """sum(total_amount) grouped by category."""
    by_cat: dict[str, float] = defaultdict(float)
    for row in rows:
        c = (row.get("category") or "").strip() or "Unknown"
        by_cat[c] += float(row.get("total_amount", 0))
    return dict(by_cat)


def top_n_users_by_spending(
    rows: list[dict[str, Any]], n: int = 3
) -> list[tuple[str, float]]:
    """Top n users by total spending (user_id -> sum(total_amount))."""
    by_user: dict[str, float] = defaultdict(float)
    for row in rows:
        u = (row.get("user_id") or "").strip() or "Unknown"
        by_user[u] += float(row.get("total_amount", 0))
    sorted_users = sorted(by_user.items(), key=lambda x: -x[1])
    return sorted_users[:n]


def main() -> None:
    with Database() as db:
        # insert
        new_user_id = db.insert_user(
            username="mohsin",
            email="mohsin@example.com",
            password="123456"
        )
        print("Inserted user id:", new_user_id)

        # get one
        user = db.get_user_by_id(new_user_id)
        print("Single user:", user)

        # get all
        users = db.get_all_users()
        print("All users:", users)


    return
    # Load and clean (Task 6)
    raw = load_transactions(CSV_PATH)
    rows = clean_data(raw)
    print(f"Loaded {len(raw)} rows, {len(rows)} after cleaning.\n")

    # Task 3 — Time-based analysis
    print("--- Task 3 — Time-based analysis ---")
    sales_per_day = total_sales_per_day(rows)
    print("Total sales per day:", sales_per_day)

    sales_per_hour = total_sales_per_hour(rows)
    print("Total sales per hour:", dict(sorted(sales_per_hour.items())))

    tx_per_weekday = transactions_per_day_of_week(rows)
    weekday_names = "Mon Tue Wed Thu Fri Sat Sun".split()
    print(
        "Transactions per day of week:",
        {weekday_names[k]: v for k, v in sorted(tx_per_weekday.items())},
    )
    print()

    # Task 4 — Filtering
    print("--- Task 4 — Filtering ---")
    after_12 = filter_after_12pm(rows)
    print(f"Transactions after 12 PM: {len(after_12)}")

    jan_11_13 = filter_jan_11_to_13(rows)
    print(f"Transactions Jan 11–13: {len(jan_11_13)}")

    usa_only = filter_usa_only(rows)
    print(f"Transactions from USA only: {len(usa_only)}")
    print()

    # Task 5 — Aggregations
    print("--- Task 5 — Aggregations ---")
    rev_country = revenue_per_country(rows)
    print("Revenue per country:", rev_country)

    rev_category = revenue_per_category(rows)
    print("Revenue per category:", rev_category)

    top3 = top_n_users_by_spending(rows, 3)
    print("Top 3 users by spending:", top3)

if __name__ == "__main__":
    main()
