#!/usr/bin/env bash
# Importér Claude Code Starter Kit ind i et eksisterende repo.
# Brug: bash scripts/import-to-repo.sh /sti/til/dit-repo
set -euo pipefail

# ─── Farver ────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
ok()   { echo -e "${GREEN}  ✓${NC} $*"; }
warn() { echo -e "${YELLOW}  ⚠${NC} $*"; }
info() { echo -e "${BLUE}  →${NC} $*"; }
err()  { echo -e "${RED}  ✗${NC} $*"; }

# ─── Argumenter ────────────────────────────────────────────────────────────
TARGET="${1:-}"
if [ -z "${TARGET}" ]; then
  err "Angiv sti til dit repo: bash scripts/import-to-repo.sh /sti/til/dit-repo"
  exit 1
fi

TARGET="$(cd "${TARGET}" && pwd)"
KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ─── Validering ────────────────────────────────────────────────────────────
if [ ! -d "${TARGET}/.git" ]; then
  err "${TARGET} er ikke et git-repository (ingen .git-mappe)"
  exit 1
fi

if [ "${TARGET}" = "${KIT_DIR}" ]; then
  err "Target må ikke være starter-kit-repo'et selv"
  exit 1
fi

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Claude Code Starter Kit — Import til repo      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"
echo ""
info "Kilde:  ${KIT_DIR}"
info "Mål:    ${TARGET}"
echo ""

# ─── Konfliktdetektering ───────────────────────────────────────────────────
CONFLICTS=()

[ -f "${TARGET}/CLAUDE.md" ]                     && CONFLICTS+=("CLAUDE.md (tages backup)")
[ -d "${TARGET}/.devcontainer" ]                 && CONFLICTS+=(".devcontainer/ (tages backup)")
[ -f "${TARGET}/scripts/devcontainer-setup.sh" ] && CONFLICTS+=("scripts/devcontainer-setup.sh (tages backup)")
[ -f "${TARGET}/scripts/devcontainer-start.sh" ] && CONFLICTS+=("scripts/devcontainer-start.sh (tages backup)")
[ -f "${TARGET}/scripts/heimsense-start.sh" ]    && CONFLICTS+=("scripts/heimsense-start.sh (tages backup)")
[ -f "${TARGET}/scripts/heimsense-uninstall.sh" ] && CONFLICTS+=("scripts/heimsense-uninstall.sh (tages backup)")
[ -f "${TARGET}/scripts/heimsense-status.sh" ]   && CONFLICTS+=("scripts/heimsense-status.sh (tages backup)")
[ -f "${TARGET}/scripts/import-to-repo.sh" ]     && CONFLICTS+=("scripts/import-to-repo.sh (tages backup)")

