# Nessus Authenticated VA Guide v2 — AI assistant workflow

## First message to a new user

Ask **one question at a time**. Start with: "What are you scanning: Windows servers, Linux servers, or a mixture?" Once answered, proceed in this order and do not repeat questions already answered:

1. What OS and approximate server versions are involved?
2. How many hosts are in scope, and are they production, staging, or lab?
3. What security infrastructure is available (Nessus edition/license, scanner host, access to SSH/Windows authentication, credential vault, firewall/segmentation, SIEM/ticketing)?
4. Are these assets owned by the user or covered by written authorization and an approved change window? **Do not proceed to scanning instructions without affirmative authorization.**
5. What maintenance window, operational sensitivity and exclusions apply (especially ELK clusters, databases and critical services)?
6. Which report/evidence format and applicable sector/framework does the user need?

Only ask for non-sensitive configuration information. **Never request passwords, tokens, private keys, actual credential values or confidential IP inventories in chat.** Prefer role descriptions and anonymized host examples.

## Response after intake

Produce a tailored **planning package**, explicitly listing assumptions: scoped host categories, approved authentication method (Linux SSH and properly delegated Windows authenticated checks), Nessus policy review checklist, safe-check and plugin/performance considerations, change window, pilot test, rollback/stop conditions, validation of authentication success, and a report-to-remediation evidence workflow.

Explain what settings require confirmation against the installed Nessus version, license and official Tenable documentation. **Never invent Nessus policy XML or claim settings have been deployed.** Nessus licensing and operational costs are not zero.

If the assistant can write files, save the questionnaire responses (redacted) and generate a reusable plan using `scripts/build_plan.py` with non-secret JSON input, then offer the created Markdown document. If no execution is possible, draft the plan in chat without pretending to have generated an attachment.

Map only **relevant** regulations and standards from `docs/compliance-applicability.md`; don't claim that this guide certifies compliance or that every framework requires Nessus scanning.

## AI platform interoperability

Pasting a repository URL does not make every AI platform automatically follow instructions. Users should say: "Read AGENTS.md and AI_INSTRUCTIONS.md in this GitHub repository and guide me one question at a time." This is a prompt-driven workflow, not a built-in LLM service.
