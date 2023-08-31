from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='HPrIm',
    version='0.1',
    description='Herramientas para el Procesamiento de Imágenes',
    author='Nakato',
    author_email='nnakato150@gmail.com',
    long_description_content_type="text/markdown",
    long_description=readme,
    requires=['numpy'],
    install_requires=['numpy'],
    url='https://github.com/nakato156/HPrIm',
    packages=find_packages(),
    keywords=['file', 'files', 'text'],
)

