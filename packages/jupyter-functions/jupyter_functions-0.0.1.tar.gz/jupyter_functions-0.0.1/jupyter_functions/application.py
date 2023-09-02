from ._version import __version__

import sys
import warnings
from pathlib import Path

from traitlets import Bool, Unicode

from datalayer.application import DatalayerApp, NoStart, base_aliases, base_flags

HERE = Path(__file__).parent


jupyter_functions_aliases = dict(base_aliases)
jupyter_functions_aliases["cloud"] = "JupyterFunctionsApp.cloud"

jupyter_functions_flags = dict(base_flags)
jupyter_functions_flags["dev-build"] = (
    {"JupyterFunctionsApp": {"dev_build": True}},
    "Build in development mode.",
)
jupyter_functions_flags["no-minimize"] = (
    {"JupyterFunctionsApp": {"minimize": False}},
    "Do not minimize a production build.",
)


class ConfigExportApp(DatalayerApp):
    """An application to export the configuration."""

    version = __version__
    description = """
   An application to export the configuration
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for workspace export.")
            self.exit(1)
        self.log.info("JupyterFunctionsConfigApp %s", self.version)


class JupyterFunctionsConfigApp(DatalayerApp):
    """A config app."""

    version = __version__
    description = """
    Manage the configuration
    """

    subcommands = {}
    subcommands["export"] = (
        ConfigExportApp,
        ConfigExportApp.description.splitlines()[0],
    )

    def start(self):
        try:
            super().start()
            self.log.error("One of `export` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)


class JupyterFunctionsShellApp(DatalayerApp):
    """A shell app."""

    version = __version__
    description = """
    Run predefined scripts.
    """

    def start(self):
        super().start()
        args = sys.argv
        self.log.info(args)
            


class JupyterFunctionsApp(DatalayerApp):
    name = "jupyter_functions"
    description = """
    Import or export a JupyterLab workspace or list all the JupyterLab workspaces

    You can use the "config" sub-commands.
    """
    version = __version__

    aliases = jupyter_functions_aliases
    flags = jupyter_functions_flags

    cloud = Unicode("ovh", config=True, help="The app directory to build in")

    minimize = Bool(
        True,
        config=True,
        help="Whether to minimize a production build (defaults to True).",
    )

    subcommands = {
        "config": (JupyterFunctionsConfigApp, JupyterFunctionsConfigApp.description.splitlines()[0]),
        "sh": (JupyterFunctionsShellApp, JupyterFunctionsShellApp.description.splitlines()[0]),
    }

    def initialize(self, argv=None):
        """Subclass because the ExtensionApp.initialize() method does not take arguments"""
        super().initialize()

    def start(self):
        super(JupyterFunctionsApp, self).start()
        self.log.info("JupyterFunctions - Version %s - Cloud %s ", self.version, self.cloud)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = JupyterFunctionsApp.launch_instance

if __name__ == "__main__":
    main()
