---
name: bash-tui
description: Best practices for flicker-free bash TUI rendering. Use when building or debugging terminal UI scripts.
---

# Bash TUI — Flimmerfri Terminal UI

Best practices for bash-baserede TUI'er (terminal user interfaces). Lært fra pipeline-tui.sh.

## Anti-flimmer teknikker

### 1. Double-buffering (KRITISK)

Render ALDRIG direkte til terminalen. Buffer al output og flush i ét styk:

```bash
# ❌ FORKERT — hvert printf flusher separat → synlig flimmer
render_frame() {
  printf "\033[H"
  draw_header
  draw_grid
  draw_footer
}

# ✅ KORREKT — samlet output i ét cat-kald
{
  render_frame
} > /tmp/.tui-frame-$$ 2>/dev/null
cat /tmp/.tui-frame-$$
```

Husk cleanup i trap:
```bash
trap 'rm -f /tmp/.tui-frame-$$; tput cnorm; stty sane; tput rmcup' EXIT INT TERM
```

### 2. Cursor home, IKKE clear

```bash
# ❌ FORKERT — clear → hele skærmen blinker hvidt
clear
draw_everything

# ✅ KORREKT — cursor home, overskriv eksisterende indhold
printf "\033[H"
draw_everything
```

### 3. Bulk clear i stedet for linje-for-linje

```bash
# ❌ FORKERT — N separate escape sequences
for (( r=row; r<ROWS; r++ )); do
  printf "\033[%d;1H\033[K" "$r"
done

# ✅ KORREKT — én escape: clear fra cursor til bund
printf "\033[%d;1H\033[J" "$row"
```

### 4. Alternativ screen buffer

```bash
tput smcup   # Enter alternativ buffer (gemmer brugerens terminal)
tput civis   # Skjul cursor
# ... TUI kører ...
tput cnorm   # Vis cursor
tput rmcup   # Forlad alternativ buffer (gendanner terminal)
```

## Refresh rate

| Interval | FPS | Brug |
|----------|-----|------|
| 0.5s | 2 | For hurtigt — unødvendig CPU/I/O |
| **1s** | 1 | **Sweet spot for de fleste TUI'er** |
| 2s | 0.5 | For langsomt — spinner ser frossen ud |

```bash
# Input-loop med 1s timeout
if read -n1 -t1 key 2>/dev/null; then
  handle_key "$key"
fi
```

### Adaptive refresh

Opdatér kun dele der faktisk ændres:

```bash
# Log-sektion: kun re-render hvis filen er ændret
_log_mtime=$(stat -c %Y "$log_file" 2>/dev/null || echo 0)
if [[ "$_log_mtime" != "${_LAST_LOG_MTIME:-}" ]]; then
  _LAST_LOG_MTIME="$_log_mtime"
  render_log_section
fi
```

### Cache eksterne kald

```bash
# ❌ FORKERT — jq kald per issue per frame = 50+ subprocesser
for issue in "${ISSUES[@]}"; do
  state=$(jq -r ".\"$nr\".status" "$STATE_FILE")
done

# ✅ KORREKT — cache hele state-filen én gang per frame
cache_state() {
  _STATE_CACHE=$(cat "$STATE_FILE" 2>/dev/null)
}
get_state() {
  echo "$_STATE_CACHE" | jq -r ".\"$1\".status // \"pending\""
}
```

## Escape sequences reference

| Escape | Effekt |
|--------|--------|
| `\033[H` | Cursor home (0,0) |
| `\033[%d;%dH` | Cursor til row;col |
| `\033[K` | Clear til end of line |
| `\033[J` | Clear til end of screen |
| `\033[2J` | Clear hele skærmen (undgå!) |
| `\033[?25l` | Skjul cursor |
| `\033[?25h` | Vis cursor |

## Keyboard input

```bash
# Non-blocking input med timeout
stty -echo -icanon time 0 min 0
if read -n1 -t1 key 2>/dev/null; then
  case "$key" in
    q) break ;;
    $'\033')  # Escape sequence (piltaster)
      read -n1 -t0.1 _esc1 2>/dev/null || true
      read -n1 -t0.1 _esc2 2>/dev/null || true
      case "$_esc1$_esc2" in
        "[A") handle_up ;;
        "[B") handle_down ;;
      esac
      ;;
  esac
fi
```

## Terminal resize

```bash
update_term_size() {
  ROWS=$(tput lines)
  COLS=$(tput cols)
}
trap 'update_term_size; clear' WINCH
```

## Typisk TUI-struktur

```bash
#!/usr/bin/env bash

# Setup
tput smcup; tput civis; stty -echo -icanon
trap 'rm -f /tmp/.tui-frame-$$; tput cnorm; stty sane; tput rmcup' EXIT INT TERM

ROWS=$(tput lines); COLS=$(tput cols)
trap 'ROWS=$(tput lines); COLS=$(tput cols)' WINCH

# Main loop
while true; do
  # Render til buffer → flush
  { printf "\033[H"; render_frame; } > /tmp/.tui-frame-$$
  cat /tmp/.tui-frame-$$

  # Input (1s timeout)
  if read -n1 -t1 key 2>/dev/null; then
    case "$key" in
      q) break ;;
      *) handle_key "$key" ;;
    esac
  fi
done
```

## Gotchas

| Problem | Årsag | Fix |
|---------|-------|-----|
| Skærm blinker | Direkte printf uden buffering | Double-buffer via tmpfile + cat |
| Flimmer ved log-sektion | Re-render uændret log hvert frame | mtime-cache, skip hvis uændret |
| Spinner fryser | Refresh interval for langt | 1s er sweet spot |
| CPU spikes | Subprocesser (jq/sed) hvert frame | Cache state, reducer kald |
| Cursor synlig under render | Manglende `tput civis` | Skjul ved start, vis ved exit |
| Terminal ødelagt ved crash | Manglende cleanup trap | ALTID trap EXIT med `stty sane; tput rmcup` |
| `clear` blinker | `clear` = slet + redraw | Brug `\033[H` (cursor home) i stedet |

---

*Oprettet: 2026-03-13*
*Lært fra: pipeline-tui.sh flimmer-debugging*
