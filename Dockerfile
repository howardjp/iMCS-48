# This dockerfile is made for creating binders at mybinder.org
FROM andrewosh/binder-base

MAINTAINER Joshua Milas <josh.milas@gmail.com>

# Install IArm
RUN python setup.py install
# Install the IArm kernel
RUN python -m iarm_kernel.install
