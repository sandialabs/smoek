Smoek Documentation
===================

Smoek is a lightweight optimization modeling library for fast model transformation.

Smoek is an experimental Python modeling environment that uses compact abstract
model expressions to enable fast transformation of model structure, deferred model
instantiation, and code generation. Smoek was designed to support lightweight model
declarations that can be transformed into back-end implementations such as Pyomo,
Poek, Coek, and other modeling languages or specialized solver interfaces.

Abstract model descriptions can be written compactly in Python, transformed quickly,
and used to generate efficient concrete optimization models in lower-level or
performance-oriented modeling systems. The overhead for Smoek declarations and problem
transformations is minimal, and low-level modeling libraries like Coek can be leveraged
to significantly accelerate model generation.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   quickstart
   api
   backends
   examples

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
