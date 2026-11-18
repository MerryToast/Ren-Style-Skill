---
section: experimental
function: procedure
source: synthetic
rules: [R01, R06, R10, R19, R20, R21]
---

### AI-default

To accurately track the evolution of electrical contact resistance throughout the torsional fretting tests, we employed a high-precision four-wire Kelvin sensing configuration, as depicted in [FIG 2]. A programmable Keithley 6220 current source was utilized to inject a stable DC current between 20 mA and 200 mA, while a Keithley 2182A nanovoltmeter captured the resulting interfacial voltage drop at a 2 kHz rate. Given the exceptional instrument tolerances of ±0.1% and ±0.05%, the overall measurement uncertainty was successfully constrained below 0.2%. All trials were executed inside an environmental chamber regulated at 25 ± 1 °C and 55 ± 3% RH, with full operating parameters summarized in Table 1. Following test termination at 5 × 10^4 cycles or 1.0 Ω, comprehensive post-mortem surface characterization was conducted by leveraging Zeiss SEM imaging, laser confocal profilometry, and 15 kV EDX elemental mapping to unravel the wear track chemistry.

### Ren

By using the four-wire Kelvin resistance measurement method (shown in [FIG 2]), the electrical contact resistance across the mated pair was continuously monitored as a function of torsional fretting cycles. A programmable constant-current source (Keithley 6220, USA) supplied a direct current load ranging from 20 mA to 200 mA, while the voltage drop across the contact interface was sampled by a nanovoltmeter (Keithley 2182A, USA) at a sampling frequency of 2 kHz. The measurement accuracies of the current source and the nanovoltmeter were ±0.1% and ±0.05%, respectively; thus, the overall uncertainty of the contact resistance measurement did not exceed 0.2%. All experiments were conducted in a temperature- and humidity-controlled cabinet maintained at 25 ± 1 °C and 55 ± 3% relative humidity. The detailed experimental parameters are listed in Table 1. Each test was run for up to 5 × 10^4 torsional cycles or terminated automatically once the contact resistance exceeded 1.0 Ω. After the endurance tests, the worn surface morphologies and three-dimensional wear depth profiles were examined by using a scanning electron microscope (Merlin Compact, Zeiss, Germany) and a laser confocal microscope. Energy-dispersive X-ray spectroscopy (EDX) area mapping and line scans were performed at an accelerating voltage of 15 kV to determine the elemental distribution across the annular wear region.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `To accurately track ... we employed a high-precision four-wire Kelvin sensing configuration` | `By using the four-wire Kelvin resistance measurement method (shown in [FIG 2]), the electrical contact resistance ... was continuously monitored as a function of` | `R06`, `R10`, `R19`, `R20` | Uses Ren's signature experimental opener (`By using the four-wire method (shown in [FIG N]), the contact resistance was continuously measured/monitored as a function of...`) in passive voice. |
| `a programmable Keithley 6220 current source was utilized` | `A programmable constant-current source (Keithley 6220, USA) supplied` | `R20`, `F17` | Formats instrument specifications in inline parentheses `(Model, Manufacturer, Country)` (`R20`) and avoids `utilized` (`F17`). |
| `Given the exceptional instrument tolerances ... was successfully constrained` | `The measurement accuracies ... were ±0.1% and ±0.05%, respectively; thus, the overall uncertainty ... did not exceed 0.2%.` | `R12`, `R20`, `F26` | States instrument accuracy and deduced measurement uncertainty without evaluative adjectives (`exceptional`, `successfully`). |
| `by leveraging Zeiss SEM imaging ... to unravel` | `were examined by using a scanning electron microscope (Merlin Compact, Zeiss, Germany) ... to determine` | `R10`, `R20`, `F17` | Uses instrument-passive (`were examined by using...`) and plain verbs (`determine`) instead of `leveraging` and `unravel`. |
