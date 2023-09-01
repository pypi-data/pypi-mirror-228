"""
Description
===========

Initialize a Celery worker or Celery beat for the Flask application.

The `--config` parameter will be parsed, and the yaml contents exported to the Celery app for usage in tasks and beats. The value will be made available in current_app.config["SETTINGS"]. These settings will be available via `flask_gordon.ext.current_settings`. A pytext fixture `current_request` will also be available to handle settings during testing.


Usage
=====

Initializing a Celery worker
----------------------------

Sample :file:`your_package/__init__.py` file:

.. code-block:: python

  #!/usr/bin/env python3

  from flask import Flask
  from flask_gordon.ext import CeleryExt

  flask = Flask(__name__)
  celery = CeleryExt(flask,
      {
          "task_default_queue": "celery.package.queue",
          "task_ignore_result": True,
          "imports": "package.tasks",
      },
  )


Starting a Celery worker
-------------------------

Sample :file:`bin/celery-worker.py` file:

.. code-block:: bash

  #!/usr/bin/env bash

  exec celery -A your_package.celery worker -Q celery.package.queue


Sample Celery shared task
-------------------------

.. code-block:: python

  from celery import shared_task
  from flask import current_app

  def call_example(*args, **kwargs):
      example_task.s(*args, **kwargs).apply_async()

  @shared_task()
  def example_task(*args, **kwargs):
      print(current_app)


Classes
=======

.. autoclass:: CeleryExt
   :members: init_app

"""
import sys
import typing as t

from .._functions import deepmerge
from ..functions import prepare_configuration, read_configuration

try:
    from celery import Celery, Task

    HAS_CELERY = True
except ImportError:
    HAS_CELERY = False


class CeleryExt:
    def __init__(self):
        if not HAS_CELERY:
            raise NotImplementedError("CeleryExt requires celery[redis] package")

    def init_app(
        self,
        app: "Flask",
        configuration=None,
        argv: t.List[str] = None,
        *,
        # borrowed from argparse ext
        cfgfilename=None,
        cfgfilepaths=None,
        default_cfg: t.Dict[str, t.Any] = None,
    ):
        """
        Parameters
        ----------
        app: FlaskApp

            A Flask application.

        configuration: dict

            If a configuration dictionnary is passed, it will be used.
            Otherwise, a configuration will be searched for in app.config["CELERY"].

        """

        # pylint: disable=abstract-method
        class FlaskTask(Task):
            def __call__(self, *args: object, **kwargs: t.Dict[str, t.Any]) -> object:
                with app.app_context():
                    return self.run(*args, **kwargs)

        cfgfilename, cfgfilepaths, defaults = prepare_configuration(cfgfilename, cfgfilepaths, default_cfg)

        # Parse arguments if they exist
        if argv is None:
            argv = sys.argv[1:]

        cfgfile = None
        if "--config" in argv:
            idx = argv.index("--config")
            cfgfile = argv[idx + 1]

        data = read_configuration(cfgfile, cfgfilename, cfgfilepaths)

        # # Merge in the reverse order of priority
        cfg = defaults
        cfg = deepmerge(cfg, data)

        configuration = configuration or {}
        if "celery" in cfg:
            cfg["celery"] = deepmerge(cfg["celery"], configuration)
        else:
            cfg["celery"] = configuration

        app.config["SETTINGS"] = cfg

        # Create a celery application
        celery_app = Celery(app.name, task_cls=FlaskTask)
        celery_app.config_from_object(cfg["celery"])
        celery_app.set_default()

        app.extensions["celery"] = celery_app

        return celery_app
