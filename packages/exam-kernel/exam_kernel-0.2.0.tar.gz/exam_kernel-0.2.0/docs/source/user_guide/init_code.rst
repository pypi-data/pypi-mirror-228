Initialization Code
===================

``init_code`` is used for executing code whenever the kernel is fully loaded.

Example:

.. code-block:: python
    :caption: ipython_config.py

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.init_code = """
    import random as rd
    from math import sqrt

    def my_fun(x):
        return x**2
    """

In the above example, the library ``random`` will always be imported under the name ``rd``. The function ``my_fun`` will be available after starting the kernel.