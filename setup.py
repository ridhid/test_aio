import os
import re

import pkg_resources
from pkg_resources import parse_requirements
from setuptools import find_packages, setup

app_name = 'test_aio'
base_path = os.path.dirname(__file__)

with open(os.path.join(base_path, 'README.MD')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

packages = find_packages()


def get_reqs(lines):
    return [str(r) for r in parse_requirements(lines)]


base_pattern = re.compile("-r (.+)")
git_pattern = re.compile("-i (.+)")


def get_requirements(req_path, excludes=None):
    if excludes is None:
        excludes = []
    excludes = set(excludes)
    reqs = set()
    dir_name = os.path.dirname(req_path)
    with open(req_path) as requirements:
        for line in requirements.readlines():
            if git_pattern.match(line):
                continue
            match = base_pattern.match(line)
            if match:
                reqs.update(get_requirements(os.path.join(dir_name, match.group(1)), excludes))
                continue
            line = line.rstrip()
            if line not in excludes:
                reqs.add(line)
    return reqs


exclude_packages = []
reqs = get_requirements(os.path.join(base_path, 'config/base/requirements.txt'), exclude_packages)
reqs.update(get_requirements(os.path.join(base_path, 'config/prod/requirements.txt'), exclude_packages))
reqs = list(reqs)


def get_package_name(req_name):
    discr = pkg_resources.get_distribution(req_name)
    top_level = open(discr._provider.egg_info + '/top_level.txt')
    return top_level.readline().rstrip(), discr.location


version = '1.0.0'

setup_cnf = {
    'name': app_name,
    'version': version,
    'python_requires': '>=3.7',
    'packages': packages,
    'include_package_data': True,
    'long_description': README,
    'entry_points': {
        'console_scripts': [
            f'run_{app_name}=app.utils.start_gunicorn:runserver',
            'load_rates=app.utils.load.load_rates:load',
        ],
    },
}

setup(**setup_cnf, install_requires=reqs)
