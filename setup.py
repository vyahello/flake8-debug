from typing import Sequence

from setuptools import find_packages, setup

from flake8_no_print.meta import Meta


def __load_requirements() -> Sequence[str]:
    """Returns requirements sequence."""
    with open("requirements.txt") as requirements:  # type: IO[str]
        return tuple(map(str.strip, requirements.readlines()))


if __name__ == '__main__':
    setup(
        name=Meta.name,
        version=Meta.version,
        description=Meta.about,
        author=Meta.author,
        author_email=Meta.email,
        url=f'https://github.com/vyahello/{Meta.name}',
        packages=find_packages(
            exclude=('*.tests', '*.tests.*', "tests.*", "tests")
        ),
        entry_points={
            'flake8.extension': [
                'NP = flake8_no_print.plugin:NoPrint',
            ],
        },
        install_requires=__load_requirements(),
        classifiers=[
            'Framework :: Flake8',
            'Environment :: Console',
            'Intended Audience :: Developers',
            f'License :: OSI Approved :: {Meta.license}',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Quality Assurance',
        ],
    )
