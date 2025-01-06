from rever.activities.ghrelease import git_archive_asset

from pkg_resources import parse_requirements

$PROJECT = $GITHUB_ORG = $GITHUB_REPO = 'deepsh'
$WEBSITE_URL = 'http://con.sh'
$ACTIVITIES = ['authors', 'version_bump', 'changelog', 'pytest', 'appimage',
               'tag', 'push_tag',
               'ghrelease',
               'sphinx',
               ]
$PYPI_SIGN = False
$PYPI_BUILD_COMMANDS = ("sdist")

$AUTHORS_FILENAME = "AUTHORS.rst"
$VERSION_BUMP_PATTERNS = [
    ('deepsh/__init__.py', r'__version__\s*=.*', '__version__ = "$VERSION"'),
    ]
$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'

$PYTEST_COMMAND = "./run-tests.xsh test"

$TAG_REMOTE = 'git@github.com:deepsh/deepsh.git'
$TAG_TARGET = 'main'

$GHPAGES_REPO = 'git@github.com:deepsh/deepsh-docs.git'

$DOCKER_APT_DEPS = ['man', 'bash-completion']


def get_requirement_args(*extras:str):
    from tomli import loads
    with open("pyproject.toml") as f:
        content = f.read()
    deps = loads(content)['project']['optional-dependencies']
    for ext in extras:
        yield from deps[ext]

pip_deps = list(get_requirement_args('test', 'doc'))
conda_deps = {'prompt_toolkit', 'pip', 'psutil', 'numpy', 'matplotlib'}
$DOCKER_PIP_DEPS = pip_deps
$DOCKER_CONDA_DEPS = sorted(conda_deps)
$DOCKER_INSTALL_COMMAND = ('rm -rf .cache/ __pycache__/ */__pycache__ */*/__pycache__ build/ && '
                           './setup.py install')
$DOCKER_GIT_NAME = 'deepsh'
$DOCKER_GIT_EMAIL = 'deepsh@googlegroups.com'

$GHRELEASE_ASSETS = [git_archive_asset, 'deepsh-x86_64.AppImage']

$APPIMAGE_PYTHON_VERSION = '3.11'
