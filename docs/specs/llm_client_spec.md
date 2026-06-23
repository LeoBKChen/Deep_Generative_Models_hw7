# LLM Client Module Spec

## Purpose

定義 `src/llm_client.py` 的 multi-provider text generation client。此模組保留單一公開函式，內部依序嘗試 OpenRouter、OpenAI、Google Gemini，並確保沒有 API key 或所有 provider 失敗時仍能用 mock response 完成 demo。

## Responsibilities

- Provide one simple text generation function.
- Route text generation through configured provider order.
- Support OpenRouter with OpenAI-compatible chat completions.
- Support OpenAI with the Responses API.
- Support Google Gemini through `google-genai`.
- Handle missing API keys through mock mode.
- Handle provider failures gracefully and try the next provider.
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

Provider order:

```python
TEXT_PROVIDER_ORDER = ["openrouter", "openai", "google"]
```

OpenRouter request shape:

```python
client.chat.completions.create(
    model=OPENROUTER_TEXT_MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    temperature=LLM_TEMPERATURE,
)
```

OpenAI request shape:

```python
client.responses.create(
    model=OPENAI_TEXT_MODEL,
    instructions=system_prompt,
    input=user_prompt,
    temperature=LLM_TEMPERATURE,
)
```

Google request shape:

```python
client.interactions.create(
    model=GOOGLE_TEXT_MODEL,
    input=f"{system_prompt}\n\nUser request:\n{user_prompt}",
)
```

## Error / Fallback Behavior

- If `MOCK_MODE=True`, return a structured mock response.
- If a provider is unsupported, skip it and record the provider name.
- If a provider is missing API key or model config, skip it and try the next provider.
- If a provider call fails, catch the exception type and try the next provider.
- If every provider fails, return a readable fallback message plus mock response.
- Do not raise raw API errors to the UI.

## Safety Requirements

- Do not print API keys.
- Do not include secrets in error messages.
- System prompt must include no-veterinary-diagnosis safety behavior.
- Provider failure summaries may include provider names and exception types only.

## Implementation Checklist

- [x] Import OpenAI client.
- [x] Read provider config values.
- [x] Implement `generate_text`.
- [x] Implement mock response helper.
- [x] Implement OpenRouter text provider.
- [x] Implement OpenAI text provider.
- [x] Implement Google text provider.
- [x] Catch provider exceptions and continue fallback chain.
- [x] Return readable fallback text on total failure.
- [x] Keep function interface simple for other modules.

## Completion Checklist

- [ ] Mock mode works without API keys.
- [ ] Real OpenRouter call works when API key and model are configured.
- [ ] Real OpenAI call works when API key and model are configured.
- [ ] Real Google Gemini call works when API key and model are configured.
- [ ] Provider fallback tries the next configured provider after failure.
- [ ] API errors do not crash the App.
- [ ] Returned text is always a string.
- [ ] API key is never exposed.
