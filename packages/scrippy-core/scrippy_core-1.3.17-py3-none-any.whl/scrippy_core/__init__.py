"""Scrippy Core module."""


import os
import grp
import pwd
import time
import yaml
import logging
from scrippy_core.conf import Config
from scrippy_core import error_handler
from scrippy_core.history import History
from scrippy_core.arguments import Parser
from scrippy_core.workspace import Workspace
from scrippy_core.context import Context, PIDStack
from scrippy_core.log.debuglogger import DebugLogger
from scrippy_core.log import LogConfig, setLoggerClass
from scrippy_core.error_handler import ScrippyCoreError


def check_users(context):
  """
  Checks if the current user is authorized to execute the script by comparing the "@user" declarations in the script's header.

  Raises a ScrippyCoreError if the user is not authorized.
  """
  user_id = os.geteuid()
  try:
    users = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@user")]
    users = [pwd.getpwnam(user).pw_uid for user in users]
    if len(users) > 0 and user_id not in users:
      raise ScrippyCoreError('[BadUserError] Unauthorized user')
  except KeyError as err:
    raise ScrippyCoreError(f"[UnknownUserError] Unknown user: {str(err)}") from err
  except Exception as err:
    err_msg = f"[{err.__class__.__name__}] {err}"
    logging.critical(err_msg)
    raise ScrippyCoreError(err_msg) from err


def check_groups(context):
  """
  Verifies that the current user is authorized to execute the script by comparing the "@group" declarations in the script's header.

  Raises a ScrippyCoreError if the user is not part of the authorized groups.
  """
  user_groups = os.getgroups()
  try:
    groups = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@group")]
    groups = [grp.getgrnam(group)[2] for group in groups]
    if len(groups) > 0:
      if not len([groups for g in user_groups if g in groups]) > 0:
        raise ScrippyCoreError("[BadGroupError] User is not member of an authorized group")
  except KeyError as err:
    raise ScrippyCoreError(f"[UnknownGroupError] Unknown group: {str(err)}") from err
  except Exception as err:
    err_msg = f"[{err.__class__.__name__}] {err}"
    logging.critical(err_msg)
    raise ScrippyCoreError(err_msg) from err


def check_instances(context):
  """
  Verifies that the maximum number of allowed instances to be simultaneously executed is not reached by comparing the declaration @max_instance in the script's header with the number of PIDs returned by the pidstack.

  If the maximum instance limit is reached, the script will pause until the number of currently running instances is lower than the allowed number of instances.

  When the maximum allowed instances are not reached, the script registers itself in the pidstack and proceeds with execution.
  """
  sleep_step = 3
  bools = ["true", "1", "on"]
  try:
    max_instance = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@max_instance")][0]
  except IndexError:
    max_instance = 0
  try:
    timeout = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@timeout")][0]
  except IndexError:
    timeout = 0
  try:
    exit_on_wait = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@exit_on_wait")][0]
  except IndexError:
    exit_on_wait = "False"
  try:
    exit_on_timeout = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@exit_on_timeout")][0]
  except IndexError:
    exit_on_timeout = "False"
  pids = context.pidstack.get_pids()
  try:
    timeout = int(timeout)
    max_instance = int(max_instance)
    exit_on_timeout = exit_on_timeout.lower() in bools
    exit_on_wait = exit_on_wait.lower() in bools
    if max_instance > 0 and len(pids) > max_instance:
      logging.info(f"[+] Waiting for an execution slot: {len(pids)}/{max_instance} [{timeout}s]")
      while len(pids) > max_instance and pids[0] != os.getpid():
        timeout -= sleep_step
        if timeout <= 0 and exit_on_timeout:
          raise Exception("TimeoutError: Timeout expired")
        if exit_on_wait:
          raise Exception(f"EagernessError: `exit_on_wait` is set to {exit_on_wait}")
        pids = context.pidstack.get_pids()
        time.sleep(sleep_step)
  except Exception as err:
    err_msg = f"[{err.__class__.__name__}] {err}"
    logging.critical(err_msg)
    raise ScrippyCoreError(err_msg) from err


# ------------------------------------------------------------------------------
# INITIALIZATION
# ------------------------------------------------------------------------------
conf_files = ["/etc/scrippy/scrippy.yml",
              os.path.expanduser("~/.config/scrippy/scrippy.yml"),
              "/usr/local/etc/scrippy/scrippy.yml"]

