# 🏄 Surfing — Parallel Agent Orchestration

Kører op til 5 agenter parallelt via TeamCreate + git worktrees.

**Aktivering:** `/surf` eller `/surfing`

---

## Quick Start (TL;DR)

Erfarne surfers — her er hele flowet i 10 trin:

```
1. LINEUP:    gh issue list --state open --label "status:ready" --json number,title --limit 20
2. CLAIM:     gh issue edit {NR} --add-label "status:in-progress" --remove-label "status:ready"  (×3)
3. FETCH:     git fetch origin develop
4. BOARDS:    ./scripts/worktree-create.sh feat/dod-1088-beskrivelse  (×3, max 3 worktrees!)
5. TEAM:      TeamCreate({ team_name: "wave-N" })
6. TASKS:     TaskCreate({ subject: "#{NR} titel", description: "Worktree: .../..." })  (×3)
7. SURFERS:   Task({ team_name: "wave-N", name: "agent1-frida", model: "haiku", ... })  (×3)
8. STOKE:     Vent på "PR #XXX" beskeder + tjek worktree commits
9. SHUTDOWN:  SendMessage({ type: "shutdown_request" }) → VENT på shutdown_approved  (×3)
10. CLEANUP:  TeamDelete() → ./scripts/worktree-cleanup.sh --force → git worktree prune
              ⚠️ TeamDelete() FØRST (kræver alle terminated), DEREFTER worktree cleanup
```

**Husk:** `gh pr merge --squash` (IKKE `--delete-branch`). Dan overvåger CI. Agent STOP efter merge.

---

## Terminologi

| Surfing | Teknisk | Beskrivelse |
|---------|---------|-------------|
| **Session** | Fuld orkestrering | Multiple waves, start til slut |
| **Wave** | Batch af 5 agenter | Én runde parallelt arbejde |
| **Surfer** | Teammate (agent) | Spawnet agent med egen context |
| **Board** | Worktree | `/workspaces/agent-worktrees/agentN` |
| **Lineup** | Issue-kø | `status:ready` issues, sorteret P0→P3 |
| **Paddle out** | Wave setup | Claim issues, opret boards, spawn surfers |
| **Drop in** | Agent starter | Surfer cd'er til board og læser issue |
| **Ride** | Agent arbejder | Implementer, commit, PR, merge queue |
| **Wipeout** | Fejl | Agent crash, CI rød, merge-konflikt |
| **Stoke** | Succes | PR merged, surfer rapporterer |
| **Shaka** | Wave summary | Resultat-tabel efter wave 🤙 |

---

## Regler (PÅKRÆVET)

Disse er non-negotiable. Bryd dem = wipeout + spildte tokens.

| # | Regel | Detalje |
|---|-------|---------|
| 1 | **TeamCreate ONLY** | Ingen Task tool til orkestrering. `TeamCreate` + `SendMessage` + `shutdown_request` |
| 2 | **max_turns ALTID** | Uden = surfer kører til context limit. Se Model Guide |
| 3 | **STOP-betingelse i HVER prompt** | Surfer stopper efter `gh pr merge`. Ikke før, ikke efter |
| 4 | **Merge queue** | `gh pr merge <NR> --squash --auto`. CI janitor klarer resten |
| 5 | **ALDRIG `gh pr checks --watch`** | Blokerer agent og forhindrer shutdown! Brug `--auto` |
| 6 | **Board path** | `/workspaces/agent-worktrees/agent1-5`. IKKE simple-bookings-worktrees |
| 7 | **Feature branches** | `fix/dod-XXXX-desc` eller `feat/issue-XXXX-desc`. ALDRIG develop |
| 8 | **Label workflow** | `status:ready` → `status:in-progress` som første handling |
| 9 | **Max 3 surfers per wave** | Disk- og RAM-begrænsning. Tjek `df -h /workspaces` og `free -h` |
| 10 | **GPG** | `git -c commit.gpgsign=false` på ALLE commits og rebases |
| 11 | **Co-authored-by** | `Co-authored-by: Persona <persona@simple-bookings.dk>` |
| 12 | **Dan overvåger CI** | Surfers merger og STOPPER. Dan håndterer post-merge issues |
| 13 | **Cleanup efter HVER wave** | Shutdown → vent terminated → TeamDelete → worktree cleanup |
| 14 | **Kort prompt** | Giv issue-nummer, lad surfer læse body selv. Spar context |
| 15 | **ALDRIG `rm -rf` teams** | Brug TeamDelete(). `rm -rf` efterlader orphaned agent-processer |
| 16 | **ALDRIG sleep i agent-prompts** | `sleep` blokerer shutdown. Brug `--auto` på merge i stedet |
| 17 | **Vent på terminated** | ALLE surfers SKAL have svaret `shutdown_approved` FØR TeamDelete |
| 18 | **Max 3 worktrees** | Disk-begrænsning. Tjek `git worktree list` mellem waves |

