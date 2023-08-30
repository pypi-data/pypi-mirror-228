
from setuptools import setup, find_packages

setup(
    name='passwordless-38',
    version='0.0.9',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Bitwarden',
    author_email='hello@bitwarden.com',
    description='A client library for Bitwarden''s Passwordless.dev API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/passwordless_38',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
