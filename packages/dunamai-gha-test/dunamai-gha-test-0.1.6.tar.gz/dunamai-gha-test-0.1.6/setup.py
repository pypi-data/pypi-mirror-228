from setuptools import setup
from dunamai import Version, Style

setup(
    name="dunamai-gha-test",
    version=Version.from_git().serialize(metadata=False, style=Style.SemVer),
)