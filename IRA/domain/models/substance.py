from dataclasses import dataclass
from typing import Optional


@dataclass
class Substance:
    """Модель вещества"""
    id: Optional[int]
    sub_name: str
    density_liquid: float
    molecular_weight: float
    boiling_temperature_liquid: float
    heat_evaporation_liquid: float
    adiabatic: float
    heat_capacity_liquid: float
    class_substance: int  # 1-4
    heat_of_combustion: float
    sigma: int  # 4 или 7
    energy_level: int  # 1 или 2
    flash_point: float
    auto_ignition_temp: float
    lower_concentration_limit: float
    upper_concentration_limit: float
    threshold_toxic_dose: Optional[float]
    lethal_toxic_dose: Optional[float]
    sub_type: int  # 0-7

    def validate(self) -> bool:
        """Валидация данных вещества"""
        if not (1 <= self.class_substance <= 4):
            return False
        if self.sigma not in (4, 7):
            return False
        if self.energy_level not in (1, 2):
            return False
        if not (0 <= self.sub_type <= 7):
            return False
        if self.lower_concentration_limit >= self.upper_concentration_limit:
            return False
        if self.flash_point >= self.auto_ignition_temp:
            return False
        return True
