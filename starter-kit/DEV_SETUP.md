# Lokal VSCode Devcontainer-opsætning

Denne vejledning viser, hvordan du sætter et projekt op lokalt med VSCode og en devcontainer.

---

## Krav

### Windows

- **Windows 10 version 2004+** eller **Windows 11**
- **WSL2** med en Linux-distro (Ubuntu 22.04 anbefales)
- **Docker Desktop** (aktivér WSL2-backend under indstillinger)
- **VSCode** med extensionen **Dev Containers** (`ms-vscode-remote.remote-containers`)

> **Hvad er WSL2?**
> WSL2 (*Windows Subsystem for Linux 2*) lader dig køre et rigtigt Linux-miljø direkte på Windows. Det er vigtigt for devcontainers, fordi containere kører Linux-baseret, og WSL2 giver bedre kompatibilitet og performance end ældre Windows-setup.

### macOS

- **macOS 11 Big Sur+** (Intel eller Apple Silicon)
- **Docker Desktop for Mac** (Apple Silicon: brug ARM-versionen)
- **VSCode** med extensionen **Dev Containers** (`ms-vsc5edode-remote.remote-containers`)

---

## Trin-for-trin: Windows (WSL2)

### 1. Aktivér WSL2

Åbn **PowerShell som administrator** og kør:

```powershell
wsl --install
```

Genstart computeren, og åbn derefter **Ubuntu** fra Start-menuen. Opret en Linux-bruger, når du bliver bedt om det.

Verificér WSL2 er aktivt:

```powershell
wsl --list --verbose
```

Du bør se `VERSION 2` ud for din Ubuntu-distro.

### 2. Installér Docker Desktop

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Kør installeren
3. Åbn Docker Desktop → **Settings → Resources → WSL Integration**
4. Aktivér integration med din Ubuntu-distro
5. Klik **Apply & Restart**

Verificér Docker virker inde i WSL2:

```bash
docker --version
docker run hello-world
```

> **WSL2-hukommelsesgrænse:** Docker Desktop bruger som standard op til 50% af systemhukommelsen. Er din PC under 16 GB RAM, kan du støde på OOM-fejl under build. Opret filen `C:\Users\<dit-navn>\.wslconfig` med:
>
> ```ini
> [wsl2]
> memory=8GB
> swap=4GB
> ```
>
> Genstart WSL2 med `wsl --shutdown` og åbn et nyt WSL-vindue.

### 3. Installér VSCode og Dev Containers-extensionen

