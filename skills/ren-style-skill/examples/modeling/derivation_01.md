---
section: modeling
function: derivation
source: synthetic
moves: [M2_governing_equations_boundary_conditions_and_dimensionless_groups]
rules: [R01, R04, R07, R22, R23]
notes: "Fictitious analytical derivation of potential distribution in a bilayer contact; demonstrates Laplace governing equation, boundary conditions, 'For simplicity, we define...' dimensionless groups, and component decomposition."
---

Under steady-state direct-current excitation, the electrostatic potential φi(r, z) in each conducting layer i (i = 1, 2, 3) satisfies the axisymmetric Laplace equation in cylindrical coordinates. The governing differential equation can be written as [EQ], where ρi denotes the electrical resistivity of layer i. At the metallurgical interfaces z = h1 and z = h1 + h2, both the electrical potential and the normal current density remain continuous. These physical requirements yield the interface continuity conditions [EQ]. Across the circular contact plane z = 0, the mixed boundary conditions are given by φ1(r, 0) = V0 for 0 ≤ r ≤ a and ∂φ1/∂z = 0 for a < r ≤ b. By applying the zero-order Hankel transform with respect to the radial coordinate r, the general solution of the potential in each layer can be expressed as [EQ]. Here, J0 denotes the zero-order Bessel function of the first kind, and Ak(ξ) and Bk(ξ) are layer coefficients determined by the boundary conditions. For simplicity, we define the normalized contact radius a* = a/b, the normalized coating thicknesses h1* = h1/a and h2* = h2/a, and the resistivity ratios κ1 = ρ1/ρ3 and κ2 = ρ2/ρ3. The total electrical contact resistance Rc can then be decomposed into three series components, namely the constriction resistance Rs, the bilayer transition resistance Rt, and the substrate bulk resistance Rb.
