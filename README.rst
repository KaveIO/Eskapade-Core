=============
Eskapade-Core
=============

* Version: 0.9.2
* Released: Dec 2018

Eskapade is a light-weight, python-based data analysis framework, meant for modularizing all sorts of data analysis problems
into reusable analysis components. 

For the full documentation on Eskapade, including many examples, please go to this `link <http://eskapade.readthedocs.io>`_.

The core functionality of Eskapade, namely: the ``Link``, ``Chain``, ``process_manager``, ``DataStore``, ``ConfigObject`` and corresponding tutorials,
has now been split off from the growing Eskapade repository, into this new package Eskapade-Core.

For the minimal documentation on Eskapade-Core, please go `here <http://eskapade-core.readthedocs.io>`_.



Release notes
=============

Version 0.9
-----------

Version 0.9 of Eskapade-Core (December 2018) is a split off of the ``core`` and ``core_ops`` modules of Eskapade v0.9
into a separate package. Eskapade v0.9 builds on top of Eskapade-Core, and focussed on analysis modules.


Installation
============

requirements
------------

Eskapade-Core works standalone and is a very light-weight Python3 package, and requires ``Python 3.6+``.


pypi
----

To install the package from pypi, do:

.. code-block:: bash

  $ pip install Eskapade-Core

github
------

Alternatively, you can check out the repository from github and install it yourself:

.. code-block:: bash

  $ git clone https://github.com/KaveIO/Eskapade-Core.git eskapade-core

To (re)install the python code from your local directory, type from the top directory:

.. code-block:: bash

  $ pip install -e eskapade-core

python
------

After installation, you can now do in Python:

.. code-block:: python

  import escore

**Congratulations, you are now ready to use Eskapade!**


Quick run
=========

To see the available examples in Eskapade-Core, do:

.. code-block:: bash

  $ export TUTDIRC=`pip show Eskapade-Core | grep Location | awk '{ print $2"/escore/tutorials" }'`
  $ ls -l $TUTDIRC/

E.g. you can now run:

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk101_helloworld.py


This documentation here is minimal on purpose.
For all examples on using Eskapade links, chains and the DataStore to set up an analysis work flow,
please see the `Eskapade tutorials section <http://eskapade.readthedocs.io/en/latest/tutorials.html>`_.

For more examples, see the `full Eskapade documentation <http://eskapade.readthedocs.io>`_.


Contact and support
===================

Contact us at: kave [at] kpmg [dot] com

Please note that the KPMG Eskapade group provides support only on a best-effort basis.
