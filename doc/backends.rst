========
Backends
========

Smoek models are abstract - they describe model structure without being tied to a specific
solver or modeling framework. To actually solve a model, you transform it to a **backend**.

Smoek supports two types of backends:

* **PyModel backends** - Generate in-memory model objects in other frameworks
* **Code generation backends** - Generate source code in other languages

Overview of Backends
====================

When to Use Each Type
---------------------

**Use PyModel backends when:**

* You want to solve models immediately in Python
* You're prototyping and iterating quickly
* You want to use features specific to the target framework
* You're working with familiar Python-based solvers

**Use code generation backends when:**

* You need maximum performance for model generation
* You're integrating optimization into a larger C++ application
* You want to share models with developers using other languages
* You want standalone model code independent of Python

PyModel Backends
================

PyModel backends generate in-memory model objects that can be solved immediately.

Pyomo Backend
-------------

The Pyomo backend generates Pyomo ``ConcreteModel`` objects.

**Import:**

.. code-block:: python

    from smoek.pymodel.pyomo import generate

**Function signature:**

.. code-block:: python

    generate(model, data=None)

**Parameters:**

``model``
    The smoek model to transform.

``data`` : JsonDataPortal, optional
    Data portal containing parameter and set values.

**Returns:**

Pyomo ``ConcreteModel`` object that can be solved with Pyomo solvers.

**Example:**

.. code-block:: python

    import smoek as smk
    from smoek.pymodel.pyomo import generate

    # Define model
    @smk.model
    class knapsack:
        ITEMS = smk.set()
        i = smk.index()

        value = smk.parameter().index_set(ITEMS)
        weight = smk.parameter().index_set(ITEMS)
        capacity = smk.parameter()

        x = smk.variable().index_set(ITEMS).bounds(0.0, 1.0)

        o = smk.objective().maximize(
            smk.sum(value[i] * x[i]).forall(i in ITEMS)
        )
        c = smk.constraint().expr(
            smk.sum(weight[i] * x[i]).forall(i in ITEMS) <= capacity
        )

    model = knapsack()

    # Load data
    data = smk.load_data_from_json(filename="knapsack.json")

    # Generate Pyomo model
    pyomo_model = generate(model, data=data)

    # Solve with Pyomo
    from pyomo.opt import SolverFactory
    solver = SolverFactory('glpk')
    results = solver.solve(pyomo_model, tee=True)

    # Access solution
    print("Objective value:", pyomo_model.o())
    for item in pyomo_model.ITEMS:
        if pyomo_model.x[item].value > 0.5:
            print(f"Select item {item}")

**Benefits:**

* Immediate solving in Python
* Access to all Pyomo solvers and features
* Interactive exploration of solutions
* Familiar Pyomo syntax for post-processing

**Limitations:**

* Model generation time is slower than code generation
* Requires Pyomo installation
* Python-only (cannot integrate into C++ applications)

Poek Backend
------------

The Poek backend generates Poek model objects (similar to Pyomo but with different internals).

**Import:**

.. code-block:: python

    from smoek.pymodel.poek import generate

**Usage:**

The API is similar to the Pyomo backend:

.. code-block:: python

    from smoek.pymodel.poek import generate

    poek_model = generate(model, data=data)
    # Solve with Poek-compatible solver

Code Generation Backends
=========================

Code generation backends produce source code rather than in-memory objects.

Coek Backend (C++ Code Generation)
-----------------------------------

The Coek backend generates standalone C++ code that uses the Coek optimization library.

**Import:**

.. code-block:: python

    from smoek.code.coek import generate

**Function signature:**

.. code-block:: python

    generate(model, outfile, model_name=None, data={}, loops="default")

**Parameters:**

``model``
    The smoek model to transform.

``outfile`` : str
    Path where the C++ code should be written.

``model_name`` : str, optional
    Name for the generated model function. If not provided, uses the model's name.

``data`` : dict or JsonDataPortal, optional
    Data values to embed in the generated code.

``loops`` : str, default="default"
    Loop generation strategy. Options include "default", "compact", "expanded".

**Example:**

