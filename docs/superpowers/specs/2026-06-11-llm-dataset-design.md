# LLM Synthetic Dataset Design
Date: 2026-06-11

## Overview

Generate a synthetic training dataset for a from-scratch LLM. The dataset uses a fixed vocabulary of exactly 100 tokens, no punctuation, and a `string.split()`-based tokenizer. All files go in a `datasets/` folder.

## Vocabulary (100 tokens)

The vocabulary is exact — every token listed below is a distinct training token. Texts may only use these exact forms (case-insensitive). No punctuation anywhere in any file.

| Category | Tokens |
|---|---|
| Articles (3) | `the` `a` `an` |
| Personal pronouns (11) | `I` `you` `he` `she` `it` `we` `they` `me` `him` `her` `us` |
| Possessive pronouns (5) | `my` `your` `his` `our` `their` |
| Demonstratives (2) | `this` `that` |
| Conjunctions (5) | `and` `or` `but` `so` `if` |
| Connectors/adverbs (5) | `not` `then` `now` `here` `there` |
| Prepositions (9) | `in` `on` `at` `to` `from` `with` `by` `of` `for` |
| Question words (5) | `what` `who` `where` `why` `how` |
| Auxiliaries (10) | `is` `are` `was` `were` `be` `have` `has` `had` `can` `will` |
| Present-tense verbs (10) | `go` `come` `see` `get` `make` `say` `know` `think` `want` `need` |
| More verbs (9) | `like` `love` `find` `give` `take` `work` `ask` `help` `put` |
| Past-tense forms (6) | `went` `came` `got` `made` `said` `knew` |
| Nouns (12) | `man` `woman` `child` `day` `time` `world` `house` `water` `food` `life` `way` `thing` |
| Adjectives (7) | `good` `big` `old` `new` `long` `right` `small` |
| Special token (1) | `<EOL>` |

**Total: 100 tokens.**

The `<EOL>` token is written literally as the string `<EOL>` inside the text files. Since the tokenizer uses `string.split()`, newline characters are treated as whitespace and are not tokens — `<EOL>` is the only sentence-boundary signal.

## Validator Script (`validate_dataset.py`)

- Stores the 100-token vocabulary as a Python `set`: the 99 regular words as lowercase strings, plus the literal string `<EOL>`
- Walks every `.txt` file inside `datasets/`
- For each file: calls `.split()` on the full text; for each token, if it equals `<EOL>` check it as-is, otherwise lowercase it and check membership in the vocabulary set
- Outputs: file name, number of violations, list of offending tokens
- Exits with code `1` if any file contains violations, `0` if all files are clean

## Dataset Files (50 total)

All files go in `datasets/`. Naming: `001.txt` through `050.txt`. Each file targets ~2000 tokens (words + `<EOL>` tokens combined).

### Content Type Distribution

| Type | Files | File numbers | Notes |
|---|---|---|---|
| Stories | 14 | 001–014 | Short narratives, past tense, character-driven |
| Q&A | 10 | 015–024 | Question line then answer line, `<EOL>` as separator |
| Dialogue | 10 | 025–034 | Back-and-forth between man / woman / child |
| Descriptive | 6 | 035–040 | Describing a person, place, or thing at length |
| Instructional | 6 | 041–046 | How to do something, step-by-step |
| Pattern/repetitive | 4 | 047–050 | Deliberate repetition to teach sentence structure |

## Agent Dispatch Strategy

1. Validator script and `datasets/` folder are created first in the main session
2. All 50 agents are dispatched in a single parallel batch — one agent per file
3. Each agent receives: the full vocabulary list, its assigned file number, content type, and the ~2000-token target
4. After all agents complete, the validator runs once over all 50 files
5. Any violations are reported; affected files can be re-generated

## Constraints for Agents

- Use only the exact tokens from the vocabulary (case-insensitive)
- No punctuation of any kind
- Write `<EOL>` literally at natural sentence boundaries
- Target approximately 2000 tokens per file (count words + `<EOL>` tokens)
- No two consecutive files should have the same sentence structure patterns
