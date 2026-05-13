

``experiments.yaml``
====================

.. code:: yaml

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
    executable: /Users/biraj/software/template_Landlab_denial_90296f6_test/aspect/build/aspect-release