---

## Wave Lifecycle

### 🏄‍♂️ Paddle Out — Wave Setup

#### 1. Hent lineup

```bash
gh issue list --state open --label "status:ready" --json number,title,labels --limit 20
```

Sortér: P0-critical → P1-high → P2-medium → P3-low

#### 2. Claim 5 issues

```bash
for issue in 1088 1094 1097 1084 1070; do
  gh issue edit $issue --add-label "status:in-progress" --remove-label "status:ready"
done
```

#### 3. Opret 5 boards

```bash
git fetch origin develop
./scripts/worktree-create.sh agent1 fix/dod-1088-button-spacing
./scripts/worktree-create.sh agent2 fix/dod-1094-meta-tags
./scripts/worktree-create.sh agent3 fix/dod-1097-privacy-footer
./scripts/worktree-create.sh agent4 docs/dod-1084-test-docs
./scripts/worktree-create.sh agent5 feat/dod-1070-markdown-render
```

#### 4. Opret team + tasks

```javascript
TeamCreate({
  team_name: "wave-14",
  description: "Surfing wave 14: #1088, #1094, #1097, #1084, #1070"
})

// Én task per issue
TaskCreate({
  subject: "Fix #1088 knap-spacing",
  description: "Issue #1088. Board: /workspaces/agent-worktrees/agent1. Branch: fix/dod-1088-button-spacing",
  activeForm: "Fixing #1088 knap-spacing"
})
// ... gentag for alle 5
```

### 🌊 Drop In — Spawn Surfers

Spawn alle 5 surfers i ÉN besked (parallelt):

```javascript
Task({
  subagent_type: "general-purpose",
  team_name: "wave-14",
  name: "agent1-frida",
  run_in_background: true,
  model: "haiku",
  max_turns: 20,
  prompt: SURFER_PROMPT   // Se Agent Prompt Template nedenfor
})
// ... gentag for agent2-5 med korrekte værdier
```

### 🤙 Ride & Stoke — Monitor

Beskeder ankommer automatisk fra surfers. Ingen polling.

- **Idle-notifikationer** = normalt. Ignorer dem
- **"PR #XXX merged for #YYYY"** = stoke! TaskUpdate → completed
- **Spørg en surfer:** `SendMessage({ type: "message", recipient: "agent1-frida", content: "Status?" })`

### 🧹 Cleanup — Wave Complete

**Automatisk via TeammateIdle hook:** Surfers der har oprettet PR og er idle i 30+ sekunder stoppes automatisk af `.claude/hooks/surfer-idle-check.sh`.

**Wave-afslutning (når alle surfers er færdige):**

