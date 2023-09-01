from setuptools import setup, find_packages
readme = open("./README.md", "r")

setup(
    name='quese',
    version='0.1.2',
    author="Arnau Canela",
    author_email="arnau.canela22@gmail.com",
    packages=find_packages(),
    description='Package that make easier the searching process in pyhton, through Embeddings and Semantic Similarity',
    long_description=readme.read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=['searching', 'search', 'embeddings', 'intelligent search', 'similarity search', 'embedding search', 'sentence transformer search', 'searcher', 'semantic similarity', 'sentence similarity'],
    install_requires=[
        'sentence_transformers',
    ],
)