#!/usr/bin/env python3
"""Generate an offline, non-secret VA scoping and audit evidence plan."""
import argparse
import json
from pathlib import Path

FIELDS=("environment","os","host_count","scanner","authentication","approval","change_window","reporting")
def markdown(data):
    if not isinstance(data,dict): raise ValueError("Expected JSON object")
    missing=[k for k in FIELDS if k not in data]
    if missing: raise ValueError("Missing fields: "+", ".join(missing))
    if not isinstance(data["host_count"],int) or isinstance(data["host_count"],bool) or data["host_count"]<1:
        raise ValueError("host_count must be positive integer")
    if not all(isinstance(data[k],str) and data[k].strip() for k in FIELDS if k!="host_count"):
        raise ValueError("Fields must be nonempty strings")
    def safe(value):
        s=str(value).replace("\r"," ").replace("\n"," ")
        return s.replace("<","&lt;").replace(">","&gt;").replace("|","\\|")
    sections=["# Authenticated VA — Review Plan (Not an executed scan)","",
        "> Planning aid only. Confirm authorization, licensing, credentials and scan safety with responsible teams.","",
        "## Submitted environment (operator supplied)","",
        "| Field | Value |","|---|---|"]
    for k in FIELDS: sections.append("| "+safe(k)+" | "+safe(data[k])+" |")
    sections+=["","## Operator approvals and execution gates","",
        "- [ ] Verify exact authorized assets, owner, exclusions and signed change ticket.",
        "- [ ] Check Nessus edition, plugin feed status and official version-specific documentation.",
        "- [ ] Validate credential storage in a vault and least-privilege delegated access.",
        "- [ ] Pilot on one noncritical authorized server; measure load and authenticated-check success.",
        "- [ ] Confirm safe-check configuration, rate limits, concurrency, timeouts and halt/rollback criteria.",
        "- [ ] Obtain production-owner sign-off for all critical services and maintenance window.",
        "- [ ] Confirm actual scan completion and authentication evidence before reporting findings.",
        "- [ ] Review findings, suppress false positives with approval, assign remediation owners and retest.",
        "- [ ] Export redacted reports and retained evidence under approved retention/access policy.",
        "","## Audit evidence checklist","",
        "| Evidence | Status |","|---|---|",
        "| Scope and written permission | To collect |",
        "| Risk assessment and approved maintenance window | To collect |",
        "| Nessus policy and authenticated checks evidence | To collect |",
        "| Scan activity and performance review | To collect |",
        "| Findings triage and risk acceptance | To collect |",
        "| Remediation tickets and retest outcomes | To collect |",
        "","## Scope limitations","",
        "The guide does not run scans, validate host access, certify compliance or replace vendor instructions."]
    services=data.get("critical_services",[])
    if services:
        if not isinstance(services,list) or not all(isinstance(x,str) for x in services): raise ValueError("critical_services must be strings")
        sections+=["","### Critical services requiring sign-off",""]+["- "+safe(x) for x in services]
    return "\n".join(sections)+"\n"
def main():
    p=argparse.ArgumentParser(description="Create a Nessus VA planning document without scanning")
    p.add_argument("--input",required=True,type=Path)
    p.add_argument("--output",default="VA-Review-Plan.md",type=Path)
    args=p.parse_args()
    doc=markdown(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(doc,encoding="utf-8")
    print("Wrote",args.output)
if __name__=="__main__":main()
