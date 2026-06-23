from __future__ import annotations


HEALTH_WARNING_KEYWORDS = [
    "refuse",
    "not eating",
    "swollen",
    "floating",
    "tilt",
    "wound",
    "bleeding",
    "breathing",
    "shell soft",
    "眼睛",
    "不吃",
    "浮",
    "歪",
    "受傷",
    "流血",
    "呼吸",
]


def _risk(category: str, level: str, message: str, suggested_action: str) -> dict:
    return {
        "category": category,
        "level": level,
        "message": message,
        "suggested_action": suggested_action,
    }


def check_risks(profile: dict) -> list[dict]:
    risks: list[dict] = []

    if profile.get("has_basking_area") is False:
        risks.append(
            _risk(
                "Basking Area",
                "high",
                "Aquatic and semi-aquatic turtles need a completely dry basking area.",
                "Add a stable dry basking platform with an easy ramp.",
            )
        )

    if profile.get("has_uvb_light") is False:
        risks.append(
            _risk(
                "UVB Lighting",
                "high",
                "UVB lighting supports calcium metabolism and shell health.",
                "Install an appropriate reptile UVB light and follow replacement guidance.",
            )
        )

    if profile.get("mixed_species") is True:
        risks.append(
            _risk(
                "Mixed Species",
                "medium",
                "Mixed-species housing can cause stress, biting, feeding competition, and injury.",
                "Prepare separation plans and avoid mixed housing unless supervised by an experienced keeper.",
            )
        )

    filtration = str(profile.get("filtration_method", "")).lower()
    if not filtration or filtration == "not provided" or any(word in filtration for word in ["none", "no", "無", "沒有", "weak"]):
        risks.append(
            _risk(
                "Filtration",
                "medium",
                "Turtles produce heavy waste, so weak or missing filtration can quickly reduce water quality.",
                "Use stronger filtration and schedule regular partial water changes.",
            )
        )

    water_depth = profile.get("water_depth_cm")
    shell_length = profile.get("shell_length_cm")
    if (
        isinstance(water_depth, (int, float))
        and isinstance(shell_length, (int, float))
        and water_depth > shell_length * 2
        and profile.get("has_basking_area") is False
    ):
        risks.append(
            _risk(
                "Deep Water Access",
                "high",
                "Deep water without accessible resting or climbing areas may fatigue a turtle.",
                "Add ramps, resting platforms, or shallow resting access.",
            )
        )

    feeding = str(profile.get("feeding_content", "")).lower()
    if not feeding or feeding == "not provided" or any(word in feeding for word in ["unclear", "only shrimp", "只吃蝦", "不清楚"]):
        risks.append(
            _risk(
                "Feeding",
                "medium",
                "Unclear or unbalanced feeding can lead to long-term nutrition issues.",
                "Use quality pellets as a base and adjust vegetables, protein, and calcium by age and species.",
            )
        )

    concern = str(profile.get("current_concern", "")).lower()
    if any(keyword in concern for keyword in HEALTH_WARNING_KEYWORDS):
        risks.append(
            _risk(
                "Health Warning",
                "high",
                "The concern includes possible health warning signs. TurtleCare AI cannot diagnose the cause.",
                "Check husbandry conditions and consult a qualified reptile veterinarian if symptoms are severe, persistent, or worsening.",
            )
        )

    return risks


def format_risk_summary(risks: list[dict]) -> str:
    if not risks:
        return "No major rule-based risks were detected. Continue monitoring water quality, basking, UVB, feeding, and behavior."
    lines = []
    for i, risk in enumerate(risks, start=1):
        lines.append(
            f"{i}. [{risk['level'].upper()}] {risk['category']}\n"
            f"   - {risk['message']}\n"
            f"   - Suggested action: {risk['suggested_action']}"
        )
    return "\n".join(lines)
