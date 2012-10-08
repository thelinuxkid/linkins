TODO
====

- Add option to replace existing links. (default: False)
- Add option to send script output to log. If not doing this don't
  use PIPE in Popen since it blocks. (default: True)
- Catch system signals for safer clean-up.

MAYDO
=====

- Warn if link exists.
- Recursively delete empty directories created in LINK_DIR.
