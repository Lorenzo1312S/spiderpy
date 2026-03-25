"""
spider_runner.py

Comandi disponibili:
  - setup: crea venv + installa dipendenze
  - run: avvia spider.py
  - build: crea spider.exe e stop_spider.exe con PyInstaller
"""

import os
import subprocess
import sys
import venv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / ".venv"


def _venv_executables():
    """
    Ritorna (python_exe, pip_exe, pyinstaller_add_data_separator).
    PyInstaller usa ';' su Windows e ':' su macOS/Linux.
    """
    if os.name == "nt":
        bin_dir = VENV_DIR / "Scripts"
        return bin_dir / "python.exe", bin_dir / "pip.exe", ";"
    bin_dir = VENV_DIR / "bin"
    return bin_dir / "python", bin_dir / "pip", ":"


PYTHON_EXE, _PIP_EXE, ADD_DATA_SEP = _venv_executables()


def create_venv():
    if not VENV_DIR.exists():
        print("Creo virtualenv...")
        venv.create(str(VENV_DIR), with_pip=True)
    else:
        print("Virtualenv già esistente.")


def install_requirements():
    # Nel progetto il file sembra chiamarsi `requirment.txt` (typo).
    req_candidates = [PROJECT_DIR / "requirements.txt", PROJECT_DIR / "requirment.txt"]
    req_file = next((p for p in req_candidates if p.exists()), None)
    if req_file is None:
        print("requirements.txt (o requirment.txt) non trovato, salto install.")
        return
    print("Installo dipendenze...")
    subprocess.check_call([str(PYTHON_EXE), "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([str(PYTHON_EXE), "-m", "pip", "install", "-r", str(req_file)])


def ensure_env():
    """
    Garantisce che la venv esista e che le dipendenze siano installate.
    Evita errori 'PyQt6 not installed' o file venv mancanti.
    """
    if not VENV_DIR.exists():
        create_venv()
    install_requirements()


def run_spider():
    print("Avvio il ragno...")
    ensure_env()
    spider_py = PROJECT_DIR / "spider.py"
    if not spider_py.exists():
        raise FileNotFoundError(f"File non trovato: {spider_py}")
    subprocess.Popen([str(PYTHON_EXE), str(spider_py)], cwd=str(PROJECT_DIR))


def build_exe():
    print("Costruisco eseguibili con PyInstaller...")
    ensure_env()
    subprocess.check_call([str(PYTHON_EXE), "-m", "pip", "install", "pyinstaller"])

    assets_dir = PROJECT_DIR / "assets"
    if not assets_dir.exists():
        raise FileNotFoundError(f"Directory assets non trovata: {assets_dir}")

    spider_py = PROJECT_DIR / "spider.py"
    if not spider_py.exists():
        raise FileNotFoundError(f"File non trovato: {spider_py}")

    stop_candidates = [PROJECT_DIR / "stop_spider.py", PROJECT_DIR / "stopspider.py"]
    stop_py = next((p for p in stop_candidates if p.exists()), None)
    if stop_py is None:
        raise FileNotFoundError(
            "Nessuno script di stop trovato: atteso stop_spider.py o stopspider.py"
        )

    # PyInstaller: SOURCE<sep>DEST (DEST è la cartella dentro l'eseguibile)
    add_data_arg = f"{assets_dir.resolve()}{ADD_DATA_SEP}assets"

    # spider.exe
    subprocess.check_call(
        [
            str(PYTHON_EXE),
            "-m",
            "PyInstaller",
            "--name",
            "spider",
            "--onefile",
            "--noconsole",
            "--add-data",
            add_data_arg,
            str(spider_py),
        ],
        cwd=str(PROJECT_DIR),
    )

    # stop_spider.exe (senza assets)
    subprocess.check_call(
        [
            str(PYTHON_EXE),
            "-m",
            "PyInstaller",
            "--name",
            "stop_spider",
            "--onefile",
            "--noconsole",
            str(stop_py),
        ],
        cwd=str(PROJECT_DIR),
    )

    print("Fatto. Gli eseguibili sono in dist/.")


def main():
    if len(sys.argv) < 2:
        print(
            "Uso:\n"
            "  python spider_runner.py setup   # crea venv + install\n"
            "  python spider_runner.py run     # lancia il ragno\n"
            "  python spider_runner.py build   # crea eseguibili spider e stop_spider\n"
        )
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "setup":
        create_venv()
        install_requirements()
    elif cmd == "run":
        run_spider()
    elif cmd == "build":
        build_exe()
    else:
        print("Comando sconosciuto:", cmd)


if __name__ == "__main__":
    main()