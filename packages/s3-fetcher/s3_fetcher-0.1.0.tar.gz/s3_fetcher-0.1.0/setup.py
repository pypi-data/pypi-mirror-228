from setuptools import setup, find_packages

setup(name='s3_fetcher',
      version='0.1.0',
      description='Simplified Command-Line Tool for Fetching Files from Amazon S3',
      author='Kristian Marlowe Ole',
      author_email='kristian.ole@done-data-solutions.com',
      license='GPLv3',
      install_requires=["boto3"],
      entry_points={
            'console_scripts': [
                  's3fetcher = s3_fetcher.cli:main',
            ],
      },
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.5'
)