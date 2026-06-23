# Turtle Profile Module Spec

## Purpose

定義 `src/turtle_profile.py` 如何將 UI inputs 轉成結構化 turtle profile，並格式化成適合 prompt 使用的 readable profile text。

## Responsibilities

- Normalize missing or blank UI inputs.
- Convert yes/no values into booleans.
- Convert numeric fields into `float | None` or `int | None`.
- Build profile dictionaries for Q&A, diagnosis, and design flows.
- Format profile text for LLM prompts.

## Inputs

- Raw UI component values.
- Dictionaries created by `app.py` handlers.

## Outputs

- Normalized profile dictionary.
- Readable profile text.

## Data Format

Profile dictionary:

```python
{
    "species": str,
    "shell_length_cm": float | None,
    "number_of_turtles": int | None,
    "tank_size_cm": {
        "length": float | None,
        "width": float | None,
        "height": float | None,
    },
    "water_depth_cm": float | None,
    "has_basking_area": bool | None,
    "has_uvb_light": bool | None,
    "heating_equipment": str,
    "filtration_method": str,
    "feeding_content": str,
    "mixed_species": bool | None,
    "current_concern": str,
}
```

Recommended functions:

```python
build_qa_profile(...)
build_diagnosis_profile(...)
build_design_profile(...)
format_profile(profile: dict) -> str
```

## Error / Fallback Behavior

- Blank strings become `"Not provided"` in formatted text.
- Invalid numeric values become `None`.
- Missing booleans become `None` or conservative defaults depending on UI flow.
- Formatting must not crash when optional fields are missing.

## Safety Requirements

- Do not infer medical diagnosis from profile fields.
- Use profile only for husbandry and environment context.

## Implementation Checklist

- [ ] Implement numeric normalization helper.
- [ ] Implement boolean normalization helper for `"是"` / `"否"`.
- [ ] Build Q&A profile.
- [ ] Build diagnosis profile.
- [ ] Build design profile.
- [ ] Format profile as readable prompt text.
- [ ] Keep output stable for missing fields.

## Completion Checklist

- [ ] Q&A profile includes species, shell length, and question context.
- [ ] Diagnosis profile includes all tank and care fields.
- [ ] Design profile includes tank size, style, required elements, and avoided elements.
- [ ] Missing values do not crash formatting.
- [ ] Boolean fields normalize correctly from Traditional Chinese UI choices.
