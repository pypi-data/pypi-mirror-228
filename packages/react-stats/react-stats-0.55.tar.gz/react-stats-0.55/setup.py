from setuptools import setup, find_packages

setup(
    name="react-stats",
    version="0.55",
    packages=find_packages(),
    package_data={
        'react_stats.commands': ['*.json']
    },
    entry_points={
        'console_scripts': [
            'get-stats = react_stats.commands.get_stats:main',
            'make-assets = react_stats.commands.make_assets:main',
            'auto-assets = react_stats.commands.auto_assets:main'
        ],
    },
    install_requires=[
        'tabulate',
        'chardet',
        'pandas',
        'asciibars',
        'watchdog'
    ],
    include_package_data=True
)
