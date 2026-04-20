---
name: tdd
description: Skriv den fejlende test først og brug red-green-refactor.
allowed-tools: Bash, Read
---

# TDD

## Red -> Green -> Refactor

1. Skriv en test der fejler
2. Skriv mindst mulig kode der gør testen grøn
3. Ryd op uden at ændre adfærd

## Regler

- Fix ikke bugs uden først at kunne reproducere dem i en test
- Beskriv hvad testen faktisk verificerer
- Brug rigtige edge cases, ikke kun happy path
