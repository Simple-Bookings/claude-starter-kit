---
name: feature-branch
description: Start nyt arbejde i en feature-branch og hold git-flowet simpelt.
allowed-tools: Bash, Read
---

# Feature Branch

## Bestem integration-branch

Læs git workflow-sektionen i `CLAUDE.md` for at finde den korrekte integration-branch (`develop` eller `main`):

```bash
grep -A5 "Git workflow" CLAUDE.md 2>/dev/null | head -10
```

Brug `develop` hvis det er beskrevet. Brug `main` hvis `develop` ikke nævnes eller ikke eksisterer:

```bash
git branch -a | grep -q "develop" && echo "develop" || echo "main"
```

## Standard-flow

```bash
BASE=$(git branch -a | grep -q "develop" && echo "develop" || echo "main")
git checkout "$BASE"
git pull origin "$BASE"
git checkout -b feature/kort-beskrivelse
```

## Regler

- Branch altid fra integration-branch (`develop` eller `main` — hvad projektet bruger)
- Lav små commits der efterlader repoet i en fungerende tilstand
- Opret PR til integration-branch, ikke direkte til `main` (medmindre main-only flow)

## Før PR

Kør test og build med de kommandoer der er defineret i `CLAUDE.md` → Key commands. Eksempel for npm-projekter:

```bash
npm test
npm run build
```

Sync derefter med integration-branch:

```bash
BASE=$(git branch -a | grep -q "develop" && echo "develop" || echo "main")
git fetch origin "$BASE"
git merge "origin/$BASE" --no-edit
```
