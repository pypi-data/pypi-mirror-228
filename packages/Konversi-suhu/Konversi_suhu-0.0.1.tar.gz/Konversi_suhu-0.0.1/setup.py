import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "Konversi_suhu",
    version = "0.0.1",
    author = "Kurnia Endah Komalasari",
    author_email = "kurniaendah.ks@gmail.com",
    description = "temperature converter ",
    url = "https://gitlab.com/kurnia_endah/pelatihan_bmkg.git",
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.9",
    install_requires = [
          ]
)