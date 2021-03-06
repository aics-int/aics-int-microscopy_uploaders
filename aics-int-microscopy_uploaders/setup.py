from setuptools import setup, find_packages


#######################################################################################################################
from wheel.bdist_wheel import bdist_wheel


class BDistWheelBranch(bdist_wheel):
    """
    This class extends bdist_wheel to allow generating feature specific artifacts.

    E.g. if the branch is feature/some-new-idea, then the command line
    > python setup.py bdist_wheel --feature-name=feature/some-new-idea
    will generate
        ./dist/aics-int-microscopy_uploaders-<version>.dev<#>.feature_some_new_idea-<python-versions>-<arch>.whl

    Note that this will work with whatever string is provided. The associated Jenkinsfile
    will provide the feature branch name
    """

    user_options = bdist_wheel.user_options + [("branch-name=", None, "The branch name, e.g. feature/x-y-z, bugfix/a-b-c")]

    def initialize_options(self):
        super().initialize_options()
        self.branch_name: str = None

    def finalize_options(self):
        if self.branch_name:
            for s in ['-', '.', '/']:
                self.branch_name = self.branch_name.replace(s, '_')
            print(f"Using feature name = {self.branch_name}")
            # NOTE: monkey patching bdist_wheel.distribution.get_version()
            self.original_version = self.distribution.get_version()
            self.distribution.get_version = self.get_version_with_feature
        super().finalize_options()

    def get_version_with_feature(self):
        return f"{self.original_version}.{self.branch_name}"


#######################################################################################################################


"""
Notes:
MODULE_VERSION is read from aics-int-microscopy_uploaders/version.py.
See (3) in following link to read about versions from a single source
https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
"""
MODULE_VERSION = ""
PACKAGE_NAME = 'aics-int-microscopy_uploaders'
exec(open(PACKAGE_NAME + "/version.py").read())


def readme():
    with open('README.md') as f:
        return f.read()


test_deps = ['pytest', 'pytest-cov', 'pytest-raises', 'pytest-runner']

lint_deps = ['flake8']
interactive_dev_deps = [
    # -- Add libraries/modules you want to use for interactive
    # -- testing below (e.g. jupyter notebook).
    # -- E.g.
    # 'matplotlib>=2.2.3',
    # 'jupyter',
    # 'itkwidgets==0.12.2',
    # 'ipython==7.0.1',
    # 'ipywidgets==7.4.1'
]
all_deps = [*test_deps, *lint_deps, *interactive_dev_deps]

extras = {
    'test': test_deps,
    'lint': lint_deps,
    'interactive_dev': interactive_dev_deps,
    # These are for legacy compatibility with the gradle build setup
    'test_group': test_deps,
    'lint_group': lint_deps,
    'interactive_dev_group': interactive_dev_deps,
    'all': all_deps
}

setup(cmdclass={'bdist_wheel': BDistWheelBranch},
      name=PACKAGE_NAME,
      version=MODULE_VERSION,
      description='repo of microscopy uploaders',
      long_description=readme(),
      author='Brian Whitney',
      author_email='brian.whitney@alleninstitute.org',
      license='Allen Institute Software License',
      packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
      entry_points={
          "console_scripts": [
              "my_example={}.bin.my_example:main".format(PACKAGE_NAME)
          ]
      },
      install_requires=[
          # List of modules required to use/run this module.
          # -- E.g.
          # 'numpy>=1.15.1',
          # 'requests'
      ],

      # For test setup. This will allow JUnit XML output for Jenkins
      setup_requires=[],
      tests_require=test_deps,

      extras_require=extras,
      zip_safe=False
      )
