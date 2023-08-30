from setuptools import setup, find_packages


setup(
    name="MyPakage",
    version="0.2.6",
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的库所需的其他Python包
        'setuptools',
        'numpy~=1.25.2',
        'imageio~=2.31.1',
        'Pillow~=10.0.0',
        'geographiclib~=2.0',
        'geopy'
    ],

    author="nwkami",
    author_email="your.email@example.com",
    description="this code is used for my learning, because other wheels are not enough or perfect author:nwkami",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    # py_modules=['MyPakage.py'],
    license="MIT",
    url="https://github.com/yourusername/my-awesome-package",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
