from IRA.domain.models.equipment import Tank
from IRA.infrastructure.database.sqlite.equipment_repository import SQLiteTankRepository


def main():
    # 1. Создаем репозиторий
    repo = SQLiteTankRepository("db_eg.db")

    # 2. Создаем новый Резервуар ()
    rvs_1000 = Tank(
        tank_id=None,
        tank_name='My_tank',
        tank_type='Одностенный',
        volume=1000,
        degree_filling=0.8,
        pressure=1.23,
        temperature=35,
        component_enterprise='SQ RVS',
        spill_square=2000,
        sub_id=1,
        coordinate='55.755844, 37.622823'
    )

    # 3. Сохраняем вещество в базу
    rvs_id = repo.create(rvs_1000)
    if rvs_id:
        print(f"RVS успешно сохранен с ID: {rvs_id}")
    else:
        print("Ошибка при сохранении RVS")
        return

    # 4. Получаем вещество из базы
    loaded_RVS = repo.get(rvs_id)
    if loaded_RVS:
        print(f"Загружено RVS: {loaded_RVS.tank_name}")
        print(f"Давление: {loaded_RVS.pressure} кг/м³")

    # 5. Изменяем параметры
    loaded_RVS.pressure = 2.59  # изменяем давление
    if repo.update(loaded_RVS):
        print("Данные успешно обновлены")
    else:
        print("Ошибка при обновлении данных")

    # 6. Ищем все 'component_enterprise'
    found_rvs = repo.search(component_enterprise='SQ RVS')
    print(f"\nРезультаты поиска по component_enterprise 'SQ RVS':")
    for i in found_rvs:
        print(f"- {i.tank_name}")

    # 7. Поиск по названию
    found_rvs = repo.search(tank_name='My_tank')
    print(f"\nРезультаты поиска по tank_name 'My_tank':")
    for i in found_rvs:
        print(f"- {i.tank_name}")

    # 8. Вывести все и удалить последний
    found_rvs = repo.get_all()
    print(f"\nРезультаты поиска Tank:")
    tank_del = None
    for i in found_rvs:
        print(f"- {i}")
        tank_del = i

    print(f"\nУдаляем id = {tank_del.tank_id}:")
    _ = repo.delete(tank_id=tank_del.tank_id)



if __name__ == "__main__":
    main()
