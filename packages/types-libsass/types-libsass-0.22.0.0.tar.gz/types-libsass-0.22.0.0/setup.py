from setuptools import setup

name = "types-libsass"
description = "Typing stubs for libsass"
long_description = '''
## Typing stubs for libsass

This is a PEP 561 type stub package for the `libsass` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`libsass`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/libsass. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `9552ec7f72f3190eb529aec096783c624b43bd29` and was tested
with mypy 1.5.1, pyright 1.1.325, and
pytype 2023.8.14.
'''.lstrip()

setup(name=name,
      version="0.22.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/libsass.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-setuptools'],
      packages=['sassutils-stubs', 'sass-stubs'],
      package_data={'sassutils-stubs': ['__init__.pyi', 'builder.pyi', 'distutils.pyi', 'wsgi.pyi', 'METADATA.toml'], 'sass-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
