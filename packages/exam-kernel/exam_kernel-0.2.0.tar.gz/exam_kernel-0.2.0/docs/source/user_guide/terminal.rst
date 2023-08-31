Blocking Terminal Commands
==========================

``block_terminal_commands`` is used for blocking any commands preceded by ``!`` (e.g. ``!ls``). This is ``True`` by default.

.. code-block:: python
    :caption: ipython_config.py

    # In ipython_config.py
    # Allow the use of commands preceded by an exclamation mark
    c.ExamKernel.block_terminal_commands = False