```javascript
// TRIN 1: TeamDelete() — når alle surfers er termineret
TeamDelete()
// TeamDelete tjekker for aktive medlemmer og FEJLER hvis nogen stadig kører

// TRIN 2: Cleanup boards EFTER TeamDelete
// Kør i bash:
// ./scripts/worktree-cleanup.sh --force && git worktree prune

// TRIN 3: Verificer rent system
// git worktree list  (kun hovedrepo)
// ls ~/.claude/teams/  (ingen stale teams)
```

**⛔ ALDRIG brug `rm -rf` på team-mapper som workaround!**
Det efterlader orphaned agent-processer der ikke kan stoppes.

**Hvis en surfer sidder fast (ikke auto-stoppet):**
1. Surfer har muligvis ikke oprettet PR endnu — tjek `gh pr list --json number,headRefName -q '[.[] | select(.headRefName == "{BRANCH}")]'`
2. Surfer kan sidde fast i en blocking call (fx `sleep`, `--watch`)
3. Send manuel `shutdown_request`: `SendMessage({ type: "shutdown_request", recipient: "agent1-frida" })`
4. Vent på `shutdown_approved` — `TeamDelete` fejler med aktive medlemmer
5. Sidste udvej: noter agenten som stuck, kør videre, ryd op manuelt senere

Vis Shaka (se format nedenfor), og start næste wave.

---

## Agent Prompt Template

ÉN template. Erstat `{PLACEHOLDERS}`.

```
Du er {PERSONA}, {ROLLE} hos Simple Bookings.

## Board (OBLIGATORISK)
cd /workspaces/agent-worktrees/{AGENT_ID}
AL arbejde SKAL ske her. ALDRIG i /workspaces/simple-bookings/.

## Claim
gh issue edit {NR} --add-label "status:in-progress" --remove-label "status:ready"

## Opgave
GitHub Issue #{NR}: {TITEL}
Læs issue: gh issue view {NR} --json body -q '.body'

## Workflow
1. cd /workspaces/agent-worktrees/{AGENT_ID}
2. Læs issue body og forstå opgaven
3. Læs eksisterende kode
4. Implementer løsningen
5. Skriv tests hvis relevant
6. Commit:
   git -c commit.gpgsign=false commit -m "{TYPE}: {DESC} (#{NR})

   Co-authored-by: {PERSONA} <{persona_lower}@simple-bookings.dk>"
7. Push: git push -u origin {BRANCH}
8. PR: gh pr create --base develop --title "{TYPE}: {DESC} (#{NR})" --body "Part of #{NR}"
9. Merge: gh pr merge {PR_NR} --squash
10. Rapportér: Send besked "STOKE: PR #XXX merged for #{NR}"
11. STOP

⚠️ BRUG ALDRIG "Fixes #", "Closes #" eller "Resolves #" i PR body — det lukker issue automatisk!
Brug KUN "Part of #", "Addresses #" eller "Related to #".

## Regler
- KUN arbejd i /workspaces/agent-worktrees/{AGENT_ID}
- GPG: git -c commit.gpgsign=false
- Merge-konflikt: git fetch origin develop && git -c commit.gpgsign=false rebase origin/develop
- Dansk med æ, ø, å i commits og kommentarer
- ALDRIG gh pr checks --watch (blokerer shutdown!)
- ALDRIG brug sleep (blokerer shutdown!)
- ALDRIG brug "Fixes #" i PR body (lukker issue før DoD er opfyldt)
- Brug gh pr merge --squash --auto (non-blocking, CI janitor klarer resten)

## STOP
Du er færdig efter PR oprettelse + merge --auto. STOP STRAKS.
Brug IKKE ekstra tokens på cleanup, tjek eller opsummering.

— {PERSONA}
```

### Placeholders

| Placeholder | Eksempel |
|-------------|----------|
| `{PERSONA}` | `@frida` |
| `{ROLLE}` | `frontend-udvikler` |
| `{AGENT_ID}` | `agent1` |
| `{NR}` | `1088` |
| `{TITEL}` | `Ret knap-spacing` |
| `{BRANCH}` | `fix/dod-1088-button-spacing` |
| `{TYPE}` | `fix` / `feat` / `docs` / `test` |
| `{DESC}` | `ret knap-spacing` |
| `{persona_lower}` | `frida` |

