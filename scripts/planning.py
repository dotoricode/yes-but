"""Plan same-provider or mixed independent explorers for a host runtime."""

from typing import Any


VALID_ROLES = ("탐험가",)
DEFAULT_ROLES = ("탐험가", "탐험가", "탐험가")


def plan_review(request: dict[str, Any]) -> dict[str, Any]:
    """Return a capability-aware review plan without starting any provider."""
    mode = request.get("mode", "single-provider")
    if mode not in ("single-provider", "mix"):
        raise ValueError("mode must be single-provider or mix")
    current_provider = request.get("current_provider")
    if current_provider not in (None, "codex", "claude"):
        raise ValueError("current_provider must be codex or claude")
    capabilities = request.get("capabilities", {})
    capability_names = ("codex", "claude", "independent_workers", "parallel")
    if not isinstance(capabilities, dict) or any(
        name in capabilities and not isinstance(capabilities[name], bool) for name in capability_names
    ):
        raise ValueError("capabilities values must be booleans")
    roles = request.get("roles", list(DEFAULT_ROLES))
    if not isinstance(roles, list) or any(role not in VALID_ROLES for role in roles):
        raise ValueError("roles must contain supported specialist roles")
    rotation = request.get("rotation", 0)
    if not isinstance(rotation, int) or rotation < 0:
        raise ValueError("rotation must be a non-negative integer")
    available = [name for name in ("codex", "claude") if capabilities.get(name, False)]
    independent_workers = capabilities.get("independent_workers", False)
    parallel = capabilities.get("parallel", False)
    result: dict[str, Any] = {
        "requested_mode": mode,
        "facilitator": "current-session",
        "synthesizer": "current-session",
        "reality_reviewer": "current-session",
        "review_depth": request.get("review_depth", "standard"),
        "workers": [],
        "can_run_concurrently": False,
        "limitations": [],
    }
    if result["review_depth"] not in ("standard", "deep"):
        raise ValueError("review_depth must be standard or deep")
    if mode == "single-provider":
        if not current_provider or not independent_workers or current_provider not in available:
            result["mode"] = "unavailable"
            result["limitations"].append(
                "Independent workers from the current provider are unavailable; do not simulate a meeting."
            )
            return result
        result["mode"] = "single-provider"
        result["workers"] = [{"role": role, "provider": current_provider} for role in roles]
        result["can_run_concurrently"] = parallel
        if not parallel:
            result["limitations"].append("Parallel execution is unavailable; explorers run sequentially.")
        return result
    if len(available) != 2 or not independent_workers:
        result["mode"] = "unavailable"
        result["limitations"].append("Both independent Codex and Claude workers are required but unavailable.")
        return result
    result["mode"] = "mix"
    result["workers"] = [
        {"role": role, "provider": available[(rotation + index) % len(available)]}
        for index, role in enumerate(roles)
    ]
    result["can_run_concurrently"] = parallel
    if not parallel:
        result["limitations"].append("Parallel execution is unavailable; reviews run sequentially.")
    result["limitations"].append("Cross-provider execution is host-dependent and unverified.")
    return result
