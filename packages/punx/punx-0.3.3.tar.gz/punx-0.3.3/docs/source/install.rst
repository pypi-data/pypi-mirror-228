.. _install:
.. index:: install

Installation
############

Released versions of punx are available on `PyPI 
<https://pypi.python.org/pypi/punx>`_. 

If you have ``pip`` installed, then you can install::

    $ pip install punx 

The latest development versions of punx can be downloaded from the
GitHub repository listed above::

    $ cd /some/directory
    $ git clone http://github.com/prjemian/punx.git

To install in the standard Python location::

    $ cd punx
    $ pip install .

Updating
********

:pip:  If you have installed previously with *pip*::

    $ pip install -U --no-deps punx

:git:  assuming you have cloned as shown above::

    $ cd /some/directory/punx
    $ git pull
    $ pip install -U --no-deps .


Required Packages
*****************

It may be necessary to install some prerequisite packages in your python installation.
If you are using an Anaconda python distribution, it is advised to install these 
pre-requisites using *conda* rather than *pip*.  The pre-requisites include:

* h5py
* lxml
* numpy
* Qt and PyQt (v5)
* requests

See your distribution's documentation for how to install these.  With Anaconda, use::

    conda install h5py lxml numpy Qt=5 PyQt=5 requests pyRestTable -c conda-forge

============  ===================================
Package       URL
============  ===================================
h5py          https://www.h5py.org
lxml          https://lxml.de
numpy         https://numpy.scipy.org
PyQt5         https://www.riverbankcomputing.com/software/pyqt/
requests      https://docs.python-requests.org 
============  ===================================

Optional Packages
*****************

============  ===================================
Package       URL
============  ===================================
pyRestTable   https://pyresttable.readthedocs.io
============  ===================================

The *pyRestTable* package is used for various reports in the punx application.
   If using the punx package as a library and developing your own custom 
   reporting, this package is not required.