### Persona-guide

| Issue-type | Persona | Rolle |
|------------|---------|-------|
| Backend, API, database, Prisma | @tom | full-stack udvikler |
| Frontend, UI, React, styling | @frida | frontend-udvikler |
| Tests, E2E, QA, coverage | @scott | QA-tester |
| Security, auth, OWASP | @quinn | sikkerhedsingeniør |
| CI/CD, infra, scripts | @dan | DevOps-ingeniør |
| GDPR, privacy, compliance | @nora | compliance officer |
| AI, webhooks, automations | @ada | AI-specialist |
| Docs, content, branding | @simone | storyteller |

---

## Model & Turns Guide

| Kompleksitet | Model | max_turns | Eksempler |
|-------------|-------|-----------|-----------|
| **Simple** (1-2 filer) | `haiku` | 20 | Ret spacing, tilføj meta tags, opdater docs |
| **Medium** (3-5 filer) | `sonnet` | 30 | Ny API endpoint, component refactor, E2E test |
| **Complex** (6+ filer) | `opus` | 35-40 | Fuld feature med tests + migration + types |

**Tommelfingerregler:**
- Docs-only → haiku
- CSS/styling → haiku
- Backend med tests → sonnet
- Tværgående features → opus
- I tvivl? → sonnet (safe default)

---

## Wipeout Recovery

### 1. Surfer hit max_turns (interrupted)

Surfer gik idle med "interrupted". Betyder max_turns nået — IKKE nødvendigvis fejl.

```bash
# Tjek om PR allerede blev oprettet
# gh pr list --head broken i gh 2.88.1 — brug client-side filter
gh pr list --state open --json number,headRefName -q '[.[] | select(.headRefName == "{BRANCH}")]'

# Hvis PR findes → merge manuelt
gh pr merge <NR> --squash

# Hvis ingen PR → re-spawn med +10 turns
```

### 2. Branch eksisterer allerede

`worktree-create.sh` fejler med "branch already exists".

```bash
rm -rf /workspaces/agent-worktrees/agentN
git worktree prune
git branch -D {BRANCH}
./scripts/worktree-create.sh agentN {BRANCH}
```

### 3. Merge-konflikt

PR kan ikke merges pga. konflikt med develop.

```bash
cd /workspaces/agent-worktrees/agentN
git fetch origin develop
git -c commit.gpgsign=false rebase origin/develop
# Løs konflikter manuelt hvis nødvendigt
git push --force-with-lease origin {BRANCH}
```

### 4. CI fejler på PR

Surfer fixer normalt selv (det er i prompten). Hvis surfer allerede stoppet:

```bash
# Re-spawn med specifik opgave
Task({
  prompt: "Fix CI-fejl på PR #XXX i /workspaces/agent-worktrees/agentN. Læs fejl, ret, push, merge."
  max_turns: 15,
  model: "haiku"
})
```

### 5. Worktree cleanup fejler

Fallback til brute force (KUN agent1-5 — RØR ALDRIG ci-janitor):

```bash
# ⚠️ Tjek ALTID hvilke worktrees der tilhører andre processer!
git worktree list
ps aux | grep ci-janitor  # CI janitor bruger /workspaces/agent-worktrees/ci-janitor

# Fjern KUN agent worktrees
rm -rf /workspaces/agent-worktrees/agent1
rm -rf /workspaces/agent-worktrees/agent2
rm -rf /workspaces/agent-worktrees/agent3
rm -rf /workspaces/agent-worktrees/agent4
rm -rf /workspaces/agent-worktrees/agent5
git worktree prune

# ALDRIG: rm -rf /workspaces/agent-worktrees  ← sletter ci-janitor worktree!
```

