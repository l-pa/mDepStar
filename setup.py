import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mDepStar",
    version="0.0.1",
    author="Lukas Papik",
    author_email="lukas.papik@vsb.cz",
    description="Mutually Dependent Star method to predict protein complexes from a PPI network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/l-pa/mDepStar",
    project_urls={"Bug Tracker": "https://github.com/l-pa/mDepStar/issues"},
    license="GPL",
    packages=["mdepstar", "mdepstar_analysis"],
    install_requires=["networkx", "tqdm"],
    entry_points={
        "console_scripts": [
            "mdepstar=mdepstar.cli:main",
        ],
    },
)
