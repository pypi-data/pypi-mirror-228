from setuptools import setup

setup(
    name='weather_app_mehdirazajaffri',
    version='1.0.2',
    description='Weather App Cli Tool',
    author='Mehdi Raza',
    author_email="mehdirazajaffri@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10", 
    ],
    long_description="Weather App",
    packages=["weather_app"],
    download_url="https://github.com/mehdirazajaffri/weather_app/archive/refs/tags/1.0.2.tar.gz",
    include_package_data=True,
    entry_points= {
        "console_scripts": [
            "weather_app = weather_app.main:main",
        ],
    },
    install_requires=[
        'requests',
        'argparse',
        'pytest'
    ],
    python_requires='>=3.6'
)