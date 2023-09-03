from setuptools import setup, find_packages

setup(name="tydataprep",
      version="0.3",
      description="this contains some kind operations in it.",
      author="shuvam mandal",
      author_email="shuvammandal121@gmail.com",
      packages=["tydataprep"],
      requires=['pandas','datasets','pprint','transformers'],
      )