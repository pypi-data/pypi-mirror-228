import shutil
from pathlib import Path

import toml
import typer
from .utils import without_special_characters_input


def create(directory: str, extension: bool = False) -> None:
    root = Path(__file__).parent.absolute()
    app_name = (
        without_special_characters_input('Digite o nome do app: ')
        .lower()
        .replace(' ', '_')
    )
    folder = Path(directory) / app_name
    shutil.rmtree(folder, ignore_errors=True)
    shutil.copytree(root / 'base', folder)
    shutil.move(folder / 'project_name', folder / app_name)
    if extension:
        with open(folder / app_name / '__init__.py', 'r') as file:
            app_class_name = app_name.title().replace('_', '')
            content = file.read()
            content = content.replace('Extension', app_class_name)
        with open(folder / app_name / '__init__.py', 'w') as file:
            file.write(content)
    else:
        with open(folder / app_name / '__init__.py', 'w') as file:
            file.write('')
    with open(folder / 'tests' / 'conftest.py', 'r') as file:
        content = file.read().replace('project_name', app_name)
    with open(folder / 'tests' / 'conftest.py', 'w') as file:
        file.write(content)
    config = toml.load(open(folder / 'config.toml', 'r'))
    config['extensions'].append(f'{app_name}.views')
    config['extensions'].append(f'{app_name}.blueprint')
    toml.dump(config, open(folder / 'config.toml', 'w'))
    with open(folder / '.env', 'r') as file:
        content = file.read().replace('project_name', app_name)
    with open(folder / '.env', 'w') as file:
        file.write(content)


def run() -> None:
    typer.run(create)
