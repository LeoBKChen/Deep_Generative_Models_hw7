# Prompt Generator Module Spec

## Purpose

定義 `src/prompt_generator.py` 如何產生 diffusion-ready turtle tank design prompt、negative prompt、建議材料與安全提醒。

## Responsibilities

- Build tank design prompt request from user requirements.
- Retrieve or consume relevant tank care knowledge.
- Generate English image prompt.
- Generate negative prompt.
- Generate practical material suggestions.
- Generate safety notes.
- Keep design safe and realistic for turtles.

## Inputs

Design input dictionary:

- Turtle species.
- Tank length, width, height.
- Water depth.
- Desired style.
- Required elements.
- Elements to avoid.
- Retrieved chunks.

## Outputs

```python
{
    "image_prompt": str,
    "negative_prompt": str,
    "materials": str,
    "safety_notes": str,
    "references": list[dict],
}
```

## Data Format

Generated English prompt should mention:

- Turtle species.
- Aquarium size and water depth.
- Stable dry basking platform.
- Gentle ramp or accessible climb.
- UVB and heat lamp placement.
- Filter placement.
- Clean water.
- Safe resting areas.
- Realistic layout and selected style.

Negative prompt should avoid:

- Sharp decorations.
- Unstable rock piles.
- Small swallowable gravel.
- Unsafe deep water without rests.
- Crowded layout.
- Dirty water.
- Fantasy-only impossible designs.

## Error / Fallback Behavior

- If LLM is unavailable, return deterministic mock design prompt.
- If user leaves style empty, use realistic clean indoor aquarium design.
- If required elements are empty, include basic safe turtle tank essentials.
- If avoided elements are empty, still include standard unsafe items in negative prompt.

## Safety Requirements

- Prioritize turtle safety over aesthetics.
- Basking platform must allow complete drying.
- Deep water must include resting or climbing access.
- Generated image is visualization only, not engineering blueprint.

## Implementation Checklist

- [ ] Build design requirements text.
- [ ] Include relevant retrieved context.
- [ ] Generate English image prompt.
- [ ] Generate negative prompt.
- [ ] Generate material suggestions.
- [ ] Generate safety notes.
- [ ] Return references for UI.
- [ ] Provide mock fallback.

## Completion Checklist

- [ ] Image prompt is English.
- [ ] Negative prompt includes unsafe design exclusions.
- [ ] Materials are practical and beginner-friendly.
- [ ] Safety notes mention visualization-only limitation.
- [ ] Prompt-only mode works without API key.
- [ ] Output can be passed to optional image generator.
