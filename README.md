IArm
====

IArm is an ARM interpreter for the ARMv6 THUMB instruction set
(More specifically for the ARM Cortex M0+ CPU).
It supports almost 100% of the instructions,
and some assembler directives.
There is also its [Jupyter](Jupyter.org) kernel counterpart so it can be
used with Jupyter notebooks.
Check out the `/docs` folder to see a technical overview
and some example notebooks.



Install
-------

Install with pip
```
pip install iarm
```
Or clone the repo and install with setuptools
```
python setup.py install
```

To install the Jupyer kernel counterpart, after installation, run
```
python -m iarm_kernel.install
```
