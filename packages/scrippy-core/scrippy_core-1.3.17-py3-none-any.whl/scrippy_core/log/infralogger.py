"""The scrippy_core.log.debuglogger sub-module allows logging in normal mode."""
import logging
from scrippy_core.context import Context


class InfraLogger(logging.Logger):
  """Log manager."""

  def __init__(self, name, level=logging.NOTSET):
    super().__init__(name, level)

  def makeRecord(self,
                 name,
                 level,
                 fn,
                 lno,
                 msg,
                 args,
                 exc_info,
                 func=None,
                 extra=None,
                 sinfo=None):
    """Override logging.Logger.makeRecord."""
    script_name = name
    context = Context.get_current()
    if context is None:
      context = Context.get_root_context()
    script_name = context.log_session_name
    msg = context.vault.protect(msg)
    return super().makeRecord(script_name,
                              level,
                              fn,
                              lno,
                              msg,
                              args,
                              exc_info,
                              func,
                              extra,
                              sinfo)
