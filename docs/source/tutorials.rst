=========
Tutorials
=========

This section briefly describes how to run Eskapade-Core.
All command examples can be run from any directory with write access.
For more in depth explanations on the functionality of the code-base,
try the `API docs <code.html>`_.



The examples in Eskapade Core
-----------------------------

All Eskapade-Core example macros can be found in the tutorials directory.
For ease of use, let's make a shortcut to the directory containing the tutorials:

.. code-block:: bash

  $ export TUTDIRC=`pip show Eskapade-Core | grep Location | awk '{ print $2"/escore/tutorials" }'`
  $ ls -l $TUTDIRC/

The numbering of the example macros is as follows:

* esk100+: basic macros describing the chains, links, and datastore functionality of Eskapade.
           They explain the basic architecture of Eskapade, i.e. how the chains, links, 
           datastore, and process manager interact.

These macros are briefly described below.
You are encouraged to run all examples to see what they can do for you!

For all Eskapade tutorial examples, please go to the `Eskapade tutorials section <http://eskapade.readthedocs.io/en/latest/tutorials.html>`_ at read-the-docs.


Example: Hello World!
~~~~~~~~~~~~~~~~~~~~~

Macro 101 runs the Hello World Link. It runs the Link twice using a repeat kwarg, showing how to use kwargs in Links.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk101_helloworld.py 

