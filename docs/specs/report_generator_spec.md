# Report Generator Module Spec

## Purpose

定義 `src/report_generator.py` 如何組合 turtle profile、retrieved RAG context、risk results 與 prompt templates，並呼叫 LLM client 產生 Q&A 與環境診斷報告。

## Responsibilities

- Build RAG Q&A prompts.
- Build environment diagnosis prompts.
- Include retrieved knowledge context.
- Include turtle profile text.
- Include risk checker results for diagnosis.
- Call `llm_client.generate_text`.
- Return formatted outputs and references.

## Inputs

Q&A:

- Turtle profile dictionary.
- User question.
- Retrieved chunks.

Diagnosis:

- Turtle profile dictionary.
- Risk results.
- Retrieved chunks.

## Outputs

Q&A output:

```python
{
    "answer": str,
    "references": list[dict],
}
```

Diagnosis output:

```python
{
    "report": str,
    "risk_summary": str,
    "references": list[dict],
}
```

## Data Format

System prompt must include:

- TurtleCare AI role.
- Use provided context.
- Beginner-friendly advice.
- No veterinary diagnosis.
- Recommend reptile veterinarian for severe, persistent, or worsening symptoms.

Q&A prompt includes:

- Retrieved turtle care knowledge.
- User turtle profile.
- User question.
- Task instructions.

Diagnosis prompt includes:

- Retrieved turtle care knowledge.
- User turtle and tank profile.
- Rule-based risk results.
- Required report sections.

## Error / Fallback Behavior

- If retrieved chunks are empty, prompt should state limited local context.
- If LLM client returns fallback/mock text, pass it through to UI.
- If risk results are empty, include "No major rule-based risks detected, but setup still requires routine monitoring."

## Safety Requirements

- Health answers must avoid diagnosis.
- Diagnosis report must frame risks as husbandry/environment observations.
- Severe symptoms must recommend a qualified reptile veterinarian.

## Implementation Checklist

- [ ] Define shared TurtleCare system prompt.
- [ ] Implement retrieved context formatting usage.
- [ ] Implement Q&A prompt builder.
- [ ] Implement diagnosis prompt builder.
- [ ] Call `generate_text`.
- [ ] Return answer/report with references.
- [ ] Preserve input language where possible.

## Completion Checklist

- [ ] Q&A output includes direct answer and practical suggestions.
- [ ] Health-related Q&A includes safety warning.
- [ ] Diagnosis report includes overall assessment, strengths, risks, priority checklist, daily checklist, weekly checklist, and safety warnings.
- [ ] Retrieved references are returned for UI display.
- [ ] Mock mode still produces usable Q&A and diagnosis outputs.
