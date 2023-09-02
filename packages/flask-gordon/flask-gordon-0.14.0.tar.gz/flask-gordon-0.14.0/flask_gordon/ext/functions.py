import typing as t

from torxtools import xdgtools
from torxtools.cfgtools import which
from torxtools.pathtools import expandpath
from yaml import safe_load

from .defaults import CFGFILE_SEARCH_PATHS, make_config


def _read(cfgfile: str) -> t.Dict[str, t.Any]:
    """
    Convenience function in order to be mocked.

    Parameters
    ----------
    cfgfile: str

        a single path representing a yaml file.

    Returns
    -------
    dict:

        a dictionary
    """
    with open(cfgfile, encoding="UTF-8") as fd:
        data = safe_load(fd)
    return data or {}


def prepare_configuration(cfgfilename, cfgfilepaths, default_cfg):
    # Sets environment variables for XDG paths
    xdgtools.setenv()

    # Prepare search path for configuration file. Disable it if we're looking
    # for a impossible (None) file name
    cfgfilename, cfgfilepaths = _prepare_search_paths(cfgfilename, cfgfilepaths)

    # Create a default configuration from what was passed
    # and what we set. Other values are filtered
    defaults = make_config(default_cfg)
    return cfgfilename, cfgfilepaths, defaults


def _prepare_search_paths(cfgfilename, cfgfilepaths):
    # Prepare search path for configuration file. Disable it if we're looking
    # for a impossible (None) file name
    if not cfgfilename:
        cfgfilename = "flask.yml"
    if cfgfilepaths is None:
        cfgfilepaths = CFGFILE_SEARCH_PATHS
    cfgfilepaths = [e.format(cfgfilename=cfgfilename) for e in cfgfilepaths]
    return cfgfilename, cfgfilepaths


def read_configuration(cfgfile, cfgfilename, cfgfilepaths):
    # Search for the configuration file
    if cfgfile is None and cfgfilepaths:
        # Search for cfgfile
        cfgfilepaths = [e.format(cfgfilename=cfgfilename) for e in cfgfilepaths]
        cfgfile = which(cfgfile, expandpath(cfgfilepaths))

    return _read(cfgfile or "/dev/null") or {}
