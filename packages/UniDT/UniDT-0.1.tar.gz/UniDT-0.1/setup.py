from setuptools import setup

setup(
    name='UniDT',
    version='0.1',
    py_modules=['UniDT'],
    install_requires=[
        'requests',
        'numpy',
        'transformers'
    ],
    entry_points={
        'console_scripts': [
            'my_script=unidt:main',
        ],
    },
    author='xuli.shen',
    author_email='xuli.shen@unidt.com',
    description='This is the repo of UniDT 1+X Plateform.',
    license='MIT',
    keywords='UniDT 1+X',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
