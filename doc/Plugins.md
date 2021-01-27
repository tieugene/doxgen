# Plugins

Making your own plugins.

## Requirements

## Examples

### Minimal

### Midi

### Multiline

## Notes:

- generate new UUID:
  ```bash
  python3 -c "import uuid; print(uuid.uuid4().hex.upper())"
  ```
  or (unix-utils):
  ```
  v=`uuidgen -x`; echo ${v^^} | sed 's/-//g'
  uuidgen -x | sed 's/-//g' | tr a-z A-Z
  ```
