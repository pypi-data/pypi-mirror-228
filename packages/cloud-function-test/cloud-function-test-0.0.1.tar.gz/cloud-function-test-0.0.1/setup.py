from setuptools import setup


name = "cloud-function-test"
version = "0.0.1"

setup(
    name=name,
    version=version,
    packages=["cloud_function_test"],
    license='apache-2.0',
    description="Test locally GCP Cloud Functions",
    url=f"https://github.com/RobinPicard/{name}",
    author='Robin Picard',
    author_email='robin.picard@sciencespo.fr',
    install_requires=[
        'functions-framework',
        'requests',
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'cloud-function-test=cloud_function_test.cli:main',
        ],
    },
    keywords=[
        "python",
        "testing",
        "tests",
        "gcp",
        "cloud functions",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
    ],
)
