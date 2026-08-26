# Evidence for the Thinking-Method Library

This note checks the conceptual foundations proposed for `yes-but`. The sources support the individual methods and their mechanics; they do **not** by themselves prove that assigning those methods to LLM agents will produce more novel or correct ideas. That system-level claim needs separate evaluation against a baseline.

## Collaboration protocol

### Brainwriting and independent ideation

- **Supported:** Brainwriting separates private idea generation from later sharing and development. The specific 6-3-5 protocol uses six participants, three ideas, five minutes, then passes written ideas to another participant for extension. A recent open-access paper describes both the historical protocol and a staged implementation with private generation, shared review, feedback, and discussion: [Lee et al., 2026](https://link.springer.com/article/10.1007/s12193-026-00480-9).
- **Supported:** Controlled human experiments identify turn-taking, or production blocking, as an important source of productivity loss in interactive verbal brainstorming. Simulated delays disrupted the organization and flexibility of idea generation: [Diehl & Stroebe, 1987](https://doi.org/10.1037/0022-3514.53.3.497), [Nijstad, Stroebe, & Lodewijkx, 2003](https://doi.org/10.1016/S0022-1031(03)00040-4).
- **Caveat:** `yes-but` should borrow the pattern—independent generation, exchange, then development—not the literal 6-3-5 counts. Production blocking is established for people; preventing early cross-agent anchoring is a plausible AI design objective, not a result established by these studies.

## Invention operators

### TRIZ: contradiction and system levels

- **Supported:** TRIZ distinguishes technical contradictions, where improving one characteristic worsens another, and physical contradictions, where opposite properties are required of the same element. Its aim is to resolve rather than merely compromise around the contradiction: [TRIZ contradiction overview](https://triz.org/contradictions/).
- **Supported:** TRIZ explicitly models nested technical systems and recommends examining interactions across subsystem, system, and supersystem levels: [TRIZ technical systems](https://triz.org/triz-technical-systems/). Its 40 principles are generic prompts abstracted from patent analysis: [TRIZ inventive principles](https://triz.org/principles/).
- **Caveat:** “Contradiction Hunt” and using a contradiction as an adversarial observation surface are `yes-but` abstractions. They are consistent with TRIZ, not named TRIZ procedures validated for every domain.

### Lateral thinking: provocation and escape

- **Supported:** de Bono's method deliberately introduces a provocative, potentially illogical step to move thinking away from familiar patterns. His formal provocation devices include escape, reversal, exaggeration, distortion, and wishful thinking; the provocation is a stepping stone, not the result: [de Bono Group, “Serious Creativity”](https://legacy.debonogroup.com/serious_creativity.php), [official lateral-thinking overview](https://www.lateralthinking.com/what-is-lateralthinking).
- **Caveat:** Extracting a “dominant frame” before applying an escape is a useful implementation rule, but that exact stage name and workflow are a `yes-but` design choice.

### Synectics: analogy across domains

- **Supported:** Synectics was developed around making the familiar strange and the strange familiar through metaphorical mechanisms including direct, personal, and symbolic analogy: [Synectics founders' account](https://synecticsworld.com/founders/), [ERIC review of Synectics](https://files.eric.ed.gov/fulltext/ED201868.pdf).
- **Supported with qualification:** A contemporaneous ERIC record reports Gordon's advice that persistent problems often require analogies less close to the original domain and describes transferring between organic, technical, and human domains: [ERIC ED017044](https://files.eric.ed.gov/fulltext/ED017044.pdf).
- **Caveat:** A distant analogy is a hypothesis generator. The transferred structure must be mapped back explicitly; surface resemblance alone is not evidence.

### Morphological analysis: systematic combination

- **Supported:** General Morphological Analysis decomposes multi-dimensional, non-quantified problem complexes into parameters and possible states, then investigates their relationships and configurations: [Ritchey, *General Morphological Analysis*](https://www.swemorph.com/pdf/gma.pdf).
- **Caveat:** Exhaustive combination grows rapidly and can produce incoherent pairs. `yes-but` should sample unusual but compatible combinations rather than enumerate every cell.

### SCAMPER: mutation checklist

- **Supported:** Eberle presented SCAMPER as a checklist of idea-spurring prompts derived substantially from Osborn's questions: [Eberle, 1972](https://doi.org/10.1002/j.2162-6057.1972.tb00929.x), [ERIC record EJ067371](https://eric.ed.gov/?id=EJ067371).
- **Caveat:** Published expansions of the letters vary, especially `M` and `R`. Treat Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, and Reverse/Rearrange as transformation prompts, not as a completeness guarantee or a novelty score.

## Exploration and trust operators

### C-K theory: concepts and knowledge

- **Supported:** C-K theory models design as interaction between concept space and knowledge space. A concept is a proposition that currently has no logical status in available knowledge—neither true nor false—while design expands concepts and knowledge together: [Hatchuel, Le Masson, & Weil, 2004](https://www.designsociety.org/download-publication/19760/c-k_theory_in_practice_lessons_from_industrial_applica), [Kazakci, Hatchuel, & Weil, 2008](https://www.designsociety.org/publication/26757/a_model_of_ck_design_theory_based_on_term_logic_a_formal_ck_background_for_a_class_of_design_assistants).
- **Caveat:** C-K supports preserving undecidable concepts long enough to identify knowledge gaps. It does not imply that every unsupported idea deserves equal effort. Turning an unknown into a targeted research question is the `yes-but` operationalization.

### Abduction and falsification

- **Supported:** In Peirce's discovery-oriented account, a surprising observation motivates an explanatory hypothesis worth investigating. Abduction introduces a candidate; it does not verify it: [Stanford Encyclopedia of Philosophy, “Peirce on Abduction”](https://plato.stanford.edu/archives/spr2023/entries/abduction/peirce.html). Modern usage often means inference to the best explanation, which is related but not identical: [SEP, “Abduction”](https://plato.stanford.edu/archives/spr2024/entries/abduction/).
- **Supported:** Falsification requires specifying observations that would conflict with a hypothesis and sincerely attempting risky tests. Passing a predicted test corroborates a hypothesis but does not prove it: [SEP, “Scientific Method”](https://plato.stanford.edu/entries/scientific-method/).
- **Caveat:** A failed observation may implicate auxiliary assumptions, measurement error, or implementation details rather than the core hypothesis. Reality checks should record the causal chain and controls, not reduce falsification to one brittle test.

## Origin example: Android camera flash

- **Supported only as a capability fact:** Android defines `PackageManager.FEATURE_CAMERA_FLASH` as the feature indicating that a device camera supports flash: [Android `PackageManager` API](https://developer.android.com/reference/android/content/pm/PackageManager.html#FEATURE_CAMERA_FLASH).
- **Not supported as a detector claim:** The API contract does not say that absence implies an emulator or that presence proves a physical phone. A real device may legitimately lack flash, and a virtual or modified environment may advertise a feature. The example therefore supports the reusable operator “ask which capabilities a genuine member would normally require,” but any authenticity detector needs population data, consistency checks, threat-model analysis, and falsification experiments.

## Safe synthesis for `yes-but`

The evidence supports a three-layer architecture:

1. **Collaboration:** private divergence, delayed exchange, and constructive development.
2. **Invention:** apply distinct operators for contradiction, provocation, analogy, combination, and mutation.
3. **Trust:** preserve undecided concepts, generate explanatory hypotheses, then require evidence and falsifying tests.

Dynamic attendee selection, lens swapping, collision of distant ideas, plateau detection, and a growing operator warehouse are original system-design hypotheses. They should be labeled as such and evaluated by comparing idea diversity, non-reducible novelty, causal clarity, and testability against a simpler independent-generation baseline.
