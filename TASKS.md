# Graded tasks

Total: 7 points. Submit one PR into your fork that contains all four deliverables.

## Task 1 -- Workflow analysis (2 points)

Create `submission/analysis.md` in your fork. For each of the nine flaws in `.github/workflows/ai-review-insecure.yml`, answer:

1. What is the flaw (1-2 sentences)?
2. Which lecture slide category covers it (prompt injection, secret leakage, output validation, privilege, sandboxing, cost/DoS, supply chain)?
3. What is the concrete exploit scenario? Who does what to trigger it?

Use one short paragraph per flaw. A numbered list is fine.

## Task 2 -- Empirical injection study (2 points)

Run at least **three distinct injection attempts** against the insecure workflow on your fork. Pick from:

- **PR description injection:** PR body instructs the AI to approve the change, to suppress findings, or to append attacker-controlled content (e.g., a link).
- **Source-comment injection:** a code comment in the diff instructs the AI to skip a file, downgrade severity, or accept a "prior approval" claim.
- **Diff-context injection:** added lines that mimic system-prompt framing ("[SYSTEM]...") or pretend to be a prior reviewer output.
- **Indirect injection:** content in a file the reviewer is asked to read (e.g., a new `SECURITY.md`, a docstring, a test fixture).
- **Output-shaping injection:** ask the reviewer to include a specific link, image, footer, or formatting that an attacker benefits from (referrer tracking, phishing).

Record each attempt in `submission/injection.md` with:

1. The exact payload used (verbatim).
2. A link to the resulting PR comment, or a screenshot if you later delete the PR.
3. Outcome: **succeeded**, **partially succeeded** (some but not all of your instruction was followed), or **detected and refused**.

**Important:** It is likely that the frontier model we are using will resist most naive payloads. That is not a failure of the lab -- it is the central finding. At the end of `submission/injection.md`, answer in 3-5 sentences:

1. Of the attempts that were detected, what *category* of defence was the model applying?
2. Of the attempts that succeeded or partially succeeded, what was common about the payload?
3. If you were asked to pick a security control for this workflow, would you rely on the model's resistance? Why or why not?

You get full credit for a thorough attempt log and honest analysis. You do **not** need at least one successful injection to earn the two points.

See [docs/attempt-log.md](docs/attempt-log.md) for the five baseline attempts the instructor ran on the reference implementation -- use them as calibration, not a cheat sheet. Design your own payloads.

## Task 3 -- Hardened workflow (2 points)

Rename `.github/workflows/ai-review-hardened.yml.TODO` to `.github/workflows/ai-review-hardened.yml` and implement it. The hardened workflow must:

- Trigger on `pull_request`, **not** `pull_request_target`.
- Declare `permissions:` explicitly with the minimum set (`contents: read`, `pull-requests: write`).
- Set a `timeout-minutes` value.
- Use `actions/checkout` with a bounded `fetch-depth`.
- Load the API key only in the step that needs it, not job-wide.
- Validate the model's JSON response against a schema before posting any PR comment. Reject and log a non-matching response instead of commenting.
- Apply a findings filter (follow the pattern from `anthropics/claude-code-security-review/claudecode/findings_filter.py`).
- Guard external-contributor PRs with an approval gate (follow the pattern documented in the reference repo's README).

Delete `ai-review-insecure.yml` in the same PR.

Credit is given for referencing the specific file or pattern from the reference repo you reused. Cite it in a short comment at the top of your workflow.

## Task 4 -- Verification (1 point)

Add a file `submission/verification.md` showing:

1. At least one payload from Task 2 that either succeeded or came closest, now producing no compromised output against the hardened workflow. If all your payloads were already detected against the insecure workflow, construct a new one designed specifically to exploit a weakness your hardened workflow explicitly closes (for example: a payload that relies on no-schema output is neutralised by your JSON schema).
2. A screenshot or log excerpt of the hardened workflow rejecting a malformed LLM response. You can force this by temporarily stubbing the API call with a fixture that returns invalid JSON.

## Submission

Open a single PR against `main` of your fork titled `lecture10 submission <your-name>`. Paste the PR URL into Moodle by the deadline. Late submissions lose 1 point per day.

## What will fail this lab

- Patching the insecure workflow in place instead of writing a new one.
- Passing the API key directly in a workflow file or committing it.
- Using `pull_request_target` in the hardened workflow.
- A hardened workflow that still concatenates PR metadata directly into the user prompt without a boundary delimiter or validation step.
