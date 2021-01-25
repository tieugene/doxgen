from setuptools import setup

setup(
    name='doxgen',
    version='0.1.0',
    packages=['src', 'src.dox', 'src.dox.ref', 'src.dox.tpl', 'src.dox.migrations', 'src.dox.templatetags'],
    url='https://github.com/tieugene/doxgen/',
    license='GPLv3',
    author='TI_Eugene',
    author_email='info@doxgen.ru',
    description='Document generator'
)
