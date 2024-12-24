# src/infrastructure/database/sqlite/substance_repository.py
import sqlite3
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
import logging

from IRA.domain.models.equipment import Tank
from IRA.domain.repositories.equipment_repository import TankRepository


class SQLiteTankRepository(TankRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('SQLiteTankRepository')
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

    def _row_to_tank(self, row: sqlite3.Row) -> Tank:
        """Конвертация строки БД в объект Tank"""
        return Tank(**dict(row))

    def _tank_to_dict(self, tank: Tank) -> Dict[str, Any]:
        """Конвертация объекта Tank в словарь для БД"""
        data = tank.__dict__.copy()
        if 'id' in data and data['id'] is None:
            del data['id']
        return data

    def create(self, tank: Tank) -> Optional[int]:
        if not tank.validate():
            self.logger.error("Validation failed for Tank")
            return None

        with self._get_connection() as conn:
            cursor = conn.cursor()
            data = self._tank_to_dict(tank)

            placeholders = ', '.join(['?'] * len(data))
            columns = ', '.join(data.keys())
            values = tuple(data.values())

            sql = f"INSERT INTO Tank ({columns}) VALUES ({placeholders})"

            try:
                cursor.execute(sql, values)
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                self.logger.error(f"Error creating Tank: {e}")
                return None

    def get(self, tank_id: int) -> Optional[Tank]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tank WHERE tank_id = ?", (tank_id,))
            row = cursor.fetchone()

            if row:
                return self._row_to_tank(row)
            return None

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Tank]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tank LIMIT ? OFFSET ?", (limit, offset))
            return [self._row_to_tank(row) for row in cursor.fetchall()]

    def update(self, tank: Tank) -> bool:
        if not tank.validate():
            self.logger.error("Validation failed for tank")
            return False

        if tank.tank_id is None:
            self.logger.error("Cannot update substance without id")
            return False

        with self._get_connection() as conn:
            cursor = conn.cursor()
            data = self._tank_to_dict(tank)

            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = tuple(data.values()) + (tank.tank_id,)

            sql = f"UPDATE Tank SET {set_clause} WHERE tank_id = ?"

            try:
                cursor.execute(sql, values)
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                self.logger.error(f"Error updating tank: {e}")
                return False

    def delete(self, tank_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM Tank WHERE tank_id = ?", (tank_id,))
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                self.logger.error(f"Error deleting substance: {e}")
                return False

    def search(self, tank_name: Optional[str] = None, component_enterprise: Optional[str] = None) -> List[Tank]:
        query = "SELECT * FROM Tank WHERE 1=1"
        params = []

        if tank_name:
            query += " AND tank_name LIKE ?"
            params.append(f"%{tank_name}%")

        if component_enterprise:
            query += " AND component_enterprise LIKE ?"
            params.append(f"%{component_enterprise}%")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [self._row_to_tank(row) for row in cursor.fetchall()]