.. code-block:: python

    import smoek as smk
    from smoek.code.coek import generate

    # Define model
    @smk.model
    class knapsack:
        ITEMS = smk.set()
        i = smk.index()

        value = smk.parameter().index_set(ITEMS)
        weight = smk.parameter().index_set(ITEMS)
        capacity = smk.parameter()

        x = smk.variable().index_set(ITEMS).bounds(0.0, 1.0)

        o = smk.objective().maximize(
            smk.sum(value[i] * x[i]).forall(i in ITEMS)
        )
        c = smk.constraint().expr(
            smk.sum(weight[i] * x[i]).forall(i in ITEMS) <= capacity
        )

    model = knapsack()

    # Load data
    data = smk.load_data_from_json(filename="knapsack.json")

    # Generate C++ code
    generate(model, outfile="knapsack.cpp", data=data)

This creates a file ``knapsack.cpp`` containing C++ code that builds the model using
the Coek library.

**Generated code structure:**

The generated C++ file includes:

* Header includes for Coek
* Data structure definitions
* Model building function
* Main function (optional)

**Benefits:**

* Very fast model generation at runtime
* Can be integrated into C++ applications
* No Python dependency at deployment
* Optimal performance for repeated model builds

**Use cases:**

* Embedding optimization in high-performance C++ applications
* Building models repeatedly with different data
* Deploying models without Python runtime
* Sharing models with C++ developers

**Compilation:**

To compile and run the generated code, you'll need:

1. Coek C++ library installed
2. A C++ compiler (g++, clang++, etc.)
3. Link against Coek and your solver libraries

.. code-block:: bash

    g++ -o knapsack knapsack.cpp -lcoek -std=c++17

Pyomo Code Backend
------------------

The Pyomo code backend generates Python source code for Pyomo models (as opposed to
in-memory objects).

**Import:**

.. code-block:: python

    from smoek.code.pyomo import generate

**Function signature:**

.. code-block:: python

    generate(model, outfile, data={})

**Parameters:**

``model``
    The smoek model to transform.

``outfile`` : str
    Path where the Python code should be written.

``data`` : dict or JsonDataPortal, optional
    Data values to embed in the generated code.

**Example:**

.. code-block:: python

    from smoek.code.pyomo import generate

    # Generate Python code
    generate(model, outfile="knapsack_model.py", data=data)

This creates a Python file containing Pyomo model building code.

**Benefits:**

* Human-readable Python code
* Can be version controlled and reviewed
* Independent of smoek at runtime
* Useful for documentation and teaching

**Use cases:**

* Creating standalone Pyomo model files
* Sharing models with Pyomo users
* Documenting model formulations
* Generating models for version control

Complete Workflow Examples
===========================

Example 1: Quick Prototyping with Pyomo
----------------------------------------

.. code-block:: python

    import smoek as smk
    from smoek.pymodel.pyomo import generate
    from pyomo.opt import SolverFactory

    # Define model
    @smk.model
    class simple_lp:
        x = smk.variable().bounds(0, None)
        y = smk.variable().bounds(0, None)

        o = smk.objective().maximize(3*x + 2*y)

        c1 = smk.constraint().expr(2*x + y <= 10)
        c2 = smk.constraint().expr(x + 2*y <= 8)

    model = simple_lp()

    # Generate and solve
    pyomo_model = generate(model)
    solver = SolverFactory('glpk')
    results = solver.solve(pyomo_model)

    print(f"Optimal objective: {pyomo_model.o()}")
    print(f"x = {pyomo_model.x.value}")
    print(f"y = {pyomo_model.y.value}")

Example 2: Data-Driven Model with JSON
---------------------------------------

.. code-block:: python

    import smoek as smk
    from smoek.pymodel.pyomo import generate

    # Define abstract model
    @smk.model
    class facility_location:
        FACILITIES = smk.set()
        CUSTOMERS = smk.set()

        i = smk.index()
        j = smk.index()

        fixed_cost = smk.parameter().index_set(FACILITIES)
        demand = smk.parameter().index_set(CUSTOMERS)
        distance = smk.parameter().index_set(FACILITIES).index_set(CUSTOMERS)

        open_facility = smk.variable().index_set(FACILITIES).within(smk.Binary)
        serve = smk.variable().index_set(FACILITIES).index_set(CUSTOMERS).bounds(0, 1)

        o = smk.objective().minimize(
            smk.sum(fixed_cost[i] * open_facility[i]).forall(i in FACILITIES)
            + smk.sum(distance[i, j] * serve[i, j]).forall(i in FACILITIES, j in CUSTOMERS)
        )

        # Meet all demand
        meet_demand = smk.constraint().expr(
            smk.sum(serve[i, j]).forall(i in FACILITIES) == 1
        ).forall(j in CUSTOMERS)

        # Can only serve if open
        must_be_open = smk.constraint().expr(
            serve[i, j] <= open_facility[i]
        ).forall(i in FACILITIES, j in CUSTOMERS)

    model = facility_location()

    # Load different datasets
    for scenario in ["small", "medium", "large"]:
        data = smk.load_data_from_json(filename=f"facility_{scenario}.json")
        pyomo_model = generate(model, data=data)
        # Solve and analyze...

