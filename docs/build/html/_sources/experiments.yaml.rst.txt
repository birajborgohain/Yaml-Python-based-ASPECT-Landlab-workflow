``experiments.yaml``
=====================

YAML-Based Experiment Configuration
-------------------------------------

Overview
--------

The ASPECT–Landlab coupling framework uses a centralized configuration file written in YAML
(`experiments.yaml`) to define simulation parameters, runtime options, and experiment variations.
This file acts as the single source of truth for controlling multiple simulation runs in a
structured and scalable way.

An example configuration is shown below:

.. code-block:: yaml

   runs:

     - run_id: R1_noAdv_iterStokes_Endtime_1e6_diffusion_1e-10
       End_time: 1e6
       formulation: "no Advection, iterated Stokes"
       diffusion: 1e-10

     - run_id: R1_single_Adv_iterStokes_Endtime_5e3_diffusion_1e-15
       End_time: 5000
       formulation: "single Advection, iterated Stokes"
       diffusion: 1e-15

   constants:
     gravity_magnitude: 9.81

   aspect:
     mpi_run: /opt/homebrew/bin/mpirun
     nproc: 25
     executable: /path/to/aspect-release


What is YAML?
--------------

YAML (``YAML Ain't Markup Language``) is a human-readable data serialization format commonly used
for configuration files. It represents data using indentation-based structure rather than
brackets or tags, making it highly intuitive and easy to read.

Key features of YAML include:

- Minimal syntax with high readability
- Native support for hierarchical data
- Easy mapping to Python dictionaries
- Widely supported across scientific and software workflows


Why YAML is Chosen?
--------------------

YAML was selected as the configuration format for this framework due to the following advantages:

1. **Readability and Simplicity**
   YAML allows users to quickly understand and modify simulation parameters without needing
   programming expertise. This is particularly useful for defining multiple runs with varying
   parameters such as ``End_time``, ``formulation``, and ``diffusion``.

2. **Hierarchical Structure**
   The nested structure naturally organizes:
   
   - ``runs`` → individual simulation cases
   - ``constants`` → global parameters
   - ``aspect`` → execution settings

   This mirrors the logical structure of the simulation workflow.

3. **Seamless Python Integration**
   YAML files can be directly parsed into Python dictionaries using libraries such as
   ``PyYAML``. This allows dynamic parameter substitution in template files without complex parsing logic.

4. **Scalability**
   YAML supports defining multiple runs in a compact format, enabling parameter sweeps and
   sensitivity analyses without duplicating files.

5. **Flexibility for Placeholders**
   YAML integrates naturally with the placeholder-based templating system used in ``.prm`` and
   ``.py`` files, allowing automated generation of simulation inputs.


Alternative Formats Considered
--------------------------------

Several alternative configuration formats were considered:

- **JSON**
  
  - Pros: Strict syntax, widely supported
  - Cons: Less readable due to brackets and quotes; no comments support
  
  JSON is less suitable for scientific workflows where readability and annotation are important.

- **INI / CFG Files**
  
  - Pros: Simple key-value structure
  - Cons: Limited support for nested data and complex configurations
  
  These formats cannot naturally represent hierarchical simulation setups.

- **XML**
  
  - Pros: Highly structured and extensible
  - Cons: Verbose and difficult to read/write manually
  
  XML introduces unnecessary complexity for lightweight configuration needs.

- **Python Scripts**
  
  - Pros: Fully flexible and programmable
  - Cons: Requires coding knowledge; less transparent for non-programmers
  
  Using Python as a config format blurs the separation between configuration and execution.

**Conclusion of Comparison:**  
YAML provides the best balance between readability, structure, flexibility, and ease of integration,
making it ideal for defining multi-run geodynamic simulations.


Integration with ASPECT–Landlab Workflow
-----------------------------------------

The YAML configuration file is tightly integrated into the automated simulation pipeline:

1. **Parsing (run_ASPECT.py)**

   - The script ``run_ASPECT.py`` reads ``experiments.yaml`` using Python.
   - Each entry under ``runs`` is interpreted as a separate simulation case.
   - Global parameters from ``constants`` and execution settings from ``aspect`` are also loaded.

2. **Template Substitution (.prm and .py)**

   - Template files (``template.prm`` and Landlab ``.py`` scripts) contain placeholders.
   - These placeholders correspond to keys in the YAML file.
   - During runtime, placeholders are replaced with actual values from YAML.

   Example:

   .. code-block:: text

      set End time = {End_time}
      set Formulation = {formulation}

3. **Run Directory Generation**

   - For each ``run_id``, a dedicated simulation directory is created.
   - Generated files include:
     
     - Modified ``.prm`` file (ASPECT input)
     - Modified Landlab ``.py`` script
     - Output directories for ASPECT and surface processes

4. **Execution**

   - ``run_ASPECT.py`` constructs the MPI command using:

     - ``mpi_run``
     - ``nproc``
     - ``executable``

   - ASPECT is executed for each run using the generated ``.prm`` file.
   - Landlab is coupled through the generated Python script.


Final Outcome
-------------

This YAML-driven approach enables:

- Automated generation of multiple simulation scenarios
- Consistent parameter management across ASPECT and Landlab
- Reproducible and scalable workflows
- Clear separation between configuration and execution

As a result, complex coupled geodynamic–surface process simulations can be executed efficiently
with minimal manual intervention.