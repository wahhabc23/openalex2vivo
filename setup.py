from setuptools import setup

setup(
    name='openalex2vivo',
    version='0.1.0',
    url='https://github.com/wahhabc23/openalex2vivo',
    author='Abdul Wahhab',
    author_email='wahhab23@gmail.com',
    py_modules=['openalex2vivo', 'openalex2vivo_loader', 'openalex2vivo_service'],
    packages=['openalex2vivo_app', ],
    scripts=['openalex2vivo.py', 'openalex2vivo_loader.py', 'openalex2vivo_service.py'],
    description="For retrieving data from the OpenAlex API and crosswalking to VIVO-ISF.",
    platforms=['POSIX'],
    test_suite='tests',
    install_requires=['rdflib>=4.2.0',
                      'requests>=2.7.0',
                      'bibtexparser>=0.6.1',
                      'flask>=0.10.1'],
    tests_require=['vcrpy>=1.7.0',
                   'mock>=1.3.0'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Framework :: Flask, FastAPI',
    ],
)
