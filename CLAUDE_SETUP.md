# CLI Setup — gh, Copilot, Claude Code og Heimsense

Kom i gang med GitHub CLI, GitHub Copilot, Claude Code og Heimsense på under 30 minutter.
Målet er at køre Claude Code gratis via din Copilot-licens i stedet for at betale direkte til Anthropic.

---

## Forudsætninger

- **Node.js 22+** — [nodejs.org](https://nodejs.org) *(Copilot CLI kræver Node.js 22 eller nyere; `gh` er et separat værktøj med sin egen installation)*
- **GitHub-konto** med en aktiv **Copilot-plan**
- **Terminal** — bash, zsh eller PowerShell

---

## 1. GitHub CLI (`gh`)

### Installation

**Mac:**
```bash
brew install gh
```

**Windows:**
```powershell
winget install GitHub.cli
```

**Linux (Debian/Ubuntu):**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh
```

### Login

```bash
gh auth login
```

Vælg **GitHub.com** → **HTTPS** → **Login with a web browser**. Følg instruktionerne i browseren.

### Verificer

```bash
gh auth status
# ✓ Logged in to github.com as <dit-brugernavn>

gh repo list --limit 5
```

---

## 2. GitHub Copilot CLI

GitHub Copilot i terminalen installeres nu som **Copilot CLI** — et selvstændigt værktøj med kommandoen `copilot`. Det er tilgængeligt på alle Copilot-planer.

### Installation

**npm:**
```bash
npm install -g @github/copilot
```

**Mac med Homebrew:**
```bash
brew install copilot-cli
```

**Windows med winget:**
```powershell
winget install GitHub.Copilot
```

### Verificer

```bash
copilot version
```

### Login

```bash
copilot login
```

Alternativt: start `copilot` og kør `/login` inde i CLI'en.

### Test

```bash
copilot
```

Spørg fx:
```text
Forklar denne kommando: git rebase -i HEAD~3
```

> Den gamle `gh extension install github/gh-copilot`-tilgang er ikke længere anbefalet. GitHubs aktuelle dokumentation peger på Copilot CLI som sit eget værktøj.

### Hent dit Copilot API-token

Du skal bruge dette token til Heimsense i trin 4.

```bash
gh auth token
# Gem outputtet — bruges som ANTHROPIC_API_KEY i Heimsense
```

> **Bemærk:** Tokenet gælder så længe din `gh auth`-session er aktiv. Hvis det udløber, kør `gh auth refresh`.

---

## 3. Claude Code CLI

### Installation

```bash
npm install -g @anthropic-ai/claude-code
```

### Verificer

```bash
claude --version
```

### Første opstart

```bash
claude
```

Ved første kørsel guides du igennem:
- Accepter terms of service
- Vælg tilladelsesniveau (anbefalet: **default** til start)

> Du behøver **ikke** en Anthropic API-nøgle nu — vi sætter Heimsense op i næste trin, så Claude bruger din Copilot-licens i stedet.

---

## 4. Heimsense — Claude via Copilot API

Heimsense er en proxy der oversætter Anthropic API-kald til GitHub Copilot API-formatet. Det betyder at Claude Code bruger din Copilot-licens i stedet for Anthropic-kvota.

```
claude → localhost:18081 (Heimsense) → api.githubcopilot.com → Claude Sonnet/Opus
```

### Installation

**Download seneste release fra GitHub:**

```bash
# Mac (Apple Silicon)
curl -L https://github.com/strowk/heimsense/releases/latest/download/heimsense-darwin-arm64 \
  -o /usr/local/bin/heimsense && chmod +x /usr/local/bin/heimsense

# Mac (Intel)
curl -L https://github.com/strowk/heimsense/releases/latest/download/heimsense-darwin-amd64 \
  -o /usr/local/bin/heimsense && chmod +x /usr/local/bin/heimsense

# Linux (amd64)
curl -L https://github.com/strowk/heimsense/releases/latest/download/heimsense-linux-amd64 \
  -o /usr/local/bin/heimsense && chmod +x /usr/local/bin/heimsense
```

**Windows:** Download `.exe` fra [releases-siden](https://github.com/strowk/heimsense/releases) og læg den i din PATH.

### Konfiguration

Opret konfigurationsfilen:

```bash
mkdir -p ~/.heimsense
```

```bash
cat > ~/.heimsense/.env << 'EOF'
# Copilot API endpoint — ingen /v1 suffix
ANTHROPIC_BASE_URL=https://api.githubcopilot.com

# Dit Copilot token (fra `gh auth token`)
ANTHROPIC_API_KEY=gho_xxxxxxxxxxxxxxxxxxxx

# Port Heimsense lytter på
LISTEN_ADDR=:18081

# Model-mapping — Copilot understøtter ikke alle Anthropic-navne
MODEL_MAP_HAIKU=claude-sonnet-4.5
MODEL_MAP_SONNET=claude-sonnet-4.6
MODEL_MAP_OPUS=claude-opus-4.6
EOF
```

Indsæt dit token (fra `gh auth token` i trin 2):

```bash
# Erstat token-værdien
COPILOT_TOKEN=$(gh auth token)
sed -i.bak "s/gho_xxxxxxxxxxxxxxxxxxxx/${COPILOT_TOKEN}/" ~/.heimsense/.env
```

### Start Heimsense

**Manuelt (test):**

```bash
heimsense run
# Listening on :18081
```

**Som permanent baggrundstjeneste med PM2 (anbefalet):**

```bash
npm install -g pm2

# HOME skal sættes eksplicit — PM2-processer arver ikke altid den korrekte HOME
HOME=$HOME pm2 start heimsense --name heimsense -- run
pm2 save
pm2 startup   # Følg instruktionerne for at aktivere autostart ved boot
```

### Konfigurer Claude Code til at bruge Heimsense

```bash
# Sæt environment-variablen permanent i din shell-profil
echo 'export ANTHROPIC_BASE_URL=http://localhost:18081' >> ~/.zshrc   # zsh
echo 'export ANTHROPIC_BASE_URL=http://localhost:18081' >> ~/.bashrc  # bash
source ~/.zshrc  # eller ~/.bashrc
```

Alternativt, sæt det kun for Claude Code via settings:

```bash
claude config set env.ANTHROPIC_BASE_URL http://localhost:18081
```

### Verificer

```bash
# Test at Heimsense kører
curl -s http://localhost:18081/v1/models | head -5

# Test at Claude Code bruger Heimsense
claude -p "reply with only the word OK"
# Svar: OK
```

---

## 5. Brug i dit projekt

Når opsætningen er klar, åbn Claude Code i dit projekt:

```bash
cd mit-projekt
claude
```

Claude bruger nu din Copilot-licens. Tjek hvilken model der bruges:

```bash
# Inde i claude-sessionen
/model
```

### Skift model

```bash
# Sonnet (standard, hurtig)
/model claude-sonnet-4.6

# Opus (kraftigere, bruger mere kvota)
/model claude-opus-4.6
```

---

## Kendte begrænsninger

| Begrænsning | Detalje |
|---|---|
| **~1500 premium requests/md** | Copilot Pro+ plan. Opus tæller ~10× mere end Sonnet |
| **Ingen Haiku** | `claude-haiku` returnerer 403 fra Copilot — Heimsense mapper automatisk til Sonnet |
| **Token udløber** | `gh auth token` udsteder et session-token. Kør `gh auth refresh` hvis Heimsense returnerer 401 |
| **Ikke alle features** | Visse Anthropic-specifikke features (prompt caching, extended thinking) virker muligvis ikke via Copilot |

---

## Fejlfinding

### `claude` kan ikke forbinde til Heimsense

```bash
# Tjek at Heimsense kører
pm2 status heimsense
# eller
curl -s http://localhost:18081/v1/models

# Genstart hvis nødvendigt
pm2 restart heimsense
```

### 401 Unauthorized fra Heimsense

```bash
# Token er udløbet — forny og opdater .env
gh auth refresh
NEW_TOKEN=$(gh auth token)
sed -i.bak "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=${NEW_TOKEN}/" ~/.heimsense/.env
pm2 restart heimsense
```

### 502 Bad Gateway

```bash
# Tjek at ANTHROPIC_BASE_URL i .env IKKE har /v1 suffix
grep ANTHROPIC_BASE_URL ~/.heimsense/.env
# Skal være: ANTHROPIC_BASE_URL=https://api.githubcopilot.com
# Ikke:      ANTHROPIC_BASE_URL=https://api.githubcopilot.com/v1
```

### Claude Code ignorerer Heimsense

```bash
# Verificer at env-variablen er sat i din aktuelle shell
echo $ANTHROPIC_BASE_URL
# Skal vise: http://localhost:18081

# Hvis tom — genindlæs din shell-profil
source ~/.zshrc
```

---

## Næste skridt

- **Skills og agents:** Se [`STARTER_KIT.md`](./STARTER_KIT.md) for at kopiére starter-kittet ind i dit projekt og aktivere AI-teamet
