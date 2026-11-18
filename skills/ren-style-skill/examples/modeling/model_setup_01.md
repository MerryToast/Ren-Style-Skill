---
section: modeling
function: model_setup
source: synthetic
moves: [M1_geometric_idealization_and_coordinate_setup, M3_fem_discretization_and_mesh_grading]
rules: [R01, R11, R22, R24]
notes: "Fictitious axisymmetric FEM setup for a bilayer-coated sphere-on-flat contact in COMSOL; demonstrates coordinate setup, boundary conditions, and graded mesh near singularity."
---

The system of interest and its geometric parameters are illustrated schematically in [FIG 1]. We consider an axisymmetric circular contact spot of radius a formed between a silver-alloy hemisphere of radius R and a flat copper substrate. The lower substrate carries a bilayer coating with layer thicknesses h1 and h2. Because the contact geometry and electric field distribution are rotationally symmetric about the vertical z-axis, the three-dimensional conduction problem reduces to a two-dimensional axisymmetric domain in cylindrical coordinates (r, z). To evaluate the constriction resistance and potential distribution over a wide range of coating thicknesses, a two-dimensional axisymmetric finite-element model is built in COMSOL Multiphysics software. In the simulation domain, the outer radial boundary at r = b is electrically insulated. Meanwhile, a uniform direct current I0 enters the top-most boundary of the upper hemisphere, and the bottom-most boundary of the lower substrate is electrically grounded (V = 0). The computational domain is meshed with six-node triangular elements. Furthermore, the mesh size is graded radially toward the contact edge (r = a) with a minimum element size of 2 × 10^-4 a to resolve the current density singularity accurately.
