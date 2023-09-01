from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3'
]

setup(
    name='clean_excel',
    version='1.0.0',
    description='Parse and filter any chaotic excel sheet into a formatted numpy array or pandas dataframe.',
    long_description='More information available at https://github.com/TimoKats/CleanExcel',
    url='',  
    author='Timo Kats',
    author_email='tpakats@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='excel', 
    packages=['cleanexcel'],
    install_requires=['openpyxl'] 
)