from setuptools import setup,find_packages
from pathlib import Path

setup(
    name='glauber_video_ferramentas',
    version=1.0,
    description='Este pacote irá fornecer ferramentas de processamento de vídeo',
    long_description=Path('README.md').read_text(),
    author='Glauber',
    author_email='glaubercostaferreira@gmail.com',
    keywords=['camera','video','processamento'],
    packages=find_packages()
)