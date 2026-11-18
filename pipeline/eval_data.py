"""Benchmark data for Phase 5 & Phase 6 evaluation on heldout [P05, P09, P16, P19] and Tier B papers.

All numbers, units, citation markers ([CIT]), and figure/equation/table references ([FIG N], [EQ], Table N)
in every translation and polish item strictly match the corresponding heldout or Tier B source paragraph.
"""
from __future__ import annotations

from typing import Any

HELDOUT_BENCHMARKS: list[dict[str, Any]] = [
    # 1. P05 abstract (para 0)
    {
        "id": "H01_P05_abstract",
        "paper_id": "P05",
        "section": "abstract",
        "function": "full",
        "para_idx": 0,
        "zh_source": (
            "本文对比研究了不同微动频率下接触电阻和切向力随微动循环次数的典型变化特征，"
            "明确记录了每个微动周期内出现的间歇现象或短时瞬态不连续现象。"
            "接触区域持续出现的瞬时高接触电阻值与接触对之间失真的切向力波形相对应。"
            "结果表明，微动频率是影响间歇接触电阻的关键参数。"
            "随后，引入电接触理论和热弹性不稳定性模型，解释了高频微动过程中摩擦受热电接触对的接触失效机理。"
        ),
        "baseline_en": (
            "This study comprehensively explores the typical evolution characteristics of electrical contact resistance "
            "and tangential force across fretting cycles under various fretting frequencies. Short-duration discontinuities "
            "and intermittent phenomena occurring within individual fretting cycles are systematically documented. "
            "Notably, instantaneous spikes in contact resistance across the contact interface consistently mirror the "
            "distorted tangential force profiles between the mating contacts. Our findings highlight that fretting frequency "
            "serves as a pivotal parameter governing intermittent contact resistance behavior. Ultimately, by leveraging "
            "classical electrical contact theory alongside a thermoelastic instability framework, we elucidate the underlying "
            "contact failure mechanisms of frictionally heated electrical contacts subjected to high-frequency fretting."
        ),
        "ablation_no_examples_en": (
            "The typical variation characteristics of electrical contact resistance and tangential force with fretting "
            "cycles are compared under different fretting frequencies, while intermittent phenomena and short-duration "
            "discontinuities during each fretting cycle are recorded. The instantaneous higher contact resistance values "
            "in the contact zone correspond to the distorted tangential force between the contacts, indicating that "
            "fretting frequency is an important parameter affecting the intermittent contact resistance, and the contact "
            "failure mechanism of frictionally heated electrical contacts under high-frequency fretting is analyzed by "
            "using electrical contact theory and a thermoelastic instability model."
        ),
        "ablation_no_profile_en": (
            "The typical characteristics of contact resistance and tangential force with fretting cycles are studied "
            "under different fretting frequencies. Intermittent phenomena or short-duration discontinuities during each "
            "fretting cycle are recorded explicitly. Meanwhile, instantaneous high contact resistance values at the contact "
            "zone correspond closely to distorted tangential forces between the contacts. It is found that fretting "
            "frequency plays a key role in governing intermittent contact resistance. Furthermore, the failure mechanism "
            "of frictionally heated electrical contacts during high-frequency fretting is clarified by using classical "
            "electrical contact theory and the thermoelastic instability model."
        ),
        "ablation_no_contrastive_en": (
            "The typical variation characteristics of contact resistance and tangential force as a function of fretting "
            "cycles are investigated under different fretting frequencies. Intermittent phenomena or short-duration "
            "discontinuities within each fretting cycle are recorded explicitly. The instantaneous high contact resistance "
            "values appearing in the contact region correspond to the distorted tangential force between the contacts. "
            "The results indicate that fretting frequency is a key parameter influencing the intermittent contact "
            "resistance. Subsequently, the failure mechanism of frictionally heated electrical contacts under "
            "high-frequency fretting is explained by using electrical contact theory and the thermoelastic instability model."
        ),
        "skill_public_en": (
            "The typical variation characteristics of contact resistance and tangential force with fretting cycles are "
            "investigated under different fretting frequencies. Intermittent phenomena, namely short-duration "
            "discontinuities within each fretting cycle, are recorded explicitly. The instantaneous high contact resistance "
            "values appearing across the contact zone correspond to the distorted tangential force between the mating "
            "contacts. The experimental results indicate that fretting frequency is the key parameter influencing the "
            "intermittent contact resistance. Subsequently, the contact failure mechanism of frictionally heated electrical "
            "contacts during high-frequency fretting is explained by using classical electrical contact theory and the "
            "thermoelastic instability model."
        ),
        "skill_full_en": (
            "The typical characteristics of the variations in contact resistance and tangential force with fretting cycles "
            "are compared under different fretting frequencies. Intermittent phenomena or short-duration discontinuities "
            "within each fretting cycle are recorded explicitly. The instantaneous high contact resistance values appearing "
            "at the contact zone continuously correspond to the distorted tangential force between the two contacts. "
            "Fretting frequency is determined to be the key parameter that influences the intermittent contact resistance. "
            "Subsequently, the contact failure mechanism of frictionally heated electrical contacts during high-frequency "
            "fretting is explained by introducing electrical contact theory and the thermoelastic instability model."
        ),
        "ai_destylized_en": (
            "In this study, we comprehensively compare the typical evolution characteristics of contact resistance and "
            "tangential force across fretting cycles under diverse fretting frequencies, while explicitly documenting "
            "short-duration discontinuities and intermittent events within each cycle. Notably, transient spikes in "
            "contact resistance across the contact zone consistently mirror the distorted tangential force profiles, "
            "underscoring that fretting frequency plays a pivotal role in governing intermittent resistance behavior. "
            "Ultimately, we elucidate the underlying failure mechanisms of frictionally heated electrical contacts "
            "during high-frequency fretting by leveraging classical electrical contact theory alongside a thermoelastic "
            "instability framework."
        ),
        "skill_public_polish_en": (
            "The typical variation characteristics of contact resistance and tangential force with fretting cycles are "
            "compared under different fretting frequencies. Intermittent events or short-duration discontinuities within "
            "each fretting cycle are recorded explicitly. The transient high contact resistance values across the contact "
            "zone continuously correspond to the distorted tangential force profiles. The results indicate that fretting "
            "frequency is the key parameter governing intermittent contact resistance behavior. Subsequently, the failure "
            "mechanism of frictionally heated electrical contacts during high-frequency fretting is explained by using "
            "classical electrical contact theory and the thermoelastic instability model."
        ),
        "skill_full_polish_en": (
            "The typical characteristics of the change in contact resistance and tangential force with fretting cycles "
            "are compared under different fretting frequencies. Intermittent phenomena or short-duration discontinuities "
            "during each fretting cycle are recorded explicitly. The instantaneous high contact resistance values appearing "
            "at the contact zone continuously correspond to the distorted tangential force between the contacts. Fretting "
            "frequency is determined as the key parameter influencing the intermittent contact resistance. Subsequently, "
            "the contact failure mechanism of frictionally heated electrical contacts during high-frequency fretting is "
            "explained by introducing electrical contact theory and the thermoelastic instability model."
        ),
    },
    # 2. P05 experimental (para 6)
    {
        "id": "H02_P05_experimental",
        "paper_id": "P05",
        "section": "experimental",
        "function": "procedure",
        "para_idx": 6,
        "zh_source": (
            "法向接触力设定为 3 N，负载电流为 10 mA。动触头为直径 2 mm 的球形骑子（rider），静电极为平面试样。"
            "基体材料采用铜合金，表面镀覆厚度为 1 μm 的纯金镀层。"
            "采用四线法实时记录接触电阻的瞬态值，测量原理由 [FIG 1] 给出。"
            "两个触头之间的瞬态切向力通过压电式力传感器（209C11, PCB, USA）进行测量。"
            "利用激光位移传感器（ILD2220, Epsilon, Germany）跟踪动触头的瞬时位移，从而精确控制微动幅值。"
            "数据采集系统由配备分析软件的个人计算机控制。"
            "此外，采用配备能谱仪（EDX）的扫描电子显微镜（Quanta FEG, FEI, USA）对微动磨损区进行表面分析。"
        ),
        "baseline_en": (
            "Throughout the experimental trials, we maintained a normal contact load of 3 N alongside a DC load current "
            "of 10 mA. The mating assembly comprised a movable 2 mm diameter spherical rider paired against a stationary "
            "flat electrode, both fabricated from copper alloy substrates electroplated with a 1 μm pure gold layer. "
            "To capture real-time transient fluctuations in contact resistance, we utilized a four-wire Kelvin sensing "
            "configuration, as depicted in [FIG 1]. Concurrently, interfacial tangential forces were monitored via a "
            "piezoelectric force transducer (209C11, PCB, USA), while a high-precision laser displacement sensor "
            "(ILD2220, Epsilon, Germany) tracked the instantaneous rider trajectory to ensure tight control over the "
            "fretting amplitude. Data acquisition was orchestrated by a PC running dedicated analytical software, and "
            "post-test morphological characterization of the fretted zone was conducted by leveraging a FEI Quanta FEG "
            "scanning electron microscope coupled with EDX spectroscopy."
        ),
        "ablation_no_examples_en": (
            "The normal contact force was set to 3 N and the load current was 10 mA. The movable contact was a spherical "
            "rider with a diameter of 2 mm, and the stationary electrode was a flat specimen. Both substrates were made "
            "of copper alloy and electroplated with a 1 μm pure gold coating. The transient contact resistance was "
            "measured in real time by using the four-wire method, as shown in [FIG 1]. The transient tangential force "
            "between the contacts was measured by a piezoelectric force transducer (209C11, PCB, USA), while the "
            "instantaneous displacement of the movable contact was monitored by a laser displacement sensor (ILD2220, "
            "Epsilon, Germany) to control the fretting amplitude accurately. Data acquisition was performed using a "
            "personal computer with analytical software, and a scanning electron microscope with energy-dispersive "
            "X-ray spectroscopy (Quanta FEG, FEI, USA) was used to analyze the worn surface."
        ),
        "ablation_no_profile_en": (
            "The normal contact force was 3 N and the load current was 10 mA. The contacts were a ball-shaped rider with "
            "a diameter of 2 mm and a flat sample, both made of copper alloy with a 1 μm pure gold coating. By using the "
            "four-wire method (shown in [FIG 1]), the transient contact resistance was continuously recorded in real time. "
            "Meanwhile, the transient tangential force between the two contacts was assessed using a piezoelectric force "
            "transducer (209C11, PCB, USA), leading to accurate force tracking, and a laser displacement sensor (ILD2220, "
            "Epsilon, Germany) was introduced to track the instantaneous displacement and ensure constant fretting "
            "amplitude. During the test, data was acquired by a personal computer with programmed software, and scanning "
            "electron microscopy with energy-dispersive X-ray spectroscopy (Quanta FEG, FEI, USA) was used to characterize "
            "the fretted zone."
        ),
        "ablation_no_contrastive_en": (
            "The normal contact force was 3 N and the load current was 10 mA. The movable contact was a ball-shaped rider "
            "with a diameter of 2 mm, and the fixed contact was a flat specimen. The substrate material was copper alloy "
            "electroplated with pure gold with a thickness of 1 μm. By using the four-wire method (shown in [FIG 1]), "
            "the transient value of contact resistance was recorded in real time. The transient tangential force between "
            "the two contacts was measured by using a piezoelectric force transducer (209C11, PCB, USA). A laser "
            "displacement sensor (ILD2220, Epsilon, Germany) was used to track the instantaneous displacement of the "
            "movable contact so that the fretting amplitude was controlled accurately. Data was acquired using a personal "
            "computer with analytical software. Scanning electron microscopy with energy-dispersive X-ray spectroscopy "
            "(Quanta FEG, FEI, USA) was used to characterize the surface of the fretted zone."
        ),
        "skill_public_en": (
            "The normal contact force was 3 N and the load current was 10 mA. The movable contact was a ball-shaped rider "
            "with a diameter of 2 mm, and the fixed electrode was a flat specimen. The substrate material was a copper "
            "alloy electroplated with pure gold with a thickness of 1 μm. By using the four-wire method (shown in [FIG 1]), "
            "the transient value of contact resistance was recorded in real time. Meanwhile, the transient tangential "
            "force between the two contacts was measured by a piezoelectric force transducer (209C11, PCB, USA). The "
            "instantaneous displacement of the movable contact was tracked by a laser displacement sensor (ILD2220, "
            "Epsilon, Germany) to ensure that the fretting amplitude was controlled accurately. The data acquisition "
            "system was controlled by a personal computer with analytical software. After the tests, a scanning electron "
            "microscope equipped with energy-dispersive X-ray spectroscopy (Quanta FEG, FEI, USA) was used for surface "
            "analysis of the fretted zone."
        ),
        "skill_full_en": (
            "The normal contact force was 3 N and the load current was 10 mA. The movable contact was a ball-shaped rider, "
            "with a diameter of 2 mm, and the fixed electrode was a flat sample. The substrate material used was a copper "
            "alloy electroplated with pure gold with a thickness of 1 μm. The transient value of contact resistance was "
            "recorded in real time by using the four-wire method, which is shown in [FIG 1]. The transient tangential "
            "force between the two contacts was measured by using a piezoelectric force transducer (209C11, PCB, USA). "
            "A laser displacement sensor (ILD2220, Epsilon, Germany) was introduced to track the instantaneous displacement "
            "of the movable contact so that the fretting amplitude could be controlled accurately. The data acquisition "
            "system was controlled by a personal computer with analytical software. Scanning electron microscopy with "
            "energy-dispersive X-ray spectroscopy (Quanta FEG, FEI, USA) was also used for the surface analysis of the "
            "fretted zone."
        ),
        "ai_destylized_en": (
            "A normal contact load of 3 N and a direct current of 10 mA were utilized throughout the experimental trials. "
            "The contact pair comprised a movable 2 mm diameter spherical rider mating against a stationary flat electrode, "
            "both fabricated from copper alloy substrates coated with a 1 μm pure gold layer. To continuously monitor "
            "transient contact resistance variations in real time, we leveraged a four-wire sensing configuration, as "
            "depicted in [FIG 1]. Concurrently, interfacial tangential forces were captured via a piezoelectric force "
            "transducer (209C11, PCB, USA), while a high-resolution laser displacement sensor (ILD2220, Epsilon, Germany) "
            "tracked the instantaneous rider trajectory, thereby ensuring precise control over the fretting amplitude. "
            "Data acquisition was orchestrated by a personal computer running dedicated analytical software, and "
            "comprehensive post-mortem surface characterization of the fretted zone was performed using a scanning "
            "electron microscope equipped with EDX spectroscopy (Quanta FEG, FEI, USA)."
        ),
        "skill_public_polish_en": (
            "The normal contact force was 3 N and the load current was 10 mA. The contact pair consisted of a movable "
            "ball-shaped rider with a diameter of 2 mm and a stationary flat electrode, both made of copper alloy "
            "substrates electroplated with a 1 μm pure gold layer. By using the four-wire method (shown in [FIG 1]), "
            "the transient value of contact resistance was monitored in real time. Meanwhile, the transient tangential "
            "force between the two contacts was measured by a piezoelectric force transducer (209C11, PCB, USA). The "
            "instantaneous displacement of the movable rider was tracked by a laser displacement sensor (ILD2220, "
            "Epsilon, Germany) so that the fretting amplitude was controlled accurately. The data acquisition system was "
            "controlled by a personal computer with analytical software. A scanning electron microscope equipped with "
            "energy-dispersive X-ray spectroscopy (Quanta FEG, FEI, USA) was used for the surface analysis of the "
            "fretted zone."
        ),
        "skill_full_polish_en": (
            "The normal contact force was 3 N and the load current was 10 mA. The movable contact was a ball-shaped rider "
            "with a diameter of 2 mm and the fixed electrode was a flat sample. Both substrates were made of a copper "
            "alloy and the surface coating was pure gold with a thickness of 1 μm. The transient value of contact "
            "resistance was recorded in real time by using the four-wire method, which is shown in [FIG 1]. The transient "
            "tangential force between the two contacts was measured by using a piezoelectric force transducer (209C11, "
            "PCB, USA). The instantaneous displacement of the movable contact was tracked by a laser displacement sensor "
            "(ILD2220, Epsilon, Germany) so that the fretting amplitude could be controlled accurately. The data "
            "acquisition system was controlled by a personal computer with analytical software. A scanning electron "
            "microscope with energy-dispersive X-ray spectroscopy (Quanta FEG, FEI, USA) was also used for the surface "
            "analysis of the fretted zone."
        ),
    },
    # 3. P09 modeling (para 9)
    {
        "id": "H03_P09_modeling",
        "paper_id": "P09",
        "section": "modeling",
        "function": "model_setup",
        "para_idx": 9,
        "zh_source": (
            "模型的端面温度保持在 293.15 K 作为参考温度。由于轴对称性，左边界和接触面设为热绝缘。"
            "右侧表面边界具有对流换热系数 h，冷却至周围室温 293.15 K。"
            "在端面施加法向电流密度 J，其中总电流为 I，且 J = I/π R2（R = 1 mm）。"
            "接触面的电位 V 设为零，侧表面边界设为电绝缘条件。"
            "[FIG 3] 给出了铜的材料属性，这些属性与温度密切相关。"
            "此外，两个表面之间的电接触和热接触被认为是理想的；不考虑接触区域内由污染膜引起的附加电热阻。"
            "受仿真软件所限，模型中也未包含 Sharvin 效应。"
        ),
        "baseline_en": (
            "In our numerical framework, the upper end boundary temperature is fixed at a reference value of 293.15 K, "
            "while the symmetry axis on the left and the contact interface are treated as adiabatic boundaries. Along the "
            "outer lateral boundary, convective cooling with a heat transfer coefficient h dissipates heat toward the "
            "ambient environment at 293.15 K. Electrical excitation is introduced by prescribing a uniform normal current "
            "density J = I/π R2 (with R = 1 mm and total current I) across the top boundary, whereas the contact plane "
            "carries zero reference potential and the lateral boundary is electrically insulated. Temperature-"
            "dependent thermophysical properties of copper are incorporated as depicted in [FIG 3]. Furthermore, we "
            "postulate ideal interfacial thermal and electrical conduction, thereby neglecting extraneous film resistance "
            "contributions as well as ballistic Sharvin constriction effects due to software constraints."
        ),
        "ablation_no_examples_en": (
            "The end surface temperature of the model is fixed at 293.15 K as a reference, and because of axisymmetry "
            "the left boundary and the contact surface are thermally insulated, whereas the right side boundary with a "
            "convection coefficient h cools toward the ambient room temperature of 293.15 K. A normal current density J "
            "is applied to the end surface where the total current is I and J = I/π R2 (R = 1 mm), while the electrical "
            "potential V at the contact surface equals zero and the side boundary remains electrically insulated. "
            "[FIG 3] shows the temperature-dependent material properties of copper, and the electrical and thermal "
            "contacts between the surfaces are assumed to be ideal so that additional resistances caused by contaminant "
            "films and the Sharvin effect are not included."
        ),
        "ablation_no_profile_en": (
            "The end surface temperature of the model is held at 293.15 K as a reference, and the left boundary and "
            "contact surface are thermally insulated for axisymmetry, while the right side boundary with convection "
            "coefficient h cools to room temperature 293.15 K. A normal current density J = I/π R2 (R = 1 mm) with "
            "total current I is applied to the end surface, the electrical potential V of the contact surface equals "
            "zero, and the side surface is electrically insulated. As shown in [FIG 3], the material properties of copper "
            "depend closely on temperature. Furthermore, electrical and thermal contacts are assumed to be perfect, "
            "neglecting contaminant film resistances and the Sharvin effect due to software limitations."
        ),
        "ablation_no_contrastive_en": (
            "The end surface temperature of the model is held at 293.15 K as a reference. The left boundary and the "
            "contact surface are thermally insulated due to axisymmetry, while the right side boundary with a convection "
            "coefficient h cools to the ambient room temperature of 293.15 K. A normal current density J is applied to "
            "the end surface, where the total current is I and J = I/π R2 (R = 1 mm). The electrical potential V of the "
            "contact surface equals zero, and the side surface boundary is electrically insulated. [FIG 3] shows the "
            "material properties of copper, which depend closely on temperature. In addition, the electrical and thermal "
            "contacts between the surfaces are considered to be ideal; additional resistances in the contact region due "
            "to contaminant films and the Sharvin effect are not considered."
        ),
        "skill_public_en": (
            "The end surface temperature of the model is held at 293.15 K as a reference. Due to axisymmetry, the left "
            "boundary and the contact surface are thermally insulated, whereas the right side boundary with a convection "
            "coefficient h cools to the surrounding room temperature of 293.15 K. A normal current density J is applied "
            "to the end surface, where the total current is I and J = I/π R2 (R = 1 mm). The electrical potential V of "
            "the contact surface equals zero, and the side surface boundary is electrically insulated. [FIG 3] shows the "
            "material properties of copper, which depend closely on temperature. In addition, the electrical and thermal "
            "contacts between the surfaces are considered to be perfect; that is, additional thermal and electrical "
            "resistances in the contact region due to contaminant films are neglected. The simulation model also omits "
            "the Sharvin effect due to the limitation of the simulation software."
        ),
        "skill_full_en": (
            "The end surface temperature of the model is held at 293.15 K as a reference. The left boundary and contact "
            "surface are thermally insulated for axisymmetry, while the right side surface boundary with convection "
            "coefficient h is cooled to the surrounding room temperature of 293.15 K. Normal current density J is "
            "applied to the end surface, where the total current is I and J = I/π R2 (R = 1 mm). The electrical "
            "potential V of the contact surface equals zero, and the side surface boundary is set as an electrically "
            "insulated condition. [FIG 3] shows the material properties of copper, which depend closely on the "
            "temperature. In addition, electric and thermal contact between the surfaces is considered to be perfect; "
            "additional thermal and electrical resistances in the contact region due to contaminant films are not "
            "considered. The model also omits the Sharvin effect due to the limitation of the simulation software."
        ),
        "ai_destylized_en": (
            "In this finite-element framework, the top boundary temperature is maintained at a reference level of 293.15 K, "
            "whereas the axisymmetric left boundary and contact interface are configured as thermally insulated. Along the "
            "right lateral surface, convective heat dissipation characterized by coefficient h cools the domain toward the "
            "ambient temperature of 293.15 K. Electrical loading is imposed via a normal current density J = I/π R2 "
            "(R = 1 mm, total current I) at the end boundary, while setting the contact plane potential V to zero and "
            "electrically insulating the lateral surface. [FIG 3] illustrates the strongly temperature-dependent material "
            "properties of copper utilized in the model. Moreover, we assume ideal thermal and electrical interfacial "
            "contact, thereby excluding contaminant film resistances as well as the ballistic Sharvin effect owing to "
            "software constraints."
        ),
        "skill_public_polish_en": (
            "The end surface temperature of the model is maintained at 293.15 K as a reference. Due to axisymmetry, the "
            "left boundary and the contact interface are thermally insulated, whereas the right side surface with a "
            "convection coefficient h cools toward the ambient room temperature of 293.15 K. A normal current density "
            "J = I/π R2 (R = 1 mm) with total current I is applied to the end boundary. Meanwhile, the electrical "
            "potential V of the contact plane equals zero, and the side surface boundary is electrically insulated. "
            "[FIG 3] shows the material properties of copper, which depend closely on temperature. In addition, thermal "
            "and electrical contact at the interface is considered to be ideal; additional resistances in the contact "
            "region due to contaminant films are not considered. The model also omits the Sharvin effect due to the "
            "limitation of the simulation software."
        ),
        "skill_full_polish_en": (
            "The end surface temperature of the model is held at 293.15 K as a reference. The left boundary and contact "
            "surface are thermally insulated for axisymmetry, while the right side surface boundary with convection "
            "coefficient h is cooled to the surrounding room temperature of 293.15 K. Normal current density J is "
            "applied to the end surface, where the total current is I and J = I/π R2 (R = 1 mm). The electrical "
            "potential V of the contact surface equals zero, and the side surface boundary is set as an electrically "
            "insulated condition. [FIG 3] shows the material properties of copper, which depend closely on the "
            "temperature. In addition, electric and thermal contact between the surfaces is considered to be perfect; "
            "additional thermal and electrical resistances in the contact region due to contaminant films are not "
            "considered. The model also omits the Sharvin effect due to the limitation of the simulation software."
        ),
    },
    # 4. P09 results (para 12)
    {
        "id": "H04_P09_results",
        "paper_id": "P09",
        "section": "results",
        "function": "trend",
        "para_idx": 12,
        "zh_source": (
            "[FIG 4] 给出了接触半径 a 为 1 μm、电流负载 I 为 12 A、对流换热系数 h 为 104 W·m−2·K−1 时触头的温度和电位分布。"
            "诚然，仿真结果表明最高接触温度 Tm 出现在靠近接触区域的部位，并且与理论估算结果吻合极好。"
            "最高接触温度 Tm 为 923.3 K，总电压降 Uc 为 0.14 V。"
            "在围绕接触中心、半径仅为几微米的狭小区域内出现了显著的温降或压降，而在接触区域内部温度几乎保持恒定。"
            "仿真确定的热收缩区与电收缩区之间的差异，可以归因于接触微凸体一侧的热阻大于半空间一侧的热阻。"
        ),
        "baseline_en": (
            "[FIG 4] depicts the simulated temperature and electrical potential contours across the contact pair for a "
            "contact spot radius of a = 1 μm, an applied current of I = 12 A, and a convective coefficient of "
            "h = 104 W·m−2·K−1. Notably, the numerical predictions reveal that the peak interfacial temperature Tm is "
            "tightly localized near the contact zone, exhibiting remarkable consistency with theoretical estimates by "
            "attaining a maximum temperature of Tm = 923.3 K alongside an overall voltage drop of Uc = 0.14 V. Furthermore, "
            "steep thermal and electrical gradients are confined within a microscopic region of only a few micrometers "
            "around the contact center, whereas the temperature across the immediate contact interface remains virtually "
            "uniform. This divergence between the simulated thermal and electrical constriction zones stems from the "
            "substantially higher thermal resistance on the micro-asperity side relative to the bulk half-space side."
        ),
        "ablation_no_examples_en": (
            "[FIG 4] shows the temperature and potential distributions of the contacts at a contact radius a of 1 μm, "
            "a current load I of 12 A, and a convection coefficient h of 104 W·m−2·K−1, indicating that the maximum "
            "contact temperature Tm occurs near the contact region and agrees with the theoretical calculation at "
            "Tm = 923.3 K and Uc = 0.14 V. A large temperature and voltage drop occurs within a small region of several "
            "micrometers around the contact center while the temperature within the contact region remains nearly "
            "constant, and the difference between the thermal constriction zone and the electrical constriction zone "
            "results from the higher thermal resistance on the asperity side compared with the half-space side."
        ),
        "ablation_no_profile_en": (
            "[FIG 4] shows the distributions of temperature and potential of contacts with contact radius a = 1 μm, "
            "current load I = 12 A, and convection coefficient h = 104 W·m−2·K−1, indicating that the maximum contact "
            "temperature Tm = 923.3 K and total voltage drop Uc = 0.14 V occur close to the contact region and agree well "
            "with theoretical estimations. A substantial drop of temperature and voltage appears within a small radius of "
            "several micrometers around the contact center, while the temperature inside the contact region stays almost "
            "constant, which is attributed to the fact that the asperity side has a larger thermal resistance than the "
            "half-space side."
        ),
        "ablation_no_contrastive_en": (
            "[FIG 4] shows the distributions of temperature and electrical potential of the contacts with a contact "
            "radius a of 1 μm, a current load I of 12 A, and a convection coefficient h of 104 W·m−2·K−1. The simulation "
            "results indicate that the maximum contact temperature Tm occurs close to the contact region and agrees well "
            "with the theoretical estimation. The maximum contact temperature Tm is 923.3 K, and the total voltage drop "
            "Uc is 0.14 V. A substantial temperature or voltage drop appears in a small region with a radius of several "
            "micrometers around the contact center. Meanwhile, the temperature in the contact region remains almost "
            "constant. The difference between the thermal constriction zone and the electrical constriction zone in the "
            "simulation is attributed to the larger thermal resistance on the asperity side than on the half-space side."
        ),
        "skill_public_en": (
            "[FIG 4] shows the distributions of temperature and potential of the contacts with a contact radius a of "
            "1 μm, a current load I of 12 A, and a convection coefficient h of 104 W·m−2·K−1. The simulation results "
            "indicate that the maximum contact temperature Tm occurs close to the contact region and agrees well with "
            "theoretical estimation. Specifically, the maximum contact temperature Tm is 923.3 K and the total voltage "
            "drop Uc is 0.14 V. A substantial temperature or voltage drop appears in a small region with a radius of "
            "several micrometers around the contact center. Meanwhile, the temperature inside the contact region is "
            "considered almost constant. The difference between the thermal constriction zone and the electrical "
            "constriction zone determined by the simulation can be attributed to a larger thermal resistance on the "
            "asperity side of the contact compared with the half-space side."
        ),
        "skill_full_en": (
            "[FIG 4] shows the distribution of temperature and potential of contacts with a contact radius a of 1 μm, "
            "current load I of 12 A, and convection coefficient h of 104 W·m−2·K−1. Admittedly, the simulation results "
            "indicate that the maximum contact temperature Tm occurs close to the contact region, and agrees well with "
            "theoretical estimation. The maximum contact temperature Tm is 923.3 K and the total voltage drop Uc is "
            "0.14 V. A substantial temperature or voltage drop appears in a small area with a radius of several "
            "micrometers around the contact center. The temperature in the contact region is considered almost constant. "
            "The difference between the thermal constriction zone and the electrical constriction zone determined by the "
            "simulation can be justified by the fact that there is a greater thermal resistance on the asperity side of "
            "the contact compared with the half-space side."
        ),
        "ai_destylized_en": (
            "[FIG 4] illustrates the simulated temperature and potential distributions across the contact interface for "
            "a = 1 μm, I = 12 A, and h = 104 W·m−2·K−1. Notably, our numerical findings demonstrate that the peak "
            "temperature Tm is localized adjacent to the contact zone and exhibits remarkable agreement with theoretical "
            "predictions, reaching Tm = 923.3 K alongside a total voltage drop of Uc = 0.14 V. Steep thermal and "
            "electrical potential gradients are tightly confined within a few micrometers of the contact center, whereas "
            "the interfacial temperature remains virtually uniform. Ultimately, the discrepancy between the simulated "
            "thermal and electrical constriction zones stems from the elevated thermal resistance on the asperity side "
            "relative to the half-space side."
        ),
        "skill_public_polish_en": (
            "[FIG 4] shows the simulated temperature and potential distributions across the contact interface at a "
            "contact radius a of 1 μm, a current load I of 12 A, and a convection coefficient h of 104 W·m−2·K−1. The "
            "simulation results indicate that the maximum contact temperature Tm occurs close to the contact zone and "
            "agrees well with theoretical predictions. The maximum contact temperature Tm is 923.3 K and the total "
            "voltage drop Uc is 0.14 V. A substantial temperature or potential drop appears within a small region of a "
            "few micrometers around the contact center. Meanwhile, the temperature in the contact region remains almost "
            "constant. The difference between the thermal constriction zone and the electrical constriction zone "
            "determined by the simulation is attributed to the greater thermal resistance on the asperity side compared "
            "with the half-space side."
        ),
        "skill_full_polish_en": (
            "[FIG 4] shows the distribution of temperature and potential of contacts with the contact radius a of 1 μm, "
            "current load I of 12 A, and convection coefficient h of 104 W·m−2·K−1. Admittedly, the simulation results "
            "indicate that the maximum contact temperature Tm occurs close to the contact region, and agrees well with "
            "theoretical estimation. The maximum contact temperature Tm is 923.3 K and the total voltage drop Uc is "
            "0.14 V. A substantial temperature or voltage drop appears in a small area with a radius of several "
            "micrometers around the contact center. The temperature in the contact region is considered almost constant. "
            "The difference between the thermal constriction zone and the electrical constriction zone determined by the "
            "simulation can be justified by reasoning that there is a greater thermal resistance on the asperity side of "
            "the contact as compared to the half-space side."
        ),
    },
    # 5. P16 introduction (para 1)
    {
        "id": "H05_P16_introduction",
        "paper_id": "P16",
        "section": "introduction",
        "function": "background",
        "para_idx": 1,
        "zh_source": (
            "在高端装备制造工业中应用的机电开关，始终对长寿命和高可靠性有着明确的要求。"
            "诚然，连续的热切换过程会导致触头熔焊、高接触电阻和严重的触头侵蚀，这些现象与开关中所用触头材料的电气特性密切相关。"
            "所谓触头材料的电气特性，是指抗熔焊能力、燃弧特性及其他一般物理特性的统称。"
            "近年来，开关中使用的氧化银系触头材料的电气特性及其相关的退化机理，一直是触头材料制造商和用户关注的焦点问题 [CIT]。"
            "已发表的研究结果表明，电负载（分断电流和电压）、电负载类型（阻性、感性、容性和 LED）、接触力、触头尺寸以及环境（温度、湿度和气体）均对触头材料的电气性能具有显著影响。"
        ),
        "baseline_en": (
            "Electromechanical switching devices deployed across advanced equipment manufacturing industries necessitate "
            "exceptional operational longevity and reliability. However, repetitive hot-switching operations inevitably "
            "induce deleterious phenomena—including contact welding, elevated contact resistance, and severe arc erosion—"
            "which are intrinsically governed by the electrical characteristics of the underlying contact metallurgy, "
            "encompassing anti-welding capability, arc-quenching behavior, and bulk physical properties. Recently, "
            "elucidating the electrical performance and degradation mechanisms of silver-oxide-based contact materials "
            "has garnered widespread attention from both component manufacturers and end-users [CIT]. Prior literature "
            "has established that electrical loading parameters (interrupting current and voltage), load categories "
            "(resistive, inductive, capacitive, and LED), mechanical contact force, contact geometry, and ambient "
            "conditions (temperature, humidity, and gas composition) collectively exert a profound influence on contact "
            "durability."
        ),
        "ablation_no_examples_en": (
            "Long lifetime and high reliability of electromechanical switches used in the high-end equipment manufacturing "
            "industry are always required, because continuous hot switching processes result in contact welding, high "
            "contact resistance, and severe contact erosion that relate to the electrical characteristics of the contact "
            "material, including anti-welding ability, arcing properties, and other physical properties. Recently, the "
            "electrical characteristics and degradation mechanism of silver oxide contact materials used in switches "
            "have become an important concern for manufacturers and users [CIT], and previous studies have shown that "
            "the electrical load (interrupting current and voltage), load type (resistive, inductive, capacitive, and "
            "LED), contact force, contact size, and ambient environment (temperature, humidity, and gas) have "
            "significant effects on the electrical performance of contact materials."
        ),
        "ablation_no_profile_en": (
            "Long lifetime and high reliability of electromechanical switches are widely required in the high-end "
            "equipment manufacturing industry. During continuous hot switching, contact welding, high contact resistance, "
            "and severe contact erosion occur, correlating closely with the electrical characteristics of the contact "
            "material, namely the anti-welding ability, arcing properties, and general physical properties. Recently, the "
            "electrical characteristics of silver oxide contact materials and the associated degradation mechanisms have "
            "been an important concern for manufacturers and users [CIT], and previous studies have revealed that electric "
            "load (interrupting current and voltage), load type (resistive, inductive, capacitive, and LED), contact "
            "force, contact size, and environment (temperature, humidity, and gas) significantly affect the electrical "
            "performance."
        ),
        "ablation_no_contrastive_en": (
            "Long lifetime and high reliability of electromechanical switches, which are widely used in the high-end "
            "equipment manufacturing industry, are always required. Admittedly, the continuous hot switching process can "
            "result in contact welding, high contact resistance, and severe contact erosion. These failure phenomena are "
            "closely related to the electrical characteristics of the contact material, namely the anti-welding ability, "
            "arcing properties, and other physical properties. Recently, the electrical characteristics of silver oxide "
            "contact materials used in switches and the associated degradation mechanisms have become an important concern "
            "for contact material manufacturers and users [CIT]. Published research results have revealed that the "
            "electrical load (interrupting current and voltage), load type (resistive, inductive, capacitive, and LED), "
            "contact force, contact size, and environment (temperature, humidity, and gas) have significant effects on "
            "the electrical performance of contact materials."
        ),
        "skill_public_en": (
            "Long lifetime and high reliability of electromechanical switches, which are widely used in the high-end "
            "equipment manufacturing industry, are always required. Admittedly, the continuous hot switching process "
            "results in contact welding, high contact resistance, and severe contact erosion, which are closely related "
            "to the electrical characteristics of the contact material used in switches. The electrical characteristics "
            "of the contact material refer to the anti-welding ability, arcing properties, and other general physical "
            "properties. Recently, the electrical characteristics of silver oxide contact materials and the associated "
            "degradation mechanism have become an important concern for contact material manufacturers and users [CIT]. "
            "Previous research results have revealed that the electric load (interrupting current and voltage), electric "
            "load type (resistive, inductive, capacitive, and LED), contact force, contact size, and environment "
            "(temperature, humidity, and gas) have significant effects on the electrical performance of contact materials."
        ),
        "skill_full_en": (
            "Long lifetime and high reliability of electromechanical switches, which are used in the high-end equipment "
            "manufacturing industry, are always expressly required. Admittedly, the continuous hot switching process "
            "results in contact welding, high contact resistance, and severe contact erosion, which are closely related "
            "to the electrical characteristics of a contact material used in switches. The so-called electrical "
            "characteristics of the contact material are a general term used to refer to the anti-welding ability, "
            "arcing properties, and other general physical properties. Recently, the electrical characteristics of silver "
            "oxide contact material used in switches and the associated degradation mechanism are always an important "
            "concern of contact material manufacturers and users [CIT]. Previous research results have revealed that the "
            "electric load (interrupting current and voltage), electric load type (resistive, inductive, capacitive, and "
            "LED), contact force, contact size, and environment (temperature, humidity, and gas) have significant effects "
            "on the electrical performance of contact materials."
        ),
        "ai_destylized_en": (
            "In advanced equipment manufacturing sectors, electromechanical switches must satisfy stringent longevity and "
            "reliability requirements. Nevertheless, repetitive hot-switching operations inevitably trigger deleterious "
            "degradation modes—such as contact welding, elevated interfacial resistance, and severe erosion—that are "
            "intimately linked to the intrinsic electrical characteristics of the contact metallurgy, encompassing "
            "anti-welding performance, arc behavior, and general physical properties. Recently, unraveling the electrical "
            "behavior and underlying degradation mechanisms of silver-oxide contact materials has attracted considerable "
            "interest from both manufacturers and end-users [CIT]. Extensive prior studies have demonstrated that "
            "electrical loading (interrupting current and voltage), load nature (resistive, inductive, capacitive, and "
            "LED), mechanical contact force, contact dimensions, and ambient conditions (temperature, humidity, and gas) "
            "profoundly govern the overall performance of contact materials."
        ),
        "skill_public_polish_en": (
            "Long lifetime and high reliability of electromechanical switches, which are used in the high-end equipment "
            "manufacturing industry, are always required. Admittedly, repetitive hot-switching operations result in "
            "contact welding, high contact resistance, and severe contact erosion, which are closely related to the "
            "electrical characteristics of the contact material. Here, the electrical characteristics of the contact "
            "material refer to the anti-welding ability, arcing properties, and general physical properties. Recently, "
            "the electrical characteristics of silver oxide contact materials and the associated degradation mechanisms "
            "have become an important concern of manufacturers and users [CIT]. Previous studies have revealed that the "
            "electric load (interrupting current and voltage), electric load type (resistive, inductive, capacitive, and "
            "LED), contact force, contact size, and ambient environment (temperature, humidity, and gas) have significant "
            "effects on the electrical performance of contact materials."
        ),
        "skill_full_polish_en": (
            "Long lifetime and high reliability of electromechanical switches, which are used in the high-end equipment "
            "manufacturing industry, are always expressly required. Admittedly, the continuous hot switching process "
            "results in contact welding, high contact resistance, and severe contact erosion, which are closely related "
            "to the electrical characteristics of a contact material used in switches. The so-called electrical "
            "characteristics of the contact material are a general term used to refer to the anti-welding ability, arcing "
            "properties, and other general physical properties. Recently, the electrical characteristics of silver oxide "
            "contact material used in switches and the associated degradation mechanism are always an important concern "
            "of contact material manufacturers and users [CIT]. Previous research results have revealed that the electric "
            "load (interrupting current and voltage), electric load type (resistive, inductive, capacitive, and LED), "
            "contact force, contact size, and environment (temperature, humidity, and gas) have significant effects on "
            "the electrical performance of contact materials."
        ),
    },
    # 6. P16 results (para 13)
    {
        "id": "H06_P16_results",
        "paper_id": "P16",
        "section": "results",
        "function": "waveform",
        "para_idx": 13,
        "zh_source": (
            "[FIG 6] 给出了触头分断过程中实测接触电压和电流波形的两个典型实例。"
            "在 [FIG 6] 中，在初始 40 μs 处，电流突然跃变至接近零的极低水平，同时观察到一个接触电压凸起（10 V）。"
            "这主要是由于电路中存在一定电感所致。"
            "随着接触力的减小，接触电流缓慢下降直至触头完全分离，该过程持续 40 μs。等效电路由 [FIG 7] 给出。"
            "如果电压凸起低于最小起弧电压（对于 AgSnO2 材料为 12 V），则不会观察到燃弧现象。"
            "此后，接触电压从 5 V 按指数规律上升至直流电源电位。"
        ),
        "baseline_en": (
            "[FIG 6] illustrates two representative transient waveforms of contact voltage and current captured during "
            "the contact breaking process. Inspection of [FIG 6] reveals that at the onset of the 40 μs window, the "
            "current undergoes an abrupt drop to a near-zero level accompanied by a pronounced 10 V voltage hump, a "
            "phenomenon primarily attributable to parasitic circuit inductance. As the mechanical contact force "
            "progressively diminishes, the current decays gradually over a 40 μs duration until complete contact "
            "separation is achieved, as modeled by the equivalent circuit in [FIG 7]. Provided that this transient "
            "voltage hump remains below the minimum arc ignition threshold (12 V for AgSnO2 metallurgy), arc discharge "
            "is effectively suppressed, and the interfacial voltage subsequently rises exponentially from 5 V toward the "
            "DC supply rail."
        ),
        "ablation_no_examples_en": (
            "Two typical examples of the measured contact voltage and current waveforms during contact breaking are "
            "shown in [FIG 6]. At the beginning of the 40 μs period in [FIG 6], the current drops abruptly to a very low "
            "level near zero, while a contact voltage hump of 10 V is observed. This phenomenon is mainly caused by the "
            "inductance in the circuit. As the contact force decreases, the contact current decreases gradually for 40 μs "
            "until the contacts separate completely. The corresponding equivalent circuit is shown in [FIG 7]. When the "
            "hump voltage is lower than the minimum arc voltage (12 V for AgSnO2 material), no arcing phenomenon occurs. "
            "Subsequently, the contact voltage increases exponentially from 5 V to the DC supply potential."
        ),
        "ablation_no_profile_en": (
            "Two distinct examples of measured contact voltage and current waveforms during contact breaking are shown in "
            "[FIG 6], where at the beginning of 40 μs an abrupt transition to almost zero current occurs accompanied by "
            "a 10 V contact voltage hump due to circuit inductance. With the reduction of contact force, the contact "
            "current decreases slowly for 40 μs until complete breakaway, with the equivalent circuit shown in [FIG 7]. "
            "If the hump voltage is below the 12 V minimum arc voltage for AgSnO2 material, no arcing is observed, and "
            "after that the contact voltage increases exponentially from 5 V to the DC supply potential."
        ),
        "ablation_no_contrastive_en": (
            "Two distinct examples of the measured contact voltage and current waveforms during contact breaking are "
            "shown in [FIG 6]. In [FIG 6], at the beginning of 40 μs, an abrupt transition to a very low current level "
            "near zero occurs. Meanwhile, a hump of contact voltage (10 V) is observed, which is mainly attributed to "
            "the inductance in the circuit. Due to the reduction of contact force, the contact current decreases slowly "
            "until the contacts separate completely, and this stage lasts for 40 μs. The equivalent circuit is shown in "
            "[FIG 7]. If the hump voltage is lower than the minimum arc voltage (12 V for AgSnO2 material), no arcing "
            "phenomenon is observed. After that, the contact voltage increases exponentially from 5 V to the DC supply "
            "potential."
        ),
        "skill_public_en": (
            "[FIG 6] shows two distinct examples of measured contact voltage and current waveforms during the contact "
            "breaking process. In [FIG 6], at the beginning of 40 μs, an abrupt transition to a significantly low current "
            "level near zero occurs, while a hump of contact voltage (10 V) is observed due to the presence of inductance "
            "in the circuit. With the reduction of contact force, the contact current decreases slowly until the contact "
            "separates completely, and this process lasts for 40 μs. The corresponding equivalent circuit is shown in "
            "[FIG 7]. If the hump voltage remains lower than the minimum arc voltage (12 V for AgSnO2 material), then no "
            "arcing phenomenon is observed. Subsequently, the contact voltage increases exponentially from 5 V to the DC "
            "supply potential."
        ),
        "skill_full_en": (
            "[FIG 6] shows two distinct examples of measured contact voltage and current waveforms of contact breaking. "
            "In [FIG 6], at the beginning of 40 μs, an abrupt transition to a significantly low level of almost zero "
            "current occurs; meanwhile, a hump of contact voltage (10 V) is observed, which is mainly due to the "
            "existence of inductance in the circuit. Due to the reduction of contact force, the contact current slowly "
            "decreases until the contact separates completely, and this stage lasts for 40 μs. The equivalent circuit is "
            "shown in [FIG 7]. If the hump voltage remains lower than the minimum arc voltage (12 V for AgSnO2 material), "
            "then no arcing phenomenon is observed. After that, the contact voltage increases from 5 V to the DC supply "
            "potential exponentially."
        ),
        "ai_destylized_en": (
            "[FIG 6] depicts two representative measured waveforms of contact voltage and current during the breaking "
            "process. As evidenced in [FIG 6], at the start of the 40 μs interval, the current plummets abruptly toward "
            "zero while concomitantly generating a 10 V voltage hump—a behavior primarily driven by circuit inductance. "
            "As the mechanical contact force diminishes, the current decays gradually over 40 μs until complete contact "
            "separation occurs, with the corresponding equivalent circuit illustrated in [FIG 7]. Whenever this transient "
            "hump voltage remains below the minimum arc voltage (12 V for AgSnO2), arcing is completely suppressed, and "
            "the contact voltage subsequently escalates exponentially from 5 V toward the DC supply voltage."
        ),
        "skill_public_polish_en": (
            "[FIG 6] shows two representative examples of measured contact voltage and current waveforms during the "
            "contact breaking process. As can be seen from [FIG 6], at the beginning of the 40 μs interval, an abrupt "
            "drop to almost zero current occurs, while a contact voltage hump of 10 V is observed due to circuit "
            "inductance. With the reduction of contact force, the contact current decreases gradually over 40 μs until "
            "the contacts separate completely. The corresponding equivalent circuit is shown in [FIG 7]. If the hump "
            "voltage remains lower than the minimum arc voltage (12 V for AgSnO2), then no arcing phenomenon is observed. "
            "After that, the contact voltage increases exponentially from 5 V to the DC supply potential."
        ),
        "skill_full_polish_en": (
            "[FIG 6] shows two distinct examples of measured contact voltage and current waveforms of contact breaking. "
            "In [FIG 6], at the beginning of 40 μs, an abrupt transition to a significantly low level of almost zero "
            "current occurs; meanwhile, a hump of contact voltage (10 V) is observed, which is mainly due to the "
            "existence of inductance in the circuit. Due to the reduction of contact force, the contact current slowly "
            "decreases until the contact separates completely, and it lasts for 40 μs. The equivalent circuit is shown "
            "in [FIG 7]. If the hump voltage remains lower than the minimum arc voltage (12 V for AgSnO2 material), then "
            "no arcing phenomenon is observed. After that, the contact voltage increases from 5 V to the DC supply "
            "potential exponentially."
        ),
    },
    # 7. P19 mechanism (para 25)
    {
        "id": "H07_P19_mechanism",
        "paper_id": "P19",
        "section": "mechanism",
        "function": "explanation",
        "para_idx": 25,
        "zh_source": (
            "[FIG 14] 总结了外部振动应力对接触电阻（ECR）的影响机理。"
            "外部振动引起插头与插座之间的相对位移，进而导致插针与插孔之间产生波动的接触力。"
            "在该接触力作用下，插针相对于插座端部产生周期性的弯曲振动，从而引起插针与插孔之间接触面积的周期性波动。"
            "由于 ECR 从根本上取决于接触力和接触面积，这就解释了外部振动引起的 ECR 波动机理。"
            "此外，插针与插孔之间的振动应力还具有以下附加效应：（1）微动磨损，影响接触表面的形貌和 ECR；"
            "（2）插针与插孔之间的挤压作用使接触区扩展并降低表面粗糙度；"
            "（3）摩擦热是连接器温升的主要来源，进而引起热应力并导致 ECR 发生变化。"
        ),
        "baseline_en": (
            "[FIG 14] encapsulates the underlying physical mechanisms through which external vibrational stresses govern "
            "electrical contact resistance (ECR). External excitation induces relative displacement between the mating "
            "plug and socket shells, which in turn drives cyclic contact force fluctuations across the pin-jack interface. "
            "Subjected to this dynamic loading, the cantilevered pin undergoes periodic flexural oscillations relative to "
            "the socket end, thereby modulating the effective interfacial contact area. Because ECR is fundamentally "
            "governed by the interplay of normal contact force and conducting area, this kinematic chain elucidates the "
            "root cause of vibration-induced ECR instability. Beyond primary mechanical modulation, interfacial vibration "
            "stress introduces three secondary phenomena: (1) fretting wear that progressively alters surface topography "
            "and resistance; (2) cyclic normal squeezing that expands contact spots and flattens surface asperities; and "
            "(3) frictional heating that elevates connector temperature, inducing thermal stresses and further resistance drift."
        ),
        "ablation_no_examples_en": (
            "[FIG 14] summarizes the influencing mechanisms of external vibration stress on electrical contact resistance "
            "(ECR), where external vibration causes relative displacement between the plug and the socket and results in "
            "a fluctuating contact force that forces the pin to undergo periodic bending vibration relative to the socket "
            "end and leads to fluctuations in the contact area between the pin and the jack. Because ECR is mainly "
            "determined by the contact force and contact area, this process explains the mechanism of ECR fluctuation "
            "under external vibration, alongside three secondary effects: (1) fretting wear changing the surface "
            "morphology and ECR; (2) squeezing action between the pin and the jack expanding the contact area and "
            "reducing surface roughness; and (3) frictional heat raising the connector temperature and inducing thermal "
            "stress and ECR variation."
        ),
        "ablation_no_profile_en": (
            "As illustrated in [FIG 14], the influencing mechanisms of external vibration stress on ECR can be explained "
            "as follows: external vibration induces relative displacement between the plug and socket, resulting in a "
            "fluctuating contact force that forces the pin into periodic bending vibration and causes a fluctuating "
            "contact area between the pin and jack. Since ECR is fundamentally determined by contact force and contact "
            "area, this explains the vibration-induced ECR fluctuation, along with three additional effects: (1) fretting "
            "wear affecting surface morphology and ECR, (2) squeezing action expanding the contacts and reducing surface "
            "roughness, and (3) frictional heat causing connector temperature rise, thermal stress, and ECR variation."
        ),
        "ablation_no_contrastive_en": (
            "[FIG 14] summarizes the influencing mechanisms of external vibration stress on ECR. The external vibration "
            "causes relative displacement between the plug and the socket, which results in a fluctuating contact force "
            "between the pin and the jack. Due to this force, the pin is forced to undergo periodic bending vibration "
            "relative to the end of the socket, which causes a fluctuating contact area between the pin and the jack. "
            "Because ECR is fundamentally determined by the contact force and contact area, this explains the ECR "
            "fluctuation mechanism induced by external vibration. Furthermore, the vibration stress between the pins and "
            "jacks has three additional effects: (1) fretting wear, which affects the surface morphology and ECR; "
            "(2) squeezing action between the pins and jacks, which expands the contact spot and reduces surface "
            "roughness; and (3) frictional heat, which is the main source of temperature rise and causes thermal stress "
            "and variation of ECR."
        ),
        "skill_public_en": (
            "[FIG 14] summarizes the influencing mechanisms of external vibration stress on ECR. The external vibration "
            "leads to relative displacement between the plug and the socket, which results in a fluctuating contact force "
            "between the pin and the jack. Under such force, the pin is forced to undergo periodic bending vibration "
            "relative to the end of the socket, causing a fluctuating contact area between the pin and the jack. ECR is "
            "fundamentally determined by the contact force and contact area, which explains the ECR fluctuation mechanism "
            "induced by external vibration. Furthermore, the vibration stress between the pins and jacks has three "
            "additional effects: (1) Fretting wear, which affects the morphology and ECR of the contact surface. "
            "(2) Squeezing action between the pins and jacks, which expands the contact zone and reduces surface "
            "roughness. (3) The frictional heat is a main source of temperature rise, which causes thermal stress and "
            "variation of ECR consequently."
        ),
        "skill_full_en": (
            "[FIG 14] summarizes the influencing mechanisms of external vibration stress on ECR. The external vibration "
            "leads to the relative displacement between the plug and the socket, which in turn results in the fluctuating "
            "contact force between the pin and the jack. The pin is forced to undergo periodic bending vibration relative "
            "to the end of the socket due to such force, causing a fluctuating contact area between the pin and the jack. "
            "ECR is fundamentally determined by contact force and contact area, which explains the ECR fluctuation "
            "mechanism caused by the external vibration. Besides, the vibration stress between the pins and jacks has "
            "additional effects including: (1) Fretting wear, which has an effect on the morphology and ECR of the "
            "contact surface. (2) Squeezing action between the pins and jacks, which makes the contacts expand and "
            "reduces roughness on the surface. (3) The frictional heat is a main source of the connector temperature "
            "rise, which causes thermal stress and variation of ECR consequently."
        ),
        "ai_destylized_en": (
            "[FIG 14] illustrates the comprehensive physical framework governing electrical contact resistance (ECR) "
            "instability under external vibrational loading. Specifically, external excitation induces relative motion "
            "between the mating plug and socket housings, thereby generating cyclic contact force variations across the "
            "pin-jack interface. Driven by this fluctuating load, the pin experiences periodic flexural deflection "
            "relative to the socket termination, which modulates the effective interfacial contact area. Since ECR is "
            "intrinsically governed by the interplay between contact force and conducting area, this kinematic chain "
            "elucidates the primary vibration-induced resistance fluctuation mechanism. Additionally, interfacial "
            "vibrational stresses trigger three secondary effects: (1) fretting wear that degrades surface morphology "
            "and elevates ECR; (2) normal squeezing that enlarges the contact zone and smooths surface asperities; and "
            "(3) frictional heating that drives connector temperature rise, thermal stress, and consequent ECR drift."
        ),
        "skill_public_polish_en": (
            "[FIG 14] summarizes the influencing mechanisms of external vibration stress on electrical contact resistance "
            "(ECR). External vibration induces relative displacement between the plug and the socket, which results in "
            "fluctuating contact force between the pin and the jack. Due to this fluctuating load, the pin is forced to "
            "undergo periodic bending vibration relative to the end of the socket, which causes a fluctuating contact "
            "area between the pin and the jack. ECR is fundamentally determined by contact force and contact area, which "
            "explains the mechanism of vibration-induced ECR fluctuation. In addition, the vibration stress between the "
            "pins and jacks produces three additional effects: (1) Fretting wear, which affects the surface morphology "
            "and ECR. (2) Normal squeezing action between the pins and jacks, which enlarges the contact zone and reduces "
            "surface roughness. (3) Frictional heat is a main source of connector temperature rise, which causes thermal "
            "stress and variation of ECR consequently."
        ),
        "skill_full_polish_en": (
            "[FIG 14] summarizes the influencing mechanisms of external vibration stress on ECR. The external vibration "
            "leads to the relative displacement between the plug and the socket, which in turn results in the fluctuating "
            "contact force between the pin and the jack. The pin is forced to undergo periodic bending vibration relative "
            "to the end of the socket due to such force, causing the fluctuating contact area between the pin and the "
            "jack. ECR is fundamentally determined by contact force and contact area, which explains the ECR fluctuation "
            "mechanism caused by the external vibration. Besides, the vibration stress between the pins and jacks has "
            "additional effects including: (1) Fretting wear, which has an effect on the morphology and ECR of the "
            "contact surface. (2) Squeezing action between the pins and jacks, which makes the contacts expand and "
            "reduces roughness on the surface. (3) The frictional heat is a main source of the connector temperature "
            "rise, which causes thermal stress and variation of ECR consequently."
        ),
    },
    # 8. P19 conclusion (para 26)
    {
        "id": "H08_P19_conclusion",
        "paper_id": "P19",
        "section": "conclusion",
        "function": "summary",
        "para_idx": 26,
        "zh_source": (
            "为了确定机械振动环境下电连接器的失效机理，本文详细实验研究了不同振动幅值和振动频率条件组合下接触电阻（ECR）的响应特性。"
            "选用最大值和波动峰峰值来反映 ECR 的变化特征并评估电连接器的性能。"
            "本文证实，ECR 的瞬态波动频率与振动频率一致，且只有当振动幅值超过 0.1 mm 量级时，ECR 的变化才变得显著。"
            "结构动力学模型表明，与插头和插座壳体间螺纹连接密切相关的固有频率 p、插针的抗弯刚度 EI 以及插针与插孔接触的弹性系数 k 均会影响插针与插孔之间的接触刚度，"
            "进而影响相对位移并导致外部振动应力下 ECR 的明显波动。"
            "本文的研究结果和初步结论可作为预测电连接器工作寿命和机械环境耐受能力的依据。"
        ),
        "baseline_en": (
            "To elucidate the underlying failure mechanisms of electrical connectors operating within mechanical "
            "vibration environments, we have conducted a comprehensive experimental investigation into the electrical "
            "contact resistance (ECR) response across diverse combinations of vibration amplitude and frequency. By "
            "leveraging both peak resistance values and peak-to-peak fluctuation amplitudes as key performance metrics, "
            "our study demonstrates that the transient ECR oscillation frequency is locked to the external excitation "
            "frequency, whereas pronounced resistance degradation emerges only once the vibration amplitude surpasses "
            "the 0.1 mm threshold. Furthermore, our structural dynamics framework reveals that the natural frequency p "
            "associated with the threaded shell coupling, the pin flexural rigidity EI, and the interfacial contact "
            "stiffness k collectively govern the relative pin-jack displacement, thereby driving severe ECR instability "
            "under vibrational loading. Ultimately, these insights provide a robust foundation for predicting the "
            "service life and environmental resilience of aerospace electrical connectors."
        ),
        "ablation_no_examples_en": (
            "In order to clarify the failure mechanism of electrical connectors under a mechanical vibration environment, "
            "the response characteristics of electrical contact resistance (ECR) under different combinations of "
            "vibration amplitude and frequency are experimentally investigated by using the maximum value and peak-to-peak "
            "fluctuation value to characterize the variation of ECR and evaluate connector performance. The results "
            "confirm that the transient fluctuation frequency of ECR equals the vibration frequency and the change of "
            "ECR becomes significant only when the vibration amplitude exceeds the order of 0.1 mm, while the structural "
            "dynamic model shows that the natural frequency p related to the threaded connection, the bending stiffness "
            "EI of the pin, and the elastic coefficient k of the pin-jack contact all affect the contact stiffness and "
            "relative displacement, resulting in obvious ECR fluctuations and providing a basis for predicting the "
            "service life and vibration endurance of electrical connectors."
        ),
        "ablation_no_profile_en": (
            "In order to determine the failure mechanism of electrical connectors under mechanical vibration, the "
            "response characteristics of ECR under different vibration amplitudes and frequencies have been experimentally "
            "investigated in detail, choosing the maximum value and peak-to-peak fluctuation value to reflect ECR "
            "variation and evaluate connector performance. This paper confirms that the transient fluctuation frequency "
            "of ECR is identical to the vibration frequency and the change of ECR becomes significant only above 0.1 mm, "
            "while the structural dynamic model reveals that the natural frequency p of the threaded shell connection, "
            "the pin bending strength EI, and the elastic coefficient k all influence contact stiffness and relative "
            "displacement, providing a basis for predicting the working life of electrical connectors."
        ),
        "ablation_no_contrastive_en": (
            "In order to determine the failure mechanism of electrical connectors under a mechanical vibration "
            "environment, the response characteristics of electrical contact resistance (ECR) under different combinations "
            "of vibration amplitude and frequency are investigated experimentally in detail. The maximum value and "
            "peak-to-peak fluctuation value are selected to reflect the variation features of ECR and evaluate the "
            "performance of electrical connectors. This paper confirms that the transient fluctuation frequency of ECR "
            "is identical to the vibration frequency. Meanwhile, the change of ECR is significant only when the vibration "
            "amplitude exceeds the 0.1 mm magnitude order. Furthermore, the structural dynamic model reveals that the "
            "natural frequency p related to the threaded connection between the plug and socket shell, the bending "
            "stiffness EI of the pin, and the elastic coefficient k of the pin-jack contact all influence the contact "
            "stiffness and relative displacement, resulting in obvious fluctuations of ECR. The conclusions of this paper "
            "can serve as a basis for predicting the working life and mechanical endurance ability of electrical connectors."
        ),
        "skill_public_en": (
            "In order to determine the failure mechanism of electrical connectors under a mechanical vibration "
            "environment, the response characteristics of electrical contact resistance (ECR) under different vibration "
            "amplitude and frequency combinations are investigated experimentally in detail. The maximum value and "
            "fluctuation peak-to-peak value are selected to reflect the variation features of ECR and evaluate the "
            "performance of electrical connectors. Our results confirm that the transient fluctuation frequency of ECR "
            "equals the vibration frequency. Meanwhile, the change of ECR becomes significant only when the vibration "
            "amplitude exceeds the 0.1 mm magnitude order. Furthermore, the structural dynamic model reveals that the "
            "natural frequency p related closely to the threaded connection between the plug and socket shell, the "
            "bending stiffness EI of the pin, and the elastic coefficient k of the pin-jack contact all influence the "
            "contact stiffness. Consequently, these parameters affect the relative displacement and result in obvious "
            "fluctuations of ECR under external vibration stress. The results of this paper can be used as a basis for "
            "predicting the working life and mechanical environment endurance of electrical connectors."
        ),
        "skill_full_en": (
            "In order to determine the failure mechanism of electrical connectors under a mechanical vibration "
            "environment, the response characteristics of electrical contact resistance under different vibration "
            "amplitude and vibration frequency condition combinations are investigated experimentally in detail. The "
            "maximum value and fluctuation peak-peak value are chosen to reflect the variation features of ECR and "
            "evaluate the performance of electrical connectors. This paper confirms that the transient fluctuation "
            "frequency of ECR is the same as the vibration frequency, and the change of ECR is significant only when the "
            "vibration amplitude exceeds the 0.1 mm magnitude order. Furthermore, the structural dynamic model reveals "
            "that the natural frequency p related closely to the threaded connection between the plug and socket shell, "
            "the bending strength EI of the pin, and the elastic coefficient k of the pin and jack contact all influence "
            "the contact stiffness between the pin and jack. This contact stiffness affects the relative displacement "
            "and results in the obvious fluctuation of ECR subjected to external vibration stress. The research and "
            "preliminary conclusions of this paper can be used as a basis for predicting the working life and mechanical "
            "environment endurance ability of electrical connectors."
        ),
        "ai_destylized_en": (
            "To systematically unravel the failure mechanisms of electrical connectors subjected to mechanical vibration, "
            "this study has comprehensively explored the electrical contact resistance (ECR) response across a wide array "
            "of vibration amplitude and frequency combinations. By utilizing the maximum resistance and peak-to-peak "
            "fluctuation magnitude as diagnostic indicators to assess connector reliability, we demonstrate that the "
            "transient ECR oscillation frequency matches the excitation frequency, whereas substantial resistance "
            "degradation manifests only when the vibration amplitude exceeds the 0.1 mm regime. Moreover, our structural "
            "dynamic modeling elucidates how the shell-threading natural frequency p, the pin flexural rigidity EI, and "
            "the interfacial elastic coefficient k collectively modulate the pin-jack contact stiffness and relative "
            "displacement, thereby driving pronounced ECR fluctuations under vibrational stress. Ultimately, these "
            "findings establish a foundational framework for predicting the operational lifetime and mechanical "
            "endurance of electrical connectors."
        ),
        "skill_public_polish_en": (
            "In order to determine the failure mechanism of electrical connectors under mechanical vibration, the "
            "response characteristics of electrical contact resistance (ECR) under different combinations of vibration "
            "amplitude and frequency are investigated experimentally in detail. The maximum resistance and peak-to-peak "
            "fluctuation value are chosen to reflect the variation features of ECR and evaluate the performance of "
            "electrical connectors. This paper confirms that the transient fluctuation frequency of ECR matches the "
            "vibration frequency. Meanwhile, a significant change of ECR occurs only when the vibration amplitude "
            "exceeds the 0.1 mm magnitude order. Furthermore, the structural dynamic model reveals that the natural "
            "frequency p related to the threaded connection between the plug and socket shell, the bending stiffness EI "
            "of the pin, and the elastic coefficient k of the pin-jack contact all influence the contact stiffness. "
            "These parameters affect the relative displacement and result in obvious fluctuations of ECR under external "
            "vibration stress. The results of this paper can be used as a basis for predicting the working life and "
            "mechanical endurance ability of electrical connectors."
        ),
        "skill_full_polish_en": (
            "In order to determine the failure mechanism of electrical connectors under a mechanical vibration "
            "environment, the response characteristics of electrical contact resistance (ECR) under different vibration "
            "amplitude and frequency combinations are investigated experimentally in detail. The maximum value and "
            "fluctuation peak-peak value are chosen to reflect the variation features of ECR and evaluate the performance "
            "of electrical connectors. This paper confirms that the transient fluctuation frequency of ECR is the same "
            "as the vibration frequency, and the change of ECR is significant only when the vibration amplitude exceeds "
            "the 0.1 mm magnitude order. Furthermore, the structural dynamic model reveals that the natural frequency p "
            "related closely to the threaded connection between the plug and socket shell, the bending strength EI of "
            "the pin, and the elastic coefficient k of the pin and jack contact all influence the contact stiffness "
            "between the pin and jack. This contact stiffness affects the relative displacement and results in the "
            "obvious fluctuation of ECR subjected to external vibration stress. The research and preliminary conclusions "
            "of this paper can be used as a basis for predicting the working life and mechanical environment endurance "
            "ability of electrical connectors."
        ),
    },
]