1. Download og installér [VSCode](https://code.visualstudio.com/)
2. Åbn VSCode → Extensions (`Ctrl+Shift+X`)
3. Søg efter **Dev Containers** og installér `ms-vscode-remote.remote-containers`

### 4. Klon repo'et (inde i WSL2)

Åbn Ubuntu-terminalen og klon til din WSL2-filsystem (ikke Windows-drevet `/mnt/c/` — det er markant langsommere):

```bash
cd ~
git clone <repo-url>
cd <projekt-mappe>
```

### 5. Åbn i devcontainer

```bash
code .
```

VSCode åbner med en notifikation: **"Reopen in Container"** — klik den.

Alternativt: Tryk `Ctrl+Shift+P` og vælg **Dev Containers: Reopen in Container**.

> **Første gang:** Docker bygger containeren fra `.devcontainer/Dockerfile`. Det tager 5-15 minutter afhængigt af din forbindelses hastighed. Efterfølgende genstarter er 10-20 sekunder (layers er cachet).

---

## Trin-for-trin: macOS

### 1. Installér Docker Desktop

1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
   - **Apple Silicon (M1/M2/M3):** Vælg ARM-versionen
   - **Intel:** Vælg Intel-versionen
2. Åbn `.dmg`-filen og træk Docker til Applications
3. Start Docker Desktop og vent på, at "Docker Desktop is running" vises i menubaren

Verificér i Terminal:

```bash
docker --version
docker run hello-world
```

> **Docker-hukommelse på Mac:** Docker Desktop på Mac kører i en Linux-VM med begrænset RAM. Gå til **Docker Desktop → Settings → Resources** og sæt memory til mindst **4 GB** (8 GB anbefales).

### 2. Installér VSCode og Dev Containers-extensionen

1. Download og installér [VSCode](https://code.visualstudio.com/)
2. Åbn VSCode → Extensions (`Cmd+Shift+X`)
3. Søg efter **Dev Containers** og installér `ms-vscode-remote.remote-containers`

### 3. Klon repo'et

```bash
git clone <repo-url>
cd <projekt-mappe>
```

### 4. Åbn i devcontainer

```bash
code .
```

Klik **"Reopen in Container"** i notifikationen (eller `Cmd+Shift+P` → **Dev Containers: Reopen in Container**).

> **Apple Silicon:** Hvis containeren er bygget til `linux/amd64`, bruger Docker automatisk Rosetta 2-emulering — det fungerer, men er lidt langsommere end native ARM. Tjek om dit projekt har en ARM-specifik Dockerfile.

---

## Hvad sker der under "Reopen in Container"?

1. **Docker bygger image** — enten fra et base-image eller en brugerdefineret `Dockerfile`, afhængigt af hvad `.devcontainer/devcontainer.json` specificerer

2. **Features installeres** — valgfrie devcontainer-features fra `devcontainer.json` (f.eks. GitHub CLI, Python, SSH-server)

3. **`postCreateCommand` kører** — typisk installation af afhængigheder og første-gangsopsætning. Se `devcontainer.json` → `postCreateCommand` for præcis hvad der sker i dit projekt.

4. **`postStartCommand` kører** — kommandoer der kører ved hver containerstart (f.eks. start af services)

5. **VSCode-extensions installeres** automatisk — de extensions der er specificeret i `devcontainer.json` → `customizations.vscode.extensions`

---

## Port-forwarding

Devcontaineren eksponerer automatisk porte til din lokale maskine, som konfigureret i `devcontainer.json` → `forwardPorts`.

Portene er tilgængelige på `localhost` — f.eks. `http://localhost:8080`.

I VSCode vises de videresendte porte i **Ports**-panelet (nederst i VSCode, ved siden af Terminal). Her kan du også manuelt tilføje ekstra porte.

> **Bemærk:** Lokalt er portene private (kun tilgængelige på din maskine). I GitHub Codespaces kan porte gøres offentlige til OAuth/CORS — dette er ikke nødvendigt lokalt.

---

## Start applikationen

Når containeren er klar, start applikationen som beskrevet i projektets README. De tilgængelige npm-scripts kan du se med:

```bash
npm run
```

---

## Troubleshooting

### Docker bruger for meget hukommelse (Windows/WSL2)

Symptom: Containeren crasher eller systemet fryser under build.

Løsning: Begræns WSL2's hukommelsesforbrug via `C:\Users\<dit-navn>\.wslconfig`:

```ini
[wsl2]
memory=8GB
swap=4GB
processors=4
```

Kør derefter `wsl --shutdown` i PowerShell og åbn WSL2 igen.

### Docker bruger for meget hukommelse (macOS)

Gå til **Docker Desktop → Settings → Resources** og justér:
- Memory: mindst 4 GB, anbefalet 8 GB
- CPUs: mindst 2, anbefalet 4
- Swap: 1-2 GB

Klik **Apply & Restart**.

### "Reopen in Container" vises ikke

- Verificér at **Dev Containers**-extensionen er installeret
- Tjek at `.devcontainer/devcontainer.json` eksisterer i roden af repo'et
- Prøv `Ctrl/Cmd+Shift+P` → **Dev Containers: Reopen in Container**

### Build fejler med "no space left on device"

Docker's disk-image er fuldt. Ryd op:

```bash
docker system prune -a --volumes
```

> **Advarsel:** Dette sletter alle ubrugte images, containere og volumes. Du kan miste lokal databasedata.

### WSL2 kan ikke tilgå netværket

Prøv at genstarte WSL2 netværket:

```powershell
# I PowerShell som administrator
wsl --shutdown
netsh winsock reset
```

Genstart computeren.

### Containerbuildet er meget langsomt (Apple Silicon)

Docker kører `linux/amd64`-images via Rosetta 2-emulering på Apple Silicon. Det er normalt 2-3x langsommere end native. Det er kun bygge-fasen — appen kører ved normal hastighed bagefter.

### Port er allerede i brug

Hvis en port allerede er i brug lokalt:

```bash
# Find hvilken proces der bruger porten (udskift 8080 med den relevante port)
lsof -i :8080   # macOS/Linux

# Stop processen
kill -9 <PID>
```

### Miljøvariabler er ikke tilgængelige i containeren

Containeren kan arve variabler fra dit lokale miljø via `devcontainer.json → containerEnv`. Tjek `devcontainer.json` for at se præcis hvilke variabler der forventes.

Sæt dem i din lokale shell (`~/.bashrc`, `~/.zshrc` eller `~/.profile`) **inden** du åbner containeren:

```bash
export MIN_VARIABEL="<værdi>"
```

Genindlæs VSCode eller genstart containeren for at ændringer træder i kraft.

---

## Relaterede ressourcer

- [Officiel Dev Containers-dokumentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [Devcontainer-specifikation](https://containers.dev/)

---

## Næste skridt

- **CLI-værktøjer:** Se [`CLAUDE_SETUP.md`](./CLAUDE_SETUP.md) for at installere gh, Claude Code og Heimsense
- **AI-team og skills:** Se [`STARTER_KIT.md`](./STARTER_KIT.md) for at kopiére starter-kittet ind og køre det første Claude Code-flow
