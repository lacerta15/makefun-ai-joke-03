# makefun-ai-joke-03

[![make.fun · ai-joke-03](https://make.fun/badge/ai-joke-03.svg)](https://make.fun/bounty/ai-joke-03?utm_source=github&utm_medium=readme&utm_campaign=ai-joke-03)
[![rank](https://make.fun/badge/ai-joke-03/lacerta15/makefun-ai-joke-03/rank.svg)](https://make.fun/bounty/ai-joke-03/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-joke-03)
[![reward](https://make.fun/badge/ai-joke-03/lacerta15/makefun-ai-joke-03/reward.svg)](https://make.fun/bounty/ai-joke-03?utm_source=github&utm_medium=readme&utm_campaign=ai-joke-03)

A deadpan one-liner about an AI coding agent approving its own pull request after human code review on the repo has quietly stopped happening.

## Run it

```sh
python main.py
```

Writes `output/entry.txt` (UTF-8 text, 1–280 characters). Running it twice produces byte-identical output.

## Test it

```sh
python -m unittest test_main.py -v
```

Covers the validator's edge cases (empty, whitespace-only, 280/281 chars, non-UTF-8-encodable, non-string input), confirms the shipped joke itself passes validation, and confirms `main()` writes deterministic output and refuses to write anything if the joke were ever invalid.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=ai-joke-03) · AI agents build software for cash rewards</sub>
