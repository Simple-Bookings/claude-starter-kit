---
name: workflow
description: Ansvarsområder, delegering og handover-protokol for AI-team coworkers
type: rule
---

# Ansvarsområder & Delegering

**Hver coworker ejer et domæne** (defineret i `profile.md` → `## Ansvarsområder`). Ejerskab betyder: informeres om ændringer, involveres i beslutninger, tildeles relevante issues.

## ⛔ Delegering — ALDRIG bare "sige det højt"

> At nævne en opgave i samtalen er IKKE nok. Den forsvinder i kontekstvinduet og bliver aldrig udført.

**Brug mindst én af disse metoder:**

| Metode | Hvornår | Hvordan |
|--------|---------|---------|
| **GitHub Issue + Label** | Bugs, features, tech debt | Opret issue med `owner:{navn}` label |
| **Email** | Vigtig info, beslutninger, handover | Send til `{navn}@dit-projekt.dk` |
| **Agent Spawn** | Akut, skal gøres NU | `Agent(subagent_type: "{navn}", prompt: "...")` |
| **GitHub Issue Comment** | Tilføj kontekst til eksisterende issue | `gh issue comment {nr} --body "..."` |

## Handover-protokol

Når du støder på noget uden for dit ansvarsområde:

1. **Identificér ansvarlig** — tjek `.claude/team/{navn}/profile.md`
2. **Opret sporbart artefakt** — issue, email eller comment (ALDRIG kun mundtligt)
3. **Inkludér kontekst** — hvad du fandt, hvorfor det er relevant, hvad der skal gøres
4. **Nævn det kort** i samtalen — "Jeg har oprettet #XXXX og tildelt [navn]"

```bash
# ✅ KORREKT — sporbart og handlingsbart
gh issue create \
  --title "fix: kort beskrivelse" \
  --label "owner:dan,P1-high,type:bug" \
  --body "Beskrivelse af problemet og hvad der skal gøres."

# ❌ FORKERT — forsvinder i kontekstvinduet
"Det her er nok noget for Dan."
```
