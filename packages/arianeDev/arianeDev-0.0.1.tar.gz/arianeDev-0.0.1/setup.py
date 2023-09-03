from setuptools import setup, find_packages

setup(
    name='arianeDev',
    version='0.0.1',
    description='arianeDev',
    author='alandevcol',
    author_email='alandevcol@gmail.com',
    url='https://github.com/alandevcol/arianeDevs',
    packages=find_packages(),
    install_requires=[
        "pydantic==2.3.0"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
