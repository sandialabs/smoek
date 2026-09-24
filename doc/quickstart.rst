==========
Quickstart
==========

This guide will get you up and running with smoek quickly through a series of examples.

Installation
============

Install smoek via pip:

.. code-block:: bash

    pip install smoek

For backend support, you may also want to install:

.. code-block:: bash

    # For Pyomo backend
    pip install pyomo

    # For Coek backend (C++ code generation)
    pip install coek

Your First Model
================

Let's create a simple optimization model with two variables, a quadratic objective, and an equality constraint:

.. code-block:: python

    import smoek as smk

    @smk.model
    class simple_model:
        x = smk.variable().value(1.0)
        y = smk.variable().value(1.0)

        o = smk.objective().minimize(x**2)
        c = smk.constraint().expr(y**2 == 4)

    model = simple_model()

Let's break this down:

* **@smk.model decorator**: Marks the class as an optimization model
* **smk.variable()**: Creates a decision variable
* **.value(1.0)**: Sets an initial value for the variable
* **smk.objective()**: Defines the objective function
* **.minimize(...)**: Specifies we want to minimize the given expression
* **smk.constraint()**: Creates a constraint
* **.expr(...)**: Specifies the constraint expression (here, an equality)

The model is instantiated by calling ``simple_model()``, which creates a concrete instance
of the abstract model definition.

Working with Indexed Components
================================

Most real optimization models involve collections of similar variables and constraints.
Smoek provides **indexed components** to handle this elegantly.

Here's an example with indexed variables and parameters:

.. code-block:: python

    import smoek as smk

    @smk.model
    class indexed_model:
        # Define an index set {0, 1, 2, 3}
        A = smk.range(stop=3)

        # Create an index variable
        i = smk.index()

        # Create indexed variable and parameter
        x = smk.variable().index_set(A)
        p = smk.parameter().index_set(A).value(1.0)

        # Objective: minimize the sum of p[i] * x[i] for all i in A
        o = smk.objective().minimize(
            smk.sum(p[i] * x[i]).forall(i in A)
        )

        # Constraint: x[i] >= 0 for all i in A
        c = smk.constraint().expr(x[i] >= 0).forall(i in A)

    model = indexed_model()

Key concepts introduced:

* **smk.range(stop=3)**: Creates an index set {0, 1, 2, 3} (note: inclusive of stop value)
* **smk.index()**: Creates an index variable used to iterate over sets
* **.index_set(A)**: Makes a component indexed over set A
* **smk.sum(...).forall(i in A)**: Sums an expression over all values in set A
* **.forall(i in A)**: Applies a constraint to all values in set A

The ``forall`` syntax is central to smoek - it allows you to create families of
constraints or aggregate expressions without writing explicit loops.

Loading Data from JSON
=======================

For larger models, you'll want to separate model structure from data. Smoek provides
a JSON-based data format and convenient loading functions.

Model with Abstract Sets
-------------------------

First, define a model with abstract sets and parameters:

.. code-block:: python

    import smoek as smk

    @smk.model
    class knapsack:
        # Abstract set - will be populated from data
        ITEMS = smk.set()

        i = smk.index()

        # Parameters indexed by ITEMS
        value = smk.parameter().index_set(ITEMS)
        weight = smk.parameter().index_set(ITEMS)
        capacity = smk.parameter()

        # Decision variables: select items
        x = smk.variable().index_set(ITEMS).bounds(0.0, 1.0)

        # Maximize total value
        o = smk.objective().maximize(
            smk.sum(value[i] * x[i]).forall(i in ITEMS)
        )

        # Respect capacity constraint
        c = smk.constraint().expr(
            smk.sum(weight[i] * x[i]).forall(i in ITEMS) <= capacity
        )

    model = knapsack()

JSON Data Format
----------------

Create a JSON file (``knapsack_data.json``) with your data:

.. code-block:: json

    {
        "ITEMS": {
            "set_type": "i",
            "data": [1, 2, 3, 4]
        },
        "value": {
            "param_type": "d",
            "key_type": "i",
            "data": [[1, 8], [2, 3], [3, 6], [4, 11]]
        },
        "weight": {
            "param_type": "d",
            "key_type": "i",
            "data": [[1, 5.0], [2, 7.0], [3, 4.0], [4, 3.0]]
        },
        "capacity": 14
    }

The format uses type indicators:

* ``"set_type": "i"`` - integer set
* ``"param_type": "d"`` - double/float parameter
* ``"key_type": "i"`` - integer index keys
* ``data`` - the actual values

For indexed parameters, data is a list of ``[key, value]`` pairs.
Scalar parameters (like ``capacity``) are just plain values.

Loading the Data
----------------

Load data from the JSON file:

.. code-block:: python

    # Load data from file
    data = smk.load_data_from_json(filename="knapsack_data.json")

    # Access data like a dictionary
    print(data["ITEMS"])      # [1, 2, 3, 4]
    print(data["capacity"])   # 14

You can also load from a JSON string or a pre-parsed dictionary:

.. code-block:: python

    # From JSON string
    data = smk.load_data_from_json(
        json_string='{"capacity": 14, "ITEMS": {"set_type": "i", "data": [1, 2, 3]}}'
    )

    # From dictionary
    data_dict = {
        "ITEMS": {"set_type": "i", "data": [1, 2, 3]},
        "capacity": 14
    }
    data = smk.load_data_from_json(packed_data=data_dict)

Using Backends
==============

Once you have a model (and optionally data), you can transform it to a backend for solving.

Pyomo Backend
-------------

Generate an in-memory Pyomo model:

.. code-block:: python

    from smoek.pymodel.pyomo import generate

    # Generate Pyomo ConcreteModel
    pyomo_model = generate(model, data=data)

    # Solve with Pyomo
    from pyomo.opt import SolverFactory
    solver = SolverFactory('glpk')
    results = solver.solve(pyomo_model)

    # Access solution
    for i in pyomo_model.ITEMS:
        print(f"x[{i}] = {pyomo_model.x[i].value}")

Coek Backend (C++ Code Generation)
-----------------------------------

Generate standalone C++ code:

.. code-block:: python

    from smoek.code.coek import generate

    # Generate C++ code
    generate(model, outfile="knapsack.cpp", data=data)

This creates a file ``knapsack.cpp`` containing C++ code that uses the Coek library
to build and solve the model. This is useful for:

* Embedding optimization in C++ applications
* High-performance model generation
* Sharing models with C++ developers

Next Steps
==========

Now that you've seen the basics, you can:

* Explore the :doc:`api` for comprehensive documentation of all components
* Check out :doc:`examples` for more complex models including facility location, nonlinear problems, and more
* Learn about different :doc:`backends` and when to use each one
* Read the :doc:`overview` for deeper understanding of smoek's architecture

Key takeaways:

1. Use ``@smk.model`` to define model structure
2. Use ``smk.range()``, ``smk.index()``, and ``.forall()`` for indexed components
3. Use ``load_data_from_json()`` to separate data from model structure
4. Transform to backends with ``generate()`` functions for solving
