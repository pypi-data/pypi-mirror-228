from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Elemental Engine - for internal API development'
LONG_DESCRIPTION = ''

setup(
    name="elemental_engine",
    version=VERSION,
    author="Elemental (Tom Neto)",
    author_email="<info@elemental.run>",
    description=DESCRIPTION,
    url='https://github.com/tomneto/ElementalEngine.git',
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    include_dirs=['elemental_engine'],
    install_requires=['pymongo', 'certifi', 'python-dotenv', 'uvicorn'],
    keywords=['python', 'api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    zip_safe=False,
    python_requires='>=3.8'
)