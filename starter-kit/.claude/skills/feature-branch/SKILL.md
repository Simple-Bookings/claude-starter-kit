---
name: feature-branch
description: Start nyt arbejde i en feature-branch fra develop og hold git-flowet simpelt.
allowed-tools: Bash, Read
---

# Feature Branch

## Standard-flow

```bash
git checkout develop
git pull origin develop
git checkout -b feature/kort-beskrivelse
```

## Regler

- Branch altid fra `develop`
- Lav små commits der efterlader repoet i en fungerende tilstand
- Opret PR til `develop`, ikke `main`

## Før PR

Kør test og build med de kommandoer der er defineret i `CLAUDE.md` → Key commands. Eksempel for npm-projekter:

```bash
npm test
npm run build
```

Sync derefter med develop:

```bash
git fetch origin develop
git merge origin/develop --no-edit
```