### 6. Duplikat-arbejde

To surfers arbejder på samme issue.

```bash
# Forebyg: Claim med label FØR spawn
# Fix: Luk den dårligste PR
gh pr close <NR> --comment "Duplikat af PR #XXX"
```

### 7. Surfer commitede i forkert mappe

Commits endte i `/workspaces/simple-bookings/` i stedet for worktree.

```bash
# Cherry-pick til korrekt branch
cd /workspaces/agent-worktrees/agentN
git cherry-pick <COMMIT_SHA>
git push -u origin {BRANCH}
```

---

## Shaka Format 🤙

### Wave Summary

```
## Wave N Shaka 🤙

| Surfer | Persona | Issue | PR | Status |
|--------|---------|-------|----|--------|
| agent1 | @frida | #1088 | #1149 | STOKE |
| agent2 | @tom | #1094 | #1147 | STOKE |
| agent3 | @quinn | #1097 | #1148 | STOKE |
| agent4 | @scott | #1084 | #1151 | STOKE |
| agent5 | @tom | #1070 | - | WIPEOUT (max_turns) |

Stoke rate: 4/5 (80%)
Wipeouts: agent5 (#1070) → re-spawn i næste wave
```

### Session Summary

```
## Session Complete 🏄

| Wave | Issues | Stoke | Wipeout | Rate |
|------|--------|-------|---------|------|
| 14 | 5 | 5 | 0 | 100% |
| 15 | 5 | 4 | 1 | 80% |
| 16 | 5 | 5 | 0 | 100% |
| **Total** | **15** | **14** | **1** | **93%** |

Wipeouts resolved: agent5 fra wave 15 → merged i wave 16
```

---

## Tips & Gotchas

- **Idle-notifikationer er NORMALT** — surfers sender dem automatisk mellem turns. Ignorer
- **ALDRIG broadcast stop-besked** — Dan håndterer CI. Lad surfers færdiggøre
- **Surfer "done" ≠ det virker** — tjek altid `gh pr view <NR> --json state`
- **Board-navne: `agent1`-`agent5`** — persona-navne hører i prompt, IKKE i path
- **Claim issues FØR spawn** — undgår duplikat-arbejde
- **`git fetch origin develop` FØR boards** — sikrer boards er up-to-date
- **Ingen `/compact` med TeamCreate** — context forbliver rent
- **Surfer DMs til hinanden = OK** — ignorer summaries i idle-notifikationer
- **`df -h /workspaces`** — tjek disk før wave hvis bekymret
- **Hvert team = unikt navn** — `wave-14`, `wave-15`, ... Genbrug ALDRIG
- **`TeamDelete()` EFTER shutdown** — fejler hvis surfers stadig kører
- **Interrupted ≠ fejl** — tjek for eksisterende PR før re-spawn
- **`ci-janitor` worktree er HELLIG** — tilhører CI janitor processen, ALDRIG fjern den
- **Tjek FØR cleanup:** `git worktree list && ps aux | grep ci-janitor` — kun agent1-5 er dine
- **`worktree-cleanup.sh --force` er safe** — scriptet fjerner kun agent1-5, ikke ci-janitor
- **CI janitor klarer merge** — brug `--auto` på PRs, CI janitor håndterer resten

---

## Auto-Memory Deling (Claude Code 2.1.63+)

Worktree-agenter deler automatisk auto-memory med hovedsessionen. Ingen manuel sync nødvendig.

### Hvordan det virker

Claude Code 2.1.63+ lagrer auto-memory i `~/.claude/projects/` baseret på repo-path. Da alle worktrees deler samme git repo, peger de til samme memory-mappe:

```
~/.claude/projects/-workspaces-simple-bookings/memory/MEMORY.md
```

