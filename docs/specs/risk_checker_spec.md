# Risk Checker Module Spec

## Purpose

定義 `src/risk_checker.py` 的 deterministic turtle care risk rules。此模組提供穩定的環境風險訊號，輔助 LLM 產生更一致的診斷報告。

## Responsibilities

- Check common turtle care risks from a structured profile.
- Return category, risk level, explanation, and suggested action.
- Avoid veterinary diagnosis claims.
- Support diagnosis report generation.

## Inputs

Normalized diagnosis profile dictionary.

## Outputs

List of risk result dictionaries:

```python
[
    {
        "category": "Basking Area",
        "level": "high",
        "message": "...",
        "suggested_action": "...",
    }
]
```

## Data Format

Risk result:

```python
{
    "category": str,
    "level": "low" | "medium" | "high",
    "message": str,
    "suggested_action": str,
}
```

Recommended functions:

```python
check_risks(profile: dict) -> list[dict]
format_risk_summary(risks: list[dict]) -> str
```

## Error / Fallback Behavior

- Missing fields should produce cautious "unknown / needs confirmation" messages only when useful.
- Empty risk list should return a low-risk summary, not claim the setup is perfect.
- Health symptoms should trigger safety warning, not diagnosis.

## Safety Requirements

- Do not state a symptom has one definite cause.
- For severe, persistent, or worsening symptoms, recommend a qualified reptile veterinarian.
- Mixed-species housing should be treated as a risk.
- Deep water without resting access should be treated as a safety risk.

## Implementation Checklist

- [ ] Check missing basking area.
- [ ] Check missing UVB light.
- [ ] Check mixed-species housing.
- [ ] Check weak or missing filtration.
- [ ] Check deep water without basking/resting access.
- [ ] Check unclear or unbalanced feeding.
- [ ] Check health warning keywords in current concern.
- [ ] Implement risk summary formatting.

## Completion Checklist

- [ ] No basking area returns high risk.
- [ ] No UVB returns medium or high risk.
- [ ] Mixed species returns compatibility risk.
- [ ] Weak filtration returns water quality risk.
- [ ] Health warning symptoms include veterinary caution.
- [ ] Output never claims veterinary diagnosis.
- [ ] Risk summary can be displayed directly in the UI.
