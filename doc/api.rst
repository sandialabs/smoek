=============
API Reference
=============

This page provides a comprehensive reference for smoek's user-facing API, organized by functionality.

Model Definition
================

@model
------

The ``@model`` decorator is the primary way to define optimization models in smoek.

.. code-block:: python

    @smk.model
    class my_model:
        # Define model components here
        x = smk.variable()
        o = smk.objective().minimize(x**2)

The decorator transforms a class definition into a model template. When you instantiate
the class, you get a concrete model object:

.. code-block:: python

    model = my_model()

You can optionally provide a name:

.. code-block:: python

    @smk.model(name="custom_name")
    class my_model:
        x = smk.variable()

Model
-----

The ``Model`` class can also be used directly, though the decorator syntax is more common:

.. code-block:: python

    m = smk.Model()
    # Add components to m

Variables
=========

variable()
----------

Create a decision variable for your optimization model.

**Basic usage:**

.. code-block:: python

    x = smk.variable()

**Methods:**

``.value(val)``
    Set the initial value for the variable.

    .. code-block:: python

        x = smk.variable().value(1.0)

``.lower(lb)``
    Set the lower bound.

    .. code-block:: python

        x = smk.variable().lower(0.0)  # x >= 0

``.upper(ub)``
    Set the upper bound.

    .. code-block:: python

        x = smk.variable().upper(10.0)  # x <= 10

``.bounds(lb, ub)``
    Set both lower and upper bounds.

    .. code-block:: python

        x = smk.variable().bounds(0.0, 1.0)  # 0 <= x <= 1

``.within(domain)``
    Specify the variable domain (see Variable Domains below).

    .. code-block:: python

        x = smk.variable().within(smk.Integers)
        y = smk.variable().within(smk.Binary)

``.fix(val)``
    Fix the variable to a constant value.

    .. code-block:: python

        x = smk.variable().fix(5.0)  # x is fixed at 5.0

``.fixed(is_fixed)``
    Alternative way to fix a variable.

    .. code-block:: python

        x = smk.variable().value(5.0).fixed(True)

``.index_set(set)``
    Make the variable indexed over a set. Can be chained for multi-dimensional indexing.

    .. code-block:: python

        A = smk.range(stop=10)
        x = smk.variable().index_set(A)  # x[0], x[1], ..., x[10]

        # Multi-dimensional
        B = smk.range(stop=5)
        y = smk.variable().index_set(A).index_set(B)  # y[i, j]

``.forall(index in set)``
    Alternative syntax for indexed variables.

    .. code-block:: python

        i = smk.index()
        A = smk.range(stop=10)
        x = smk.variable().forall(i in A).value(0.0)

**Chaining methods:**

Methods can be chained together:

.. code-block:: python

    x = smk.variable().lower(0).upper(10).value(5.0).within(smk.Integers)

binary_variable()
-----------------

Convenience function to create a binary (0-1) variable:

.. code-block:: python

    x = smk.binary_variable()

    # Equivalent to:
    x = smk.variable().within(smk.Binary)

Variable Domains
----------------

Use these domain specifiers with ``.within()`` to constrain variable types:

**Continuous domains:**

``smk.Reals``
    Real-valued variables (default, no restriction)

``smk.PositiveReals``
    Positive real values (x > 0)

``smk.NegativeReals``
    Negative real values (x < 0)

**Integer domains:**

``smk.Integers``
    Integer-valued variables

``smk.PositiveIntegers``
    Positive integers (x > 0)

``smk.NegativeIntegers``
    Negative integers (x < 0)

``smk.NonNegativeIntegers``
    Non-negative integers (x >= 0)

``smk.NonPositiveIntegers``
    Non-positive integers (x <= 0)

**Binary domain:**

``smk.Binary``
    Binary variables (x ∈ {0, 1})

**Example:**

.. code-block:: python

    a = smk.variable().within(smk.Integers).bounds(0, 10)
    b = smk.variable().within(smk.Binary)
    c = smk.variable().within(smk.PositiveReals).upper(100)

Parameters and Data
===================

parameter()
-----------

Create a parameter (fixed input value) for your model.

**Basic usage:**

.. code-block:: python

    p = smk.parameter().value(42)

**Methods:**

