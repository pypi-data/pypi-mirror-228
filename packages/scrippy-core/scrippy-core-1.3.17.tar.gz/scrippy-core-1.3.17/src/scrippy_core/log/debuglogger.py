"""The scrippy_core.log.debuglogger sub-module allows logging in debug mode."""
import logging
from scrippy_core.log.infralogger import InfraLogger


class DebugLogger(InfraLogger):
  """Specific log manager for debug mode."""

  def __init__(self, name, level=logging.NOTSET):
    super(DebugLogger, self).__init__(name, level)

  def setLevel(self, level):
    """Override logging.Logger.setLevel."""
    # Nothing to do as log level is forced to DEBUG
    pass
