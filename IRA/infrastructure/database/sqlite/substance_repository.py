# src/infrastructure/database/sqlite/substance_repository.py
import sqlite3
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
import logging

from IRA.domain.models.substance import Substance
from IRA.domain.repositories.substance_repository import SubstanceRepository


class SQLiteSubstanceRepository(SubstanceRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = self._setup_logger()
        self._initialize_database()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('SQLiteSubstanceRepository')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _initialize_database(self) -> None:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS substances (
            id INTEGER PRIMARY KEY,
            sub_name TEXT NOT NULL,
            density_liquid REAL,
            molecular_weight REAL,
            boiling_temperature_liquid REAL,
            heat_evaporation_liquid REAL,
            adiabatic REAL,
            heat_capacity_liquid REAL,
            class_substance INTEGER CHECK (class_substance BETWEEN 1 AND 4),
            heat_of_combustion REAL,
            sigma INTEGER CHECK (sigma IN (4, 7)),
            energy_level INTEGER CHECK (energy_level IN (1, 2)),
            flash_point REAL,
            auto_ignition_temp REAL,
            lower_concentration_limit REAL,
            upper_concentration_limit REAL,
            threshold_toxic_dose REAL,
            lethal_toxic_dose REAL,
            sub_type INTEGER CHECK (sub_type BETWEEN 0 AND 7)
        );
        """
        with self._get_connection() as conn:
            conn.executescript(create_table_sql)

    def _row_to_substance(self, row: sqlite3.Row) -> Substance:
        """Конвертация строки БД в объект Substance"""
        return Substance(**dict(row))

    def _substance_to_dict(self, substance: Substance) -> Dict[str, Any]:
        """Конвертация объекта Substance в словарь для БД"""
        data = substance.__dict__.copy()
        if 'id' in data and data['id'] is None:
            del data['id']
        return data

    def create(self, substance: Substance) -> Optional[int]:
        if not substance.validate():
            self.logger.error("Validation failed for substance")
            return None

        with self._get_connection() as conn:
            cursor = conn.cursor()
            data = self._substance_to_dict(substance)

            placeholders = ', '.join(['?'] * len(data))
            columns = ', '.join(data.keys())
            values = tuple(data.values())

            sql = f"INSERT INTO substances ({columns}) VALUES ({placeholders})"

            try:
                cursor.execute(sql, values)
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                self.logger.error(f"Error creating substance: {e}")
                return None

    def get(self, substance_id: int) -> Optional[Substance]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM substances WHERE id = ?", (substance_id,))
            row = cursor.fetchone()

            if row:
                return self._row_to_substance(row)
            return None

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Substance]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM substances LIMIT ? OFFSET ?", (limit, offset))
            return [self._row_to_substance(row) for row in cursor.fetchall()]

    def update(self, substance: Substance) -> bool:
        if not substance.validate():
            self.logger.error("Validation failed for substance")
            return False

        if substance.id is None:
            self.logger.error("Cannot update substance without id")
            return False

        with self._get_connection() as conn:
            cursor = conn.cursor()
            data = self._substance_to_dict(substance)

            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = tuple(data.values()) + (substance.id,)

            sql = f"UPDATE substances SET {set_clause} WHERE id = ?"

            try:
                cursor.execute(sql, values)
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                self.logger.error(f"Error updating substance: {e}")
                return False

    def delete(self, substance_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM substances WHERE id = ?", (substance_id,))
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                self.logger.error(f"Error deleting substance: {e}")
                return False

    def search(self, name: Optional[str] = None, sub_type: Optional[int] = None) -> List[Substance]:
        query = "SELECT * FROM substances WHERE 1=1"
        params = []

        if name:
            query += " AND sub_name LIKE ?"
            params.append(f"%{name}%")

        if sub_type is not None:
            query += " AND sub_type = ?"
            params.append(sub_type)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [self._row_to_substance(row) for row in cursor.fetchall()]