# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Kernel spec for Spyder kernels
"""

# Standard library imports
import logging
import os
import os.path as osp
import sys

# Third party imports
from jupyter_client.kernelspec import KernelSpec

# Local imports
from spyder.api.config.mixins import SpyderConfigurationAccessor
from spyder.config.base import (get_safe_mode, is_pynsist, running_in_mac_app,
                                running_under_pytest)
from spyder.utils.conda import (add_quotes, get_conda_activation_script,
                                get_conda_env_path, is_conda_env)
from spyder.utils.environ import clean_env
from spyder.utils.misc import get_python_executable
from spyder.utils.programs import is_python_interpreter

# Constants
HERE = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger(__name__)


def is_different_interpreter(pyexec):
    """Check that pyexec is a different interpreter from sys.executable."""
    executable_validation = osp.basename(pyexec).startswith('python')
    directory_validation = osp.dirname(pyexec) != osp.dirname(sys.executable)
    return directory_validation and executable_validation


def get_activation_script(quote=False):
    """
    Return path for bash/batch conda activation script to run spyder-kernels.

    If `quote` is True, then quotes are added if spaces are found in the path.
    """
    scripts_folder_path = os.path.join(os.path.dirname(HERE), 'scripts')
    if os.name == 'nt':
        script = 'conda-activate.bat'
    else:
        script = 'conda-activate.sh'

    script_path = os.path.join(scripts_folder_path, script)

    if quote:
        script_path = add_quotes(script_path)

    return script_path


HERE = osp.dirname(os.path.realpath(__file__))


class SpyderKernelSpec(KernelSpec, SpyderConfigurationAccessor):
    """Kernel spec for Spyder kernels"""

    CONF_SECTION = 'ipython_console'

    def __init__(self, is_cython=False, is_pylab=False,
                 is_sympy=False, **kwargs):
        super(SpyderKernelSpec, self).__init__(**kwargs)
        self.is_cython = is_cython
        self.is_pylab = is_pylab
        self.is_sympy = is_sympy

        self.display_name = 'Python 3 (Spyder)'
        self.language = 'python3'
        self.resource_dir = ''

    @property
    def argv(self):
        """Command to start kernels"""
        # Python interpreter used to start kernels
        if self.get_conf('default', section='main_interpreter'):
            pyexec = get_python_executable()
        else:
            pyexec = self.get_conf('executable', section='main_interpreter')
            if not is_python_interpreter(pyexec):
                pyexec = get_python_executable()
                self.set_conf('executable', '', section='main_interpreter')
                self.set_conf('default', True, section='main_interpreter')
                self.set_conf('custom', False, section='main_interpreter')

        # Part of spyder-ide/spyder#11819
        is_different = is_different_interpreter(pyexec)

        # Command used to start kernels
        if is_different and is_conda_env(pyexec=pyexec):
            # If this is a conda environment we need to call an intermediate
            # activation script to correctly activate the spyder-kernel

            # If changes are needed on this section make sure you also update
            # the activation scripts at spyder/plugins/ipythonconsole/scripts/
            kernel_cmd = [
                get_activation_script(),  # This is bundled with Spyder
                get_conda_activation_script(),
                get_conda_env_path(pyexec),  # Might be external
                pyexec,
                '{connection_file}',
            ]
        else:
            kernel_cmd = [
                pyexec,
                # This is necessary to avoid a spurious message on Windows.
                # Fixes spyder-ide/spyder#20800.
                '-Xfrozen_modules=off',
                '-m',
                'spyder_kernels.console',
                '-f',
                '{connection_file}'
            ]
        logger.info('Kernel command: {}'.format(kernel_cmd))

        return kernel_cmd

    @property
    def env(self):
        """Env vars for kernels"""
        default_interpreter = self.get_conf(
            'default', section='main_interpreter')
        env_vars = os.environ.copy()

        # Avoid IPython adding the virtualenv on which Spyder is running
        # to the kernel sys.path
        env_vars.pop('VIRTUAL_ENV', None)

        # Do not pass PYTHONPATH to kernels directly, spyder-ide/spyder#13519
        env_vars.pop('PYTHONPATH', None)

        # List of paths declared by the user, plus project's path, to
        # add to PYTHONPATH
        pathlist = self.get_conf(
            'spyder_pythonpath', default=[], section='pythonpath_manager')
        pypath = os.pathsep.join(pathlist)

        # List of modules to exclude from our UMR
        umr_namelist = self.get_conf(
            'umr/namelist', section='main_interpreter')

        # Environment variables that we need to pass to the kernel
        env_vars.update({
            'SPY_EXTERNAL_INTERPRETER': not default_interpreter,
            'SPY_UMR_ENABLED': self.get_conf(
                'umr/enabled', section='main_interpreter'),
            'SPY_UMR_VERBOSE': self.get_conf(
                'umr/verbose', section='main_interpreter'),
            'SPY_UMR_NAMELIST': ','.join(umr_namelist),
            'SPY_RUN_LINES_O': self.get_conf('startup/run_lines'),
            'SPY_PYLAB_O': self.get_conf('pylab'),
            'SPY_BACKEND_O': self.get_conf('pylab/backend'),
            'SPY_AUTOLOAD_PYLAB_O': self.get_conf('pylab/autoload'),
            'SPY_FORMAT_O': self.get_conf('pylab/inline/figure_format'),
            'SPY_BBOX_INCHES_O': self.get_conf('pylab/inline/bbox_inches'),
            'SPY_RESOLUTION_O': self.get_conf('pylab/inline/resolution'),
            'SPY_WIDTH_O': self.get_conf('pylab/inline/width'),
            'SPY_HEIGHT_O': self.get_conf('pylab/inline/height'),
            'SPY_USE_FILE_O': self.get_conf('startup/use_run_file'),
            'SPY_RUN_FILE_O': self.get_conf('startup/run_file'),
            'SPY_AUTOCALL_O': self.get_conf('autocall'),
            'SPY_GREEDY_O': self.get_conf('greedy_completer'),
            'SPY_JEDI_O': self.get_conf('jedi_completer'),
            'SPY_SYMPY_O': self.get_conf('symbolic_math'),
            'SPY_TESTING': running_under_pytest() or get_safe_mode(),
            'SPY_HIDE_CMD': self.get_conf('hide_cmd_windows'),
            'SPY_PYTHONPATH': pypath
        })

        if self.is_pylab is True:
            env_vars['SPY_AUTOLOAD_PYLAB_O'] = True
            env_vars['SPY_SYMPY_O'] = False
            env_vars['SPY_RUN_CYTHON'] = False
        if self.is_sympy is True:
            env_vars['SPY_AUTOLOAD_PYLAB_O'] = False
            env_vars['SPY_SYMPY_O'] = True
            env_vars['SPY_RUN_CYTHON'] = False
        if self.is_cython is True:
            env_vars['SPY_AUTOLOAD_PYLAB_O'] = False
            env_vars['SPY_SYMPY_O'] = False
            env_vars['SPY_RUN_CYTHON'] = True

        # App considerations
        if (running_in_mac_app() or is_pynsist()):
            if default_interpreter:
                # See spyder-ide/spyder#16927
                # See spyder-ide/spyder#16828
                # See spyder-ide/spyder#17552
                env_vars['PYDEVD_DISABLE_FILE_VALIDATION'] = 1
            else:
                env_vars.pop('PYTHONHOME', None)

        # Remove this variable because it prevents starting kernels for
        # external interpreters when present.
        # Fixes spyder-ide/spyder#13252
        env_vars.pop('PYTHONEXECUTABLE', None)

        # Making all env_vars strings
        clean_env_vars = clean_env(env_vars)

        return clean_env_vars
