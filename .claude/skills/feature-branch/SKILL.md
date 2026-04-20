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

```bash
npm test
npm run build
git fetch origin develop
git merge origin/develop --no-edit
```
