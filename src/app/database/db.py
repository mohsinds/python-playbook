from __future__ import annotations

from datetime import datetime
from typing import Any

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict

from app.config.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


class Database:
    _instance: "Database | None" = None
    _connection: MySQLConnection | None = None

    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_connection(self) -> MySQLConnection:
        """
        Returns a single shared DB connection.
        Reconnects if connection is missing or closed.
        """
        if self._connection is None or not self._connection.is_connected():
            self._connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
            )
        return self._connection

    def __enter__(self) -> "Database":
        """Context manager entry: return self for use in 'with' block."""
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any) -> None:
        """Context manager exit: close the connection when leaving the 'with' block."""
        self.close_connection()
        return None

    def close_connection(self) -> None:
        if self._connection is not None and self._connection.is_connected():
            self._connection.close()
            self._connection = None

    def insert_user(self, username: str, email: str, password: str) -> int:
        """
        Inserts a user and returns the inserted row id.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO users (username, email, password, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        now = datetime.now()

        cursor.execute(query, (username, email, password, now, now))
        conn.commit()

        user_id = cursor.lastrowid
        cursor.close()
        return user_id

    def get_user_by_id(self, user_id: int) -> dict[str, Any] | None:
        """
        Returns one user as a dictionary, or None if not found.
        """
        conn = self.get_connection()
        cursor: MySQLCursorDict = conn.cursor(dictionary=True)

        query = """
            SELECT id, username, email, password, created_at, updated_at
            FROM users
            WHERE id = %s
        """
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

        cursor.close()
        return row

    def get_all_users(self) -> list[dict[str, Any]]:
        """
        Returns all users as a list of dictionaries.
        """
        conn = self.get_connection()
        cursor: MySQLCursorDict = conn.cursor(dictionary=True)

        query = """
            SELECT id, username, email, password, created_at, updated_at
            FROM users
            ORDER BY id ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        return rows