Metrics
=======

The ``Argenta`` metrics system provides tools for measuring the performance of key library components. This allows tracking performance regression/progression between releases and optimizing critical code sections.

-----

Running Metrics
---------------

To work with metrics, you need to clone the repository and install dependencies:

.. code-block:: bash

   git clone https://github.com/koloideal/Argenta.git
   cd Argenta
   uv sync --group metrics

Running the metrics system:

.. code-block:: bash

   python -m metrics

After launch, an interactive session will open with available commands for working with benchmarks.

-----

Available Commands
------------------

run-all
~~~~~~~

Runs all registered benchmarks and outputs results as tables.

**Syntax:**

.. code-block:: shell

   run-all [--without-gc] [--without-system-info]

**Flags:**

- ``--without-gc`` — disables garbage collector during benchmark execution for more stable results
- ``--without-system-info`` — hides system information in output

-----

list-types
~~~~~~~~~~

Displays a list of all available benchmark types with the number of tests in each category.

**Syntax:**

.. code-block:: shell

   list-types

**Example output:**

.. code-block:: text

   Available benchmark types:

     • app_startup (5 benchmarks)
     • command_autocomplete (3 benchmarks)
     • command_dispatch (3 benchmarks)
     • command_groups_render (2 benchmarks)
     • command_history_completion (4 benchmarks)
     • finds_appropriate_handler (5 benchmarks)
     • flag_validation (9 benchmarks)
     • input_command_parse (7 benchmarks)
     • most_similar_command (5 benchmarks)
     • validate_routers_for_collisions (5 benchmarks)

-----

run-type
~~~~~~~~

Runs benchmarks of a specific type.

**Syntax:**

.. code-block:: shell

   run-type --type <type_name> [--without-gc] [--without-system-info]

**Flags:**

- ``--type`` — benchmark type to run (required)
- ``--without-gc`` — disables garbage collector
- ``--without-system-info`` — hides system information

-----

diagrams-generate
~~~~~~~~~~~~~~~~~

Generates visual performance comparison diagrams for all benchmarks.

**Syntax:**

.. code-block:: shell

   diagrams-generate [--iterations <number>] [--without-gc]

**Flags:**

- ``--iterations`` — number of iterations for each benchmark (default 100)
- ``--without-gc`` — disables garbage collector

Diagrams are saved to the ``metrics/reports/diagrams/<timestamp>/`` directory.

-----

release-generate
~~~~~~~~~~~~~~~~

Generates a complete performance report for the current library version. Used when preparing releases.

**Syntax:**

.. code-block:: shell

   release-generate

The command automatically:

1. Determines the current library version
2. Runs all benchmarks with 1000 iterations and disabled GC
3. Generates JSON reports and comparison diagrams
4. Saves results to ``metrics/reports/releases/<version>/``

-----

Interpreting Results
--------------------

Benchmark results include the following metrics:

**Mean time (mean)**
  Average operation execution time. The primary metric for performance comparison.

**Median (median)**
  Median execution time value. Less sensitive to outliers than the mean.

**Standard deviation (std)**
  Shows measurement stability. A lower value means more predictable performance.

-----

Usage Recommendations
---------------------

**History completion**
  The ``command_history_completion`` benchmarks use temporary, synthetic file histories
  with 1,000, 10,000 and 100,000 entries. Background loading and the initial completion
  happen before timing starts. These measure repeated completion requests in a running
  session, including a prefix with one match; they do not measure startup or disk loading.

**For optimization**
  Use ``run-type`` to focus on a specific area and ``--without-gc`` for more accurate measurements.

**For visualization**
  The ``diagrams-generate`` command creates clear charts suitable for presentations and documentation.

**For stable results**
  Close resource-intensive applications, use the ``--without-gc`` flag, and increase the number of iterations via ``--iterations``.

-----

Adding New Benchmarks
---------------------

You can implement your own benchmarks to test specific library units. New benchmarks are added via the ``@benchmarks.register`` decorator:

.. literalinclude:: ../code_snippets/metrics/add_new_benchmark.py
   :language: python
   :linenos:

.. important::

  The benchmark must be imported in ``metrics/benchmarks/__init__.py`` for automatic registration.

-----

Continuous Benchmarking
-----------------------

The ``ci-benchmarks`` workflow compares every pull request that touches ``src/`` or ``metrics/`` against ``main`` and posts the result as a single, self-updating comment on the pull request.

Both versions of the library are installed side by side on the same runner, and all registered benchmarks are run against them in interleaved rounds. Each benchmark is timed in batches with the garbage collector disabled; the reported value is the median of the per-round best times.

.. important::

  Absolute times are specific to the CI runner that produced them (its CPU is shown in the comment footer). Compare the ``main`` and ``this branch`` columns within one report; do not compare absolute values between different reports. Changes within ±10% are treated as noise.

To produce the same report locally, install both versions into separate virtual environments and run:

.. code-block:: bash

   python -m metrics.ci.compare \
       --base-python .venv-base/bin/python \
       --head-python .venv-head/bin/python \
       --output report.md
