"""
Description
===========

.. docs/ext/argparse/flask.rst
.. include:: argparse/flask.rst

.. docs/ext/argparse/gunicorn.rst
.. include:: argparse/gunicorn.rst


Usage
=====

.. program:: flask-dev

Initializing a Flask application
--------------------------------

.. code-block:: python

  #!/usr/bin/env python3

  from flask import Flask
  from flask_gordon.ext import ArgParseExt

  flask = Flask(__name__)
  flask = ArgParseExt(flask)

Accessing current settings
--------------------------

Settings are available when an application context is available.

.. code-block:: python

  from flask_gordon.ext import current_settings

  def example():
      print(current_settings)


Mocking current settings
------------------------

.. code-block:: python

  from flask_gordon.ext import current_settings

  def example():
      print(current_settings)


Classes
=======

.. autoclass:: ArgParseExt
   :members: __init__, init_app

"""
import argparse
import os
import sys
import typing as t

from torxtools.argtools import is_not_dir
from torxtools.pathtools import cachedir

from .._functions import deepmerge
from ..functions import prepare_configuration, read_configuration
from .flask import FlaskHelper
from .gunicorn import GunicornHelper


class ArgParseExt:
    def __init__(
        self,
        app: "FlaskApp" = None,
        middleware: str = "gunicorn",
        argv: t.List[str] = None,
        cfgfilename=None,
        cfgfilepaths=None,
        default_cfg: t.Dict[str, t.Any] = None,
        description="Flasket server",
        appname: str = None,
    ):
        """
        Parameters
        ----------
        app: FlaskApp

            A Flask application.

        middleware: str

            Middleware to use: 'gunicorn' for production, 'flask' for debug.

        argv: list[str]

            Uses :code:`sys.argv[1:]` if None. Use :code:`[]` if you desire to deactive argument parsing.

        cfgfilename: str

            Configuration filename to use. Typically this is your packagename with a 'yml' extension.

        cfgfilepaths: str

            Paths to search for in order to find the configuration file. Every value of the list must contain the placeholder '{cfgfilename}' such as :code:`["/home/jdoe/{cfgfilename}"]`

        default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

            Dictionary containing the defaults for the command line arguments and configuration.
            Passed value will be merged with the default factory configuration, command line arguments
            and the configuration file that was read.

        description: str

            Text description to use in argparse.

        appname: str

            Application name. Used to figure out cachepath. Otherwise, defaults to sys.argv[0]
        """
        if app is not None:
            self.init_app(
                app=app,
                argv=argv,
                middleware=middleware,
                cfgfilename=cfgfilename,
                cfgfilepaths=cfgfilepaths,
                default_cfg=default_cfg,
                description=description,
                appname=appname,
            )

    def init_app(
        self,
        app: "Flask",
        middleware: str = "gunicorn",
        argv: t.List[str] = None,
        *,
        cfgfilename=None,
        cfgfilepaths=None,
        default_cfg: t.Dict[str, t.Any] = None,
        description="Flask server",
        appname: str = None,
    ):
        # Verify middleware exists
        middleware = middleware.lower().strip()
        if middleware not in ["flask", "gunicorn"]:
            raise ValueError('middleware argument must be in ["flask", "gunicorn"]')
        if middleware == "flask":
            helper = FlaskHelper()
        if middleware == "gunicorn":
            helper = GunicornHelper()

        # Parse arguments if they exist
        if argv is None:
            argv = sys.argv[1:]
            if appname is None:
                appname = os.path.basename(sys.argv[0])

        cfgfilename, cfgfilepaths, defaults = prepare_configuration(cfgfilename, cfgfilepaths, default_cfg)

        arguments = self._parse_arguments(
            argv=argv,
            cfgfilepaths=cfgfilepaths,
            helper=helper,
            defaults=defaults,
            description=description,
        )

        # Copy arguments over to an dict with server
        arguments = {k: v for k, v in arguments.items() if v is not None}
        cfgfile = arguments.pop("cfgfile", None)
        arguments = {"server": arguments}

        data = read_configuration(cfgfile, cfgfilename, cfgfilepaths)

        # Merge in the reverse order of priority
        cfg = defaults
        cfg = deepmerge(cfg, data)
        cfg = deepmerge(cfg, arguments)
        cfg = helper.force_cfg(cfg)

        app.config["SETTINGS"] = cfg

        # Set cachdir from configuration or default
        path = cfg.get("server", {}).get("cachedir", {})
        app.cachedir = cachedir(appname, path)

        return app

    @staticmethod
    def _parse_arguments(*, argv, cfgfilepaths, helper, defaults, description):
        if not argv:
            return {}

        # argument_default=None does not set the default to None for boolean options,
        # so we'll specifically set default=None for those values
        #
        # Default values aren't actually added/set here, but in the FlasketSettings,
        # We only care about values that were specified.
        parser = argparse.ArgumentParser(
            description=description,
            argument_default=None,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        # Create helptext for UI option
        b_ui = {True: "enabled", False: "disabled"}[defaults["server"]["ui"]]
        if cfgfilepaths:
            # Keep on two lines, otherwise line continuation will make
            # an obsure argparse bug appear
            helpmsg_cfgfile = "Use CFGFILE as configuration file, "
            helpmsg_cfgfile += (
                f"otherwise first file found in search path is used. (default search path: {cfgfilepaths})"
            )
        else:
            helpmsg_cfgfile = "Use CFGFILE as configuration file."

        # fmt: off
        parser.add_argument(
            "-l", "--listen", metavar="HOST",
            help=f'The ip to listen on (default: {defaults["server"]["listen"]})',
        )
        parser.add_argument(
            "-p", "--port", metavar="PORT", type=int,
            help=f'The port to listen on (default: {defaults["server"]["port"]})',
        )
        parser.add_argument(
         "-c", "--cfgfile", metavar="CFGFILE",
           help=helpmsg_cfgfile,
           type=is_not_dir,
        )
        parser.add_argument(
            "--ui", action="store_true", default=None,
            help=f"Enable the OpenAPI UI. Disable with --no-ui. (default: {b_ui})",
        )
        parser.add_argument(
            "--no-ui", action="store_false", default=None, dest="ui",
            help=argparse.SUPPRESS,
        )
        # fmt: on
        helper.add_arguments(defaults["server"], parser)
        args = parser.parse_args(argv)
        return vars(args)
