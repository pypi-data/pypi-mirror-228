from setuptools import setup

name = "types-mock"
description = "Typing stubs for mock"
long_description = '''
## Typing stubs for mock

This is a PEP 561 type stub package for the `mock` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`mock`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/mock. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `d13d9859f64dbb7fee93707859a0854612a30fd2` and was tested
with mypy 1.5.1, pyright 1.1.325, and
pytype 2023.8.14.
'''.lstrip()

setup(name=name,
      version="5.1.0.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/mock.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['mock-stubs'],
      package_data={'mock-stubs': ['__init__.pyi', 'backports.pyi', 'mock.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
