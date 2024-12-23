from IRA.domain.models.substance import Substance
from IRA.infrastructure.database.sqlite.substance_repository import SQLiteSubstanceRepository

def main():
    # 1. Создаем репозиторий
    repo = SQLiteSubstanceRepository("substances.db")

    # 2. Создаем новое вещество (бензин)
    benzin = Substance(
        id=None,  # id будет присвоен базой данных
        sub_name="Бензин АИ-92",
        density_liquid=750.0,
        molecular_weight=0.095,
        boiling_temperature_liquid=35.0,
        heat_evaporation_liquid=372000.0,
        adiabatic=1.1,
        heat_capacity_liquid=2100.0,
        class_substance=4,
        heat_of_combustion=43600.0,
        sigma=4,
        energy_level=2,
        flash_point=-27.0,
        auto_ignition_temp=255.0,
        lower_concentration_limit=0.76,
        upper_concentration_limit=8.0,
        threshold_toxic_dose=None,
        lethal_toxic_dose=None,
        sub_type=0  # ЛВЖ
    )

    # 3. Сохраняем вещество в базу
    benzin_id = repo.create(benzin)
    if benzin_id:
        print(f"Бензин успешно сохранен с ID: {benzin_id}")
    else:
        print("Ошибка при сохранении бензина")
        return

    # 4. Получаем вещество из базы
    loaded_benzin = repo.get(benzin_id)
    if loaded_benzin:
        print(f"Загружено вещество: {loaded_benzin.sub_name}")
        print(f"Плотность: {loaded_benzin.density_liquid} кг/м³")

    # 5. Изменяем параметры
    loaded_benzin.density_liquid = 760.0  # изменяем плотность
    if repo.update(loaded_benzin):
        print("Данные успешно обновлены")
    else:
        print("Ошибка при обновлении данных")

    # 6. Ищем все вещества типа ЛВЖ
    lvg_substances = repo.search(sub_type=0)
    print(f"\nНайдено ЛВЖ веществ: {len(lvg_substances)}")
    for substance in lvg_substances:
        print(f"- {substance.sub_name}")

    # 7. Поиск по названию
    found_substances = repo.search(name="бензин")
    print(f"\nРезультаты поиска по слову 'бензин':")
    for substance in found_substances:
        print(f"- {substance.sub_name}")


if __name__ == "__main__":
    main()