``.value(val)``
    Set the parameter value. For indexed parameters, can be a constant or expression.

    .. code-block:: python

        p = smk.parameter().value(10.0)

        # Indexed parameter with constant value
        A = smk.range(stop=5)
        p = smk.parameter().index_set(A).value(1.0)

        # Computed value using other parameters
        i = smk.index()
        q = smk.parameter().index_set(A)
        p = smk.parameter().forall(i in A).value(2 * q[i])

``.index_set(set)``
    Make the parameter indexed over a set.

    .. code-block:: python

        A = smk.range(stop=10)
        p = smk.parameter().index_set(A)

``.forall(index in set)``
    Alternative syntax for indexed parameters with computed values.

    .. code-block:: python

        i = smk.index()
        A = smk.range(stop=5)
        B = smk.range(stop=3)
        j = smk.index()

        ppp = smk.parameter().index_set(A).index_set(B).value(1)
        pp = smk.parameter().forall(i in A).value(
            smk.sum(ppp[i, j]).forall(j in B)
        )

data()
------

Alias for ``parameter()``. Use ``data()`` to emphasize that a parameter represents
fixed data rather than a mutable parameter:

.. code-block:: python

    capacity = smk.data().value(100)

Sets and Indices
================

index()
-------

Create an index variable for iterating over sets:

.. code-block:: python

    i = smk.index()
    j = smk.index()

    # Use in expressions
    A = smk.range(stop=10)
    x = smk.variable().index_set(A)
    total = smk.sum(x[i]).forall(i in A)

set()
-----

Create an abstract set that will be populated from data:

.. code-block:: python

    ITEMS = smk.set()

    # Use with indexed components
    x = smk.variable().index_set(ITEMS)
    p = smk.parameter().index_set(ITEMS)

index_set()
-----------

Alias for ``set()``:

.. code-block:: python

    NODES = smk.index_set()

range()
-------

Create a numeric range set. Note: the range is **inclusive** of the stop value.

**Single argument (stop):**

.. code-block:: python

    A = smk.range(stop=5)  # Creates {0, 1, 2, 3, 4, 5}

**Two arguments (start, stop):**

.. code-block:: python

    A = smk.range(start=1, stop=5)  # Creates {1, 2, 3, 4, 5}

**Note:** This differs from Python's ``range()``, which excludes the stop value.

sequence()
----------

Create a sequence with explicit start and stop (1-based, inclusive):

.. code-block:: python

    S = smk.sequence(start=1, stop=4)  # Creates {1, 2, 3, 4}

Constraints
===========

constraint()
------------

Create a constraint in your model.

**Basic usage:**

.. code-block:: python

    c = smk.constraint().expr(x + y <= 10)

**Methods:**

``.expr(expression)``
    Set the constraint expression. The expression should be a comparison:

    * Equality: ``expr1 == expr2``
    * Less than or equal: ``expr1 <= expr2``
    * Greater than or equal: ``expr1 >= expr2``
    * Range: ``smk.inequality(lb, expr, ub)``

    .. code-block:: python

        c1 = smk.constraint().expr(x + y == 10)
        c2 = smk.constraint().expr(x <= y)
        c3 = smk.constraint().expr(2*x + 3*y >= 15)

``.forall(index in set)``
    Create an indexed family of constraints:

    .. code-block:: python

        i = smk.index()
        A = smk.range(stop=10)
        x = smk.variable().index_set(A)
        p = smk.parameter().index_set(A)

        # Create constraint for each i in A
        c = smk.constraint().expr(x[i] <= p[i]).forall(i in A)

**Multiple indices:**

.. code-block:: python

    i, j = smk.index(), smk.index()
    A = smk.range(stop=5)
    B = smk.range(stop=3)
    y = smk.variable().index_set(A).index_set(B)

    c = smk.constraint().expr(y[i, j] >= 0).forall(i in A, j in B)

inequality()
------------

Create a range constraint with both lower and upper bounds:

.. code-block:: python

    # -7 <= 3*x + 2*y <= 7
    c = smk.constraint().expr(
        smk.inequality(-7, 3*x + 2*y, 7)
    )

This is more concise than creating two separate constraints.

Objectives
==========

objective()
-----------

Define the objective function for your model.

**Methods:**

``.minimize(expr)``
    Minimize the given expression:

    .. code-block:: python

        o = smk.objective().minimize(x**2 + y**2)

``.maximize(expr)``
    Maximize the given expression:

    .. code-block:: python

        o = smk.objective().maximize(profit - cost)

