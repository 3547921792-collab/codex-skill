---
name: jev-decision-router
description: Use TypeSafe Jev to choose among skills, plugins, or implementation options when a project has multiple plausible paths.
---

# JEV Decision Router

Use this skill at project start when selecting a Codex skill or built-in plugin, and whenever the user asks to compare multiple implementation approaches. The model doing the selection is TypeSafe Jev; Codex remains responsible for collecting candidates, executing the selected path, and checking the result.

Do not use this skill for deterministic lookups, exact repository rules, or choices with only one viable option. Do not use it to decide whether to invoke this skill.

## Workflow

1. State the decision, constraints, success criteria, and the complete candidate list. Keep candidate IDs stable and include enough evidence for Jev to compare them.
2. Submit one `choice` question to `scripts/jev_decide.py` (or an equivalent HTTP client) with `model: "jev-latest"` and the state as structured JSON.
3. Accept a result only when the returned `choice` is one of the supplied candidate IDs and `confidence` is at least `JEV_MIN_CONFIDENCE` (default `0.60`). Preserve the probabilities in the decision record.
4. If the API is unavailable, credentials are missing, the response is malformed, or confidence is below the threshold, stop the automatic selection and ask the user to choose. Never silently substitute GPT reasoning for the requested JEV decision.
5. Execute only the selected candidate. Re-evaluate if the candidate set, constraints, or evidence changes materially.

## API contract

The helper reads a JSON request from stdin and writes the JSON response to stdout. Set `TYPESAFE_API_KEY`; optionally set `TYPESAFE_API_URL` (default `https://api.typesafe.ai/v1/systemone`), `JEV_MODEL` (default `jev-latest`), and `JEV_MIN_CONFIDENCE`.

Request shape:

```json
{
  "state": {"decision": "...", "constraints": [], "candidates": {}},
  "questions": {
    "selected": {
      "type": "choice",
      "instructions": "Which candidate best satisfies the decision and constraints?",
      "criteria": {"candidate_a": "...", "candidate_b": "..."}
    }
  }
}
```

Jev returns `answers.selected.choice`, `answers.selected.probabilities`, and `answers.selected.confidence`. Treat typed output as a recommendation with uncertainty, not as permission to perform external or irreversible actions.

## Security and privacy

Keep the API key in an environment variable and never place it in files, prompts, logs, or commits. Send only the minimum project context needed for the comparison; remove secrets and personal data. Do not send source code or credentials unless they are necessary to distinguish candidates.
