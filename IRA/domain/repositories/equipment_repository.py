from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.equipment import Tank


class TankRepository(ABC):
    """Интерфейс репозитория для работы с Резервуаром"""

    @abstractmethod
    def create(self, tank: Tank) -> Optional[int]:
        """Создание нового Резервуара"""
        pass

    @abstractmethod
    def get(self, tank_id: int) -> Optional[Tank]:
        """Получение Резервуара по ID"""
        pass

    @abstractmethod
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Tank]:
        """Получение списка веществ с пагинацией"""
        pass

    @abstractmethod
    def update(self, tank: Tank) -> bool:
        """Обновление данных вещества"""
        pass

    @abstractmethod
    def delete(self, tank_id: int) -> bool:
        """Удаление Резервуара"""
        pass

    @abstractmethod
    def search(self, tank_name: Optional[str] = None, sub_id: Optional[int] = None) -> List[Tank]:
        """Поиск Резервуара по параметрам"""
        pass