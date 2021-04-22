import subprocess
import os
import sys
from pathlib import Path


def get_python_path():
    # try:
    #     desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    #     path = desktop + "\TalpiBot\Virtual_Environments\Scripts\python.exe"
    #     if os.path.exists(path):
    #         return path
    # except:
    #     return sys.executable
    return sys.executable


PYTHON_INTERPRETER = get_python_path()


def install(file_path):
    print(f"[*] Trying to install {file_path}")

    with open(file_path, 'r') as req_file:
        for package in req_file.readlines():
            print(f"\t\t[*] Trying to install package: {package}")
            try:
                subprocess.check_call([PYTHON_INTERPRETER, "-m", "pip", "install", "-U", package])
            except:
                print(f'\t\t[!!!!] Cannot install package: {package}')


def main():
    for path in Path('../').rglob('requirements.txt'):
        full_path = os.path.abspath(path.absolute())
        try:
            print(full_path)
            install(full_path)
        except:
            print(f"[!!!!] Can't install from: {full_path}")


if __name__ == '__main__':
    main()
