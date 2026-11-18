---
section: modeling
function: validation
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
rules: [R01, R04, R08, R22, R24]
---

### AI-default

[FIG 4] and [FIG 5] illustrate the simulated isopotential contours and electric current streamline distributions under a 10 mA excitation for the sphere-plane and cylinder-plane contact configurations, respectively. Consistent with theoretical expectations, the current streamlines remain strictly orthogonal to the equipotential surfaces while converging radially toward the constriction zone, where the current density peaks sharply. To rigorously validate whether the finite hemisphere height of r0 = 1 mm in our finite-element setup introduces artificial boundary distortions, we examine the potential profile along the upper boundary. Specifically, [FIG 6] plots the potential variations across horizontal planes at elevations h ranging from 0.5 mm to 1.0 mm above the contact interface. At h = 0.5 mm, a noticeable radial potential gradient from 8.25 µV to 8.275 µV is observed; however, this variation progressively diminishes with increasing elevation until the potential becomes completely uniform at the top surface (h = 1 mm). This confirms that the upper boundary behaves as a true equipotential surface despite the truncated domain height.

### Ren

The simulation results of isopotential maps and electrical current lines profile at 10mA electrical current load are shown in [FIG 4] and [FIG 5] for sphere-plane contact and cylinder-plane contact, respectively. As expected, the current lines are orthogonal to the potential lines and shrink uniformly radially toward the contact region. And the distribution of current lines are densest around the vicinity of the contact region. It is necessary to investigate the electrical potential distribution on the top-most surface in order to illustrate whether the half-sphere with limited height of r0 = 1mm in finite-element model has influence on the constriction of current lines. The height h is defined as the vertical distance from the horizontal line to the contact region. And the potential distribution on the horizontal lines with different heights from 0.5mm to 1mm are shown in [FIG 6]. It is noted that the electrical potential increases significantly from 8.25 µ V to 8.275 µ V along the horizontal line away from the vertical z-axis for h = 0.5mm. And the variations of electrical potential becomes smaller with the height h increasing until all potential are equal for h = 1mm corresponding to the top-most surface. This means that the top-most surface is an isopotential surface even under limited height. For better description, the isopotential lines corresponding to 90%U, 75%U, 50%U, 25%U and 10%U are drawn in [FIG 4] and [FIG 5], where U is the electrical potential of the top-most surface.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `[FIG 4] and [FIG 5] illustrate the simulated isopotential contours` | `The simulation results of isopotential maps and electrical current lines profile ... are shown in [FIG 4] and [FIG 5]` | `R04`, `R22`, `R24` | Uses passive figure pointer (`are shown in [FIG N]`) and Ren's exact field terminology (`isopotential maps`, `electrical current lines profile`). |
| `To rigorously validate whether the finite hemisphere height ... introduces artificial boundary distortions, we examine` | `It is necessary to investigate the electrical potential distribution on the top-most surface in order to illustrate whether...` | `R08`, `R22`, `F26` | Uses `It is necessary to investigate...` (`R08`) and domain-specific boundary term `top-most surface` (`R22`) without `rigorously`. |
| `At h = 0.5 mm, a noticeable radial potential gradient ... is observed` | `It is noted that the electrical potential increases significantly from 8.25 µ V to 8.275 µ V ... for h = 0.5mm.` | `R08`, `R26` | Uses `It is noted that...` (`R08`) with exact numerical bounds (`from X to Y`). |
| `This confirms that the upper boundary behaves as a true equipotential surface` | `This means that the top-most surface is an isopotential surface even under limited height.` | `R07`, `R24` | Uses direct causal restatement (`This means that...`) to state the physical implication of the numerical check. |
