import subprocess
import sys
from pathlib import Path

import pkg_resources


PLATFORM_IS_WIN = sys.platform == 'win32'
EXE_SUFFIX = '.exe' if PLATFORM_IS_WIN else ''

SCRIPT_PATH = Path(__file__).resolve()
PYTHON_PATH = Path(sys.base_prefix).joinpath('python').with_suffix(EXE_SUFFIX)

REQUIREMENTS_FILENAME = 'requirements.txt'
REQUIREMENTS_PATH     = SCRIPT_PATH.with_name(REQUIREMENTS_FILENAME)

VENV_NAME        = '.venv'
VENV_PATH        = SCRIPT_PATH.with_name(VENV_NAME)
VENV_BIN_PATH    = VENV_PATH.joinpath('Scripts' if PLATFORM_IS_WIN else 'bin')
VENV_PYTHON_PATH = VENV_BIN_PATH.joinpath('python').with_suffix(EXE_SUFFIX)
VENV_PIP_PATH    = VENV_BIN_PATH.joinpath('pip').with_suffix(EXE_SUFFIX)

# extra precautionary measure in order to prevent any modifications of non-venv pip
VENV_PIP_ARG = '--require-virtualenv'
    
    
def ensure_requirements() -> None:
    if _all_required_packages_found():
        return

    if _launched_from_venv():
        _install_from_requirements_file()
        return

    if not _venv_exists():
        _create_venv()
        _install_from_requirements_file()

    _relaunch_script()
    sys.exit()
    
def _all_required_packages_found() -> bool:
    with open(REQUIREMENTS_PATH, 'r') as requirements_file:
        requirements = pkg_resources.parse_requirements(requirements_file)
        # map converts to list so every unsatisfied requirement is printed out
        return all(list(map(_requirement_satisfied, requirements)))

def _requirement_satisfied(req: pkg_resources.Requirement) -> bool:
    try:
        pkg_resources.require(str(req))
        return True
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict) as error:
        print(error)
        return False

def _launched_from_venv() -> bool:
    return sys.prefix != sys.base_prefix

def _install_from_requirements_file() -> None:
    print("Installing all required packages...")
    args = [VENV_PIP_PATH, VENV_PIP_ARG, 'install', '-r', REQUIREMENTS_PATH]
    subprocess.run(args)

def _venv_exists() -> bool:
    paths_to_check = [
        VENV_PYTHON_PATH, 
        VENV_PIP_PATH
    ]
    return all(map(Path.exists, paths_to_check))

def _relaunch_script() -> None:    
    print(f"Relaunching script from {VENV_NAME} virtual env...")
    subprocess.run([VENV_PYTHON_PATH, *sys.argv])
    
def _create_venv() -> None:
    print(f"Creating {VENV_NAME} virtual env...")
    subprocess.run([PYTHON_PATH, '-m', 'venv', VENV_PATH])

    print(f"Upgrading pip in {VENV_NAME} virtual env...")
    args = [VENV_PYTHON_PATH, '-m', 'pip', VENV_PIP_ARG, 'install', '--upgrade', 'pip']
    subprocess.run(args)


if __name__ == '__main__':
    ensure_requirements()