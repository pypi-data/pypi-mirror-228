from pkg_resources import DistributionNotFound, get_distribution

from python_anvil_encryption import cli, encryption

try:
    __version__ = get_distribution("python_anvil").version
except DistributionNotFound:
    __version__ = "(local)"
