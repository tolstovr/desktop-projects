from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "MathBasics",
    version = "22.2.11",
    description = "MathBasics",
    executables = [Executable("main.py", base=base, icon="assets/img/favicon.ico")]
)