**Alle worktrees i `simple-bookings` repo bruger denne mappe automatisk:**
- Hovedsession i `/workspaces/simple-bookings/`
- Worktree i `/workspaces/simple-bookings/.worktrees/feat-xyz/`
- Agent worktrees i `/workspaces/agent-worktrees/agent1/`

### Hvad det betyder for surfing

| Før 2.1.63 | Efter 2.1.63 |
|------------|--------------|
| Manuel memory-sync mellem worktrees | Automatisk deling |
| Risiko for out-of-sync kontekst | Altid opdateret |
| Scripts til kopiering af MEMORY.md | Ingen scripts nødvendige |

### Gotchas

- **Cura Hub memory (MCP) er separat** — `memory_store`/`memory_recall` via MCP er cloud-baseret og uafhængig af lokal auto-memory
- **MEMORY.md ændringer er øjeblikkelige** — alle worktrees ser ændringer med det samme
- **Projektnøglen er repo-path** — worktrees med forskellig repo-rod får separat memory

---

## ⚠️ Zombie-Agent Prevention (Lært på den hårde måde)

### Problemet

Når du bruger `rm -rf` på team-mapper i stedet for `TeamDelete`, eller kører `TeamDelete` før alle agenter er termineret, får du **orphaned agent-processer** der:
- Stadig vises i UI (idle panes)
- Bruger RAM og tokens
- Ikke kan stoppes via `shutdown_request` (teamet er slettet)
- Overlever på tværs af waves og forurener nye teams

### Root Causes

1. **`rm -rf ~/.claude/teams/wave-N`** — sletter filer men IKKE processer
2. **`TeamDelete` før alle shutdown_approved** — efterlader kørende agenter
3. **Agenter stuck i blocking calls** — `sleep`, `gh pr checks --watch`, `npm run test` der hænger
4. **Worktree-cleanup-script matcher ikke nye path-format** — undermapper som `feat/dod-XXX` fanges ikke

### Løsning: Strict Shutdown Protocol

**Note:** Trin 1-2 er nu automatiseret via TeammateIdle hook (`.claude/hooks/surfer-idle-check.sh`).
Surfers med PR der er idle i 30+ sekunder stoppes automatisk.

```
1. [AUTO] TeammateIdle hook stopper surfers med PR + idle > 30s
2. [AUTO] Surfers terminerer og sender teammate_terminated
3. Verificer: ls ~/.claude/teams/wave-N/config.json → tjek members
4. TeamDelete()  ← FØRST når alle surfers er termineret!
5. ./scripts/worktree-cleanup.sh --force && git worktree prune
6. Verificer: git worktree list (kun hovedrepo)
7. Verificer: ls ~/.claude/teams/ (ingen stale teams)
```

### Hvis du allerede har zombies

```bash
# Find stale teams
ls ~/.claude/teams/

# Send shutdown til alle kendte agent-navne
# (virker kun hvis teamet stadig eksisterer)
SendMessage({ type: "shutdown_request", recipient: "agent2-tom" })

# Hvis teamet er slettet, kan du IKKE nå agenterne
# Eneste løsning: restart Claude Code sessionen
```

### Forebyggelse i Agent-Prompts

Tilføj ALTID disse regler i surfer-prompts:
- `ALDRIG brug sleep` — blokerer shutdown
- `ALDRIG brug gh pr checks --watch` — blokerer shutdown
- `Brug gh pr merge --squash --auto` — non-blocking merge
- `STOP straks efter PR oprettelse` — ingen post-merge cleanup

---

*Battle-tested gennem 37 waves (100+ issues, 80+ merged PRs)*
*Surfing v1.0 — 12. februar 2026*
*Opdateret 17. februar 2026: ci-janitor worktree er hellig*
*Opdateret 17. februar 2026: zombie-agent prevention + strict shutdown protocol*
*Opdateret 6. marts 2026: TeammateIdle hook til auto-stop af surfers med PR*
*Opdateret 6. marts 2026: Dokumenteret auto-memory worktree deling (#4594)*
