import os
import sys

from setuptools import setup, find_packages
from pip.req import parse_requirements


def test_python_version():
    if float("%d.%d" % sys.version_info[:2]) < 2.6:
        print('Your Python version {0}.{1}.{2} is not supported.'.format(
            *sys.version_info[:3]))
        print('stackdio requires Python 2.6 or newer.')
        sys.exit(1)


def load_pip_requirements(fp):
    reqs, deps = [], []
    for r in parse_requirements(fp):
        if r.url is not None:
            deps.append(str(r.url))
        reqs.append(str(r.req))
    return reqs, deps

# Set version
__version__ = '0.0.0' # Explicit default
execfile("stackdio/client/version.py")


SHORT_DESCRIPTION = ('A cloud deployment, automation, and orchestration '
                     'platform for everyone.')
LONG_DESCRIPTION = SHORT_DESCRIPTION

# If we have a README.md file, use its contents as the long description
if os.path.isfile('README.md'):
    with open('README.md') as f:
        LONG_DESCRIPTION = f.read()


if __name__ == "__main__":
    # build our list of requirements and dependency links based on our
    # requirements.txt file
    reqs, deps = load_pip_requirements('requirements.txt')

    # Call the setup method from setuptools that does all the heavy lifting
    # of packaging stackdio
    setup(
        name='stackdio',
        version=__version__,
        url='http://stackd.io',
        author='Digital Reasoning Systems, Inc.',
        author_email='info@stackd.io',
        description=SHORT_DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license='Apache 2.0',
        include_package_data=True,
        packages=find_packages(),
        zip_safe=False,
        install_requires=reqs,
        dependency_links=deps,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: System :: Clustering',
            'Topic :: System :: Distributed Computing',
        ]
    )
