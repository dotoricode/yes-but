# Causal Residue

## Trigger

Use this operator when direct traces are hidden, normalized, or easy for the observed actor to manipulate, or when every proposal keeps searching the same visible surface.

## Transformation

Shift the question from “What trace remains?” to “What had to happen to create this clean state, and what did that work cost?”

```text
hidden surface
→ assumed mechanism
→ prerequisite work
→ paid cost or changed state
→ observer outside the same control boundary
→ contradiction between the surface and the residue
→ falsifying intervention
```

Change one or more observation axes:

- state → process
- present → prior history
- local → global
- same layer → independent layer
- absolute value → relationship between observations

## Explorer questions

1. Which direct signal disappeared or can be manipulated?
2. Under the assumed mechanism, what work creates that appearance?
3. Is the work logically necessary, common in the current implementation, or speculative?
4. What time, calls, memory, energy, cache, retries, ordering, or global state might that work consume or change?
5. Which observer records that residue outside the actor's effective control boundary?
6. Which two observations should be inconsistent if the hidden work occurred?
7. What normal alternative could create the same residue, and which intervention separates the explanations?

## Required candidate

A candidate produced with this operator must identify:

- the hidden signal and assumed mechanism;
- prerequisite work and its necessity level;
- a residue and its observer;
- a relational contradiction, not only a large value;
- a normal alternative explanation;
- a result that would falsify the hypothesis.

Treat an untested candidate as a promising hypothesis. Promote it only when the predicted residue moves with an intervention on the proposed cause, survives a negative control with similar normal cost, and the observer's independence is credible for the threat model.

## Origin lesson

This operator was abstracted from a root-detection idea developed after direct Magisk and mount traces could be hidden. Absolute startup I/O varied too much, and mount count alone varied across devices. The new idea came from relating a clean, small visible mount state to unexpectedly high work already recorded at process birth, then observing the value fall when the suspected cause was disabled. A second line of reasoning used a differently privileged observer to inspect global SELinux policy effects.

The reusable insight is not a particular metric. It is the move from visible artifact to prerequisite work, from one value to a contradiction, and from correlation to a falsifiable intervention. This is a hypothesis generator, not a law that every action leaves an observable residue.
