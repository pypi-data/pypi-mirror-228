Blocking Imports
================

There are two ways to configure how imports are blocked or allowed.

* ``allowed_imports`` - Takes a list of module names. If this option is set, only imports in this list can be imported
* ``blocked_imports`` - Takes a list of module names. If this option is set, all inputs specified are blocked. If ``allowed_imports`` is set, ``blocked_imports`` will be ignored.

Example of using ``allowed_imports``:

.. code-block:: python
    :caption: ipython_config.py

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.allowed_imports = ["math", "random"]

.. code-block:: python
    :caption: Example of trying to import a module that is not in the allowed imports

    import os
    ---------------------------------------------------------------------------
    ModuleNotFoundError: No module named os or os blocked by kernel.
    Allowed imports are: [math, random]
    

Example of using ``blocked_imports``:

.. code-block:: python
    :caption: ipython_config.py

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.blocked_imports = ["os", "pandas"]

.. code-block:: python
    :caption: Example of trying to import a module that is in the blocked imports

    import os
    ---------------------------------------------------------------------------
    ModuleNotFoundError: No module named os or os blocked by kernel.
    The following imports are blocked: [os, pandas]