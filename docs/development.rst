.. _development:

***********
Development
***********

Installing from source
======================

you need `poetry`:

>>> pip3 install poetry

(Refer to `Poetry installation guide <https://python-poetry.org/docs/#installation>`_
for alternative ways of installing Poetry.)

Then `cd` to where the source code located and run:

>>> poetry install
>>> poetry build

It will create a virtual environment and installs `octopus-sensing` with its dependencies in it.

Coding Style
==============

We're following Python PEP 8 for our coding style.

For formatting the code, `autopep8 <https://github.com/hhatto/autopep8>`_ is a good tool.
Many editors support it. You can use it to automate the code formatting.

In-code Comments
~~~~~~~~~~~~~~~~~~~
Add comments to clarify *why* you did things this way. Usually, it's easy to figure out *what* a piece
of code does, but *why* is harder or impossible to figure out.

Also, add a comment for complex algorithms even if they are written very clearly.

Doc Strings
~~~~~~~~~~~~
Every public method or function should have doc string. We also generate our API Reference document
from these doc strings. So ensure they are clear and addresses all the functionality and exceptions
of a method.

Static Type Checking
======================

We use `mypy <http://www.mypy-lang.org/>`_ to type-check our sources. Every variable or parameter
in the source code should have a type, unless MyPy can automatically determine the type.

To run MyPy use our make file:

.. code-block:: bash

   $ make mypy


Tests
======
We're using `pytest <https://docs.pytest.org>`_ to run the tests. You can simply invoke the tests using:

.. code-block:: bash

   $ make test

There are two sets of tests: An integration test that checks the overall health of the library by running
a full scenario, and a lot of small unit tests that are testing functionalities individually.

All tests are located in `octopus-sensing/tests` directory.
