# Demo And Submission Spec

## Purpose

定義 Deep Generative Models HW7 最終 demo 與提交項目的規格，確保專案不只可執行，也能被順利評分。

## Responsibilities

- Prepare demo screenshot or video.
- Verify the running App.
- Prepare repository or shared drive link.
- Prepare required submission filenames.
- Run final validation checklist.

## Inputs

- Completed TurtleCare AI project.
- Running Gradio App.
- Student ID.
- Public GitHub repository link or shared Google Drive link.

## Outputs

Required submission files for this project:

```text
314831018_HW7.txt
314831018_HW7.png
```

Where:

- `314831018_HW7.txt` contains the public GitHub or shared drive link.
- `314831018_HW7.png` is the planned screenshot demo material.

## Data Format

TXT file example:

```text
GitHub Repository:
https://github.com/<user>/<repo>
```

Demo material can be:

- Screenshot proving the App runs and outputs results.
- Short video showing Gradio App usage, only if later requested.

Recommended demo scenarios:

- Q&A tab with a water depth or UVB question.
- Diagnosis tab with missing basking area or missing UVB.
- Tank design tab showing prompt-only output.
- Optional image output only if at least one image provider is configured and reliable.

## Error / Fallback Behavior

- If image generation is unavailable, demo prompt-only mode.
- If real API key is unavailable, demo mock mode and explain it in README/workflow log.
- If GitHub cannot be public, use Google Drive with "Anyone with the link" sharing.

## Safety Requirements

- Demo should not show private API keys.
- Demo should not show private personal data.
- Health-related demo examples should include no-diagnosis safety language.

## Implementation Checklist

- [ ] Confirm App runs locally.
- [ ] Capture screenshot or record video.
- [ ] Include at least one working output from each tab.
- [ ] Create public GitHub repository or shared drive folder.
- [ ] Confirm README and workflow log are included.
- [ ] Create `314831018_HW7.txt`.
- [ ] Create `314831018_HW7.png` demo screenshot.
- [ ] Verify sharing permissions.

## Completion Checklist

- [ ] Source code is accessible from submitted link.
- [ ] Dependency list is included.
- [ ] README is included.
- [ ] workflow log is included.
- [ ] Demo material opens correctly.
- [ ] Demo proves the App has an interactive UI.
- [ ] Demo can succeed in prompt-only mode.
- [ ] Submission filenames match course requirements for Student ID `314831018`.