TIER_B_BENCHMARKS: list[dict[str, Any]] = [
    # 1. P17 modeling para 12 (contains rhetorical question F34 + "Let ... being" grammar error)
    {
        "id": "B01_P17_modeling",
        "paper_id": "P17",
        "section": "modeling",
        "function": "model_setup",
        "para_idx": 12,
        "student_drift_markers": ["F34 (rhetorical question opener)", "grammar ('Let the radius ... being constant')"],
        "skill_full_polish_en": (
            "To clarify whether the electrodynamic force is more closely related to the cross-sectional area or the "
            "perimeter of contact bridges, a hollow cylindrical contact model is built, and the schematic of its cross "
            "section is shown in [FIG 5]. The radius of the external circle r1 remains constant, whereas the contact "
            "area is varied by changing the radius of the inner circle r2. Thus, the contact area can be expressed as "
            "[EQ]. In order to investigate the electrodynamic force of stationary contact pairs with multiple contact "
            "a-spots, we first consider the two-contact a-spots case, whose geometric dimensions (d, l, θ, r, and R) "
            "are specified in [FIG 6]. Kawase et al. [CIT] stated that the deviation of the contact bridge from the "
            "contact center O affects the electrodynamic force substantially. Therefore, the distance between each of "
            "the two contact spots and the origin O is uniformly set as d, namely 0.5 and 1 mm, respectively. The "
            "straight-line distance between the two contact spots is l, which satisfies 0 < l < 2d. For simplicity, we "
            "define the normalized distance l* = l/2d, which yields sin(θ/2) = l*."
        ),
    },
    # 2. P18 introduction para 2 (contains "It is top-urgent" F32 + "Ever published research results" F31)
    {
        "id": "B02_P18_introduction",
        "paper_id": "P18",
        "section": "introduction",
        "function": "background",
        "para_idx": 2,
        "student_drift_markers": ["F32 ('It is top-urgent to')", "F31 ('Ever published research results')"],
        "skill_full_polish_en": (
            "It is becoming increasingly important to understand and determine the failure mechanisms of silver tin "
            "oxide composite materials, which are widely used in switching devices. Previous research results have "
            "revealed that the electric load (interrupting current and voltage), electric load type (resistive, "
            "inductive, capacitive, and LED), contact force, contact size, and ambient environment (temperature, "
            "humidity, and gas) have significant effects on the electrical performance of contact materials. In "
            "particular, the capacitive load is commonly encountered in DC voltage networks [CIT]. The high inrush "
            "current occurring at the moment of contact making increases the welding probability of contacts during the "
            "making process [CIT]. Therefore, the degradation process and typical characteristics of silver tin oxide "
            "composite materials during electrical endurance tests are investigated as an important concern in this "
            "research field."
        ),
    },
    # 3. P20 introduction para 3 (contains "However, to the best of our knowledge" F30 + "The existed")
    {
        "id": "B03_P20_introduction",
        "paper_id": "P20",
        "section": "introduction",
        "function": "gap",
        "para_idx": 3,
        "student_drift_markers": ["F30 ('However, to the best of our knowledge')", "L2 participle ('The existed sliding distance')"],
        "skill_full_polish_en": (
            "However, relatively little is known about the quantitative effects of sliding behavior on electrical "
            "contact performance in relay spring systems. Admittedly, the non-rectilinear movement of the moving contact "
            "necessarily produces relative sliding motion between the mating contact surfaces. An appropriate sliding "
            "distance (SD) can improve the reliability of static contact by wiping off dust and thin oxide films on the "
            "contact surface [CIT]. On the other hand, an excessive increase in SD leads to higher mechanical energy "
            "consumption and severe surface wear. Recently, numerical simulations of the mechanical operation of "
            "switching device prototypes based on commercial finite-element analysis (FEA) software have been conducted "
            "to determine the optimal combination of structural and dimensional parameters [CIT]. Furthermore, Xiong et "
            "al. [CIT] applied the dynamic Euler–Bernoulli beam theory to spring systems and modeled the contact force "
            "by using the Kelvin–Voigt viscoelastic contact model to reduce contact bounce. Ciocirlan and Herrmann [CIT] "
            "used the principle of eccentric impact to convert the rebound motion of the contacts after initial impact "
            "into sliding motion. Nevertheless, because the switching process involves both electric arcing and material "
            "erosion, designing or modifying a moving-contact mechanism remains challenging."
        ),
    },
    # 4. P23 introduction para 3 (contains "Ever published research results" F31 + "Regards to")
    {
        "id": "B04_P23_introduction",
        "paper_id": "P23",
        "section": "introduction",
        "function": "prior_work",
        "para_idx": 3,
        "student_drift_markers": ["F31 ('Ever published research results')", "grammar ('Regards to contact materials')"],
        "skill_full_polish_en": (
            "Previous research results have revealed that contact welding correlates closely with internal mechanical "
            "structures, contact material properties, current levels, and load types. The degradation of mechanical "
            "structural parameters in electromechanical relays can aggravate dynamic contact welding [CIT]. Meanwhile, "
            "contact welding is significantly influenced by the contact bounce pattern [CIT], particularly when a single "
            "bounce of short duration occurs [CIT]. By contrast, the rolling and sliding motion during contact making "
            "can effectively suppress welding failure [CIT]. With regard to contact materials, such as Ag/CdO, Ag/SnO2, "
            "and Ag/ZnO, additives of metal oxides with low melting and boiling points (Bi2O3, ZnO, and CuO) are used "
            "to reduce the welding force [CIT]. Furthermore, previous studies on the contact welding behavior under "
            "different current levels and load types showed that a higher load current increases both the welding "
            "probability and the welding force amplitude [CIT]."
        ),
    },
    # 5. P23 mechanism para 25 (contains "As above mentioned" F35 + incomplete conditional "If the transient..., which is")
    {
        "id": "B05_P23_mechanism",
        "paper_id": "P23",
        "section": "mechanism",
        "function": "explanation",
        "para_idx": 25,
        "student_drift_markers": ["F35 ('As above mentioned')", "incomplete clause ('If the transient..., which is written by')"],
        "skill_full_polish_en": (
            "Based on the above analysis, the generated molten bridge energy Qm during the contact breaking process can "
            "be expressed as [EQ]. Here, E is the supply voltage, Ii is the transient contact current, Ui is the "
            "transient contact voltage drop, t0 represents the initial moment of contact break, and t1 represents the "
            "moment of molten bridge rupture. In addition, Rci is the transient molten bridge resistance, f is the "
            "sampling frequency of 250 kHz, n is the sample number, and R is the series load resistance in the circuit. "
            "Meanwhile, the transient molten bridge resistance can be approximated by the constriction resistance, which "
            "is written as [EQ]. In this expression, ρ is the electrical resistivity of the contact material, and ai and "
            "Ai denote the radius and cross-sectional area of the transient molten bridge, respectively."
        ),
    },
    # 6. P24 modeling para 12 (contains "We give the following assumptions, that is:" F36 + "equals to" F09)
    {
        "id": "B06_P24_modeling",
        "paper_id": "P24",
        "section": "modeling",
        "function": "model_setup",
        "para_idx": 12,
        "student_drift_markers": ["F36 ('We give the following assumptions, that is:')", "F09 ('equals to')"],
        "skill_full_polish_en": (
            "To simplify the analytical derivation, the following assumptions are made in the model: (1) The melting "
            "zone consists of two symmetrical hemispheres, and there is no heat exchange across the contact interface. "
            "(2) The expansion of the melting zone ceases when the contact temperature reaches a steady state, where r1 "
            "denotes the boundary radius between the liquid zone and the solid zone at the melting temperature Tm. "
            "Furthermore, the melting area πr12 is defined as the mechanical contact area after expansion, over which "
            "the load current is uniformly distributed. (3) The mechanical deformation of the heated material and the "
            "further expansion of the contact area induced by the load force are neglected. (4) Because the radius of "
            "the contact zone is much smaller than the electrode dimension, the outer boundary of the solid zone is "
            "treated as infinity. (5) The final welding zone is equal to the melting zone."
        ),
    },
]
