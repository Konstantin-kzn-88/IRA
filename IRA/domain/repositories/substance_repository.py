# src/domain/repositories/substance_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.substance import Substance


class SubstanceRepository(ABC):
    """Интерфейс репозитория для работы с веществами"""

    @abstractmethod
    def create(self, substance: Substance) -> Optional[int]:
        """Создание нового вещества"""
        pass

    @abstractmethod
    def get(self, substance_id: int) -> Optional[Substance]:
        """Получение вещества по ID"""
        pass

    @abstractmethod
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Substance]:
        """Получение списка веществ с пагинацией"""
        pass

    @abstractmethod
    def update(self, substance: Substance) -> bool:
        """Обновление данных вещества"""
        pass

    @abstractmethod
    def delete(self, substance_id: int) -> bool:
        """Удаление вещества"""
        pass

    @abstractmethod
    def search(self, name: Optional[str] = None, sub_type: Optional[int] = None) -> List[Substance]:
        """Поиск веществ по параметрам"""
        pass