if [ ${#CONFLICTS[@]} -gt 0 ]; then
  warn "Følgende filer/mapper eksisterer allerede og vil blive backed up (.bak):"
  for c in "${CONFLICTS[@]}"; do
    echo "     - ${c}"
  done
  echo ""
fi

# ─── Bekræftelse ───────────────────────────────────────────────────────────
echo "Følgende vil blive kopieret til ${TARGET}:"
echo "  • .claude/ (agents, skills, rules)"
echo "  • .devcontainer/ (Dockerfile, devcontainer.json)"
echo "  • scripts/ (heimsense-* og devcontainer-*)"
echo "  • docs/ (template-dokumentation — springer over hvis fil har indhold)"
echo "  • .github/ (dependabot.yml, shellcheck workflow — overskrives altid)"
echo "  • CLAUDE.md (projektskabelon)"
echo "  • .gitignore (tilføjer manglende linjer)"
echo ""
read -r -p "Fortsæt? [j/N] " CONFIRM
if [[ ! "${CONFIRM}" =~ ^[jJ]$ ]]; then
  echo "Afbrudt."
  exit 0
fi
echo ""

# ─── Hjælpefunktion: backup ────────────────────────────────────────────────
backup() {
  local file="$1"
  if [ -e "${file}" ]; then
    cp -r "${file}" "${file}.bak"
    warn "Backup: ${file} → ${file}.bak"
  fi
}

# ─── Kopiér .claude/ ───────────────────────────────────────────────────────
mkdir -p "${TARGET}/.claude"
cp -r "${KIT_DIR}/.claude/agents"  "${TARGET}/.claude/"
cp -r "${KIT_DIR}/.claude/skills"  "${TARGET}/.claude/"
cp -r "${KIT_DIR}/.claude/rules"   "${TARGET}/.claude/"
ok ".claude/agents, skills, rules kopieret"

# settings.json: kopiér kun hvis mål ikke har en
if [ ! -f "${TARGET}/.claude/settings.json" ]; then
  cp "${KIT_DIR}/.claude/settings.json" "${TARGET}/.claude/"
  ok ".claude/settings.json kopieret"
else
  warn ".claude/settings.json eksisterer allerede — springer over (tilpas manuelt)"
fi

# ─── Kopiér .devcontainer/ ─────────────────────────────────────────────────
backup "${TARGET}/.devcontainer"
cp -r "${KIT_DIR}/.devcontainer" "${TARGET}/"
ok ".devcontainer/ kopieret"

# ─── Kopiér scripts/ ───────────────────────────────────────────────────────
mkdir -p "${TARGET}/scripts"
SCRIPT_FILES=(
  devcontainer-setup.sh
  devcontainer-start.sh
  heimsense-start.sh
  heimsense-uninstall.sh
  heimsense-status.sh
  import-to-repo.sh
)
for f in "${SCRIPT_FILES[@]}"; do
  backup "${TARGET}/scripts/${f}"
  cp "${KIT_DIR}/scripts/${f}" "${TARGET}/scripts/${f}"
done
ok "scripts/ kopieret"

# ─── Kopiér docs/ (spring over filer med reelt indhold) ───────────────────
mkdir -p "${TARGET}/docs"
for src in "${KIT_DIR}/docs"/*.md; do
  fname="$(basename "${src}")"
  dest="${TARGET}/docs/${fname}"
  if [ -f "${dest}" ]; then
    # Tjek om målfilen er mere end 5 linjer (har reelt indhold)
    lines=$(wc -l < "${dest}")
    if [ "${lines}" -gt 5 ]; then
      warn "docs/${fname} har allerede indhold (${lines} linjer) — springer over"
      continue
    fi
  fi
  cp "${src}" "${dest}"
  ok "docs/${fname} kopieret"
done

# ─── Kopiér .github/ ───────────────────────────────────────────────────────
mkdir -p "${TARGET}/.github/workflows"
[ -f "${KIT_DIR}/.github/dependabot.yml" ] && \
  cp "${KIT_DIR}/.github/dependabot.yml" "${TARGET}/.github/" && \
  ok ".github/dependabot.yml kopieret"
[ -f "${KIT_DIR}/.github/workflows/shellcheck.yml" ] && \
  cp "${KIT_DIR}/.github/workflows/shellcheck.yml" "${TARGET}/.github/workflows/" && \
  ok ".github/workflows/shellcheck.yml kopieret"

# ─── Kopiér CLAUDE.md ──────────────────────────────────────────────────────
backup "${TARGET}/CLAUDE.md"
cp "${KIT_DIR}/CLAUDE.md" "${TARGET}/CLAUDE.md"
ok "CLAUDE.md kopieret"

# ─── Merge .gitignore ──────────────────────────────────────────────────────
if [ -f "${KIT_DIR}/.gitignore" ]; then
  touch "${TARGET}/.gitignore"
  ADDED=0
  while IFS= read -r line; do
    # Spring tomme linjer og kommentarer over ved søgning
    if [[ -z "${line}" || "${line}" == \#* ]]; then
      continue
    fi
    if ! grep -qF "${line}" "${TARGET}/.gitignore" 2>/dev/null; then
      echo "${line}" >> "${TARGET}/.gitignore"
      ADDED=$((ADDED + 1))
    fi
  done < "${KIT_DIR}/.gitignore"
  ok ".gitignore: ${ADDED} nye linjer tilføjet"
fi

# ─── Kopiér starter-kit docs til reference ─────────────────────────────────
mkdir -p "${TARGET}/starter-kit"
cp -r "${KIT_DIR}/starter-kit/"* "${TARGET}/starter-kit/"
ok "starter-kit/ (setup-guides) kopieret"

# ─── Næste skridt ──────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Import fuldført!                               ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo "Næste skridt:"
echo ""
echo "  1. Udfyld CLAUDE.md i dit repo:"
echo "     cd ${TARGET}"
echo "     # Ret projektnavn, tech stack og key commands"
echo ""
echo "  2. Commit starter-kit-filerne:"
echo "     git add . && git commit -m \"feat: tilføj Claude Code starter-kit\""
echo ""
echo "  3. Åbn devcontainer i VSCode og vent på postCreateCommand"
echo "     (eller: bash scripts/devcontainer-start.sh for at starte heimsense manuelt)"
echo ""
echo "  4. Start Claude Code og kør /onboarding:"
echo "     claude"
echo "     > /onboarding"
echo ""