``.expr(expression)``
    Set the objective expression (must then specify sense separately):

    .. code-block:: python

        o = smk.objective().expr(x + y)

``.sense(sense)``
    Set optimization sense: ``True`` for minimize, ``False`` for maximize:

    .. code-block:: python

        o = smk.objective().expr(x + y).sense(True)  # minimize

**Note:** Typically you use either ``.minimize()`` or ``.maximize()`` directly, which
sets both the expression and sense in one call.

Mathematical Expressions
========================

Arithmetic Operators
--------------------

Standard Python operators work with smoek expressions:

.. code-block:: python

    # Addition, subtraction
    expr1 = x + y
    expr2 = x - y

    # Multiplication, division
    expr3 = 3 * x
    expr4 = x / 2

    # Exponentiation
    expr5 = x**2
    expr6 = (x + y)**3

sum()
-----

Sum an expression over an index set:

.. code-block:: python

    i = smk.index()
    A = smk.range(stop=10)
    x = smk.variable().index_set(A)
    c = smk.parameter().index_set(A)

    # Sum of c[i] * x[i] for all i in A
    total = smk.sum(c[i] * x[i]).forall(i in A)

**Multiple indices:**

.. code-block:: python

    i, j = smk.index(), smk.index()
    A = smk.range(stop=5)
    B = smk.range(stop=3)
    y = smk.variable().index_set(A).index_set(B)

    # Sum over both indices
    total = smk.sum(y[i, j]).forall(i in A, j in B)

prod()
------

Product of an expression over an index set:

.. code-block:: python

    # Product of x[i] for all i in A
    product = smk.prod(x[i]).forall(i in A)

Syntax is identical to ``sum()``.

forall()
--------

The ``forall()`` quantifier is used with ``sum()``, ``prod()``, and ``.forall()`` methods
to specify iteration over index sets.

**Basic syntax:**

.. code-block:: python

    smk.sum(expr).forall(i in A)
    smk.constraint().expr(expr).forall(i in A)

**Multiple indices:**

.. code-block:: python

    smk.sum(expr).forall(i in A, j in B)
    smk.constraint().expr(expr).forall(i in A, j in B, k in C)

Mathematical Functions
----------------------

Smoek provides standard mathematical functions:

**Trigonometric:**

.. code-block:: python

    smk.sin(x)
    smk.cos(x)
    smk.tan(x)

**Other functions:**

.. code-block:: python

    smk.log(x)      # Natural logarithm
    smk.sqrt(x)     # Square root

**Example:**

.. code-block:: python

    o = smk.objective().minimize(
        smk.sin(x) + smk.cos(y) + smk.log(z + 1)
    )

Data Loading and Storage
========================

load_data_from_json()
---------------------

Load data from JSON format into a DataPortal object.

**Function signature:**

.. code-block:: python

    load_data_from_json(
        filename=None,
        packed_data=None,
        json_string=None,
        schema="coek",
        lazyload=False
    )

**Parameters:**

``filename`` : str, optional
    Path to a JSON file containing model data.

``packed_data`` : dict, optional
    Dictionary with data in the packed format (see JSON Schema Format below).

``json_string`` : str, optional
    JSON string to parse.

``schema`` : str, default="coek"
    Schema format to use. Currently only "coek" is supported.

``lazyload`` : bool, default=False
    If True, delay loading data until accessed. If False, load immediately.

**Returns:**

``JsonDataPortal`` object that provides dictionary-like access to the data.

**Examples:**

Load from file:

.. code-block:: python

    data = smk.load_data_from_json(filename="model_data.json")

Load from JSON string:

.. code-block:: python

    json_str = '{"capacity": 100, "ITEMS": {"set_type": "i", "data": [1, 2, 3]}}'
    data = smk.load_data_from_json(json_string=json_str)

Load from dictionary:

.. code-block:: python

    data_dict = {
        "ITEMS": {"set_type": "i", "data": [1, 2, 3, 4]},
        "capacity": 14
    }
    data = smk.load_data_from_json(packed_data=data_dict)

Access data:

.. code-block:: python

    print(data["ITEMS"])     # [1, 2, 3, 4]
    print(data["capacity"])  # 14

store_data_to_json()
--------------------

Store data to a JSON file.

**Function signature:**

.. code-block:: python

    store_data_to_json(
        filename=None,
        schema="coek",
        indent=None,
        **kwargs
    )

