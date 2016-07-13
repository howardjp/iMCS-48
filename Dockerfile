# This dockerfile is made for creating binders at mybinder.org
FROM andrewosh/binder-python-3.5-mini

MAINTAINER Joshua Milas <josh.milas@gmail.com>

USER main

# Install IArm
#Clone the repo
# TODO replace with `pip install iarm`
RUN git clone https://github.com/DeepHorizons/iarm && \
    cd iarm && \
    python setup.py install

# Install the IArm kernel
RUN python -m iarm_kernel.install
