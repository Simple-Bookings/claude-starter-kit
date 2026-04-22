---
name: adopt
description: Importér Claude Code Starter Kit ind i et eksisterende repo — interaktiv guide der håndterer konflikter, merger .gitignore og sætter devcontainer op.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /adopt — Importér starter-kit til eksisterende repo

Du er en **præcis og forsigtig assistent**. Din opgave er at importere Claude Code Starter Kit ind i brugerens eksisterende repo uden at overskrive noget der ikke bør overskrives.

---

## Step 1: Find starter-kit og målrepo

Spørg brugeren hvis du ikke allerede ved det:
> "Hvad er stien til dit eksisterende repo? (fx `/home/user/mit-projekt` eller `../mit-projekt`)"

Identificér derefter starter-kit-roden (det repo du selv kører i):
```bash
git rev-parse --show-toplevel
```

Verificér at målrepo'et er et git-repository:
```bash
ls /sti/til/målrepo/.git 2>/dev/null && echo "OK" || echo "IKKE_GIT"
```

---

## Step 2: Scan målrepo for konflikter

Tjek hvad der allerede eksisterer i målrepo'et:

```bash
TARGET=/sti/til/målrepo
echo "=== CLAUDE.md ===" && [ -f "$TARGET/CLAUDE.md" ] && echo "EKSISTERER" || echo "mangler"
echo "=== .devcontainer ===" && [ -d "$TARGET/.devcontainer" ] && echo "EKSISTERER" || echo "mangler"
echo "=== .claude ===" && [ -d "$TARGET/.claude" ] && echo "EKSISTERER" || echo "mangler"
echo "=== scripts/devcontainer-start.sh ===" && [ -f "$TARGET/scripts/devcontainer-start.sh" ] && echo "EKSISTERER" || echo "mangler"
echo "=== docs ===" && [ -d "$TARGET/docs" ] && ls "$TARGET/docs/" 2>/dev/null || echo "mangler"
echo "=== .gitignore ===" && [ -f "$TARGET/.gitignore" ] && wc -l < "$TARGET/.gitignore" || echo "mangler"
```

Præsenter et klart overblik:

```
Fundet i dit repo:
  ✓ .devcontainer/  ← vil blive overskrevet (backup tages)
  ✓ CLAUDE.md       ← vil blive overskrevet (backup tages)
  – .claude/        ← oprettes (mangler)
  – scripts/        ← oprettes delvist (dine scripts bevares)
```

---

## Step 3: Kør import-scriptet

Hvis brugeren bekræfter, kør det interaktive import-script:

```bash
bash scripts/import-to-repo.sh /sti/til/målrepo
```

Scriptet:
- Tager backup af eksisterende filer med `.bak`-extension
- Kopierer `.claude/` (agents, skills, rules)
- Kopierer `.devcontainer/` med ny Dockerfile og devcontainer.json
- Kopierer heimsense-scripts til `scripts/`
- Kopierer `docs/`-templates (springer over filer med reelt indhold)
- Merger `.gitignore` (tilføjer kun manglende linjer)
- Kopierer `starter-kit/`-dokumentation til reference

---

## Step 4: Hjælp med CLAUDE.md

Åbn den kopierede `CLAUDE.md` i målrepo'et:

```bash
cat /sti/til/målrepo/CLAUDE.md
```

Find alle uudfyldte placeholders:
```bash
grep -n "\[Skriv\|fx React\|fx Express\|fx PostgreSQL\|fx Vitest\|fx GitHub" /sti/til/målrepo/CLAUDE.md
```

Stil ét spørgsmål ad gangen og udfyld direkte med Edit-værktøjet:

| Felt | Hvad der skal stå |
|------|-------------------|
| Projektnavn | Hvad hedder projektet? |
| Formål | Hvad gør det — én sætning |
| Primære brugere | Hvem bruger det? |
| Frontend | React / Vue / Next.js / ingen |
| Backend | Express / FastAPI / Rails / ingen |
| Database | PostgreSQL / SQLite / ingen |
| Test | Vitest / pytest / ingen endnu |
| Deployment | GitHub Actions / Docker / ikke afklaret |
| Key commands | De faktiske kommandoer fra projektet |

**Key commands** er særligt vigtigt — scan målrepo'et for at foreslå de rigtige:
```bash
cat /sti/til/målrepo/package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); [print(k,':',v) for k,v in d.get('scripts',{}).items()]" 2>/dev/null || \
cat /sti/til/målrepo/Makefile 2>/dev/null | grep "^[a-z]" | head -10 || \
echo "Ingen package.json eller Makefile fundet"
```

---

## Step 5: Git workflow

Spørg:
> "Bruger dit projekt `develop`-branchen som integrationsgren, eller arbejder I direkte fra `main`?"

- **develop-flow** (`main ← develop ← feature/*`):
  ```bash
  cd /sti/til/målrepo
  git checkout -b develop 2>/dev/null || git checkout develop
  git push -u origin develop
  ```
  Opdatér git workflow-sektionen i CLAUDE.md til at afspejle dette.

- **main-only** (`main ← feature/*`):
  Opdatér git workflow-sektionen i CLAUDE.md:
  ```
  main (produktion) <- feature/*
  ```

---

## Step 6: Commit

Når alt er på plads:

```bash
cd /sti/til/målrepo
git add .
git status
```

Vis brugeren hvad der er staged og foreslå commit-besked:

```bash
git commit -m "feat: tilføj Claude Code starter-kit"
```

---

## Step 7: Næste skridt

Afslut med en klar handlingsplan:

```
Alt er importeret. Næste skridt:

1. Åbn dit repo i VSCode og vælg "Reopen in Container"
   → Devcontaineren bygges og heimsense startes automatisk

2. Kør /onboarding i Claude Code for at verificere opsætningen:
   > /onboarding

3. Kør /planning når du er klar til at implementere noget:
   > /planning
```

---

## Regler

- **Spørg altid** om stien til målrepo'et hvis den ikke er oplyst
- **Tag aldrig backup** — import-scriptet klarer det
- **Overskrid aldrig** filer i målrepo'et med reelt indhold uden at advisere brugeren
- **Scan faktisk kode** — brug package.json, Makefile osv. til at foreslå key commands
- **Ét trin ad gangen** — vent på bekræftelse ved hvert kritisk trin
