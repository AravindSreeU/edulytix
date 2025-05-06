import subprocess
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(base_dir, "edulib")

subprocess.run(["python3", os.path.join(script_dir, "main.py")], check=True)
subprocess.run(["python3", os.path.join(script_dir, "gemini_summary.py")], check=True)
subprocess.run(["python3", os.path.join(script_dir, "compose.py")], check=True)
