ASPECT–Landlab Coupling Framework
=================================

A Python-driven workflow for coupling geodynamic simulations in
ASPECT with surface-process modeling in Landlab using YAML-based
automation, MPI parallel execution, and template-driven experiment
generation.

Overview
========

This framework integrates large-scale geodynamic simulations with
landscape evolution modeling in a reproducible and automated workflow.

The system combines:

- **ASPECT**
  
  - Finite-element geodynamics simulation
  - Lithosphere deformation and mantle convection

- **Landlab**
  
  - Surface process and landscape evolution toolkit
  - Erosion, diffusion, and topographic evolution

- **YAML-based configuration**
  
  - Centralized experiment control
  - Automated parameter sweeps

- **Python automation**
  
  - Dynamic generation of ``.prm`` and ``.py`` files
  - MPI-based execution management

The workflow is orchestrated through:

.. code-block:: text

   experiments.yaml  →  run_ASPECT.py  →  ASPECT + Landlab Coupling

This enables scalable, reproducible, and structured multi-run simulations.

Architecture
=============

.. code-block:: text

   project_root/
   ├── config/
   │   └── experiments.yaml
   ├── templates/
   │   ├── template.prm
   │   └── import-template.py
   ├── outputs/
   ├── run_ASPECT.py
   └── docs/

Main Components
================

+--------------------------+-------------------------------------------+
| Component                | Purpose                                   |
+==========================+===========================================+
| ASPECT                   | Geodynamic simulation engine              |
+--------------------------+-------------------------------------------+
| Landlab                  | Surface process and topography evolution  |
+--------------------------+-------------------------------------------+
| ``experiments.yaml``     | Central experiment configuration          |
+--------------------------+-------------------------------------------+
| ``run_ASPECT.py``        | Workflow automation and execution         |
+--------------------------+-------------------------------------------+
| Templates                | Simulation input generation               |
+--------------------------+-------------------------------------------+

Key Features
=============

Automated Workflow
-------------------

- Automatic generation of simulation directories
- Dynamic creation of ASPECT ``.prm`` files
- Dynamic creation of Landlab Python scripts
- MPI-based execution

YAML-Based Configuration
-------------------------

Experiments are controlled using a single YAML file:

.. code-block:: yaml

   runs:

     - run_id: R1
       End_time: 1e6
       diffusion: 1e-10

   constants:
     gravity_magnitude: 9.81

   aspect:
     mpi_run: mpirun
     nproc: 4
     executable: /path/to/aspect

Advantages:

- Human-readable
- Easy parameter sweeps
- Reproducible simulations
- Centralized configuration

Coupling Workflow
==================

The coupling mechanism works as follows:

.. code-block:: text

   ASPECT starts simulation
           ↓
   MPI communicator split
           ↓
   Landlab Python initialized
           ↓
   ASPECT sends surface fields
           ↓
   Landlab evolves topography
           ↓
   Landlab returns dz
           ↓
   ASPECT converts dz → mesh velocity
           ↓
   Mesh deformation updated

The Python interface uses:

- ``mpi4py``
- ``RasterModelGrid``
- Landlab components such as ``LinearDiffuser``

Installation
=============

1. Clone Repository
--------------------

.. code-block:: bash

   git clone --recurse-submodules https://github.com/landlab-aspect/aspect
   cd aspect

2. Create Python Environment
-----------------------------

Using ``uv``:

.. code-block:: bash

   brew install uv

   uv venv --python 3.12
   source .venv/bin/activate

   uv sync
   uv pip install numpy meshio mpi4py

3. Compile ASPECT with Python Support
--------------------------------------

.. code-block:: bash

   mkdir build
   cd build

   cmake \
     -DDEAL_II_DIR=/path/to/dealii \
     -DASPECT_WITH_PYTHON=ON \
     -DPython3_EXECUTABLE=$(which python) \
     ..

   make -j8

Important flags:

+----------------------------------+-----------------------+
| Flag                             | Purpose               |
+==================================+=======================+
| ``ASPECT_WITH_PYTHON=ON``        | Enables coupling      |
+----------------------------------+-----------------------+
| ``Python3_EXECUTABLE``           | Uses correct Python   |
+----------------------------------+-----------------------+

Example Landlab Coupling Script
================================

.. code-block:: python

   from mpi4py import MPI
   from landlab import RasterModelGrid
   from landlab.components import LinearDiffuser

   def initialize(comm_handle):
       pass

   def set_mesh_information(_):
       model_grid = RasterModelGrid((5,5), xy_spacing=0.25)

   def update_until(end_time, _):
       linear_diffuser.run_one_step(dt)
       return dz

   def get_grid_x(_):
       return model_grid.node_x

   def get_grid_y(_):
       return model_grid.node_y

ASPECT Configuration Example
=============================

.. code-block:: ini

   subsection Mesh deformation
     set Mesh deformation boundary indicators = top: Landlab

     subsection Landlab
       set MPI ranks for Landlab = 1
       set Script name = random_noise_surface_test_squar_grid
       set Script path = .
     end
   end

``run_ASPECT.py``
==================

The automation engine:

- Reads ``experiments.yaml``
- Generates simulation inputs
- Creates run directories
- Executes MPI simulations
- Logs outputs

Execution loop:

.. code-block:: text

   experiments.yaml
           ↓
      run_ASPECT.py
           ↓
   template.prm + template.py
           ↓
   case.prm + import.py
           ↓
      ASPECT execution
           ↓
   Landlab coupling
           ↓
         Outputs

Output Structure
=================

Each simulation run is isolated:

.. code-block:: text

   outputs/
   ├── run_001/
   │   ├── case.prm
   │   ├── import.py
   │   ├── log.txt
   │   └── solution/
   ├── run_002/
   │   └── ...

Benefits:

- Reproducibility
- Easy comparison between runs
- Organized parameter studies

Running Simulations
====================

Manual execution:

.. code-block:: bash

   mpirun -np 4 ./aspect case.prm

Automated execution:

.. code-block:: bash

   python run_ASPECT.py

Design Goals
=============

- Automated experiment generation
- Reproducible workflows
- Scalable parameter sweeps
- Flexible coupling architecture
- Minimal manual editing

Core Technologies
==================

+------------------+--------------------------------+
| Technology       | Role                           |
+==================+================================+
| Python           | Automation and coupling        |
+------------------+--------------------------------+
| YAML             | Experiment configuration       |
+------------------+--------------------------------+
| MPI (``mpi4py``) | Parallel communication         |
+------------------+--------------------------------+
| ASPECT           | Geodynamics                    |
+------------------+--------------------------------+
| Landlab          | Surface processes              |
+------------------+--------------------------------+

Future Extensions
==================

Potential additions include:

- Advanced erosion models
- Adaptive coupling strategies
- Parallel Landlab execution
- HPC workflow integration
- Machine-learning-assisted parameter exploration

References
===========

- ASPECT
  
  https://aspect.geodynamics.org

- Landlab
  
  https://landlab.readthedocs.io