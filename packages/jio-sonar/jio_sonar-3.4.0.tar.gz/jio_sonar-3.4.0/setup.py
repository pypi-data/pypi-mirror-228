from setuptools import setup, find_packages

setup(
    name='jio_sonar',
    version='3.4.0',
    description='maronette',
    long_description='marionetetee client',
    license='MIT',
    packages=find_packages(),
    author='shayan',
    author_email='syedshayan109@gmail.com',
    install_requires=['mozrunner==8.3.0',
                      'mozversion==2.4.0',
                      'six==1.16.0',
                      'future==0.18.3',
                      'manifestparser==2.1.0'],
    keywords=['jsonar', 'jio_sonar'],
    download_url='https://pypi.org/project/jio_sonar/'
)

