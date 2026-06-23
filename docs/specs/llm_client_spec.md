# LLM Client Module Spec

## Purpose

定義 `src/llm_client.py` 的 OpenRouter / OpenAI-compatible text generation client，並確保沒有 API key 時仍能用 mock response 完成 demo。

## Responsibilities

- Provide one simple text generation function.
- Use OpenAI-compatible chat completions API.
- Read settings from `src/config.py`.
- Handle missing API key through mock mode.
- Handle API errors gracefully.
- Never expose API keys.

## Inputs

```python
system_prompt: str
user_prompt: str
```

## Outputs

```python
generated_text: str
```

Required function:

```python
generate_text(system_prompt: str, user_prompt: str) -> str
```

## Data Format

OpenAI-compatible request shape:

```python
client.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    temperature=LLM_TEMPERATURE,
)
```

## Error / Fallback Behavior

- If `MOCK_MODE=True`, return a structured mock response.
- If OpenRouter call fails, return a readable fallback message.
- If response content is empty, return a clear message explaining no content was generated.
- Do not raise raw API errors to the UI.

## Safety Requirements

- Do not print API keys.
- Do not include secrets in error messages.
- System prompt must include no-veterinary-diagnosis safety behavior.

## Implementation Checklist

- [ ] Import OpenAI client.
- [ ] Read config values.
- [ ] Implement `generate_text`.
- [ ] Implement mock response helper.
- [ ] Catch API exceptions.
- [ ] Return readable fallback text on failure.
- [ ] Keep function interface simple for other modules.

## Completion Checklist

- [ ] Mock mode works without API key.
- [ ] Real OpenRouter call works when API key and model are configured.
- [ ] API errors do not crash the App.
- [ ] Returned text is always a string.
- [ ] API key is never exposed.
