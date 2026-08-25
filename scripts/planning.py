"""Plan portable solo or mix reviews; worker launching belongs to the host."""

from typing import Any


VALID_ROLES = ("제안자", "반대 검토자", "사실 확인자")


def plan_review(request: dict[str, Any]) -> dict[str, Any]:
    """Return a capability-aware review plan without starting any provider."""
    mode = request.get("mode", "solo")
    if mode not in ("solo", "mix"):
        raise ValueError("mode must be solo or mix")
    capabilities = request.get("capabilities", {})
    capability_names = ("codex", "claude", "independent_workers", "parallel")
    if not isinstance(capabilities, dict) or any(
        name in capabilities and not isinstance(capabilities[name], bool) for name in capability_names
    ):
        raise ValueError("capabilities values must be booleans")
    roles = request.get("roles", list(VALID_ROLES))
    if not isinstance(roles, list) or any(role not in VALID_ROLES for role in roles):
        raise ValueError("roles must contain supported specialist roles")
    rotation = request.get("rotation", 0)
    if not isinstance(rotation, int) or rotation < 0:
        raise ValueError("rotation must be a non-negative integer")
    require_both = request.get("require_both", False)
    if not isinstance(require_both, bool):
        raise ValueError("require_both must be a boolean")

    available = [name for name in ("codex", "claude") if capabilities.get(name, False)]
    independent_workers = capabilities.get("independent_workers", False)
    parallel = capabilities.get("parallel", False)
    result: dict[str, Any] = {
        "requested_mode": mode,
        "facilitator": "current-session",
        "decision_maker": "current-session",
        "review_depth": request.get("review_depth", "standard"),
        "workers": [],
        "can_run_concurrently": False,
        "limitations": [],
    }
    if result["review_depth"] not in ("standard", "deep"):
        raise ValueError("review_depth must be standard or deep")
    if mode == "solo":
        result["mode"] = "solo"
        result["workers"] = [{"role": role, "provider": "current-session"} for role in roles]
        return result
    if require_both and (len(available) != 2 or not independent_workers):
        result["mode"] = "unavailable"
        result["limitations"].append("Both independent Codex and Claude workers are required but unavailable.")
        return result
    if not available or not independent_workers:
        result["mode"] = "solo"
        result["workers"] = [{"role": role, "provider": "current-session"} for role in roles]
        if not independent_workers:
            result["limitations"].append("Independent workers are unavailable; using the current session.")
        else:
            result["limitations"].append("No mix provider is available; using the current session.")
        return result
    result["mode"] = "mix"
    result["workers"] = [
        {"role": role, "provider": available[(rotation + index) % len(available)]}
        for index, role in enumerate(roles)
    ]
    result["can_run_concurrently"] = parallel
    if len(available) == 1:
        result["limitations"].append("Only one mix provider is available; independent cross-provider review is unavailable.")
    if not parallel:
        result["limitations"].append("Parallel execution is unavailable; reviews run sequentially.")
    result["limitations"].append("Cross-provider execution is host-dependent and unverified.")
    return result
