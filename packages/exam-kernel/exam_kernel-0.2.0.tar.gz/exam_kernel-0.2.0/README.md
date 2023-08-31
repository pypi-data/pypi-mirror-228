# Exam Kernel

[![PyPi](https://img.shields.io/pypi/v/exam_kernel)](https://pypi.org/project/exam_kernel)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/exam-kernel/badge/?version=latest)](https://exam-kernel.readthedocs.io/en/latest/?badge=latest)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A wrapper for the IPython kernel that sanitizes the input before execution.

A more in depth explanation can be found in the [docs](https://exam-kernel.readthedocs.io/en/latest/).

This kernel blocks all magic commands including ```!```.

The libraries a user can use can be restricted by blocking or allowing certain imports. The module ```importlib``` is blocked by default.

## Installation

```
pip install exam_kernel
python -m exam_kernel.install --sys-prefix
```

## Configuration

You can configure the kernel via the ```ipython_config.py```.
This file is usually located under ```~/.ipython```.

### 1. Initialization Code

This is the code that will be executed every time the kernel is initialized and set via the configuration option ```IPKernelApp.exec_lines```.

Example config:

```
# sample ipython_config.py

c = get_config()

c.IPKernelApp.exec_lines = ['import math', 'import random']
```

In this example the libraries ```math``` and ```random``` are imported every time the kernel is initialized, making them available to the user right away.

### 2. Allowed Imports

If you want to allow the user to only use certain libraries, you can specify them using the ```allowed_imports``` configuration option. All other libraries will be blocked by default if this option is set.

Example config:

```
# sample ipython_config.py

c = get_config()

c.ExamKernel.allowed_imports = ['math', 'numpy', 'scipy']
```

In this example the student can only import the libraries ```math```, ```numpy``` and ```scipy```. If the user tries to import any other library (e.g. ```matplotlib```), he or she will see the following message:

```
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
<ipython-input-5-041c468338fc> in <module>
----> 1 raise ModuleNotFoundError('No module named matplotlib or matplotlib blocked by kernel.')

ModuleNotFoundError: No module named matplotlib or matplotlib blocked by kernel.
```

### 3. Blocked Imports

If you want to block the user from importing certain libraries, but let them use all others, you can use the ```blocked_imports``` configuration option. 

**If the ```allowed_import``` option is used, the blocked imports will take no effect.**

Example config:

```
# sample ipython_config.py

c = get_config()

c.ExamKernel.blocked_imports = ['math', 'numpy', 'scipy']
```

In this example the student can not import the libraries ```math```, ```numpy``` and ```scipy```. If the user tries to import a blocked library (e.g. ```math```), he or she will see the following message:

```
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
<ipython-input-5-041c468338fc> in <module>
----> 1 raise ModuleNotFoundError('No module named math or math blocked by kernel.')

ModuleNotFoundError: No module named math or math blocked by kernel.
```
