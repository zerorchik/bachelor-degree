import sys
import os

# Додати корінь проєкту до шляху імпортів
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from interface_recruiter.cli_recruiter import run_recruiter_cli

if __name__ == "__main__":
    run_recruiter_cli()
