# Playbook: `modeling`

## Functions
- `model_setup` — Idealized contact geometry, coordinate system, symmetry assumptions, and finite-element (COMSOL) mesh/boundary setup.
- `derivation` — Governing differential/integral equations (`[EQ]`), boundary conditions, `where` symbol definitions, and analytical resistance/force derivation.
- `validation` — Comparison of analytical predictions with classical Holm/Hertz theory, FEM simulations, or experimental benchmark data.

## Quantitative Targets (S+A Train Weighted)
- **Paragraph length**: **127 words** median (IQR: `44–198` words), **5 sentences** per paragraph.
- **Sentence length**: Median **21 words** (IQR: `16–28` words, P90: `39` words; lint range P50 `14–30`, P90 `21–46`).
- **Voice & pronouns**: **50.2%** passive sentences (lint range `0.20–0.80`), combined with the **highest active `we` rate in the corpus (`2.27 / 1,000w`)**: `"We consider..."`, `"we set..."`, `"For simplicity, we define..."`.
- **Tense mix**: **75.9%** Present / **23.7%** Past / **0.4%** Present Perfect; `4.56` `It is <VBN> that` per 100 sentences.
- **Top connectives**: `Thus,` (`3.65 / 100 sents`), `Therefore,` (`1.82`), `Then,` (`1.82`), `As shown in [FIG n],` (`1.82`), `Furthermore,` (`1.52`), `For simplicity,` (`0.91`).

## Move Order
1. **Move 1 (`model_setup`) — Geometric Configuration & Symmetry Assumptions (1–2 paragraphs)**
   - Reference the schematic `[FIG n]`, define radii/thicknesses ($r_0, r_1, h, a$), and state symmetry assumptions using active `we` (`We consider the simple situation of...`).
   - *Evidence*: `"The system of interest and associated boundary conditions are described in relation to [FIG 2]."` (`P13`)
2. **Move 2 (`derivation`) — Governing Equation & Boundary Conditions (1–2 paragraphs)**
   - State the governing Laplace/heat/elastic equation `[EQ]`, list boundary conditions `as follows: [EQ]`, and define all symbols in a `where ... respectively` clause.
   - *Evidence*: `"The boundary conditions are taken as follows: [EQ] where ρ1 is the electrical resistivity of the substrate..."` (`P13`)
3. **Move 3 (`derivation`) — Dimensionless Ratios & Analytical Solution (1–3 paragraphs)**
   - Introduce dimensionless groups (`For simplicity, we define g = ρ1/ρ2...`), substitute boundary conditions (`Combining (3)–(5) yields [EQ]`), and decompose total resistance into spreading, transition, and bulk terms.
   - *Evidence*: `"For simplicity, we define g = ρ1/ρ2 and (∂V2/∂r)|r=r0 = f(θ)."` (`P13`)
4. **Move 4 (`model_setup` / `validation`) — FEM Simulation Setup & Validation (1–2 paragraphs)**
   - Specify COMSOL Multiphysics version, 2D axisymmetric / 3D geometry, radial mesh grading toward the contact constriction (`[FIG n]`), minimum mesh element size, and electrical/thermal boundary conditions; compare analytical vs FEM/Holm curves.
   - *Evidence*: `"The meshes, presented in [FIG 3], are graded radially outward from the initial point of contact..."` (`P13`)

## Sentence Frames (Slot Templates)
1. `The system of interest and associated size/boundary parameters are described schematically in relation to [FIG n].`
2. `We consider the simple situation of a <hemispherical/cambered> conductor of radius <r1> surrounded by a metal film of thickness <h>.`
3. `Assuming electrical current passes through the circular constriction of contact radius <a>, as shown in [FIG n], the model is symmetric about <axis>.`
4. `The equation describing the distribution of the electrical potential within the contact is [EQ].`
5. `The boundary conditions are taken as follows: [EQ] where <ρ1> and <ρ2> are the electrical resistivities of the substrate and coating, respectively.`
6. `For simplicity, we define <g = ρ1/ρ2> and normalize the contact resistance by the classical Holm constriction resistance.`
7. `Similar to the known distribution of electrical current in a semi-infinite solid [CIT], the current density distribution within the constriction is assumed as [EQ].`
8. `Substituting <Eq. A> into <Eq. B>, the total contact resistance between <surface A> and <surface B> can be expressed as [EQ].`
9. `To visualize the isopotential and electrical current line distributions, the commercial program COMSOL Multiphysics is used to perform simulations by solving electric field equations through FEM.`
10. `The meshes, presented in [FIG n], are graded radially outward from the initial point of contact, with the densest mesh in the contact region (minimal mesh size of <X> μm).`
11. `Electrically, a prescribed constant voltage of <V> is applied to the top-most surface, the bottom-most surface is electrically grounded, and the lateral surfaces are considered electrically insulated.`

## Guardrails & Tier-S Precedence
- Always follow `[EQ]` immediately with a lower-case `where <symbol> is ...` clause when new symbols appear in the equation.
- Keep algebraic derivations connected with explicit logical bridges (`Thus,`, `Therefore,`, `Then,`, `Furthermore,`, `Combining (X) and (Y) yields`).
