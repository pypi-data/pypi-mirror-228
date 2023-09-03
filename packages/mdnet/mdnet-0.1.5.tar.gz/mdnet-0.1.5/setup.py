from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mdnet',
    version='0.1.5',
    packages=['mdnet'],
    install_requires=[
        'markdown',
        'jinja2',
        'python-frontmatter'
    ],
    entry_points={
        'console_scripts': [
            'mdnet=mdnet.mdnet:main',
        ],
    },
)
