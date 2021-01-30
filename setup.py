from setuptools import setup
import distutils.command.install_egg_info
import doxgen

class my_egg_info(distutils.command.install_egg_info.install_egg_info):
    """
    Disable egg_info installation, seems pointless for a non-library.
    Copied from virt-manager.
    """
    def run(self):
        pass

setup(
    name='doxgen',
    version=doxgen.__version__,
    url='https://github.com/tieugene/doxgen/',
    license='GPLv3',
    author='TI_Eugene',
    author_email='info@doxgen.ru',
    description='Document generator',
    python_requires='>=3.7',
    keywords="rml html pdf pagetemplate",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    packages=('doxgen',),
    install_requires=[
        'Django',
    ],
    include_package_data=True,
    # use_scm_version=True,
    # setup_requires=['setuptools_scm'],
    cmdclass={
    'install_egg_info': my_egg_info,
    },
)
