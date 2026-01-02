from setuptools import setup, find_packages

setup(
    name="todo-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "todo=todo_cli.main:main",
        ],
    },
)
