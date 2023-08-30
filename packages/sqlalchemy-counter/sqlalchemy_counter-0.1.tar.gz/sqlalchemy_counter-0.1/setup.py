from distutils.core import setup

setup(
    name="sqlalchemy_counter",
    packages=["sqlalchemy_counter"],
    version="0.1",
    license="MIT",
    description="A simple tool for counting and printing database queries when using SLQAlchemy",
    author="Luis Garcia",
    author_email="luisgc93@gmail.com",
    url="https://github.com/luisgc93/sqlalchemy-counter/",
    download_url="https://github.com/user/reponame/archive/v_01.tar.gz",
    keywords=[
        "query",
        "db",
        "debug",
    ],
    install_requires=[
        "sqlalchemy",
        "pytest",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.11',
    ],
)
