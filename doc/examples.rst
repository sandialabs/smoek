========
Examples
========

This page provides comprehensive examples demonstrating smoek's capabilities, from simple
models to complex optimization problems.

Simple Unconstrained Problems
==============================

Example 1: Quadratic Minimization
----------------------------------

A basic model with a quadratic objective and an equality constraint:

.. code-block:: python

    import smoek as smk

    @smk.model
    class quadratic:
        x = smk.variable().value(1.0)
        y = smk.variable().value(1.0)

        o = smk.objective().minimize(x**2)
        c = smk.constraint().expr(y**2 == 4)

    model = quadratic()

This model:

* Has two continuous variables ``x`` and ``y`` with initial values of 1.0
* Minimizes ``x²``
* Subject to the constraint ``y² = 4``

The optimal solution is ``x = 0``, ``y = ±2``.

Example 2: Linear Programming
------------------------------

A simple linear objective:

.. code-block:: python

    @smk.model
    class linear:
        x = smk.variable().value(1.0)
        y = smk.variable().value(1.0)

        o = smk.objective().minimize(x)
        c = smk.constraint().expr(y**2 == 4)

    model = linear()

Here the objective is simply to minimize ``x`` (linear in ``x``).

Example 3: Nonlinear Product Objective
---------------------------------------

An objective with a product term:

.. code-block:: python

    @smk.model
    class nonlinear:
        x = smk.variable().value(1.0)
        y = smk.variable().value(1.0)

        o = smk.objective().minimize(-(x * y))
        c = smk.constraint().expr(y**2 == 4)

    model = nonlinear()

The objective ``-x·y`` is nonlinear. With the constraint ``y² = 4``, the optimal
solution depends on which root of ``y`` is chosen.

Example 4: Multiple Constraints with Bounds
--------------------------------------------

A more complex model with multiple constraints:

.. code-block:: python

    @smk.model
    class bounded:
        x = smk.variable().bounds(0, 1)
        y = smk.variable().bounds(0, 1)

        o = smk.objective().minimize(x + y)

        c1 = smk.constraint().expr(x + y == 1)
        c2 = smk.constraint().expr(2*x + y <= 1)
        c3 = smk.constraint().expr(y - 2*x >= 1)

    model = bounded()

This linear program has:

* Two variables bounded between 0 and 1
* Three constraints defining the feasible region
* Objective to minimize the sum of variables

Variable Domains and Bounds
============================

Example 5: Multiple Variable Types
-----------------------------------

Demonstrating different variable domains:

.. code-block:: python

    @smk.model
    class variable_types:
        # Integer variable bounded [0, 1]
        a = smk.variable().lower(0).upper(1).value(0).within(smk.Integers)

        # Binary variable
        b = smk.variable().lower(0).upper(1).value(0).within(smk.Binary)

        # Continuous with lower bound only
        c = smk.variable().lower(0)

        # Continuous with upper bound only
        d = smk.variable().upper(0)

        # Fixed variable
        e = smk.variable().fix(1.0)

        # Parameter
        q = smk.parameter().value(2)

        o = smk.objective().maximize(3*a + q)

        C = [
            smk.constraint().expr(3*b + q - a <= 0),
            smk.constraint().expr(3*b + b == 0),
            smk.constraint().expr(3*b*a + q + b*b + b*b == 0),
            smk.constraint().expr(3*b*b + q - a*b - a*a <= 0),
            smk.constraint().expr(smk.inequality(-7, 3*b*b + q - a*b - a*a, 7)),
            smk.constraint().expr(c + d == 0),
            smk.constraint().expr(e + 3*d == 1),
            smk.constraint().expr(smk.inequality(7, 3*b + q - a, 7)),
        ]

    model = variable_types()

This example shows:

* Integer variable with ``.within(smk.Integers)``
* Binary variable with ``.within(smk.Binary)``
* One-sided bounds using ``.lower()`` or ``.upper()``
* Fixed variables using ``.fix()``
* Range constraints using ``smk.inequality(lb, expr, ub)``

Example 6: Parameter-Based Bounds
----------------------------------

Using parameters in bounds and constraints:

.. code-block:: python

    @smk.model
    class parameter_bounds:
        x = smk.variable().lower(-1).upper(1).value(1.0)
        y = smk.variable().lower(-1).upper(2).value(2.0)
        v = smk.variable().lower(-1).upper(3).value(3.0)

        p = 2.0  # Python constant
        q = smk.parameter().value(2)  # Smoek parameter

        o = smk.objective().minimize((x**2)/p + (x**2)/q)

        c = [
            smk.constraint().expr(1/p * v * (x - y) == 2),
            smk.constraint().expr(v * 1/p * (x - y) == 2),
            smk.constraint().expr(v * (x - y) / p == 2),
            smk.constraint().expr(v * (x / p - y / p) == 2),
            smk.constraint().expr(v * (x - y) * (1/p) == 2),
            smk.constraint().expr(v * (x - y) == 2 * p),
        ]

    model = parameter_bounds()

