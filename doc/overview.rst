========
Overview
========

What is Smoek?
==============

Smoek is a lightweight Python library for abstract optimization modeling that enables fast model transformation and code generation. It provides a compact, declarative syntax for describing optimization problems that can be transformed into various backend solvers and modeling languages.

Key benefits of smoek include:

* **Fast transformation**: Minimal overhead for model declarations and transformations
* **Deferred instantiation**: Models are abstract until transformed to a backend
* **Backend agnostic**: Write once, transform to multiple backends (Pyomo, Coek, etc.)
* **Code generation**: Generate standalone solver code in C++ or Python
* **Compact syntax**: Clean, readable model declarations using Python decorators

Key Concepts
============

Abstract vs Concrete Models
----------------------------

Smoek uses **abstract models** - models where the structure is defined independently of the data. This allows you to:

* Define a model structure once and reuse it with different datasets
* Transform the same abstract model to different backends
* Generate efficient code for performance-critical applications

When you define a smoek model, you're creating a template that describes:

* What decision variables exist and their properties
* What parameters and sets are needed
* How the objective function is calculated
* What constraints must be satisfied

The model becomes **concrete** when it's transformed to a backend with actual data values.

Model Components
----------------

A smoek model consists of several types of components:

**Variables**
  Decision variables represent the unknowns your optimization solver will determine.
  Variables can be continuous, integer, or binary, and can have bounds.

**Parameters and Data**
  Parameters represent fixed input values to your model. They can be scalars or indexed arrays.

**Sets and Indices**
  Sets define the index spaces for indexed components. Indices are used to reference
  elements within indexed variables, parameters, and constraints.

**Objectives**
  The objective function defines what you want to minimize or maximize.

**Constraints**
  Constraints define the feasible region for your optimization problem using
  mathematical expressions over variables and parameters.

Indexed Components
------------------

One of smoek's powerful features is support for **indexed components** - variables, parameters,
and constraints that are defined over index sets. This allows you to concisely express
patterns that repeat across many elements.

For example, instead of creating variables ``x1, x2, x3, ...`` individually, you can create
an indexed variable ``x`` over an index set, then reference individual elements as ``x[i]``.

The ``forall`` operator is used to create families of constraints or to aggregate values
across an index set using operations like ``sum()`` and ``prod()``.

Architecture Overview
=====================

Smoek has a layered architecture:

Core Modeling Layer
-------------------

The core layer (``smoek.core``) provides the abstract modeling constructs:

* Variable, parameter, and set declarations
* Expression building and manipulation
* Model structure representation
* The ``@model`` decorator for defining models

This layer is lightweight and focused on model structure, not computation.

Backend Transformation Layer
-----------------------------

Smoek supports two types of backends:

**PyModel Backends** (``smoek.pymodel.*``)
  Generate in-memory model objects in other modeling frameworks:

  * ``smoek.pymodel.pyomo`` - Generate Pyomo ConcreteModel objects
  * ``smoek.pymodel.poek`` - Generate Poek model objects

  These are useful for immediate solving with the target framework's solvers.

**Code Generation Backends** (``smoek.code.*``)
  Generate source code in other languages:

  * ``smoek.code.coek`` - Generate C++ code using the Coek library
  * ``smoek.code.pyomo`` - Generate Python source code for Pyomo models

  These are useful for creating standalone model implementations or
  integrating into larger codebases.

Data Portal System
------------------

The data portal system (``smoek.core.data_apis``) provides:

* JSON-based data storage format (Coek schema)
* Data loading from files, strings, or dictionaries
* Type metadata for sets and parameters
* Support for scalar, indexed, and multi-dimensional data

The data portal allows you to separate model structure from data, making it easy to:

* Test models with different datasets
* Share data between different modeling tools
* Version control data separately from model code

When to Use Smoek
=================

Smoek is particularly well-suited for:

**Model Prototyping**
  Quickly experiment with different model formulations before committing to
  a specific implementation or backend.

**Cross-Backend Development**
  Develop models that need to work with multiple solving backends or that
  may need to switch backends in the future.

**Performance-Critical Applications**
  Use the Coek code generation backend to create highly optimized C++ model
  code for applications where model generation time is critical.

**Model Structure Transformations**
  Transform model structure programmatically before instantiation, enabling
  metaheuristics, model reduction techniques, or automated reformulation.

**Teaching and Documentation**
  The clean, declarative syntax makes smoek models easy to read and understand,
  ideal for teaching optimization concepts or documenting model formulations.

Smoek may not be the best choice when:

* You need advanced features specific to a particular modeling framework
* You're working with a small, one-off model that will never change
* Your target solver has its own specialized modeling language that you must use
