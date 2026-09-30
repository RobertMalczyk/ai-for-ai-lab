# Evidence boundary for an AI publisher

The publisher may turn public repository evidence into stories. Audience feedback
may improve titles, pacing and explanation, but it must not select or alter lab
experiments. Version 1 plans are private and require human review.

Validate a plan without network access or credentials:

```bash
PYTHONPATH=src python3 -m ai_for_ai_lab publisher-check --root . \
  publisher/plan.example.json
```

Success emits a compact JSON receipt containing SHA-256 fingerprints for every
evidence reference. Exit 2 emits a stable JSON error for malformed plans, unsafe
or missing evidence, public visibility, disabled review, or any research influence.
The receipt establishes referenced bytes and policy compliance only; it does not
prove a story is accurate, fair, useful, or legally publishable.

This command never renders, uploads, sends mail, reads analytics or calls a paid
service. A later real episode must evaluate whether the contract prevents an
actual unsupported or feedback-driven publishing decision before it is expanded.