This demonstrates using both Python constants and smoek parameters in expressions.

Indexed Models
==============

Example 7: Basic Indexing
--------------------------

Single and multi-dimensional indexing:

.. code-block:: python

    @smk.model
    class indexed:
        # Define index sets
        A = smk.range(stop=3)  # {0, 1, 2, 3}
        B = smk.range(stop=4)  # {0, 1, 2, 3, 4}

        # Define index variables
        i = smk.index()
        j = smk.index()

        # Parameters: scalar, 1D, 2D
        p = smk.parameter().value(0)
        pp = smk.parameter().index_set(A).value(0)
        ppp = smk.parameter().index_set(A).index_set(B).value(0)

        # Variables: scalar, 1D, 2D
        x = smk.variable()
        xx = smk.variable().index_set(A)
        xxx = smk.variable().index_set(A).index_set(B)

        o = smk.objective().minimize(p * x)

        # Constraints with different indexing patterns
        c = smk.constraint().expr(x == 0)
        cc = smk.constraint().expr(pp[i] * xx[i] == 0).forall(i in A)
        ccc = smk.constraint().expr(
            ppp[i, j] * xxx[i, j] == 0
        ).forall(i in A, j in B)

    model = indexed()

Key points:

* Use ``.index_set(A)`` to make a component indexed
* Chain ``.index_set()`` for multi-dimensional indexing
* Use ``.forall(i in A)`` to create constraint families
* Multiple indices: ``.forall(i in A, j in B)``

Example 8: Computed Parameter Values
-------------------------------------

Parameters whose values depend on other parameters:

.. code-block:: python

    @smk.model
    class computed_params:
        A = smk.range(stop=3)
        B = smk.range(stop=4)

        i = smk.index()
        j = smk.index()

        # Base parameter: 2D, all values = 1
        ppp = smk.parameter().index_set(A).index_set(B).value(1)

        # Computed: sum over j for each i
        pp = smk.parameter().forall(i in A).value(
            smk.sum(ppp[i, j]).forall(j in B)
        )

        # Computed: sum over all i
        p = smk.parameter().value(
            smk.sum(pp[i]).forall(i in A)
        )

        # Variables using computed parameters
        x = smk.variable().value(smk.sum(pp[i]).forall(i in A))
        xx = smk.variable().forall(i in A).value(pp[i]).lower(pp[i]).upper(pp[i])
        xxx = smk.variable().index_set(A).index_set(B)

        o = smk.objective().minimize(
            p * x + smk.sum(xx[i]).forall(i in A)
        )

        c = smk.constraint().expr(
            smk.sum(pp[i] * xx[i]).forall(i in A) == 0
        )

        cc = smk.constraint().expr(pp[i] * xx[i] == 0).forall(i in A)

        ccc = smk.constraint().expr(
            smk.sum(ppp[i, j] * xxx[i, j]).forall(i in A) == 0
        ).forall(j in B)

    model = computed_params()

This shows:

* Using ``.forall(i in A).value(expr)`` for computed parameter values
* Parameters that depend on sums of other parameters
* Variable bounds based on parameter values

Optimization Problems
=====================

Example 9: Knapsack Problem
----------------------------

The classic 0-1 knapsack problem: select items to maximize value while respecting capacity.

**Version A: Programmatic Data**

.. code-block:: python

    @smk.model
    class knapsack:
        # Problem size
        N = 10
        capacity = N / 10.0

        i = smk.index()

        # Index set {0, 1, ..., N-1}
        INDEX = smk.range(stop=N - 1)

        # Parameters: weight and value for each item
        w = smk.parameter().index_set(INDEX).value(1 / capacity)
        v = smk.parameter().index_set(INDEX).value(1)

        # Decision variables: select items (0-1)
        x = smk.variable().index_set(INDEX).bounds(0.0, 1.0)

        # Maximize total value
        o = smk.objective().maximize(
            smk.sum(v[i] * x[i]).forall(i in INDEX)
        )

        # Respect capacity constraint
        c = smk.constraint().expr(
            smk.sum(w[i] * x[i]).forall(i in INDEX) <= capacity
        )

    model = knapsack()

**Version B: Data from JSON**

For larger problems, use external data:

