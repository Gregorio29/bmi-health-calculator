"""
Build script to compile CALCULADORA_IMC into a standalone Windows executable via PyInstaller.
"""

import subprocess
import sys


def build():
    print("[*] Building standalone executable with PyInstaller...")
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name",
        "CALCULADORA_IMC",
        "main.py"
    ]
    res = subprocess.run(cmd)
    if res.returncode == 0:
        print("[+] Build successful! Output in dist/CALCULADORA_IMC/")
    else:
        print("[-] Build failed.")
        sys.exit(res.returncode)


if __name__ == "__main__":
    build()
