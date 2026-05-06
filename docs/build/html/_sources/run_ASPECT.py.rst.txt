``run_ASPECT.py``
==================

Run Automation Script (run_ASPECT.py)
---------------------------------------

Overview
~~~~~~~~~

The ``run_ASPECT.py`` script is the core execution engine of the ASPECT–Landlab
coupling framework. It automates the entire workflow from reading experiment
configurations to generating input files and executing simulations.

The script is designed to:

- Parse experiment definitions from a YAML configuration file
- Generate ASPECT (``.prm``) and Landlab (``.py``) input files using templates
- Create structured output directories for each simulation
- Execute ASPECT in parallel using MPI
- Log outputs for reproducibility and debugging

This approach enables scalable and reproducible multi-run simulations.


Directory Structure 
~~~~~~~~~~~~~~~~~~~~

The script assumes the following project structure:

.. code-block:: text

   project_root/
   ├── config/
   │   └── experiments.yaml
   ├── templates/
   │   ├── template.prm
   │   └── import-template.py
   ├── outputs/
   └── run_ASPECT.py



.. figure:: /_images/run_ASPECT.py_high_level.png
    :width: 1000px
    :align: center



Key Components
--------------

Path Configuration
~~~~~~~~~~~~~~~~~~

The script dynamically determines paths relative to its own location:

- ``BASE_DIR``: Root directory of the project
- ``CONFIG_PATH``: YAML configuration file
- ``TEMPLATE_PRM_PATH``: ASPECT template file
- ``TEMPLATE_PY_PATH``: Landlab template script
- ``OUTPUT_BASE``: Directory where simulation outputs are stored

This ensures portability and avoids hardcoded paths.


.. figure:: /_images/High_level_run_ASPECT.png
    :width: 1000px
    :align: center


Configuration Loader, Loop and Final Output
-----------------------------------------------

All experiment settings are defined in a YAML file, which 
Python reads and processes to automatically generate input 
files (``.prm`` and ``.py``), create run directories, and 
execute simulations. This eliminates manual editing, enables 
efficient parameter sweeps, and ensures reproducible, scalable 
workflows.

.. figure:: /_images/render_YAML_loop_python_ASPECT.png
    :width: 1000px
    :align: center



.. code-block:: python

   def load_config(path):

This function:

- Validates the existence of the YAML file
- Loads the configuration using ``yaml.safe_load``
- Returns a Python dictionary representation

It provides a clean abstraction for reading experiment definitions.


Template Rendering System
~~~~~~~~~~~~~~~~~~~~~~~~~

The script uses a lightweight placeholder replacement mechanism.

**Sanitization**

.. code-block:: python

   def sanitize(value):

- Converts values to strings
- Replaces spaces and special characters
- Ensures safe file and directory naming

**Safe Rendering**

.. code-block:: python

   def safe_render(template_text, context):

- Replaces placeholders of the form ``{key}``
- Uses values from a combined context dictionary
- Leaves unknown placeholders unchanged

This avoids runtime failures due to missing keys and allows flexible templates.


Main Execution Workflow
-------------------------

The ``run_all()`` function orchestrates the complete workflow:

1. Load Configuration
~~~~~~~~~~~~~~~~~~~~~

- Reads ``experiments.yaml``
- Extracts:

  - ``runs``: Individual simulation cases
  - ``constants``: Global parameters
  - ``aspect``: Execution settings (MPI, executable)

2. Read Templates
~~~~~~~~~~~~~~~~~

- Loads:

  - ``template.prm`` (ASPECT input)
  - ``import-template.py`` (Landlab coupling script)

3. Prepare Execution Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- MPI command (``mpi_run``)
- Number of processes (``nproc``)
- ASPECT executable path

4. Loop Over Simulation Runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each entry in ``runs``:

- Validate ``run_id``
- Create a dedicated output directory:

  .. code-block:: text

     outputs/<run_id>/

- Merge parameters:

  .. code-block:: python

     context = {**constants, **run}

- Render templates into:

  - ``case.prm``
  - ``import.py``

5. Environment Setup
~~~~~~~~~~~~~~~~~~~~~

The script modifies the runtime environment:

.. code-block:: python

   env["PYTHONPATH"] = ASPECT_PYTHON_SCRIPTS + ...

This ensures that ASPECT can access required Python modules for coupling.


6. Simulation Execution
~~~~~~~~~~~~~~~~~~~~~~~~

Each simulation is executed using ``subprocess.run``:

.. code-block:: text

   mpirun -np <nproc> aspect case.prm

Key features:

- Runs inside the respective output directory
- Redirects stdout and stderr to ``log.txt``
- Uses ``check=True`` to detect failures


7. Logging and Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Output logs are saved per run:

  .. code-block:: text

     outputs/<run_id>/log.txt

- Failed runs are:

  - Reported to the console
  - Skipped without stopping the entire workflow

This ensures robustness for batch simulations.


Design Highlights
~~~~~~~~~~~~~~~~~~~

**1. Automation**

- Eliminates manual editing of ``.prm`` and ``.py`` files
- Supports large parameter sweeps

**2. Reproducibility**

- Each run is isolated in its own directory
- Logs and inputs are preserved

**3. Flexibility**

- Easily extendable via YAML configuration
- Template-driven system supports new parameters without code changes

**4. Fault Tolerance**

- Individual run failures do not interrupt the full batch


Integration in Coupling Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The script acts as the bridge between configuration and execution:

.. code-block:: text

   experiments.yaml
           ↓
      run_ASPECT.py
           ↓
   template.prm + template.py
           ↓
   case.prm + import.py (per run)
           ↓
      ASPECT execution (MPI)
           ↓
   Landlab coupling via Python
           ↓
         Outputs


Final Remarks
-------------

The ``run_ASPECT.py`` script provides a scalable and modular solution for
running coupled geodynamic–surface process simulations. By combining YAML-based
configuration, template-driven file generation, and automated execution, it
enables efficient exploration of complex parameter spaces with minimal user effort.