The headline number of a role or project, big enough to find while scrolling, with one line saying what it measures.

The number uses `fs-30` at weight 800 in the tone colour (`*-text` tier for purple and blue). Pass `from` and `to` to add two thin bars that show a before and after (for example an app rating of 2.0 to 4.2): the earlier bar is neutral, the later bar takes the tone. Bars are decorative and hidden from screen readers, so the label must carry the meaning ("App-store rating, 2.0 to 4.2").

**You provide:** `value` (the final formatted figure, already in the markup), `label` (what it measures, with its scope), and optionally `from`, `to` (numbers on the same scale) and `context` (one short reference line).

- Do lead with three at most per role. Choose the figures a stranger would remember.
- Do count up from zero on scroll only as an enhancement: the final value is in the HTML at rest, the animation runs once, takes `dur-count`, and is skipped when `prefers-reduced-motion` is set.
- Do give every number a unit or a direction (+, −, $, %, ×).
- Bars are optional. Draw them only when there is an honest before and after on the same scale (a rating, a wait time, a count); a role without one shows the number alone.
- Don't repeat the figure in a bullet right beside it unless the bullet adds the story behind it.
