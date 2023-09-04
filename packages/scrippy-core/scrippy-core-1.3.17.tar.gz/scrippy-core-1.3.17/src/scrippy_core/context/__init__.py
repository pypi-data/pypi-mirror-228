"""The scrippy_core.context module provides all the necessary objects for managing the execution context of scripts."""
import os
import re
import time
import errno
import logging
import inspect
import importlib
from filelock import FileLock
from scrippy_core.scriptinfo import ScriptInfo


class Vault:
  """The Vault class manages sensitive information that should not appear in logs."""

  def __init__(self):
    self.secrets = []
    self.pattern = None

  def add(self, value):
    self.secrets.append(str(value))
    self.pattern = re.compile(f"{'|'.join(self.secrets)}")

  def is_secret(self, value):
    return value in self.secrets

  def protect(self, msg):
    if self.pattern is not None:
      return re.sub(self.pattern, "*******", str(msg))
    return msg


class PIDStack:
  """The PIDStack class allows for the management of concurrent executions."""

  def __init__(self, filename, tmpdir):
    """Initialise la pile d'exécution."""
    filename = os.path.basename(filename)
    filename = os.path.splitext(filename)[0]
    self.stack_file_path = os.path.join(tmpdir, f"{filename}.pids")
    self.lock = FileLock(f"{self.stack_file_path}.lock")

  def _read(self):
    pids = []
    if os.path.isfile(self.stack_file_path):
      with open(self.stack_file_path, mode="r", encoding="utf-8") as stack_file:
        pids = [pid.strip() for pid in stack_file.readlines()]
      if pids is None:
        pids = []
    return pids

  def _write(self, pids):
    with open(self.stack_file_path, mode="w", encoding="utf-8") as stack_file:
      for pid in pids:
        stack_file.write(f"{pid}\n")

  def get_pids(self):
    """Returns the list of PIDs in queue or currently executing."""
    pids = []
    with self.lock.acquire():
      for pid in self._read():
        try:
          os.kill(int(pid), 0)
          pids.append(int(pid))
        except OSError as e:
          if e.errno == errno.EPERM:
            pids.append(pid)
          elif e.errno == errno.ESRCH:
            pass
      self._write(pids)
      return pids

  def register(self):
    """Registers a new PID in the stack"""
    with self.lock.acquire():
      pids = self.get_pids()
      pids.append(os.getpid())
      self._write(pids)

  def checkout(self):
    """Cleans the stack."""
    with self.lock.acquire():
      self._write([pid for pid in self.get_pids() if pid != str(os.getpid())])


class Context:
  """The Context class enables management of the script's execution context"""

  _root_context = None

  def __init__(self, filename, session, root=False, temp=False):
    """Context initialization."""
    self.filename = os.path.basename(filename)
    self.name = os.path.splitext(self.filename)[0]
    self.session = session
    self.vault = Vault()
    self.childs = []
    self.root = root
    self.temp = temp
    logging.getLogger('filelock').setLevel(logging.CRITICAL)
    self.log_session_name = f"{self.name}_{self.session}"
    if root:
      self.doc = ScriptInfo.get_doc()
    else:
      self.doc = importlib.import_module(self.name).__doc__

  @staticmethod
  def create(filename):
    """Context creation"""
    Context.get_root_context()  # Force la creation du rootContext
    if Context._root_context.temp:
      new_context = Context(filename,
                            session=Context._root_context.session,
                            root=True)
      Context._root_context = new_context
    else:
      session = f"{time.time()}_{os.getpid()}"
      new_context = Context(filename, session=session)
    parent_context = Context.get_current()
    if parent_context:
      Context.find(parent_context)._add_child(new_context)
    return new_context

  @staticmethod
  def find(context_to_find, current_context=None):
    """Returns the complete execution contexte."""
    if not current_context:
      current_context = Context._root_context
    if current_context == context_to_find:
      return current_context
    else:
      for child in current_context.childs:
        found = Context.find(context_to_find, child)
        if found:
          return found
      return None

  @staticmethod
  def get_root_context():
    """Return the root context."""
    if not Context._root_context:
      session = f"{time.time()}_{os.getpid()}"
      Context._root_context = Context(ScriptInfo.get_script_filename(),
                                      session=session,
                                      root=True,
                                      temp=True)
    return Context._root_context

  @staticmethod
  def get_current():
    """Returns the current context."""
    for fi in inspect.stack():
      if '_context' in fi[0].f_locals and isinstance(fi[0].f_locals['_context'], Context):
        context = fi[0].f_locals['_context']
        return context
    return None

  @staticmethod
  def print_full_stack(context=None, lvl=0):
    """Prints the full context stack."""
    if not context:
      context = Context.get_root_context()
    print(' |-' + lvl * '--' + context.name + ' ' + context.session)
    for child in context.childs:
      Context.print_full_stack(child, lvl + 1)

  def _add_child(self, child_context):
    self.childs.append(child_context)

  def print_stack(self):
    """Prints the stack."""
    lvl = 0
    for context in self.stack():
      print(' |-' + lvl * '--' + context.name)
      lvl += 1

  def get_parent(self, tree=None):
    tree = tree or Context.get_root_context()
    for context in tree.childs:
      if context == self:
        return tree
      else:
        res = self.get_parent(context)
        if res:
          return res
    return None

  def stack(self):
    stack = []
    current = self
    while current:
      stack.append(current)
      current = current.get_parent()
    stack.reverse()
    return stack

  def __eq__(self, other):
    """Overrides the default implementation"""
    if isinstance(other, Context):
      return self.name == other.name and self.session == other.session
    return False

  def __str__(self):
    return f"Context(name='{self.name}', filename='{self.filename}', session='{self.session}', childs='{list(map(lambda child: str(child), self.childs))}', root={self.root})"
