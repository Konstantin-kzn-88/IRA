from dataclasses import dataclass
from typing import Optional


@dataclass
class Tank:
    """Модель Резервуара"""
    tank_id: Optional[int]
    tank_name: str
    tank_type: str  # - Одностенный, С внешней защитной оболочкой, С двойной оболочкой и т.д.
    volume: float
    degree_filling: float
    pressure: float
    temperature: float
    component_enterprise: str
    spill_square: float
    sub_id: int
    coordinate: str

    def validate(self) -> bool:
        """Валидация данных вещества"""
        if self.tank_type not in (
        'Одностенный', 'С внешней защитной оболочкой', 'С двойной оболочкой', 'Полной герметизации'):
            return False
        if not self.volume > 0.1 and self.volume <= 50000:
            return False
        if not self.degree_filling >= 0 and self.degree_filling <= 1:
            return False
        if self.temperature <= -273:
            return False
        if self.spill_square < 1:
            return False
        return True

