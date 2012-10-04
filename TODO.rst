TODO
====

- Add option to run script. (default: False)
- Add option to change script name.
- Add option to replace existing links. (default: False)
- Add option to send script output to log. If not doing this don't
  use PIPE in Popen since it blocks. (default: True)
- Catch system signals for safer clean-up.

MAYDO
=====

- Warn if link exists.
- Replace script file if it exists.
- Recursively delete empty directories created in LINK_DIR.
