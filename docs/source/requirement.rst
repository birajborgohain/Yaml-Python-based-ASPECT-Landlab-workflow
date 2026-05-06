Requirements
=======================================

Before running this project, ensure the following dependencies and setup are complete:

Install and Compile ASPECT–Landlab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You must have a working installation of:

- ASPECT (geodynamics simulation software)
- Landlab (Python surface process modeling toolkit)

Make sure:

- ASPECT is compiled with necessary plugins
- Landlab is installed in your Python environment
- Both systems are compatible for coupling

--------------------------------------------------

Required File Structure
-----------------------

The project relies on the following directory organization::

    project_root/
    │
    ├── config/
    │   └── experiments.yaml
    │
    ├── templates/
    │   ├── template.prm
    │   └── import-template.py
    │
    ├── contribution/
    │   └── script/
    │       └── python/
    │           └── landlab_template.py
    │
    ├── run_ASPECT.py
    

--------------------------------------------------

File Descriptions
~~~~~~~~~~~~~~~~~~~~

1. experiments.yaml
---------------------

Defines all simulation runs.

- Location: ``config/``
- Contains:
  
  - ``run_id`` for each experiment
  - Parameter variations (e.g., time, solver type, physics options)

Example::

    runs:
      - run_id: R1_test
        End_time: 10000
        formulation: "No Advection, iterated Stokes"

      - run_id: R2_fast
        End_time: 5000

This file acts as the **central control panel** for all experiments.

--------------------------------------------------

2. run_ASPECT.py
-------------------

Main execution script.

Responsibilities:

- Reads ``experiments.yaml``
- Parses each experiment
- Replaces placeholders in template files
- Generates run-specific ``.prm`` and ``.py`` files
- Executes ASPECT simulations

Run using::

    python run_ASPECT.py

--------------------------------------------------

3. template.prm
-----------------

ASPECT input template.

- Location: ``templates/``

Contains placeholders such as::

    set End time = {End_time}
    set Nonlinear solver scheme = {formulation}

These placeholders are replaced dynamically for each run.

--------------------------------------------------

4. import-template.py
------------------------

Landlab import template.

- Location: ``templates/``

- Defines how Landlab components are initialized
- Uses placeholders for experiment-specific values

--------------------------------------------------

5. landlab_template.py
-----------------------

Core Landlab script.

Location::

    ../aspect/contrib/script/python/

Handles:

- Surface evolution
- Coupling logic
- Interaction with ASPECT outputs

--------------------------------------------------

Workflow
~~~~~~~~~~

1. Define experiments in ``experiments.yaml``
-----------------------------------------------

2. Run the main script::
--------------------------

       python run_ASPECT.py

3. For each experiment:
-------------------------

   - A new run directory is created
   - Template files are populated
   - ASPECT simulation is executed

--------------------------------------------------

How It Works (Conceptual)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Placeholders in:

  - ``template.prm`` → ASPECT parameters  
  - ``import-template.py`` → Landlab setup  

- Values from ``experiments.yaml`` are injected into both files  

- This creates a synchronized **ASPECT–Landlab coupling environment** for each run  

--------------------------------------------------

Notes
-----

- Ensure all placeholder names in templates match keys in ``experiments.yaml``  
- Incorrect or missing keys will result in runtime errors  
- Always verify ASPECT compilation before running large batches  

--------------------------------------------------

Use Cases
-------------------

- Sensitivity analysis  
- Parameter sweeps  
- Coupled surface–tectonic modeling experiments  
- Benchmarking solver configurations  