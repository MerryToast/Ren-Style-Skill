---
section: modeling
function: validation
source: synthetic
moves: [M4_analytical_fem_classical_theory_validation]
rules: [R01, R04, R08, R22, R24]
notes: "Fictitious model validation comparing analytical solution, COMSOL FEM, and classical Holm formula; demonstrates quantitative regime agreement and physical reason for divergence."
---

To verify the accuracy of the derived analytical solution, illustrative calculations of the normalized contact resistance Rc* = 2aRc/ρ3 as a function of the normalized contact radius a* are compared with the finite-element simulation results in [FIG 3]. The classical Holm formula is also plotted for reference. In the limiting case of an uncoated homogeneous contact (h1* = 0, κ1 = 1), the analytical expression is reduced to the classical single-spot constriction resistance formula Rc = (ρ1 + ρ3)/(4a) for small contact spots. As shown in [FIG 3], the analytical predictions agree well with the finite-element simulation data over the entire range of aspect ratios 0.01 ≤ a* ≤ 0.60. The maximum relative deviation between the two methods is less than 1.4%. Specifically, when a* ≤ 0.08, the analytical values, numerical results, and classical Holm curve practically coincide because the outer radial boundary has a negligible effect on current constriction near the a-spot. When a* exceeds 0.15, however, the contact resistance is increasingly overestimated by the classical Holm theory. By contrast, both the analytical model and the finite-element simulation capture the monotonic decrease of Rc* caused by radial boundary confinement, which confirms the validity of the analytical formulation.