Example 3: High-Performance with Coek
--------------------------------------

.. code-block:: python

    import smoek as smk
    from smoek.code.coek import generate

    # Define model (same as before)
    @smk.model
    class production_planning:
        PERIODS = smk.set()
        PRODUCTS = smk.set()

        t = smk.index()
        p = smk.index()

        demand = smk.parameter().index_set(PERIODS).index_set(PRODUCTS)
        capacity = smk.parameter().index_set(PERIODS)
        cost = smk.parameter().index_set(PRODUCTS)

        produce = smk.variable().index_set(PERIODS).index_set(PRODUCTS).bounds(0, None)

        o = smk.objective().minimize(
            smk.sum(cost[p] * produce[t, p]).forall(t in PERIODS, p in PRODUCTS)
        )

        meet_demand = smk.constraint().expr(
            produce[t, p] >= demand[t, p]
        ).forall(t in PERIODS, p in PRODUCTS)

        capacity_limit = smk.constraint().expr(
            smk.sum(produce[t, p]).forall(p in PRODUCTS) <= capacity[t]
        ).forall(t in PERIODS)

    model = production_planning()
    data = smk.load_data_from_json(filename="production.json")

    # Generate C++ code
    generate(model, outfile="production_model.cpp", data=data)

    # Now compile and run the C++ code for maximum performance

Performance Considerations
==========================

Model Generation Time
---------------------

Approximate relative performance for model generation:

1. **Coek code generation** - Fastest (10-100x faster than Pyomo for large models)
2. **Pyomo code generation** - Fast
3. **Poek pymodel** - Medium
4. **Pyomo pymodel** - Slowest (but still acceptable for most applications)

For most applications, Pyomo pymodel is perfectly adequate. Consider code generation
when:

* Building the same model structure repeatedly with different data
* Model generation time is a bottleneck in your application
* You're building very large models (thousands of variables/constraints)

Memory Usage
------------

* PyModel backends keep the model in memory
* Code generation backends produce files (no memory overhead at generation time)

For very large models, code generation can be more memory-efficient.

Backend-Specific Features
==========================

Expression Support
------------------

All backends support:

* Linear expressions
* Quadratic expressions
* Polynomial expressions
* Standard mathematical functions (sin, cos, log, sqrt, etc.)

Some solvers have limitations on nonlinear expressions - check your solver's documentation.

Data Type Mappings
------------------

Smoek types map to backend types as follows:

**Variables:**

* ``Reals`` → continuous variables in all backends
* ``Integers`` → integer variables in all backends
* ``Binary`` → binary/boolean variables in all backends
* ``PositiveReals``, etc. → continuous with appropriate bounds

**Parameters:**

* Python int/float → backend numeric types
* Python string → backend string types (where supported)

**Sets:**

* Python lists → backend index sets
* Numeric ranges → backend range sets

Limitations and Workarounds
============================

Current Limitations
-------------------

Some features are not yet fully supported:

* Multi-dimensional set products (``A*B``) - use separate ``.forall()`` for each dimension
* Some advanced Pyomo features (blocks, disjunctions) - use Pyomo directly for these
* Solver-specific annotations - add these in backend-specific code

These limitations may be addressed in future versions.

Workarounds
-----------

**For multi-dimensional iteration**, instead of:

.. code-block:: python

    # Not yet supported
    .forall((i,j) in A*B)

Use:

.. code-block:: python

    # Supported
    .forall(i in A, j in B)

**For solver-specific features**, generate the backend model then modify it:

.. code-block:: python

    pyomo_model = generate(model, data=data)

    # Add Pyomo-specific annotations
    pyomo_model.x.domain = pyomo.environ.NonNegativeReals
    pyomo_model.some_special_constraint.deactivate()

    # Solve
    results = solver.solve(pyomo_model)