for conf_file in conf_files:
  if os.path.isfile(conf_file):
    with open(conf_file, mode="r", encoding="utf-8") as conf_file:
      scrippy_conf = yaml.load(conf_file, Loader=yaml.FullLoader)
      SCRIPPY_LOGDIR = scrippy_conf.get("env").get("logdir")
      SCRIPPY_HISTDIR = scrippy_conf.get("env").get("histdir")
      SCRIPPY_REPORTDIR = scrippy_conf.get("env").get("reportdir")
      SCRIPPY_TMPDIR = scrippy_conf.get("env").get("tmpdir")
      SCRIPPY_DATADIR = scrippy_conf.get("env").get("datadir")
      SCRIPPY_TEMPLATEDIR = scrippy_conf.get("env").get("templatedir")
      SCRIPPY_CONFDIR = scrippy_conf.get("env").get("confdir")

conf_keys = [SCRIPPY_LOGDIR,
             SCRIPPY_HISTDIR,
             SCRIPPY_REPORTDIR,
             SCRIPPY_TMPDIR,
             SCRIPPY_DATADIR,
             SCRIPPY_TEMPLATEDIR,
             SCRIPPY_CONFDIR]

for conf_key in conf_keys:
  if conf_key is None:
    raise ScrippyCoreError(f"Missing configuration key: {conf_key}")

LogConfig.default_configuration()
arg_parser = Parser()
args = arg_parser.args
LOG_FILE_ENABLED = True

if args.nolog:
  logging.getLogger().setLevel(logging.ERROR)

if args.debug:
  logging.warning("[+] Option --debug is set -> Logging level is now immutable")
  logging.getLogger().setLevel(logging.DEBUG)
  setLoggerClass(DebugLogger)

logging.debug(f"[+] Arguments : {vars(args)}")

if args.no_log_file:
  LOG_FILE_ENABLED = False
  logging.warning("[+] Option --no-log-file is set -> This session will not be logged nor recorder into history")

# Root Configuration file loading and checking
root_config = Config()

if root_config.has('log', 'level'):
  logging.info(f"[!] Logging configuration: {root_config.get('log', 'level').upper()}")
  logging.getLogger().setLevel(root_config.get('log', 'level').upper())

if root_config.has('log', 'file') and \
   not root_config.get('log', 'file', 'bool'):
  logging.warning("[+] Config log.file = False -> This session will not be logged nor recorder into history")
  LOG_FILE_ENABLED = False

if LOG_FILE_ENABLED:
  LogConfig.add_file_handler()


class ScriptContext:
  """Script execution context."""

  def __init__(self, name, retention=50, workspace=False):
    self.name = name
    self.hist_enabled = True
    self.worskspace_enabled = workspace
    # The _context variable is necessary for getCurrentContext()
    # Don't touch that, you little rascal©
    # Touche pas à ça p'tit con©
    _context = Context.create(self.name)
    self.context = _context
    if self.context.root:
      self.context.config = root_config
    else:
      self.context.config = Config()
    self.context.config.register_secrets(self.context)
    arg_parser.register_secrets(self.context)
    if self.worskspace_enabled:
      self.workspace = Workspace(self.context.log_session_name)
    if LOG_FILE_ENABLED:
      self.context.hist = History(retention=retention)
    else:
      self.hist_enabled = False
    check_users(self.context)
    check_groups(self.context)
    try:
      self.context.pidstack = PIDStack(self.name, SCRIPPY_TMPDIR)
      self.context.pidstack.register()
    except PermissionError as err:
      err_msg = f"Error while creating instances stack: [{err.__class__.__name__}] {err}"
      logging.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err
    check_instances(self.context)

  def __enter__(self):
    """Entry point."""
    # The _context variable is necessary for getCurrentContext()
    # Don't touch that, you little rascal©
    # Touche pas à ça p'tit con©
    _context = self.context
    if self.hist_enabled:
      self.context.hist.__enter__()
    if self.worskspace_enabled:
      self.context.workspace_path = self.workspace.__enter__()
    return self.context

  def __exit__(self, kind, value, tb):
    """Exit point."""
    # The _context variable is necessary for getCurrentContext()
    # Don't touch that, you little rascal©
    # Touche pas à ça p'tit con©
    _context = self.context
    if self.worskspace_enabled:
      self.workspace.__exit__(kind, value, tb)
    if self.hist_enabled:
      self.context.hist.__exit__(kind, value, tb)
    self.context.pidstack.checkout()
    error_handler.handle_error(kind, value, tb)
