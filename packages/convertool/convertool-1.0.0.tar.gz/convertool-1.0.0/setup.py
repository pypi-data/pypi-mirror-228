from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='convertool',
    version='1.0.0',
    author='Lee Seonghyun',
    author_email='john.doe@foo.com',
    license='<the license you chose>',
    description='<short description for the tool>',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['my_tool', 'app'],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        convertool=my_tool:cli
    '''
)
