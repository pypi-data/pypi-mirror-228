import setuptools
import sysadms_sdk


with open('readme.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as req_file:
    requirements = [s for s in [r.replace('\n', '') for r in req_file.readlines()] if s and not s.startswith('-')]

setuptools.setup(
    name='sysadms_sdk',
    verversion=sysadms_sdk.__version__,
    author='Tabby.ai | Sysadms Team',
    description='Sysadms SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package=setuptools.find_packages(exclude=['tests']),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
