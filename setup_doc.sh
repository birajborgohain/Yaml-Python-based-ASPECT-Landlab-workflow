#!/usr/bin/env bash

set -e

DOCS_DIR="docs"

echo "📁 Creating Sphinx documentation with starter content..."

# -----------------------------
# Create docs directory
# -----------------------------
mkdir -p $DOCS_DIR
cd $DOCS_DIR

# -----------------------------
# Initialize Sphinx
# -----------------------------
sphinx-quickstart -q \
  -p "ASPECT–Landlab Framework" \
  -a "Author" \
  -v "1.0" \
  --sep \
  --makefile \
  --batchfile

cd source

# -----------------------------
# Create folder structure
# -----------------------------
echo "📂 Creating folder structure..."

mkdir -p configuration coupling modules outputs examples testing demonstration developer appendix
mkdir -p config images scripts

# -----------------------------
# index.rst
# -----------------------------
cat > index.rst << 'EOF'
ASPECT–Landlab Coupled Modeling Framework
=========================================

A Python-based framework for coupling geodynamic simulations 
(ASPECT) with surface process modeling (Landlab).

.. toctree::
   :maxdepth: 2

   introduction
   quickstart
   installation
   workflow
   architecture

   configuration/yaml_config
   configuration/prm_template

   coupling/aspect_landlab
   coupling/import_template

   modules/runner
   modules/prm_writer
   modules/landlab_model

   outputs/output_files
   outputs/visualization

   examples/basic_run

   testing/validation

   demonstration/live_demo
EOF

# -----------------------------
# introduction.rst
# -----------------------------
cat > introduction.rst << 'EOF'
Introduction
============

This project integrates ASPECT (geodynamics) with Landlab (surface processes)
through a Python-based workflow.

Core Integration Files
----------------------

+----------------------+----------------------+---------------------------------------------+
| File                 | Role                 | Description                                 |
+======================+======================+=============================================+
| experiments.yaml     | Configuration        | Defines simulation runs                     |
+----------------------+----------------------+---------------------------------------------+
| template.prm         | ASPECT input         | Simulation parameters                       |
+----------------------+----------------------+---------------------------------------------+
| import-template.py   | Coupling interface   | Connects ASPECT with Landlab                |
+----------------------+----------------------+---------------------------------------------+
| run_ASPECT.py        | Execution script     | Runs full workflow                          |
+----------------------+----------------------+---------------------------------------------+
EOF

# -----------------------------
# quickstart.rst
# -----------------------------
cat > quickstart.rst << 'EOF'
Quick Start
===========

Run a simple simulation:

.. code-block:: bash

    python src/run_ASPECT.py

Outputs will be generated automatically.
EOF

# -----------------------------
# installation.rst
# -----------------------------
cat > installation.rst << 'EOF'
Installation
============

Install dependencies:

.. code-block:: bash

    pip install -r requirements.txt

Ensure ASPECT is installed and accessible:

.. code-block:: bash

    aspect --version
EOF

# -----------------------------
# workflow.rst
# -----------------------------
cat > workflow.rst << 'EOF'
Workflow
========

Pipeline:

YAML → PRM → ASPECT → Landlab → VTK

Steps:

1. Define experiment (YAML)
2. Generate .prm file
3. Run ASPECT
4. Apply Landlab evolution
5. Export outputs
EOF

# -----------------------------
# architecture.rst
# -----------------------------
cat > architecture.rst << 'EOF'
Architecture
============

Components:

- Configuration layer (YAML)
- Execution layer (Python)
- Simulation layer (ASPECT)
- Surface layer (Landlab)

Design Principles:

- Modular
- Reproducible
- Extensible
EOF

# -----------------------------
# configuration
# -----------------------------
cat > configuration/yaml_config.rst << 'EOF'
YAML Configuration
==================

Defines simulation runs and parameters.

Example:

.. code-block:: yaml

    runs:
      - run_id: demo
        End_time: 1000
EOF

cat > configuration/prm_template.rst << 'EOF'
PRM Template
============

Template for ASPECT simulation input.

Parameters are dynamically injected.
EOF

# -----------------------------
# coupling
# -----------------------------
cat > coupling/aspect_landlab.rst << 'EOF'
ASPECT–Landlab Coupling
=======================

ASPECT computes geodynamic evolution.
Landlab updates surface processes based on output.
EOF

cat > coupling/import_template.rst << 'EOF'
Import Template
===============

This script connects ASPECT outputs to Landlab inputs.
EOF

# -----------------------------
# modules
# -----------------------------
cat > modules/runner.rst << 'EOF'
Runner Module
=============

Controls execution of simulations and workflow management.
EOF

cat > modules/prm_writer.rst << 'EOF'
PRM Writer
==========

Generates ASPECT .prm files dynamically.
EOF

cat > modules/landlab_model.rst << 'EOF'
Landlab Model
=============

Handles surface evolution modeling.
EOF

# -----------------------------
# outputs
# -----------------------------
cat > outputs/output_files.rst << 'EOF'
Outputs
=======

Generated outputs include:

- VTK files
- Logs
- Simulation data
EOF

cat > outputs/visualization.rst << 'EOF'
Visualization
=============

Use ParaView:

.. code-block:: bash

    paraview output.pvd
EOF

# -----------------------------
# examples
# -----------------------------
cat > examples/basic_run.rst << 'EOF'
Basic Example
=============

Run:

.. code-block:: bash

    python src/run_ASPECT.py
EOF

# -----------------------------
# testing
# -----------------------------
cat > testing/validation.rst << 'EOF'
Validation
==========

Ensure:

- Simulation runs successfully
- Outputs are generated
- Results are consistent
EOF

# -----------------------------
# demonstration
# -----------------------------
cat > demonstration/live_demo.rst << 'EOF'
Live Demonstration
==================

Steps:

1. Configure YAML
2. Run script
3. Visualize outputs
EOF

# -----------------------------
# conf.py tweak
# -----------------------------
echo "html_static_path = ['_static', 'images']" >> conf.py

# -----------------------------
# Build docs
# -----------------------------
cd ..
make html

echo "✅ Documentation ready!"
echo "👉 Open: build/html/index.html"