from setuptools import setup


setup(
    name='search-terminal',
    version='0.0.1',
    author="Babalo Majiyezi",
    author_email="raymondbabalo5@gmail.com",
    description="This is a program that allows you to search the web from the comfort of your terminal.",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    packages=["search_package"], 
    url="https://github.com/Dr-GameDev/Google-Search_Package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'go-search = search_package.search:main', 
        ],
    },
)
