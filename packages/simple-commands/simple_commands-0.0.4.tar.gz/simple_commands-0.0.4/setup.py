from setuptools import setup, find_packages

setup(
    name='simple_commands',
    version='0.0.4',
    description='simple_commands',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
'pillow',
'numpy',
'opencv-python',
'tqdm',
'colorama',
'Flask',
]
)
