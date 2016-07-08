from setuptools import setup, find_packages

setup(name="iarm",
      version="0.1",
      description="A Jupyter kernel for the ARM instruction set",
      url="https://github.com/DeepHorizons/iarm",
      author="Joshua Milas",
      author_email="josh.milas@gmail.com",
      license='MIT',
      packages=find_packages('.'),
      install_requires=[
          'jupyter'
      ],
      zip_safe=True)
