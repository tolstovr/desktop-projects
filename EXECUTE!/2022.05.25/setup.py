from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "EXECUTE!",
    version = "22.5.25",
    description = "EXECUTE!",
    executables = [Executable("main.py", base=base, icon="assets/images/favicon.ico")]
)
