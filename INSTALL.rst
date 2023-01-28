============
Installation
============

To install PyLFG, you have multiple options:

- Using pip: 
  This is the preferred method to install PyLFG, as it will always install the most recent stable release. 
  To install PyLFG, run this command in your terminal:

.. code-block:: console

  $ pip install pylfg


If you don't have `pip`_ installed, this `Python installation guide`_ can guide you through the process.

- Using pipx_ (recommended for users who want to avoid conflicts with other Python packages):

.. code-block:: console

  $ pipx install pylfg


- Using conda:
  You can also install PyLFG by using Anaconda_ or Miniconda_ instead of `pip`.
  To install Anaconda or Miniconda, please follow the installation instructions on their respective websites.
  After having installed Anaconda or Miniconda, run these commands in your terminal:

.. code-block:: console

  $ conda config --add channels conda-forge
  $ conda config --set channel_priority strict
  $ conda install pylfg
  
If you already have Anaconda or Miniconda available on your system, just type this in your terminal:

.. code-block:: console

  $ conda install -c conda-forge pylfg

.. warning::
  If you intend to install PyLFG on a Apple Macbook with an Apple M1 or M2 processor or newer,
  it is advised that you install PyLFG by using the conda installation method as all dependencies will be pre-compiled.

.. _pip: https://pip.pypa.io
.. _pipx: https://github.com/pypa/pipx
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Anaconda: https://www.anaconda.com/products/individual
.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html



From sources
~~~~~~~~~~~~

The sources for PyLFG can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/SekouDiaoNlp/PyLFG

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/SekouDiaoNlp/PyLFG/tarball/master

Once you have a copy of the source, get in the source directory and you can install it with:

.. code-block:: console

    $ python setup.py install

Alternatively, you can use poetry to install the software:

.. code-block:: console

    $ pip install poetry
    
    $ poetry install


.. _Github repo: https://github.com/SekouDiaoNlp/PyLFG
.. _tarball: https://github.com/SekouDiaoNlp/PyLFG/tarball/master