.. code-block:: python

    @smk.model
    class knapsack_data:
        # Abstract set - will be populated from data
        ITEMS = smk.set()
        i = smk.index()

        # Parameters from data
        value = smk.parameter().index_set(ITEMS)
        weight = smk.parameter().index_set(ITEMS)
        capacity = smk.parameter()

        # Decision variables
        x = smk.variable().index_set(ITEMS).bounds(0.0, 1.0)

        # Objective and constraint
        o = smk.objective().maximize(
            smk.sum(value[i] * x[i]).forall(i in ITEMS)
        )
        c = smk.constraint().expr(
            smk.sum(weight[i] * x[i]).forall(i in ITEMS) <= capacity
        )

    model = knapsack_data()

    # Load data from JSON
    data = smk.load_data_from_json(filename="knapsack.json")

    # Generate and solve
    from smoek.pymodel.pyomo import generate
    from pyomo.opt import SolverFactory

    pyomo_model = generate(model, data=data)
    solver = SolverFactory('glpk')
    results = solver.solve(pyomo_model)

    # Display solution
    print(f"Total value: {pyomo_model.o()}")
    for item in pyomo_model.ITEMS:
        if pyomo_model.x[item].value > 0.5:
            print(f"Select item {item}")

Example 10: P-Median Facility Location
---------------------------------------

The p-median problem: select p facilities to minimize total distance to customers.

.. code-block:: python

    def pmedian(N=10, P=3):
        @smk.model
        class pmedian:
            # N locations (potential facilities)
            # M customers (same as N in this version)
            M = N
            # P facilities to open

            n = smk.index()
            m = smk.index()

            # Index sets
            N_set = smk.range(stop=N - 1)
            M_set = smk.range(stop=M - 1)

            # Distance from location n to customer m
            d = smk.parameter().index_set(N_set).index_set(M_set)

            # Binary: is facility n serving customer m?
            x = smk.variable().index_set(N_set).index_set(M_set).bounds(0.0, 1.0)

            # Binary: is facility n open?
            y = smk.variable().index_set(N_set).bounds(0.0, 1.0)

            # Minimize total distance
            o = smk.objective().minimize(
                smk.sum(d[n, m] * x[n, m]).forall(n in N_set, m in M_set)
            )

            # Each customer served by exactly one facility
            single = smk.constraint().expr(
                smk.sum(x[n, m]).forall(n in N_set) == 1
            ).forall(m in M_set)

            # Can only serve from open facilities
            serve = smk.constraint().expr(
                x[n, m] <= y[n]
            ).forall(n in N_set, m in M_set)

            # Open exactly P facilities
            limit = smk.constraint().expr(
                smk.sum(y[n]).forall(n in N_set) == P
            )

        return pmedian()

    # Create and solve model
    model = pmedian(N=20, P=5)

    # Generate distance data
    import random
    distances = {}
    for n in range(20):
        for m in range(20):
            distances[n, m] = random.uniform(1.0, 10.0)

    # Store data
    smk.store_data_to_json(
        filename="pmedian.json",
        d=distances,
        indent=2
    )

    # Load and solve
    data = smk.load_data_from_json(filename="pmedian.json")
    from smoek.pymodel.pyomo import generate
    pyomo_model = generate(model, data=data)
    # ... solve and analyze

This example demonstrates:

* Multi-dimensional decision variables (2D)
* Multiple constraint families
* Integrality constraints (binary variables)
* Using parameters to store distance matrices

Working with External Data
===========================

Example 11: Complete Data Workflow
-----------------------------------

Creating, storing, loading, and using data:

**Step 1: Create and store data**

.. code-block:: python

    import smoek as smk
    import random

    # Generate synthetic data
    n_items = 50
    items = list(range(1, n_items + 1))

    values = {}
    weights = {}
    for i in items:
        values[i] = random.uniform(10, 100)
        weights[i] = random.uniform(1, 20)

    capacity = sum(weights.values()) * 0.3  # 30% of total weight

    # Store to JSON
    smk.store_data_to_json(
        filename="large_knapsack.json",
        ITEMS={"set_type": "i", "data": items},
        value=values,
        weight=weights,
        capacity=capacity,
        indent=2
    )

**Step 2: Define model**

.. code-block:: python

    @smk.model
    class knapsack:
        ITEMS = smk.set()
        i = smk.index()

        value = smk.parameter().index_set(ITEMS)
        weight = smk.parameter().index_set(ITEMS)
        capacity = smk.parameter()

        x = smk.variable().index_set(ITEMS).bounds(0, 1)

        o = smk.objective().maximize(
            smk.sum(value[i] * x[i]).forall(i in ITEMS)
        )

        c = smk.constraint().expr(
            smk.sum(weight[i] * x[i]).forall(i in ITEMS) <= capacity
        )

    model = knapsack()

**Step 3: Load and solve**

