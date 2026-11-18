---
section: results
function: trend
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
rules: [R01, R04, R05, R06, R25, R26, R27]
---

### AI-default

[FIG 17] compares the vertical height distributions of the 90%U, 75%U, 50%U, 25%U, and 10%U equipotential contours across normalized curvature radii r/L spanning from 0.1 to 10 for both sphere-plane and cylinder-plane contacts. Notably, both the normalized height h* and the relative constriction zone height Δh* exhibit a pronounced downward trend as the normalized curvature radius increases. For any given equipotential level, the sphere-plane configuration consistently yields lower h* and Δh* values compared to its cylinder-plane counterpart, signifying that the potential drop is much more tightly localized around the spherical a-spot. Consequently, the cylinder-plane geometry experiences weaker current crowding and a correspondingly smaller constriction voltage drop. Nevertheless, a substantial potential drop develops along the extended cylindrical arc profile, which introduces a considerable bulk resistance component that escalates with increasing cylinder curvature radius. This competing bulk effect ultimately explains why the total resistance of the cylinder-plane contact surpasses that of the sphere-plane contact at larger curvature radii.

### Ren

The height distributions of various isopotential with 90%U, 75%U, 50%U, 25%U and 10%U with varied curvature radius r/L from 0.1 to 10 for sphere-plane contact and with varied normalized curvature radius of cambered surface r/L = 0.1, 1 and 10. cylinder-plane contact are shown in [FIG 17]. The normalized height h∗and the relative height of the constriction region 1h∗both decrease significantly with the normalized curvature radius increasing. For the fixed isopotential, the parameters h∗and 1h∗of sphere-plane contact are always lower than that of cylinder-plane contact, which indicates that the isopotential distribution of former is closer to the contact a-spot than the latter. So the crowding ability for electrical current of cylinder-plane is weaker than that of sphere-plane contact, and there would be a lower potential difference for cylinder-plane contact corresponding to a smaller contact resistance. However, the potential decreases significantly for cylinder-plane contact along the arc profile of cylinder, which causes a larger bulk resistance. And the bulk resistance would increase with the curvature radius of cylinder increasing. This is the root reason for a larger resistance for cylinder-plane contact with the curvature radius increasing than that of sphere-plane contact.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `[FIG 17] compares the vertical height distributions ... across normalized curvature radii` | `The height distributions of various isopotential ... are shown in [FIG 17].` | `R04`, `R25` | Uses passive figure pointer (`The distributions ... are shown in [FIG N]`) instead of anthropomorphizing the figure (`[FIG 17] compares...`). |
| `exhibit a pronounced downward trend as the normalized curvature radius increases` | `both decrease significantly with the normalized curvature radius increasing` | `R06`, `R26` | Uses direct trend verb (`decrease significantly`) + `with the <X> increasing` (`R06`). |
| `signifying that the potential drop is much more tightly localized` | `, which indicates that the isopotential distribution of former is closer to the contact a-spot than the latter.` | `R03`, `R27` | Uses finite `, which indicates that...` clause instead of participial `-ing` tail (`signifying that...`, `F24`). |
| `This competing bulk effect ultimately explains why` | `This is the root reason for a larger resistance for cylinder-plane contact...` | `R27`, `R29` | Uses direct causal summary (`This is the root reason for...`) to close the trend comparison. |
