from setuptools import setup, find_packages
import codecs, os

# python setup.py sdist bdist_wheel
# twine upload dist/*

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding='utf-8') as fh:
    LONG_DESCRIPTION = '\n' + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Taiwanese Hokkien Transliterator and Tokeniser'

# Setting up
setup(
    name='taibun',
    version=VERSION,
    author='Andrei Harbachov',
    author_email='andrei.harbachov@gmail.com',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    python_requires='>=3.7',
    packages=find_packages(),
    package_dir={'taibun': 'taibun'},
    package_data={'taibun': ['data/*.json']},
    license='MIT',
    url='https://github.com/andreihar/taibun',
    install_requires=[],
    keywords=['python', 'taiwan', 'taiwanese', 'taigi', 'hokkien', 'romanization', 'transliteration', 'transliterator', "tokenization", "tokenizer"],
    classifiers=[
        'Topic :: Text Processing :: Linguistic',
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)