# Capability Inversion

## Trigger

Use this operator when a synthetic, copied, simulated, or fraudulent target is being inspected mainly for its own known fingerprints.

## Transformation

Replace “What marks the imitation?” with “What capabilities or capability relationships should a genuine instance naturally have?” Inspect absence, implausible combinations, or inconsistent behavior across related capabilities.

## Required candidate

- Define the genuine class and why the capability is normally expected.
- Prefer relationships among capabilities over one missing flag.
- Name legitimate exceptions and configuration-dependent absence.
- State which layer reports the capability and whether the target can manipulate it.
- Provide a falsifier and a diverse genuine control set.

## Origin lesson

This operator was abstracted from an emulator-detection idea that moved away from emulator fingerprints and toward physical capabilities expected of a real phone, including camera flash support. Its novelty was the inversion from properties of the fake to expectations of the genuine, not the particular Android feature flag.
