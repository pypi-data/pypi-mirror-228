from setuptools import setup, find_packages

setup(
    name='element_python_package',
    version='0.2.7',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'seaborn',
        'matplotlib',
        'pandas',
    ],
    author='Sharadind Peddiraju',
    author_email='sharadind.pv@gmail.com',
    description='A simple example package',
)