.. code-block:: python

    # Load data
    data = smk.load_data_from_json(filename="large_knapsack.json")

    # Verify data loaded correctly
    print(f"Number of items: {len(data['ITEMS'])}")
    print(f"Capacity: {data['capacity']}")

    # Generate backend model
    from smoek.pymodel.pyomo import generate
    pyomo_model = generate(model, data=data)

    # Solve
    from pyomo.opt import SolverFactory
    solver = SolverFactory('cbc')  # Use CBC for integer programming
    results = solver.solve(pyomo_model, tee=True)

    # Extract solution
    selected_items = [
        item for item in pyomo_model.ITEMS
        if pyomo_model.x[item].value > 0.5
    ]

    total_value = sum(
        data["value"][item] for item in selected_items
    )
    total_weight = sum(
        data["weight"][item] for item in selected_items
    )

    print(f"\nSelected {len(selected_items)} items")
    print(f"Total value: {total_value:.2f}")
    print(f"Total weight: {total_weight:.2f} / {data['capacity']:.2f}")

Advanced Expression Features
=============================

Example 12: Nonlinear Expressions
----------------------------------

Using trigonometric and nonlinear functions:

.. code-block:: python

    @smk.model
    class nonlinear:
        a = smk.variable().lower(0).upper(2).value(0).within(smk.Integers)
        b = smk.variable().lower(0).upper(1).value(0).within(smk.Binary)
        q = smk.parameter().value(2)

        # Fix variable
        b.fix(1.0)

        # Complex nonlinear expression
        e = (3*a + q + a*a*a * (-a + b + 3*a + 3*b) +
             smk.sin(-smk.cos(a)))

        o = smk.objective().minimize(e)

    model = nonlinear()

This shows:

* Polynomial expressions (``a*a*a``)
* Trigonometric functions (``sin``, ``cos``)
* Nested function calls
* Mixing variable types in expressions

Example 13: Herschel-Lawler Problem
------------------------------------

A nonlinear constrained optimization problem:

.. code-block:: python

    @smk.model
    class herschel_lawler:
        # Index set {1, 2, 3, 4} (1-based)
        N = smk.sequence(start=1, stop=4)

        x = smk.variable().index_set(N).value(2.0).bounds(-10, 10)

        # Nonlinear objective
        o = smk.objective().minimize(
            (x[1] - 1)**2 +
            (x[1] - x[2])**2 +
            (x[2] - x[3])**4
        )

        # Nonlinear constraint
        c = smk.constraint().expr(
            x[1] * (1 + x[2]**2) + x[3]**4 == 4 + 3 * smk.sqrt(2)
        )

    model = herschel_lawler()

Note the use of ``smk.sequence(start=1, stop=4)`` for 1-based indexing.

Multi-Backend Transformation
=============================

Example 14: Same Model, Multiple Backends
------------------------------------------

Demonstrating how one model can be transformed to different backends:

.. code-block:: python

    import smoek as smk

    # Define model once
    @smk.model
    class production:
        PRODUCTS = smk.set()
        p = smk.index()

        profit = smk.parameter().index_set(PRODUCTS)
        capacity = smk.parameter()
        resources = smk.parameter().index_set(PRODUCTS)

        produce = smk.variable().index_set(PRODUCTS).bounds(0, None)

        o = smk.objective().maximize(
            smk.sum(profit[p] * produce[p]).forall(p in PRODUCTS)
        )

        c = smk.constraint().expr(
            smk.sum(resources[p] * produce[p]).forall(p in PRODUCTS) <= capacity
        )

    model = production()
    data = smk.load_data_from_json(filename="production.json")

    # Transform to Pyomo
    from smoek.pymodel.pyomo import generate as pyomo_generate
    pyomo_model = pyomo_generate(model, data=data)

    from pyomo.opt import SolverFactory
    solver = SolverFactory('glpk')
    results = solver.solve(pyomo_model)
    print("Pyomo solution:", pyomo_model.o())

    # Generate C++ code for Coek
    from smoek.code.coek import generate as coek_generate
    coek_generate(model, outfile="production.cpp", data=data)
    print("Generated C++ code in production.cpp")

    # Generate Python code
    from smoek.code.pyomo import generate as pyomo_code_generate
    pyomo_code_generate(model, outfile="production_model.py", data=data)
    print("Generated Python code in production_model.py")

This demonstrates smoek's key benefit: **write once, transform to multiple backends**.

Tips for Effective Modeling
============================

1. **Use descriptive names**: Make your models self-documenting with clear variable and parameter names.

2. **Separate data from structure**: Use JSON data files for anything that might change between runs.

3. **Start simple**: Build and test with small examples before scaling to large instances.

4. **Leverage indexing**: Use indexed components and ``.forall()`` instead of creating components individually.

5. **Choose the right backend**:

   * Pyomo pymodel for rapid prototyping
   * Coek code generation for performance-critical applications

6. **Test with different data**: Abstract models should work with any compatible dataset.

7. **Use type hints in data**: The JSON schema's type metadata helps catch errors early.

8. **Version control data separately**: Keep ``.json`` data files in version control independent of code.