**Parameters:**

``filename`` : str, optional
    Path where the JSON file should be written.

``schema`` : str, default="coek"
    Schema format to use.

``indent`` : int, optional
    Number of spaces for JSON indentation (for pretty printing).

``**kwargs``
    Keyword arguments where each key-value pair represents a data element.
    Keys become parameter/set names, values are the data.

**Examples:**

Store simple data:

.. code-block:: python

    smk.store_data_to_json(
        filename="output.json",
        capacity=100,
        num_items=5,
        indent=2
    )

Store indexed data:

.. code-block:: python

    # Create indexed data
    costs = {}
    for i in range(10):
        costs[i] = i * 1.5

    smk.store_data_to_json(
        filename="costs.json",
        costs=costs,
        indent=2
    )

JsonDataPortal / DataPortal
----------------------------

The data portal classes provide dictionary-like access to model data.

**Accessing data:**

.. code-block:: python

    data = smk.load_data_from_json(filename="data.json")

    # Dictionary-style access
    items = data["ITEMS"]
    capacity = data["capacity"]
    values = data["value"]

**Methods:**

``.is_set(name)``
    Check if a name corresponds to a set:

    .. code-block:: python

        if data.is_set("ITEMS"):
            print("ITEMS is a set")

``.is_parameter(name)``
    Check if a name corresponds to a parameter:

    .. code-block:: python

        if data.is_parameter("capacity"):
            print("capacity is a parameter")

``.parameters()``
    Iterate over parameter names:

    .. code-block:: python

        for param_name in data.parameters():
            print(param_name, data[param_name])

``.sets()``
    Iterate over set names:

    .. code-block:: python

        for set_name in data.sets():
            print(set_name, data[set_name])

``.load(filename)``
    Load data from a file:

    .. code-block:: python

        data = smk.JsonDataPortal()
        data.load("data.json")

``.store(filename, indent=None)``
    Save data to a file:

    .. code-block:: python

        data.store("output.json", indent=2)

JSON Schema Format
------------------

The Coek JSON schema uses type metadata to describe sets and parameters.

**Type indicators:**

* ``"i"`` - integer
* ``"d"`` - double/float
* ``"s"`` - string

**Sets:**

Sets use ``set_type`` to indicate element type:

.. code-block:: json

    {
        "ITEMS": {
            "set_type": "i",
            "data": [1, 2, 3, 4]
        }
    }

**Indexed parameters:**

Indexed parameters specify ``param_type`` (value type) and ``key_type`` (index type):

.. code-block:: json

    {
        "cost": {
            "param_type": "d",
            "key_type": "i",
            "data": [[1, 10.5], [2, 15.3], [3, 8.7]]
        }
    }

The ``data`` is a list of ``[key, value]`` pairs.

**Multi-dimensional indexed parameters:**

For parameters indexed by multiple sets, use ``key_type`` as a list:

.. code-block:: json

    {
        "distance": {
            "param_type": "d",
            "key_type": ["i", "i"],
            "data": [
                [[1, 2], 10.5],
                [[1, 3], 15.3],
                [[2, 3], 8.7]
            ]
        }
    }

**Scalar parameters:**

Scalar values are stored directly:

.. code-block:: json

    {
        "capacity": 100,
        "budget": 5000.0,
        "name": "problem1"
    }

**Complete example:**

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

This example defines:

* A set ``ITEMS`` with integer elements {1, 2, 3, 4}
* An indexed parameter ``value`` mapping items to float values
* An indexed parameter ``weight`` mapping items to float weights
* A scalar parameter ``capacity`` with value 14

Utilities
=========

expr_to_string()
----------------

Convert an expression to a string representation:

.. code-block:: python

    expr = x**2 + 2*y
    s = smk.expr_to_string(expr)
    print(s)

expr_to_list()
--------------

Convert an expression to a list representation (useful for programmatic manipulation):

.. code-block:: python

    expr = x + y
    lst = smk.expr_to_list(expr)

model_to_dict()
---------------

Convert a model to a dictionary representation:

.. code-block:: python

    model = my_model()
    d = smk.model_to_dict(model)

collect_info()
--------------

Collect information about model components:

.. code-block:: python

    model = my_model()
    info = smk.collect_info(model)

valid_order()
-------------

Validate and get the declaration order of model components:

.. code-block:: python

    info = smk.collect_info(model)
    order = smk.valid_order(info)
