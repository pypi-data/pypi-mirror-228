Blocking Magic Commands
=======================

There are two ways to configure how both line and cell magic commands (e.g. ``%%time``) are blocked or allowed.

* ``allowed_magics`` - Takes a list of magic names. If this option is set, only magics in this list can be used
* ``blocked_magics`` - Takes a list of magic names. If this option is set, all magics specified are blocked. If ``allowed_magics`` is set, ``blocked_magics`` will be ignored.

Example of using ``allowed_magics``:

.. code-block:: python
    :caption: ipython_config.py

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.allowed_imports = ["time"]

.. code-block:: python
    :caption: Example of trying to use a magic that is not in the allowed magics

    %timeit my_fun()
    ---------------------------------------------------------------------------
    ValueError: No magic named timeit or timeit blocked by kernel.
    Allowed magics are: [time]

Example of using ``blocked_magics``:

.. code-block:: python
    :caption: ipython_config.py

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.blocked_imports = ["time"]

.. code-block:: python
    :caption: Example of trying to use a magic that is in the blocked magics

    %%time
    ---------------------------------------------------------------------------
    ValueError: No magic named time or time blocked by kernel.
    The following magics are blocked: [time]