#!/usr/bin/env python3
print("Hello from gaussian_test.py")

from mpi4py import MPI
import numpy as np
import os
from landlab import RasterModelGrid
from landlab.components import LinearDiffuser

# ============================================
# OUTPUT DIRECTORY
# ============================================
OUTPUT_DIR = os.path.join("output", "random_noise_surface_test_vtu_squar_grid", "landlab_vtu")

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================
# OPTIONAL VTU SUPPORT
# ============================================
VTU_AVAILABLE = False
try:
    import meshio
    VTU_AVAILABLE = True
except Exception:
    VTU_AVAILABLE = False


# ============================================
# GLOBAL STATE
# ============================================
current_time = 0.0
comm = None
model_grid = None
elevation = None
linear_diffuser = None


# ============================================
# MPI INIT
# ============================================
def initialize(comm_handle):
    global comm
    if comm_handle is not None:
        comm = MPI.Comm.f2py(comm_handle)
        print(f"[Python] Rank {comm.rank}/{comm.size}")
    else:
        print("[Python] Running sequentially")


def finalize():
    pass


# ============================================
# VTU WRITER
# ============================================
def write_vtu_pvd(x, y, z, step_id):
    import meshio

    ensure_output_dir()

    points = np.column_stack((x, y, z))
    cells = [("vertex", np.arange(len(points)).reshape(-1, 1))]

    filename = f"landlab_{step_id:06d}.vtu"
    filepath = os.path.join(OUTPUT_DIR, filename)

    mesh = meshio.Mesh(
        points=points,
        cells=cells,
        point_data={"elevation": z}
    )

    mesh.write(filepath)

    # ---- PVD ----
    pvd_file = os.path.join(OUTPUT_DIR, "landlab_collection.pvd")

    try:
        with open(pvd_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = [
            '<?xml version="1.0"?>\n',
            '<VTKFile type="Collection" version="0.1">\n',
            '  <Collection>\n',
            '  </Collection>\n',
            '</VTKFile>\n'
        ]

    entry = f'    <DataSet timestep="{step_id}" file="{filename}"/>\n'
    lines.insert(-2, entry)

    with open(pvd_file, "w") as f:
        f.writelines(lines)

    print(f"[Output] VTU: {filepath}")


# ============================================
# FALLBACK VTK
# ============================================
def write_simple_vtk(filename, x, y, z):
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write("Landlab output\n")
        f.write("ASCII\n")
        f.write("DATASET POLYDATA\n")
        f.write(f"POINTS {len(x)} float\n")
        for i in range(len(x)):
            f.write(f"{x[i]} {y[i]} {z[i]}\n")


# ============================================
# GRID + INITIAL CONDITION
# ============================================
def set_mesh_information(dict_grid_information):
    global model_grid, elevation, linear_diffuser

    if model_grid is None:
        print("* Creating Raster grid (ASPECT-compatible)")

        model_grid = RasterModelGrid((5, 5), xy_spacing=0.25)

        x = model_grid.node_x
        y = model_grid.node_y

        # print(" Initializing Gaussian hill")

        # z = np.exp(-((x - 0.5)**2 + (y - 0.5)**2) / 0.01)

        # print(" Initializing linear slope")

        # z = 0.5 * x

        # Quadratic slope
        # z = 0.5 * x + 0.2 * x**2
        # z = 1.0 * (x - 0.5)**2

        # Flat surface
        # elevation = model_grid.add_zeros(
        #     "topographic__elevation", at="node"
        # )
        # Random noise surface
        np.random.seed(42)  # for reproducibility
        z = np.random.rand(len(x))   # values between 0 and 1
        
        elevation = model_grid.add_field(
            "topographic__elevation", z, at="node"
        )

        linear_diffuser = LinearDiffuser(
            model_grid,
            linear_diffusivity=50
        )

        print(f"* Nodes: {model_grid.number_of_nodes}")

        if comm is None or comm.rank == 0:
            # REQUIRED FOR TEST
            np.savetxt("initial_elevation.txt", elevation)

            # also save in output folder
            ensure_output_dir()
            np.savetxt(
                os.path.join(OUTPUT_DIR, "initial_elevation.txt"),
                elevation
            )


# ============================================
# TIME STEPPING
# ============================================
def update_until(end_time, dict_variable_name_to_value_in_nodes):
    global current_time, elevation, linear_diffuser, model_grid

    dt_total = end_time - current_time
    dz = np.zeros(model_grid.number_of_nodes)

    if dt_total > 0:
        n = 10
        dt = dt_total / n

        for _ in range(n):
            before = elevation.copy()
            linear_diffuser.run_one_step(dt)
            dz += elevation - before

    current_time = end_time

    write_output()

    return dz


def write_output():
    global model_grid, elevation, current_time

    if model_grid is None:
        return

    if comm is None or comm.rank == 0:
        x = model_grid.node_x
        y = model_grid.node_y
        z = elevation

        ensure_output_dir()

        step_id = int(round(current_time / 1e-4))

        # REQUIRED FOR TEST
        np.savetxt("output_elevation.txt", z)

        # (optional but good) also store in output folder
        np.savetxt(
            os.path.join(OUTPUT_DIR, "output_elevation.txt"),
            z
        )

        # debug xyz
        np.savetxt(
            os.path.join(OUTPUT_DIR, f"xyz_{step_id:06d}.txt"),
            np.column_stack((x, y, z))
        )

        # VTU
        if VTU_AVAILABLE:
            try:
                write_vtu_pvd(x, y, z, step_id)
            except Exception as e:
                print("VTU failed → fallback:", e)
                write_simple_vtk(f"fallback_{step_id:06d}.vtk", x, y, z)
        else:
            write_simple_vtk(f"fallback_{step_id:06d}.vtk", x, y, z)
# ============================================
# REQUIRED INTERFACE
# ============================================
def get_grid_x(grid_id):
    return model_grid.node_x


def get_grid_y(grid_id):
    return model_grid.node_y


def get_initial_topography(grid_id):
    return elevation