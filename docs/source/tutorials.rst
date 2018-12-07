=========
Tutorials
=========

This section contains materials on how to use Eskapade-Core.
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



Example esk101: Hello World!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Macro 101 runs the Hello World Link. It runs the Link twice using a repeat kwarg, showing how to use kwargs in Links.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk101_helloworld.py 


Example esk102: Multiple chains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Macro 102 uses multiple chains to print different kinds of output from one Link. This link is initialized multiple
times with different kwargs and names. There are if-statements in the macro to control the usage of the chains.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk102_multiple_chains.py


Example esk103: Print the DataStore
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Macro 103 has some objects in the DataStore. The contents of the DataStore are printed in the standard output.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk103_printdatastore.py


Example esk104: Basic DataStore operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Macro 104 adds some objects from a dictionary to the DataStore and then moves or deletes some of the items. Next it
adds more items and prints some of the objects.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk104_basic_datastore_operations.py


Example esk105: DataStore Pickling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Macro 105 has 3 versions: A, B and C. These are built on top of the basic macro esk105. Each of these 3 macro's does
something slightly different:

* A does not store any output pickles,
* B stores all output pickles,
* C starts at the 3rd chain of the macro.

Using these examples one can see how the way macro's are run can be controlled and what it saves to disk.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk105_A_dont_store_results.py
  $ eskapade_run $TUTDIRC/esk105_B_store_each_chain.py
  $ eskapade_run $TUTDIRC/esk105_C_begin_at_chain3.py


Example esk106: Command line arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Macro 106 shows us how command line arguments can be used to control the chains in a macro. By adding the arguments
from the message inside of the macro we can see that the chains are not run.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk106_cmdline_options.py


Example esk107: Chain loop
~~~~~~~~~~~~~~~~~~~~~~~~~~

Example 107 adds a chain to the macro and using a repeater Link it repeats the chain 10 times in a row.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk107_chain_looper.py


Example esk108: Event loop
~~~~~~~~~~~~~~~~~~~~~~~~~~

Example 108 processes a textual data set, to loop through every word and do a Map and Reduce operation on the data set.
Finally a line printer prints out the result.

.. code-block:: bash

  $ source $TUTDIRC/esk108_eventlooper.sh


Example esk109: Debugging tips
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This macro illustrates basic debugging features of Eskapade.
The macro shows how to start a python session while
running through the chains, and also how to break out of a chain.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk109_debugging_tips.py


Example esk110: Code profiling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This macro demonstrates how to run Eskapade with code profiling turned on.

.. code-block:: bash

  $ eskapade_run $TUTDIRC/esk110_code_profiling.py

