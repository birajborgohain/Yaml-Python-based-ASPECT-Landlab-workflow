Setup Installation
=================================================

This guide summarizes the minimal steps required to install, configure,
and run a coupled ASPECT–Landlab simulation using Python (mpi4py).

------------------------------------------------------------
1. Python Environment (uv)
------------------------------------------------------------

Install and manage Python using ``uv``:

.. code-block:: bash

   brew install uv
   mkdir /Users/biraj/software/landlab_aspect
   cd /Users/biraj/software/landlab_aspect
   git clone --recurse-submodules https://github.com/landlab-aspect/aspect
   cd aspect
   uv venv --python 3.12
   source .venv/bin/activate
   uv sync
   uv pip install numpy meshio (optional)

------------------------------------------------------------
2. Install ASPECT with Python Support
------------------------------------------------------------

Compile ASPECT with deal.II and enable Python:

.. code-block:: bash
    
   cd /Users/biraj/software/landlab_aspect/aspect
   mkdir build
   cd build
   cmake \
     -DDEAL_II_DIR=/Users/biraj/software/dealii/dealii-9.7.1/install/deal.II-v9.7.0 \
     -DASPECT_WITH_PYTHON=ON \
     -DPython3_EXECUTABLE=$(which python) \
     ..
    make -j8
    #Done

**Critical flags:**

- ``ASPECT_WITH_PYTHON=ON`` → enables coupling
- ``Python3_EXECUTABLE`` → must point to uv/conda environment

------------------------------------------------------------
3. Coupling Mechanism (C++ ↔ Python)
------------------------------------------------------------

ASPECT uses the Landlab mesh deformation plugin:

- Loads Python module
- Calls required functions:

  - ``initialize()``
  - ``set_mesh_information()``
  - ``get_grid_x(), get_grid_y()``
  - ``update_until()``
  - ``get_initial_topography()``

Core bridge logic (C++):

- Python module imported dynamically
- MPI communicator passed to Python
- Surface nodes exchanged each timestep
- Python returns elevation change → converted to velocity

.. raw:: html

    <details>
    <summary>▶ Click to expand landlab.cc</summary>
    <div style="max-height:500px; overflow-y:auto; background:#f7f7f7;
                border:1px solid #ccc; padding:10px;
                font-family:monospace; font-size:12px; white-space:pre;">

.. literalinclude:: landlab.cc
   :language: cpp
   :linenos:

.. raw:: html

    </div>
    </details>

Reference implementation: :contentReference[oaicite:0]{index=0}

------------------------------------------------------------
4. Python Script (Landlab Side)
------------------------------------------------------------

Key structure:

.. code-block:: python

   from mpi4py import MPI
   from landlab import RasterModelGrid
   from landlab.components import LinearDiffuser

   def initialize(comm_handle):
       pass

   def set_mesh_information(_):
       model_grid = RasterModelGrid((5,5), xy_spacing=0.25)

       z = np.random.rand(model_grid.number_of_nodes)

       elevation = model_grid.add_field(
           "topographic__elevation",
           z,
           at="node"
       )

   def update_until(end_time, _):
       linear_diffuser.run_one_step(dt)
       return dz

   def get_grid_x(_): return model_grid.node_x
   def get_grid_y(_): return model_grid.node_y
   def get_initial_topography(_): return elevation

Key features:

- Raster grid must match ASPECT surface
- Returns elevation change ``dz`` (NOT absolute elevation)
- Uses ``mpi4py`` for parallel compatibility

.. raw:: html

    <style>
    details {
        margin-bottom: 20px;
    }
    details summary {
        color: #2E86C1;
        font-weight: bold;
        cursor: pointer;
    }
    details summary:hover {
        color: #1B4F72;
    }
    </style>

    <details>
    <summary>▶ Click to expand random_noise_surface_test_squar_grid.py</summary>
    <div style="max-height:500px; overflow-y:auto; background:#f7f7f7;
                border:1px solid #ccc; padding:10px;
                font-family:monospace; font-size:12px; white-space:pre;">

.. literalinclude:: random_noise_surface_test_squar_grid.py
   :language: python
   :linenos:

.. raw:: html

    </div>
    </details>



------------------------------------------------------------
5. ASPECT .prm Configuration (Essential Parts)
------------------------------------------------------------

Mesh deformation using Landlab in ASPECT:

.. code-block:: ini

   subsection Mesh deformation
     set Mesh deformation boundary indicators = top: Landlab

     subsection Landlab
       set MPI ranks for Landlab = 1
       set Script name = random_noise_surface_test_squar_grid
       set Script path = .
     end
   end

.. note:: `random_noise_surface_test_squar_grid` is the name of python script mentioned in point 4 above

Model setup (Geometry and Mesh Refinement) in ASPECT:

.. code-block:: ini

   set Dimension = 3
   set End time = 0.01
   set Maximum time step = 0.0001

   subsection Geometry model
     set Model name = box
     subsection Box
       set X extent = 1
       set Y extent = 1
       set Z extent = 1
     end
   end

  subsection Mesh refinement
    set Initial global refinement                = 2
    set Initial adaptive refinement              = 0
    set Time steps between mesh refinement       = 0
  end

.. raw:: html

    <details>
    <summary>▶ Click to expand ASPECT input random_noise_surface_test_squar_grid.prm</summary>
    <div style="max-height:500px; overflow-y:auto; background:#f7f7f7;
                border:1px solid #ccc; padding:10px;
                font-family:monospace; font-size:12px; white-space:pre;">

.. literalinclude:: random_noise_surface_test_squar_grid.prm
   :language: ini
   :linenos:

.. raw:: html

    </div>
    </details>

------------------------------------------------------------
6. Key Execution Flow
------------------------------------------------------------

1. ASPECT starts simulation
2. MPI communicator split
3. Python Landlab initialized
4. Grid points requested from Python
5. ASPECT sends surface solution fields
6. Python evolves topography (diffusion)
7. Python returns ``dz``
8. ASPECT converts to mesh velocity
9. Mesh deforms accordingly

------------------------------------------------------------
7. Important Notes
------------------------------------------------------------

- ``dz`` controls deformation → not absolute elevation
- Ensure grid consistency (ASPECT ↔ Landlab)
- MPI ranks can be split between ASPECT and Landlab
- Output debugging via VTU/VTK recommended

------------------------------------------------------------
8. Minimal Run Command
------------------------------------------------------------

.. code-block:: bash

   mpirun -np 4 ./aspect your_model.prm

------------------------------------------------------------
Summary
------------------------------------------------------------

Core requirements for coupling:

- ASPECT compiled with Python support
- Landlab Python script implementing required interface
- MPI communication via ``mpi4py``
- Proper ``.prm`` configuration linking to Python script

This setup enables dynamic surface evolution in ASPECT driven by
Landlab processes (e.g., diffusion, erosion, uplift).