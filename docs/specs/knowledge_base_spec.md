# Knowledge Base Spec

## Purpose

定義 `data/knowledge_base/` 的本地 Markdown 烏龜照護知識庫。此知識庫供 RAG 使用，目標是簡潔、初學者友善、安全且不做獸醫診斷。

## Responsibilities

- Provide curated turtle care content.
- Cover species, tank setup, water quality, lighting, feeding, health warnings, mixed species, and emergency warnings.
- Include health disclaimer.
- Support heading/paragraph chunking for RAG.

## Inputs

Knowledge authoring input:

- `docs/agent.md` requirements.
- Beginner turtle care topics.
- Safety rules.

## Outputs

Eight required Markdown files:

```text
data/knowledge_base/
├── turtle_species.md
├── tank_setup.md
├── water_quality.md
├── lighting_and_basking.md
├── feeding.md
├── common_health_issues.md
├── mixed_species_warning.md
└── emergency_warning.md
```

## Data Format

Each file should use Markdown headings:

```markdown
# Topic Title

## Section

Paragraph content...

- Bullet point
- Bullet point
```

RAG-friendly rules:

- Use clear headings.
- Keep paragraphs concise.
- Include concrete keywords users may ask about.
- Avoid overly long sections.

## Error / Fallback Behavior

- Missing files should be detected by `src/rag.py`.
- If a topic is incomplete, app should still run with available files.
- Health-related missing content should be treated as documentation gap before final submission.

## Safety Requirements

Mandatory disclaimer in `common_health_issues.md`:

```text
TurtleCare AI does not provide veterinary diagnosis.
If symptoms are severe, persistent, or rapidly worsening, consult a qualified reptile veterinarian.
```

Emergency warning content must recommend professional help for severe signs.

## Implementation Checklist

- [ ] Create `data/knowledge_base/`.
- [ ] Write `turtle_species.md`.
- [ ] Write `tank_setup.md`.
- [ ] Write `water_quality.md`.
- [ ] Write `lighting_and_basking.md`.
- [ ] Write `feeding.md`.
- [ ] Write `common_health_issues.md`.
- [ ] Write `mixed_species_warning.md`.
- [ ] Write `emergency_warning.md`.
- [ ] Ensure health disclaimer is present.
- [ ] Ensure headings are RAG-friendly.

## Completion Checklist

- [ ] All eight required files exist.
- [ ] Taiwan stripe-necked turtle, red-eared slider, African side-necked turtle, musk turtle, and map turtle are covered.
- [ ] Tank setup includes basking area, ramps, resting areas, escape prevention, and unsafe decorations.
- [ ] Water quality includes filtration, partial water changes, ammonia, nitrite, nitrate, and dechlorination.
- [ ] Lighting includes UVB, UVA, heat lamp, schedule, and bulb replacement.
- [ ] Feeding includes juvenile/adult differences, pellets, vegetables, animal protein, calcium, and overfeeding risks.
- [ ] Health warning file includes no-diagnosis disclaimer.
- [ ] Mixed-species warning includes stress, biting, competition, quarantine, and separation plans.
- [ ] Emergency warning includes symptoms requiring professional help.
