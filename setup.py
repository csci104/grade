from setuptools import setup, find_packages

setup(name="curricula",
      version="0.0.1",
      description="A content manager and grading toolkit for evaluating student code",
      url="https://github.com/csci104/curricula",
      author="Noah Kim",
      author_email="noahbkim@gmail.com",
      packages=find_packages(),
      zip_safe=False,
      install_requires=["jinja2", "jsonschema"],
      scripts=["scripts/curricula"])
