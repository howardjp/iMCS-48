# This dockerfile is made for creating binders at mybinder.org
FROM andrewosh/binder-python-3.5-mini

MAINTAINER Joshua Milas <josh.milas@gmail.com>

USER main

# Install IArm
# TODO replace with `pip install iarm`
RUN python setup.py install

# Install the IArm kernel
RUN python -m iarm_kernel.install
