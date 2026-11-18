# Playbook: `introduction`

## Functions
- `background` — Engineering application context, reliability bottleneck (`weak link`), and classical contact physics/theory baseline (Holm `[EQ]`).
- `prior_work` — Literature review organized as chronological/thematic `<Author> et al. [CIT] <past verb> ... and <past verb> that ...` chains.
- `gap` — Pivot with `However,` highlighting unexamined operating conditions, coupled processes, or coating/geometry effects (`are very limited` / `little is known`).
- `this_paper` — Final roadmap paragraph opening with `In this paper,` or `This paper first presents...` and closing with `explicitly`.

## Quantitative Targets (S+A Train Weighted)
- **Paragraph length**: **97 words** median (IQR: `64–140` words), **4 sentences** per paragraph (`5–9` paragraphs total for a full Introduction).
- **Sentence length**: Median **23 words** (IQR: `16–28` words, P90: `36` words; lint range P50 `15–30`, P90 `22–44`).
- **Voice & pronouns**: **39.3%** passive sentences (lint range `0.15–0.70`); low `we` (`0.81 / 1,000w`).
- **Tense mix**: **50.2%** Present (`background` & `this_paper`), **43.9%** Past (`prior_work`), **5.9%** Present Perfect (highest in corpus: `has been extensively investigated`, `have shown`).
- **Top connectives**: `However,` (`5.74 / 100 sents`), `Therefore,` (`3.01`), `Finally,` (`2.28`), `In this paper,` (`1.82`), `In addition,` (`1.64`), `Then,` (`1.28`), `Next,` (`1.00`).

## Move Order
1. **Move 1 (`background`) — Engineering Application & Reliability Bottleneck (1–2 paragraphs)**
   - Establish widespread use of relays/connectors/contacts and identify contact failure (`fretting`, `contact welding`, `contact resistance`) as a weak link.
   - *Evidence*: `"In terms of reliability, metal contacts present in electrical connectors often represent a weak link in the whole system..."` (`P01`)
2. **Move 2 (`background`) — Classical Theory or Material Baseline (1 paragraph)**
   - Introduce the governing physical definition or classical Holm/Sharvin/Kohlrausch equation `[EQ]` with `where` variable definitions, or contrast noble (Au) vs non-noble (Sn) coatings.
   - *Evidence*: `"Holm [CIT] has shown that the constriction resistance of a single circular a-spot in a bulk interface..."` (`P13`)
3. **Move 3 (`prior_work`) — Thematic Literature Survey (1–3 paragraphs)**
   - Open with a factor-listing sentence (`Many factors influence..., such as... [CIT]`), then chain 3–5 concrete author-verb sentences reporting exact experimental ranges and findings.
   - *Evidence*: `"Park et al. [CIT] examined the effect of current load under 1–3 A and observed that..."` (`P01`)
4. **Move 4 (`gap`) — Research Gap Statement (2–4 sentences, either closing `prior_work` or opening the final paragraph)**
   - Pivot with `However,`; point out that studies on the specific combined condition or physical mechanism are `very limited` or `remain absent`.
   - *Evidence*: `"However, studies on the nature of electrical conduction through fretted contacts... are very limited."` (`P01`)
5. **Move 5 (`this_paper`) — Scope & Stepwise Roadmap of This Paper (1 paragraph, 3–5 sentences)**
   - State the objective (`In this paper, ... is investigated...`) and walk through the paper's steps (`firstly... then... next... finally...`) using passive voice and closing with `explicitly`.
   - *Evidence*: `"Next, the effects of contact radius, electrical conductivity, and coating thickness... are addressed explicitly."` (`P13`)

## Sentence Frames (Slot Templates)
1. `With the increasing application of <system> in <industry>, more and more electromechanical devices with metal contacts, including <connectors, relays, and switches>, are used in <systems>.`
2. `The electrical contact resistance across an interface between two conductors is an important quantity in many electromechanical device measurements and design [CIT].`
3. `<Phenomenon>, which occurs at the interface of contacting metal materials subjected to <stimulus>, is caused by <micro-process> between contacting surfaces [CIT].`
4. `Holm [CIT] has shown that the constriction resistance of a single circular a-spot in a bulk interface can be expressed as [EQ] where <sym1> and <sym2> are <def1> and <def2>, respectively.`
5. `Many factors influence the <property> of contacts, such as <factor 1>, <factor 2>, <factor 3>, and <factor 4> [CIT].`
6. `<Author> et al. [CIT] investigated/examined the effect of <parameter> under <numeric range> and found/observed/concluded that <specific finding>.`
7. `However, studies on the nature of <process> and the influence of <parameter> on <failure mode> are very limited.`
8. `Relatively little is known about the <mechanism> of <material> used in <parameter> over the range of <A–B>.`
9. `In this paper, an attempt is made to explore the effect of various <parameters> on the change of <metric> of <contacts> by introducing our newly designed test rig.`
10. `This paper first presents a universal mathematical model of <contact> for <analysis>, and then the corresponding finite-element method (FEM) simulation model is built for comparison. Next, the effects of <parameters> on <target> are addressed explicitly.`

## Guardrails & Tier-S Precedence
- In `prior_work`, always report what each cited author **actually varied or measured** (e.g., `under 10 and 100 mA`, `in the frequency range of 1–100 Hz`), rather than vague summaries.
- In `this_paper`, follow Tier S (`P01`, `P03`, `P13`) by using passive constructions (`is investigated`, `is built`, `are analyzed`, `are addressed explicitly`) rather than `"In this paper, we..."`.
