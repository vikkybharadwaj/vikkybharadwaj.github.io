A dark inset block for terminal commands, or a blue-bordered block for a prompt the reader should paste.

Default is `code-bg` with a `border` hairline and `radius-md`, text in `code-text`; scrolls horizontally rather than wrapping. `prompt` switches to the blue prompt style with a "PROMPT" label above the text, wrapping lines.

**You provide:** the text as a string child (preserve newlines). For syntax colour, wrap spans with class `c` (comment, `text-3`) or `k` (keyword, `green`).

- Do keep commands copy-pasteable; no prompt characters.
- Don't set long prose in a code block.

Hand-written from `playbook/index.html` (`.code`, `.prompt`).
