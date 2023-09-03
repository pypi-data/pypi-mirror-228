import os
from typing import Optional
import typer
import requests


app = typer.Typer()


class Temet:
    def __init__(
            self, 
            venv_name:Optional[str]=".venv",
            project_name:Optional[str]="core",
            superuser:Optional[str]="admin"
            ) -> None:
        self.venv_name = venv_name
        self.project_name = project_name
        self.superuser = superuser
        self.cwd = self.__get_current_dir()

    def __repr__(self) -> str:      
        return f"Temet(venv_name={self.venv_name}, project_name={self.project_name}, superuser={self.superuser})"

    def __get_current_dir(self):
        """Get the current directory."""
        return os.getcwd()

    def check_for_empty_dir(self):
        """Check if the directory is empty."""
        if os.listdir(self.cwd):
            print("Directory is not empty.")

    def create_venv(self):
        """Create a virtual environment."""
        os.chdir(self.cwd)
        os.system(f"python -m venv {self.venv_name}")
        print("Virtual environment created.")
        #self.__activate_venv()

    def create_requirements(self):
        """Create a requirements.txt file."""
        if os.path.exists("requirements.txt"):
            print("requirements.txt already exists.")
        else:
            with open("requirements.txt", "w") as f:
                f.write("django\n")
            self.install_requirements()

    def update_pip(self):
        """Update pip to the latest version."""
        if os.name == "nt":
            os.system(f"{self.cwd}\\{self.venv_name}\\Scripts\\python.exe -m pip install --upgrade pip")
        else:
            os.system(f"{self.cwd}/{self.venv_name}/bin/python -m pip install --upgrade pip")


    def install_requirements(self):
        """Install requirements.txt."""
        if os.name == "nt":
            os.system(f"{self.cwd}\\{self.venv_name}\\Scripts\\pip.exe install -r requirements.txt")
        else:
            os.system(f"source {self.cwd}/{self.venv_name}/bin/pip install -r requirements.txt")

    def create_gitignore(self):
        """Create a python .gitignore file."""
        gitignore = requests.get("https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore")
        with open(".gitignore", "w") as f:
            f.write(gitignore.text)

    def create_django_project(self):
        """Create a django project."""
        if os.name == "nt":
            os.system(f"{self.cwd}\\{self.venv_name}\\Scripts\\django-admin.exe startproject {self.project_name} .")
            print("Django project created.")
        else:
            os.system(f"{self.cwd}/{self.venv_name}/bin/django-admin startproject {self.project_name} .")
            print("Django project created.")

    def migrate(self):
        """Migrate the database."""
        if os.name == "nt":
            os.system(f"{self.cwd}\\{self.venv_name}\\Scripts\\python.exe .\\manage.py migrate")
        else:
            os.system(f"{self.cwd}/{self.venv_name}/bin/python ./manage.py migrate")

    def create_superuser(self):
        """Create a superuser."""
        if os.name == "nt":
            os.system(f"{self.cwd}\\{self.venv_name}\\Scripts\\python.exe .\\manage.py createsuperuser --username {self.superuser}")
        else:
            os.system(f"{self.cwd}/{self.venv_name}/bin/python ./manage.py createsuperuser --username {self.superuser}")

temet = Temet()

@app.command()
def main(
    init:str,
    project_name:Optional[str]="core",
    venv_name:Optional[str]=".venv",
    superuser:Optional[str]="admin"
        ):
    """Create a django project."""
    if init == "init":
        print("Creating django project...")
        temet.venv_name = venv_name
        temet.project_name = project_name
        temet.superuser = superuser
        temet.check_for_empty_dir()
        temet.create_venv()
        temet.create_requirements()
        temet.create_gitignore()
        temet.create_django_project()
        temet.migrate()
        temet.create_superuser()


if __name__ == "__main__":
    app()
