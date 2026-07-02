# Coding Patterns

## General

- Follow existing patterns before introducing new ones
- Keep functions small and focused
- Name things clearly — avoid abbreviations

## Error Handling

```typescript
// Handle errors explicitly
try {
  await riskyOperation();
} catch (error) {
  console.error('Operation failed:', error);
  // Handle or rethrow
}
```

## File Operations

```bash
# Always use absolute paths
Edit /path/to/file.ts

# Check before destructive operations
if [ -d "$DIR" ] && [ "$DIR" != "/" ]; then
  rm -rf "$DIR"
fi
```

## Bash

```bash
# Use strict mode in scripts
set -euo pipefail

# local is only valid inside functions
my_function() {
  local var="value"  # OK
}
var="value"  # In main script, no local
```
