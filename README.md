# Lecture 10 -- AI-Powered Code Review Lab

**Course:** CI/CD Security (KSE, Spring 2026)
**Lecture:** 10 -- AI-Powered Security Tools in CI/CD

## What this lab is

This repository ships a GitHub Actions workflow that calls the Anthropic API via `curl` to review pull requests. **The workflow is intentionally insecure.** Every design decision in `.github/workflows/ai-review-insecure.yml` violates at least one best practice from Lecture 10.

Your job is:

1. Read the insecure workflow and identify why each piece is unsafe.
2. Run a structured injection study against it and document what the model does or does not resist.
3. Replace the insecure workflow with a hardened one, reusing the patterns from [anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review).

See [TASKS.md](TASKS.md) for the graded checklist, [docs/insecure-workflow-analysis.md](docs/insecure-workflow-analysis.md) for a hint sheet that maps each flaw to a specific lecture slide, and [docs/attempt-log.md](docs/attempt-log.md) for the instructor's baseline runs.

## Reality check up front

Modern frontier models are fairly robust against naive prompt injection. Expect several of your payloads to be detected and refused. That is part of the lesson, not a bug in the lab: the model's resistance is empirical and probabilistic, it depends on which model you send the call to, and it provides no guarantee at all for the other structural flaws in this workflow. The hardened version you write must be safe regardless of whether the model happens to catch the attack.

## Three workflow files on purpose

The `.github/workflows/` directory holds three files that demonstrate different design points:

- `ai-review-insecure.yml` -- the lab target. Review it, criticise it, do **not** modify it in place.
- `ai-review-hardened-reference.yml` -- Anthropic's official `claude-code-security-review` action wrapped in a minimal workflow. Runs alongside the insecure one on every PR so you can compare output quality and see what a hardened real-world setup looks like. Read the source on GitHub. Do **not** copy this file verbatim into your Task 3 submission.
- `ai-review-hardened.yml.TODO` -- the file you rename and implement yourself for Task 3. It must reuse the *patterns* from the reference action, not wrap it.

## Repo layout

```
.
|-- README.md                          this file
|-- TASKS.md                           graded tasks + submission format
|-- sample-app/                        tiny Flask API with seeded vulnerabilities
|   |-- app.py                         the target the AI will review
|   |-- requirements.txt
|   `-- tests/test_smoke.py            sanity tests
|-- .github/workflows/
|   |-- ai-review-insecure.yml             the bad workflow (DO NOT fix in place)
|   |-- ai-review-hardened-reference.yml   Anthropic's official action -- study, don't copy
|   `-- ai-review-hardened.yml.TODO        stub you must rewrite and rename to .yml
`-- docs/
    |-- insecure-workflow-analysis.md  per-flaw hints mapped to lecture slides
    |-- hardening-checklist.md         checklist for the hardened workflow
    `-- attempt-log.md                 instructor baseline injection runs
```

## Getting started

1. Fork this repository into your own GitHub account.
2. In your fork, add a repository secret named `ANTHROPIC_API_KEY` with a key that has access to the Claude API. Use a low-budget key -- the insecure workflow does not rate-limit itself.
3. Read Lecture 10 slides before touching anything.
4. Work through [TASKS.md](TASKS.md) in order.
5. Submit via a single PR into your fork. Include the PR URL in Moodle.

## Warning

Do not enable the insecure workflow on a repository that contains real secrets or proprietary code. The workflow sends file contents and PR metadata to a third-party API with no redaction. Keep the lab repo self-contained.

## References

- Lecture 10 slides (on Moodle)
- [anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review) -- the reference the hardened workflow must reuse
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [GitHub Actions security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
