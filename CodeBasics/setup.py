from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "CodeBasics",
    version = "22.8.12",
    description = "CodeBasics",
    executables = [Executable("main.py", base=base, icon="resources/images/main.ico")]
)
