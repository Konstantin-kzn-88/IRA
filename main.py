import os
import pathlib


def create_directory(path):
    """Создание директории, если она не существует"""
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def create_file(path, content=''):
    """Создание пустого файла"""
    # Убеждаемся, что директория существует
    directory = os.path.dirname(path)
    create_directory(directory)

    # Создаем файл
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def create_project_structure(base_path):
    """Создание структуры проекта industrial_risk_analyzer"""
    # Создаем корневую директорию проекта
    project_root = os.path.join(base_path, 'industrial_risk_analyzer')
    create_directory(project_root)

    # Структура src
    src_path = os.path.join(project_root, 'src')

    # Domain
    domain_paths = [
        os.path.join('domain', 'models'),
        os.path.join('domain', 'repositories'),
        os.path.join('domain', 'services', 'calculators'),
        os.path.join('domain', 'services', 'validators')
    ]

    domain_files = [
        os.path.join('domain', 'models', 'equipment.py'),
        os.path.join('domain', 'models', 'substance.py'),
        os.path.join('domain', 'models', 'calculation.py')
    ]

    # Infrastructure
    infra_paths = [
        os.path.join('infrastructure', 'database', 'repositories'),
        os.path.join('infrastructure', 'database', 'models'),
        os.path.join('infrastructure', 'file_storage')
    ]

    # Application
    app_paths = [
        os.path.join('application', 'interfaces'),
        os.path.join('application', 'services'),
        os.path.join('application', 'dto')
    ]

    # Presentation
    presentation_paths = [
        os.path.join('presentation', 'gui', 'windows'),
        os.path.join('presentation', 'gui', 'dialogs'),
        os.path.join('presentation', 'gui', 'widgets'),
        os.path.join('presentation', 'gui', 'views'),
        os.path.join('presentation', 'viewmodels')
    ]

    # Common
    common_files = [
        os.path.join('common', 'constants.py'),
        os.path.join('common', 'exceptions.py')
    ]

    # Создаем все директории в src
    for folder in domain_paths + infra_paths + app_paths + presentation_paths:
        create_directory(os.path.join(src_path, folder))

    # Создаем файлы в src
    for file in domain_files + common_files:
        create_file(os.path.join(src_path, file))

    # Создаем структуру тестов
    test_paths = [
        os.path.join('tests', 'unit'),
        os.path.join('tests', 'integration'),
        os.path.join('tests', 'e2e')
    ]

    for folder in test_paths:
        create_directory(os.path.join(project_root, folder))

    # Создаем остальные директории
    other_dirs = ['docs', 'resources']
    for folder in other_dirs:
        create_directory(os.path.join(project_root, folder))

    # Создаем файлы requirements
    req_path = os.path.join(project_root, 'requirements')
    create_directory(req_path)

    requirement_files = ['base.txt', 'dev.txt', 'prod.txt']
    for file in requirement_files:
        create_file(os.path.join(req_path, file))

    print("Структура проекта успешно создана!")


if __name__ == '__main__':
    # Создаем структуру в текущей директории
    create_project_structure('.')