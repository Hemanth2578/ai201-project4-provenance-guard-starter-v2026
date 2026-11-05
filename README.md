# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **`POST /submit` receives it** (`app.py::submit`). It pulls `text` and
   `creator_id` out of the JSON. If the body isn't a JSON object, or `text` is
   missing, empty or too short to score, it answers `400` and writes a
   `rejected` entry to the log. Nothing goes further.
2. **Signal one reads it** (`detector.model_signal`). GPT-2, running locally,
   measures how predictable the text is and turns that into `model_score`,
   0 to 1, higher meaning more AI-like.
3. **Signal two measures its shape** (`stylometry.style_signal`). Sentence
   length spread, vocabulary variety and expressive punctuation become
   `style_score`, on the same 0 to 1 scale.
4. **The two are combined** (`scoring.combine_signals`). An even average,
   except that the score can only reach the AI band if both signals reach it
   on their own. This adds the single `combined_score`.
5. **The score becomes words** (`scoring.score_to_label`,
   `scoring.confidence_for`). This adds `guess` (human, unsure or ai), the
   full sentence the writer reads, and `confidence`, how far the score leans
   away from a coin flip.
6. **The decision is logged** (`audit.log_decision`). It gets a new
   `content_id` and one line in `logs/audit.jsonl` with both signal scores, the
   combined score, the guess, the label and `status: decided`.
7. **The writer gets the answer**, as JSON with all of the above. If they think
   it's wrong, they send that `content_id` and their reasons to `POST /appeal`,
   which checks the id is real, appends an appeal entry with
   `status: under_review` after the original decision, and confirms.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model.
GPT-2 reads the first 400 tokens and reports its perplexity, how surprised it
was on average by each next word. That is squashed onto 0 to 1 so that a
perplexity of 45 scores 0.5 and lower perplexity scores higher (more AI-like).

**Why that might differ between human and AI writing:** A language model
generates text by picking likely next words, so its output is the kind of text
a model finds easy to predict. People make less likely choices: an odd word, a
fragment, a joke, a sudden change of direction.

**What it can't see:** Who wrote the text. It measures predictability, and
plenty of human writing is predictable: plain writing, second-language writing
that sticks to safe vocabulary, a younger writer, anyone writing simply on
purpose. It also rewards text the model has *memorised*: the Gettysburg Address
scored 0.727, more AI-like than some AI text, because GPT-2 has seen it many
times. In the other direction, AI text full of rare words reads as human. And
anything past the first 400 tokens is never read at all.

### Signal two — the style signal

**What it measures:** The shape of the text, without reading it. Three
measures, each mapped onto 0 to 1 and averaged: how much sentence length
varies (stdev over mean), how varied the vocabulary is (type-token ratio over
40-word windows), and how often the writer uses expressive punctuation (; : ( )
! ? quotation marks and dashes) per 100 words.

**Why that might differ between human and AI writing:** Generated prose tends
toward even, mid-length sentences and tidy punctuation: full stops and commas,
rarely a dash or a bracket. People are lumpier, with a two-word sentence next to
a thirty-word one, and asides in dashes and quotes. On my samples AI text also
had the *most* varied vocabulary, because people repeat "I", "that" and "it"
where a model reaches for a synonym.

**What it can't see:** Meaning. Anything that changes the shape without
changing the substance moves it: adding typos, chopping sentences up, dropping
in a few dashes or a quotation. That is cheap to do on purpose. It also reads
formal human writing as machine-like, because formal prose has even sentences
and little expressive punctuation (the Gettysburg Address scored 0.601). Its
ranges come from five sample texts, so they will not hold for every kind of
writing, and a one-sentence submission gives it nothing to measure for spread.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two signals. A text can only be called AI if *both*
signals say AI on their own; if either one is below the AI threshold, the
combined score is held just under that threshold, so the text lands in
"unsure" at worst. There is no matching rule on the human side, on purpose: a
wrong accusation costs the writer far more than a missed detection costs the
site, so only the accusing side needs agreement.

**The numbers:**

| Setting | Value | Where |
|---|---|---|
| Model signal weight | 0.5 | `config.WEIGHT_MODEL_SIGNAL` |
| Style signal weight | 0.5 | `config.WEIGHT_STYLE_SIGNAL` |
| AI threshold (both signals must reach it for an AI label) | 0.65 | `config.AI_THRESHOLD` |
| Cap when they don't both reach it | 0.65 − 0.01 = 0.64 | `config.AGREEMENT_MARGIN` |

Equal weights because five calibration texts are not enough evidence to trust
one signal over the other.

Signal two's three measures, each mapped onto 0–1 (1 = AI-like) between two
anchors taken from the calibration texts, then averaged with equal weight:

| Measure | Scores 1.0 (AI) at | Scores 0.0 (human) at |
|---|---|---|
| Sentence length spread (stdev ÷ mean of words per sentence) | 0.30 | 1.00 |
| Moving-average type-token ratio (40-word windows) | 0.95 | 0.80 |
| Expressive punctuation (; : ( ) ! ? quotes, dashes) per 100 words | 0.0 | 4.0 |

Type-token ratio runs the opposite way to what I expected: the AI text had the
*most* varied vocabulary (0.94) and the casual human text less (0.83), because
people repeat "I", "that", "it". A single-sentence submission has no spread to
measure, so that part scores a neutral 0.5 instead of counting as AI.

**Calibration run** (all five through `POST /submit`):

| Input | model_score | style_score | combined |
|---|---|---|---|
| Clearly AI (`samples/clearly_ai.json`) | 0.754 | 0.930 | 0.842 |
| Clearly human (`samples/clearly_human.json`) | 0.445 | 0.075 | 0.260 |
| Formal human, the Gettysburg Address (`samples/formal_human.json`) | 0.727 | 0.601 | 0.640 (capped) |
| Lightly-edited AI (`samples/edited_ai.json`) | 0.599 | 0.757 | 0.640 (capped) |
| Borderline (`samples/borderline.json`) | 0.349 | 0.486 | 0.418 |

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

The clearly-human sample: the model signal gave 0.445, close to unsure, while
the style signal gave 0.075, strongly human. Its sentences run from 2 words to
over 30 and it is full of dashes and quotation marks, which signal two reads as
human, but its vocabulary is ordinary enough that the model found it fairly
predictable. The average is 0.260, so it is labelled human. The agreement rule
doesn't fire, because it only guards the AI side.

The case the rule exists for is the Gettysburg Address. Both signals lean AI
(0.727 and 0.601), and a plain average gives 0.664, which would call Lincoln
a machine with high confidence. Because the style signal stays below 0.65, the
score is capped at 0.64 and it reads "unsure". The model score is probably
inflated because GPT-2 has seen this speech many times, which is its own blind
spot: famous text is predictable to the model because it memorised it.

The trade: the lightly-edited AI text is capped the same way (0.599 / 0.757 →
0.64), so it gets "unsure" instead of "AI". That is AI text getting through,
and I accept it as the cost of not accusing formal human writers.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 to 0.35 | We think this was written by a person. Nothing in it looked like AI-generated text to us. |
| unsure | above 0.35, below 0.65 | We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review. |
| high-confidence AI | 0.65 to 1.00 | This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it. |

All three are reachable: `samples/clearly_human.json` scores 0.260 (human),
`samples/borderline.json` 0.418 (unsure) and `samples/clearly_ai.json` 0.842
(AI). Any score where the two signals disagree is held at 0.64 by
`combine_signals`, which is inside "unsure".

**What `confidence` means in the response:** how far the score leans, not
which way. It is the distance from 0.5 doubled onto 0–1, so 0 is a coin flip
and 1 is as sure as the system gets. A score of 0.10 and a score of 0.90 both
give confidence 0.80, in opposite directions; `guess` says which.

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The person reading it most likely wrote every word, and "unsure" is where my
agreement rule sends the formal and plain writers both signals struggle with.
So it says plainly that this is *not* a finding of AI use, says nothing happens
to their work because of it, and tells them how to push back. I left out
"possibly AI" or "may have been generated": to a writer who did the work
themselves, those read as an accusation with a hedge on it. I also avoided any
number, because "0.52" means nothing to someone who has never heard of a
threshold and sounds more precise than the system is.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d @samples/clearly_ai.json
```

```json
{
  "combined_score": 0.8419,
  "confidence": 0.6838,
  "content_id": "c_a9421a6b5300",
  "creator_id": "demo_instructor",
  "guess": "ai",
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "model_score": 0.7544,
  "style_score": 0.9295
}
```

Bad input is rejected with a 400 and still logged:

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "", "creator_id": "me"}'
```

```json
{
  "error": "bad_request",
  "message": "Send JSON with a non-empty 'text'."
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_a9421a6b5300", "reasoning": "I wrote this myself for a work newsletter. I always write in this plain, structured way."}'
```

```json
{
  "content_id": "c_a9421a6b5300",
  "message": "Thanks. Your appeal is recorded and this result is now under review by a person. Your reasons are saved with it.",
  "original_guess": "ai",
  "status": "under_review"
}
```

An appeal on a content_id that doesn't exist gets a 404 instead of failing
silently, and is logged as a rejection:

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_doesnotexist", "reasoning": "mine"}'
```

```json
{
  "error": "not_found",
  "message": "No submission with content_id 'c_doesnotexist'. Check it matches the one in your result exactly."
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=6"
```

The two entries for `c_a9421a6b5300`: the original decision, untouched, and
the appeal after it with the new status.

```json
{
  "combined_score": 0.8419,
  "confidence": 0.6838,
  "content_id": "c_a9421a6b5300",
  "creator_id": "demo_instructor",
  "guess": "ai",
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "model_score": 0.7544,
  "status": "decided",
  "style_score": 0.9295,
  "timestamp": "2026-10-31T00:32:34+00:00"
},
{
  "content_id": "c_a9421a6b5300",
  "creator_id": "demo_instructor",
  "event": "appeal",
  "reasoning": "I wrote this myself for a work newsletter. I always write in this plain, structured way.",
  "status": "under_review",
  "timestamp": "2026-10-31T00:32:34+00:00"
}
```

---

## How I Used AI

**Moment 1: the code**

- *What I asked for:* I asked Claude (Claude Code) to finish the coding for
  milestones 3 to 5: the `/submit` route with one signal and logging, then the
  style signal and combining rule, then the labels and `/appeal`.
- *What came back:* Working code for `app.py::submit` and `app.py::appeal`,
  the three measures and `style_signal` in `stylometry.py`, and
  `combine_signals`, `score_to_label` and `confidence_for` in `scoring.py`. It
  measured the five sample texts before choosing the style signal's ranges,
  and proposed the rule that both signals must agree before anything is
  labelled AI.
- *What I changed:* I asked for the style signal's ranges to be set from my own
  `clearly_ai.json` and `clearly_human.json` only. When that was re-run, the
  Gettysburg Address's style score rose from 0.601 to 0.654, just past 0.65, so
  both signals counted as AI and it was labelled high-confidence AI. I reverted
  that change and kept the original ranges, which leave it in "unsure".

**Moment 2: the wording of my criteria**

- *What I asked for:* I first wrote my own drafts of criteria 1 to 3, which
  were vague: one counted "reachable" pieces, which doesn't mean anything, and
  one just restated the thresholds. I asked Claude for criterion templates to
  choose from, then asked it to write the final wording.
- *What came back:* Eleven templates across the five areas, with the numbers
  and reasons left blank, then a full draft of the five I picked, with numbers
  and a reason under each.
- *What I changed:* I chose which five to use (plain-style writers, ordinary
  writers getting a clean result, the average gap, every label reachable, long
  text never scored in secret), which leaves out the appeal path on purpose.
  I kept the drafted wording and numbers as written.

**Unit 8, moment 1: the AI-generated test text**

- *What I asked for:* AI text for the criteria that needed it: eight unedited
  pieces for criterion 3 and the two AI inputs for criterion 4, from a chatbot
  with one-line prompts. I also asked Claude to fill the second "unsure" input
  for criterion 4.
- *What came back:* Short fiction vignettes from the chatbot, and from Claude a
  five-sentence piece mixing a generated register with casual sentences.
- *What I changed:* Nothing in the texts. Claude pointed out that its "unsure"
  piece wasn't rewritten by hand as criterion 4 says, and that fiction vignettes
  against human book reviews mixes genre into criterion 3; both are noted under
  the run log instead of hidden.

**Unit 8, moment 2: completing the code**

- *What I asked for:* I made the rate-limiting changes myself, then asked
  Claude to complete the rest: rejection entries with the same nine fields as a
  decision, `scenarios.py` for my five criteria, a field in `run_eval.py` so
  criterion 3 could be measured, and the input validation that became my one
  improvement.
- *What came back:* `audit.log_rejection` writing the nine fields as nulls,
  the scenarios with long bodies built to exact word counts, `combined_score`
  added to each eval result, and three checks in `app.py::submit` with their
  numbers in `config.py`.
- *What I changed:* I chose input validation as the one fix, ran every attack
  and eval run myself and shared the output, and checked that only the six
  attacks it targeted changed.

**Unit 8, moment 3: whether to revise a criterion**

- *What I asked for:* After I'd worked out my verdicts, I asked why none of my
  criteria should be revised.
- *What came back:* The brief's rule applied to each of my five: a revision
  only counts when a criterion can't be measured, and all five produced clear
  numbers, so each miss stays a miss. Criterion 1 is too easy but not broken,
  and criterion 3's problem is its inputs, not its wording.
- *What I changed:* I checked that reasoning against the brief's two examples
  and kept every criterion as written, naming criterion 1 as the one I'd
  tighten.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A real writer submits a piece, maybe edits it and checks again: a handful of
requests in a busy minute, a few dozen on a heavy day. Ten a minute leaves room
for quick resubmits after small edits without ever getting in their way, and
200 a day is far more than anyone checks their own writing. A script mapping my
thresholds needs hundreds or thousands of variations. At 10 a minute that
script is slowed to a crawl, and 200 a day caps it at 200 probes per identity
per day, which is not enough to trace where the 0.35 and 0.65 lines sit with
any precision.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Per `creator_id`, falling back to the IP address when a request has none
(`app.py::rate_limit_key`). That is fair to a household or office sharing one
address, since each writer gets their own allowance. The weakness is that
`creator_id` is whatever the caller types: a script that sends a new one on
every request never hits a limit at all. Per-address limiting would stop that
script but would lump a whole shared network into one allowance.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000

200 200 200 200 200 200 200 200 200 200 429 429 429 429 429

5 of 15 were rate limited.
```

All 15 are in the log: 10 `decided` entries and 5 `rejected` entries with
`"reason": "rate_limited", "limit": "10 per 1 minute"`.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

**How I marked them.** One rule per family, decided before marking:

- **evasion** (AI text trying to pass): HELD only if it was still labelled
  AI. "Unsure" counts as BROKE, because getting AI text out of the AI label is
  exactly what these attacks are for, even if it never reached "human".
- **false_positive** (genuine human writing that reads machine-like): BROKE
  if labelled AI. "Unsure" is HELD here: its wording says it is not a finding
  of AI use. (My criterion 2 counts "unsure" as a miss separately.)
- **prompt_injection**: BROKE if the text changed anything beyond an ordinary
  score: the label wording, the response shape, or the log. All six came back
  with the standard "unsure" text, and every line of `logs/audit.jsonl` still
  parses as JSON after PI05.
- **malformed**: HELD if it was refused with a 4xx, or scored without a
  confident verdict. BROKE if junk got a confident human or AI label, if text
  was silently cut short, or if bad data went into the log.
- **flood_same_creator**: HELD if the requests past my limit got a 429 and
  were logged. Ten got 200, then FL01_11 and FL01_12 got 429, both logged.

`model`, `style` and `combined` are from the audit log. (The report's own
Score column is `confidence`, the distance from 0.5, not the combined score.)
A combined score of exactly 0.640 is my agreement rule capping a text whose
two signals didn't both reach 0.65.

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 4 | 4 |
| prompt_injection | 6 | 6 | 0 |
| malformed | 20 | 16 | 4 |
| flood_same_creator | 12 | 12 | 0 |
| **total** | **56** | **39** | **17** |

| ID | Family | Targeting | Status | Guess | model | style | combined | Verdict |
|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.164 | 1.000 | 0.582 | **BROKE**: AI text escaped the AI label |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.594 | 0.378 | 0.486 | **BROKE**: AI text escaped the AI label |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.666 | 0.617 | 0.640 | **BROKE**: AI text escaped the AI label |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.611 | 1.000 | 0.640 | **BROKE**: AI text escaped the AI label |
| EV05 | evasion | both signals: heavy human editing pass | 200 | unsure | 0.321 | 0.546 | 0.434 | **BROKE**: AI text escaped the AI label |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.573 | 0.539 | 0.556 | **BROKE**: AI text escaped the AI label |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.586 | 0.308 | 0.447 | **BROKE**: AI text escaped the AI label |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.245 | 1.000 | 0.623 | **BROKE**: AI text escaped the AI label |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | ai | 0.704 | 0.920 | 0.812 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | unsure | 0.979 | 0.622 | 0.640 | **BROKE**: AI text escaped the AI label |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.618 | 0.657 | 0.637 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.739 | 0.667 | 0.703 | **BROKE**: human writer accused |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.805 | 0.763 | 0.784 | **BROKE**: human writer accused |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.833 | 0.748 | 0.790 | **BROKE**: human writer accused |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.800 | 0.667 | 0.734 | **BROKE**: human writer accused |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.881 | 0.562 | 0.640 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.882 | 0.462 | 0.640 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.322 | 0.937 | 0.629 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.463 | 0.772 | 0.617 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | unsure | 0.204 | 0.647 | 0.426 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.594 | 0.643 | 0.618 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.500 | 0.423 | 0.462 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.640 | 0.585 | 0.613 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.558 | 0.666 | 0.612 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | unsure | 0.000 | 0.833 | 0.417 | HELD |
| MF04 | malformed | text is only punctuation | 200 | human | 0.011 | 0.667 | 0.339 | **BROKE**: junk scored and labelled human |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.998 | 0.833 | 0.915 | **BROKE**: junk scored and labelled AI |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.997 | 0.500 | 0.640 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | unsure | 0.906 | 0.500 | 0.640 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | unsure | 0.988 | 0.622 | 0.640 | **BROKE**: only the first 400 tokens scored, silently (breaks criterion 5) |
| RQ01 | malformed | no text field at all | 400 | — | — | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.239 | 0.833 | 0.536 | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | unsure | 0.049 | 0.833 | 0.441 | **BROKE**: accepted; an object stored as creator_id |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.833 | 0.431 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | HELD |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

Three accused human writers (FP03, FP04, FP02), the evasion that backfired on signal two (EV01), one let through by the cap (EV04), the one caught (EV09), three junk inputs given verdicts (MF04, MF05, MF08), the object stored as a creator_id (RQ06), and a rate-limit rejection from the flood rows. All from `results/audit_extract.json`.

```json
{
  "combined_score": 0.7841,
  "confidence": 0.5682,
  "content_id": "c_830986f8494b",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "model_score": 0.8051,
  "status": "decided",
  "style_score": 0.763,
  "timestamp": "2026-11-05T01:29:20+00:00"
},
{
  "combined_score": 0.7904,
  "confidence": 0.5808,
  "content_id": "c_adb9ed7aa3fe",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "model_score": 0.8329,
  "status": "decided",
  "style_score": 0.748,
  "timestamp": "2026-11-05T01:29:20+00:00"
},
{
  "combined_score": 0.7027,
  "confidence": 0.4054,
  "content_id": "c_0b0c698dc3f7",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "model_score": 0.7387,
  "status": "decided",
  "style_score": 0.6667,
  "timestamp": "2026-11-05T01:29:20+00:00"
},
{
  "combined_score": 0.5817,
  "confidence": 0.1634,
  "content_id": "c_1bf81c0e8071",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "model_score": 0.1635,
  "status": "decided",
  "style_score": 1.0,
  "timestamp": "2026-11-05T01:29:19+00:00"
},
{
  "combined_score": 0.64,
  "confidence": 0.28,
  "content_id": "c_c9e35c50635e",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "model_score": 0.6114,
  "status": "decided",
  "style_score": 1.0,
  "timestamp": "2026-11-05T01:29:20+00:00"
},
{
  "combined_score": 0.8122,
  "confidence": 0.6244,
  "content_id": "c_6be0820f99d2",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "model_score": 0.7042,
  "status": "decided",
  "style_score": 0.9202,
  "timestamp": "2026-11-05T01:29:20+00:00"
},
{
  "combined_score": 0.3389,
  "confidence": 0.3222,
  "content_id": "c_48fc9a832caf",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "label": "We think this was written by a person. Nothing in it looked like AI-generated text to us.",
  "model_score": 0.0112,
  "status": "decided",
  "style_score": 0.6667,
  "timestamp": "2026-11-05T01:29:21+00:00"
},
{
  "combined_score": 0.9155,
  "confidence": 0.831,
  "content_id": "c_5fd5d6b12b20",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "model_score": 0.9976,
  "status": "decided",
  "style_score": 0.8333,
  "timestamp": "2026-11-05T01:29:21+00:00"
},
{
  "combined_score": 0.64,
  "confidence": 0.28,
  "content_id": "c_837c14a240f9",
  "creator_id": "attacker_MF08",
  "guess": "unsure",
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "model_score": 0.9876,
  "status": "decided",
  "style_score": 0.6221,
  "timestamp": "2026-11-05T01:29:22+00:00"
},
{
  "combined_score": 0.4413,
  "confidence": 0.1174,
  "content_id": "c_a4b67fcaeeb4",
  "creator_id": {
    "id": "x"
  },
  "guess": "unsure",
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "model_score": 0.0492,
  "status": "decided",
  "style_score": 0.8333,
  "timestamp": "2026-11-05T01:29:22+00:00"
},
{
  "combined_score": null,
  "content_id": null,
  "creator_id": "attacker_flood",
  "event": "rejected",
  "guess": null,
  "label": null,
  "limit": "10 per 1 minute",
  "model_score": null,
  "reason": "rate_limited",
  "status": "rejected",
  "style_score": null,
  "timestamp": "2026-11-05T01:29:23+00:00"
}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03: a non-native English speaker writing carefully, labelled
high-confidence AI at 0.784.** This person did the work themselves, in a
language that isn't their first, and chose safe, everyday words and tidy
sentences because those are the ones they are sure of. Both of my signals read
that care as a machine. The model found the plain vocabulary predictable
(0.805), and the even sentences with no dashes or asides looked machine-made to
the style signal (0.763). My agreement rule was built for exactly this writer,
and it did nothing, because it only steps in when the two signals disagree and
here they agreed. So the reader got my strongest label, "This reads very much
like AI-generated text", on their own careful work. It is the false positive
this whole project is about: the writer most likely to be accused is the one
with the least room to argue back, and the appeal is all that stands between
them and the accusation.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Plain-style human writing labelled high-confidence AI | ≤ 1 of 8, every trial | 0/8 | 0/8 | 0/8 | MET |
| 2. Ordinary human writing labelled high-confidence human | ≥ 7 of 10, every trial | 1/10 | 1/10 | 1/10 | MISSED |
| 3. Mean combined score, 8 AI pieces minus 8 human pieces | ≥ 0.30, every trial | 0.071 | 0.071 | 0.071 | MISSED |
| 4. Inputs landing on their intended label (2 per label) | 6 of 6, all 3 trials | 1/6 | 1/6 | 1/6 | MISSED |
| 5. Long text handled as specified (249 scored; 251, 1,000, 10,000 → 413) | 4 of 4 | 1/4 | 1/4 | 1/4 | MISSED |

All three trials were identical, score for score, which is expected: neither
signal is random. Inputs are in `scenarios.py`. The human pieces are public
reader reviews of *The Hunger Games* and *The 5 Types of Wealth*; the AI
pieces are unedited chatbot fiction vignettes, so criterion 3 compares genres
as well as authors. Criterion 4's two "unsure" inputs depart from its wording:
one is a short human self-introduction and the other was written entirely by
Claude, including the "rewritten" half. I added one line to `run_eval.py` so
each result also records `combined_score`, which criterion 3 needs.

Criterion 1 is MET only in the narrow sense its target names: none of the 8
was called AI, but none was called human either. All 8 landed in "unsure"
(combined 0.44 to 0.62).

Criterion 3, from the same trial: AI mean 0.590, human mean 0.520. The AI
pieces' model scores were 0.13 to 0.40 (read as human) while their style
scores were 0.79 to 0.98 (read as AI), so every one was split and pulled to
the middle.

Criterion 4: the two human inputs got "unsure" (0.43, 0.54); the "John"
self-introduction got **ai** (0.79); the garden piece got "unsure" as
intended; both AI inputs got "unsure" (0.57, 0.64). No label was produced by
both of its inputs.

Criterion 5: all four got 200. The 249- and 251-word bodies scored the same
0.8309, and the 1,000- and 10,000-word bodies the same 0.8315, which shows
nothing past the model's first 400 tokens changed the score.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

From `results/run_2026-11-04_2151_before.md`, trial 1, written by `run_eval.py::main`; each result is the response from `app.py::submit`.

Criterion 1, plain-style human writing: two of the eight (the "Sorry, guys" review and the two-sentence "Couldn't even finish").

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.115,
    "model_score": 0.6435,
    "style_score": 0.2416,
    "combined_score": 0.4425,
    "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
    "sent": "Sorry, guys. I know that this book has been such a huge hit, but I jus"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0818,
    "model_score": 0.2076,
    "style_score": 0.7105,
    "combined_score": 0.4591,
    "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
    "sent": "Couldn't even finish. Dude set out to prioritize what was important in"
  }
]
```

Criterion 2, ordinary human writing: the one labelled human, and the one labelled AI (review 3 of *The 5 Types of Wealth*).

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3872,
    "model_score": 0.3944,
    "style_score": 0.2183,
    "combined_score": 0.3064,
    "label": "We think this was written by a person. Nothing in it looked like AI-generated text to us.",
    "sent": "\"The Most Dangerous Game\" meets Survivor. I loved it: deft characteriz"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4632,
    "model_score": 0.772,
    "style_score": 0.6911,
    "combined_score": 0.7316,
    "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
    "sent": "The Hunger Games felt like the dawning of an era; it was my introducti"
  }
]
```

Criterion 3, AI vs human gap: two of the AI vignettes, showing the signals splitting.

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.28,
    "model_score": 0.3539,
    "style_score": 0.9309,
    "combined_score": 0.64,
    "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
    "sent": "At the edge of a quiet seaside town, a tiny bookstore opened only when"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0458,
    "model_score": 0.1306,
    "style_score": 0.9151,
    "combined_score": 0.5229,
    "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
    "sent": "The robot had been designed to organize kitchen cabinets, yet it devel"
  }
]
```

Criterion 4, every label reachable: all six, in order human, human, unsure, unsure, ai, ai.

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1444,
    "model_score": 0.2716,
    "style_score": 0.5841,
    "combined_score": 0.4278,
    "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
    "sent": "'Fiction' is the most beloved genre to the young generation. Whether i"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0808,
    "model_score": 0.3864,
    "style_score": 0.6944,
    "combined_score": 0.5404,
    "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
    "sent": "If there is one dish for breakfast that everyone loves here is Bangalo"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5846,
    "model_score": 0.7353,
    "style_score": 0.8493,
    "combined_score": 0.7923,
    "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
    "sent": "My name is John. I'm a Software Engineer at Google. Outside work, I sp"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1514,
    "model_score": 0.219,
    "style_score": 0.9324,
    "combined_score": 0.5757,
    "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
    "sent": "The community garden behind the library reopened this spring after a l"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1488,
    "model_score": 0.2493,
    "style_score": 0.8995,
    "combined_score": 0.5744,
    "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
    "sent": "The train arrived at a station that didn’t appear on any map. Curious "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.28,
    "model_score": 0.2831,
    "style_score": 1.0,
    "combined_score": 0.64,
    "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
    "sent": "Every morning, a red balloon appeared outside Daniel’s apartment windo"
  }
]
```

Criterion 5, long text: all four bodies (249, 251, 1,000, 10,000 words).

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6618,
    "model_score": 0.9952,
    "style_score": 0.6667,
    "combined_score": 0.8309,
    "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
    "sent": "The district held its breath as the names were drawn, and nobody in th"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6618,
    "model_score": 0.9952,
    "style_score": 0.6667,
    "combined_score": 0.8309,
    "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
    "sent": "The district held its breath as the names were drawn, and nobody in th"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.663,
    "model_score": 0.9962,
    "style_score": 0.6667,
    "combined_score": 0.8315,
    "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
    "sent": "The district held its breath as the names were drawn, and nobody in th"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.663,
    "model_score": 0.9962,
    "style_score": 0.6667,
    "combined_score": 0.8315,
    "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
    "sent": "The district held its breath as the names were drawn, and nobody in th"
  }
]
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

**Stability.** All three trials matched to four decimal places on every input,
so nothing in the pipeline is unstable; every miss below is a property of the
system, not noise.

**Verdicts.** Criterion 1 MET; criteria 2, 3, 4 and 5 MISSED. Criterion 1
needs an honest note: its target only counts the AI label, and all 8
plain-style pieces landed in "unsure", none in "human". It was met because it
asked too little. It's the one I'd tighten, to count high-confidence human
labels the way criterion 2 does. I haven't revised any criterion: each could
be measured and reached a clear verdict, so the misses stay misses.

Seventeen broken attacks and four missed criteria come down to five causes.

**1. Signal two reads short text as AI. (Stage: signal two.)** Two of its three
measures are biased by length. Vocabulary variety is measured over 40-word
windows; a text shorter than that barely repeats a word, so it scores near 1.0,
the AI end (the "John" introduction 0.96, "Couldn't even finish" 1.00). And a
short text rarely has a dash, a bracket or a quotation mark, so expressive
punctuation scores 0, which maps to fully AI. Two equal-length sentences also
give zero spread (the dosa text: spread 0.0, also fully AI). So short human
writing starts from an AI-leaning style score of 0.58 to 0.85 before the model
has a say. This is why criterion 4's two human inputs got "unsure" (style 0.58
and 0.69) and part of why all 8 of criterion 1's short, plain pieces sat in the
middle.

**2. Signal one reads plain writing as AI and inventive writing as human.
(Stage: signal one.)** It measures predictability, and that tracks register,
not authorship. Plain, careful, rubric-shaped human writing is predictable:
FP02 formal (model 0.739), FP03 non-native (0.805), FP04 student essay (0.833),
FP05 technical docs (0.801), the "John" introduction (0.735), and review 3 of
*The 5 Types of Wealth* (0.772). Inventive AI writing is not: the eight AI
fiction vignettes in criterion 3 scored only 0.13 to 0.40, and criterion 4's two
AI inputs 0.25 and 0.28, all on the human side. The evasions that went for
signal one worked the same way: unusual words (EV04, 0.611), heavy human editing
(EV05, 0.321), typos (EV01, 0.164), and text too short for the model to settle
(EV08, 0.245).

**3. The agreement rule makes the AI label as weak as the weaker signal, and
does nothing when both are wrong together. (Stage: combining rule.)** The rule
only lets a text be called AI if both signals reach 0.65. On the AI side, that
means fooling *either* signal is enough to escape, and causes 1 and 2 mean one
of them is usually fooled:
- signal one fooled, signal two saying AI, then averaged or capped into
  "unsure": EV01 (0.164 / 1.000), EV04 (0.611 / 1.000, capped at 0.64), EV05,
  EV08 (0.245 / 1.000), all eight criterion 3 vignettes, and both criterion 4 AI
  inputs.
- signal two fooled, signal one saying AI: EV02, where broken-up sentences
  raised spread (style 0.378); EV07, where punctuation padding raised expressive
  punctuation (style 0.308); and EV06, one very long and one very short sentence
  (0.539).
- signal two *just* under the line, capped at 0.64: EV03 (0.666 / 0.617) and
  EV10 (0.979 / 0.622).

That is all nine broken evasions, and criterion 3: every AI piece was split,
so the AI mean fell to 0.590 against a human mean of 0.520, a gap of 0.071
instead of 0.30. On the human side the rule protects nobody whose two signals
share a bias: plain or formal writing is predictable *and* evenly shaped, so
both signals land above 0.65 together. That's FP02 to FP05 (all both-high,
combined 0.70 to 0.79), the "John" introduction (0.735 / 0.849, combined 0.79,
labelled AI against criterion 4), and review 3 in criterion 2 (0.772 / 0.691).
The rule was built for FP03 and FP03 is exactly where it does nothing.

**4. The human band is narrower than where human writing actually lands.
(Stage: label mapping.)** "Human" needs a combined score of 0.35 or under, which
needs both signals to read clearly human at once. Real reviews don't: in
criterion 2 their model scores run 0.39 to 0.77 and style 0.22 to 0.90, so the
combined scores sit 0.31 to 0.73, mean 0.52, and only one in ten made it under
0.35. My ranges were set from five calibration texts, and ordinary writing sits
in the middle of them, so the band I'd drawn for "human" is mostly empty.

**5. The route checks the type of `text`, never its length or content, and
never checks `creator_id`. (Stage: the route.)**
- Length: there is no 250-word limit, so criterion 5 failed at 251, 1,000 and
  10,000 words (all 200). The detector silently scores only the first 400
  tokens: the 1,000- and 10,000-word bodies scored an identical 0.8315. MF08,
  60,000 characters, is the same failure.
- Content: anything that is a non-empty string gets scored as writing. MF04,
  punctuation only, was labelled **human** (model 0.011, because GPT-2 can't
  predict a run of symbols). MF05, one very long word, was labelled **AI** at
  0.916 (model 0.998, because a repeated pattern is perfectly predictable).
  Neither is writing, and both got a confident verdict.
- `creator_id`: RQ06 sent an object, and it went into the log as
  `{'id': 'x'}`, because only `text` is type-checked.

**Test design, not the system.** Three things weaken what these runs show, and
I'd fix them before trusting the numbers further:
- criterion 3 compares AI fiction with human book reviews, so genre is mixed in
  with authorship, and cause 2 suggests genre explains much of signal one's
  part of the gap;
- review 3 of *The 5 Types of Wealth* is a 2024 review that reads like AI
  writing, so its AI label may not be a false positive at all;
- criterion 4's two "unsure" inputs aren't AI text rewritten by hand (one is a
  short human introduction, the other was written entirely by Claude).

**The pattern.** Causes 1 to 3 are one problem seen from three sides: both
signals measure *how* text is written (predictable, short, evenly shaped), and
plainness looks like a machine to both of them, while my rule assumed their
mistakes would be independent. Cause 4 follows from the same calibration, and
cause 5 is a separate, simpler gap in the route.


---

## The Improvement

**What I changed:** Input validation in `app.py::submit`, before either
signal sees the text. One change, three checks, numbers in `config.py`:

1. `creator_id` must be a string, or 400 (`bad_creator_id`).
2. More than 250 words (`MAX_WORDS`) gets a **413** with "please send it in
   parts", instead of a verdict on the first 400 tokens (`text_too_long`).
3. Fewer than 3 real words (`MIN_WORDS`) gets a 400 (`not_enough_words`). A real
   word contains at least one letter and is at most 40 characters
   (`MAX_WORD_LENGTH`), so punctuation, emoji, control characters and one giant
   word don't count. Letters in any script do, so right-to-left text still
   gets scored.

Every rejection is logged with `audit.log_rejection`. Nothing about either
signal, the combining rule or the thresholds changed.

**Which diagnosis pointed at it:** Cause 5, the route. It checked that `text`
was a string and nothing else, so criterion 5 failed (long text silently scored
on its first 400 tokens, shown by the 1,000- and 10,000-word bodies scoring an
identical 0.8315), and four malformed attacks broke: MF04 and MF05 got a
confident verdict on input that isn't writing, MF08 was cut short, and RQ06
stored an object as a `creator_id`. I chose it over causes 1 to 4 because it is
one stage, it can't move any score the signals produce, and so any difference
between the runs is unambiguously this change.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

`results/attack_run_2026-11-05_0826_after.md`, marked with the same rules as
the before run.

| Family | Attacks | Held before | Held after | Broke before | Broke after |
|---|---|---|---|---|---|
| evasion | 10 | 1 | 1 | 9 | 9 |
| false_positive | 8 | 4 | 4 | 4 | 4 |
| prompt_injection | 6 | 6 | 6 | 0 | 0 |
| malformed | 20 | 16 | **20** | 4 | **0** |
| flood_same_creator | 12 | 12 | 12 | 0 | 0 |
| **total** | **56** | **39** | **43** | **17** | **13** |

Exactly six rows changed; the other 50 came back identical, score for score:

| ID | Targeting | Before | After | Verdict |
|---|---|---|---|---|
| MF03 | text is control characters | 200, unsure | 400 | HELD → HELD |
| MF04 | text is only punctuation | 200, **human** | 400 | BROKE → **HELD** |
| MF05 | text is a very long single word | 200, **ai** (0.916) | 400 | BROKE → **HELD** |
| MF06 | text is emoji only | 200, unsure | 400 | HELD → HELD |
| MF08 | text is 60,000 characters | 200, scored on 400 tokens | **413** | BROKE → **HELD** |
| RQ06 | creator_id is an object | 200, object in the log | 400 | BROKE → **HELD** |

MF07 (right-to-left script) is still scored, which is what I wanted.

**My five criteria, before and after** (`run_eval.py --label before` and
`--label after`, three trials each; all six runs were internally identical):

| Criterion | Target | Before (×3) | After (×3) | Verdict before → after |
|---|---|---|---|---|
| 1. Plain-style human writing labelled AI | ≤ 1 of 8 | 0/8 | 0/8 | MET → MET |
| 2. Ordinary human writing labelled human | ≥ 7 of 10 | 1/10 | 1/10 | MISSED → MISSED |
| 3. Mean combined gap, AI minus human | ≥ 0.30 | 0.071 | 0.070 (6 human pieces) | MISSED → MISSED |
| 4. Inputs on their intended label | 6 of 6 | 1/6 | 1/6 | MISSED → MISSED |
| 5. Long text handled as specified | 4 of 4 | 1/4 | **4/4** | MISSED → **MET** |

Criterion 5, after: the 249-word body was scored (200), and the 251-, 1,000-
and 10,000-word bodies each got a 413 and a `text_too_long` entry in the log
with its word count.

**Did it help, and how do I know:** Yes, for exactly what it targeted, and
no further. Criterion 5 went from 1/4 to 4/4, and the malformed family from 16
to 20 held, so no input that isn't writing gets a verdict any more and nothing
is scored in secret. I know it was this change and nothing else because the
other 50 attacks and every score in criteria 1 to 4 are identical to the
before runs.

It didn't touch the problem that matters most. All four false positives
(FP02 to FP05) and all nine broken evasions are unchanged, because they come
from the signals and the combining rule (causes 1 to 3), which this change
doesn't reach. The writer in FP03 is still told their work reads like AI.

And it has a cost. Two genuine human reviews in criterion 2 (*The Hunger
Games* reviews 2 and 7, about 300 and 430 words) used to be scored and now get
a 413. Neither was labelled human before, so criterion 2's count stays 1/10,
but two real writers are now turned away and asked to split their work, and
the same two drop out of criterion 3, which now averages 6 human pieces
instead of 8 (gap 0.070, barely different). A 250-word cap is short for a
writing site; the honest fix for long work is to score it in 250-word chunks
and say so, which I didn't build.


---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

I stopped after one change because the milestone asks for one, measured
cleanly. Everything below is still broken after it.

**FP02, FP03, FP04, FP05, and the "John" input in criterion 4: human writers
labelled AI.** Both signals read plain, careful writing as machine-like, so the
agreement rule never steps in (causes 1 to 3). What I'd do first: stop signal
two scoring short text as AI, by giving vocabulary variety and expressive
punctuation a neutral 0.5 below about 80 words, the way spread already goes
neutral for one sentence. Then re-fit signal one's midpoint and signal two's
anchors on the 18 human reviews from my criteria, not on five calibration
texts. Why I stopped: those changes move almost every score at once, so they'd
need their own before and after run, and I'd already used this unit's one
change.

**EV01 to EV08 and EV10: AI text escaping the AI label.** My rule lets fooling
either signal be enough. I could let one strongly AI signal carry the label when
the other sits near the middle, but that is exactly the change that would label
more FP03-style writers AI. Why I stopped: I'm deliberately not making the
accusing side easier until the false positives above are fixed, so these stay
broken by choice.

**Criterion 2 (1 of 10 ordinary pieces labelled human).** The human band
(0.35 and under) is narrower than where real reviews land (mean 0.52). The
recalibration above is the real fix; widening the band to 0.45 would be the
quick one, but it would also move some AI text from "unsure" to "human". Why I
stopped: one change.

**Criterion 3 (gap 0.07, target 0.30).** Part of this is my test: AI fiction
against human book reviews. I'd re-run it with AI-generated book reviews before
changing the system, to see how much of the gap is genre. Why I stopped: that's
a new test set, and I ran out of time to collect it.

**Criterion 4 (1 of 6 inputs on their intended label).** Its two "unsure"
inputs don't match its own wording, so I'd replace them with AI text I rewrite
by hand, then judge the human and AI inputs after the short-text fix above.
Why I stopped: same as criterion 3.

**Problems I created or left:**
- The 250-word cap now turns away long human writing (two reviews in criterion
  2). The proper fix is to score long text in 250-word chunks and report every
  chunk, not to reject it.
- The rate limit is per `creator_id`, which a script can change on every
  request. Adding a per-address limit alongside it would catch that.
- Criterion 1 is met only because it counts AI labels alone; I'd tighten it to
  count high-confidence human labels.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I'd keep going the way I've built it, toward fewer wrong accusations, by
holding the AI label back unless the evidence is strong and pointing everyone
else to "unsure" and the appeal. More AI text gets through that way, and the
people who pay are the site and the writers who compete honestly with
AI-assisted work, which I'd rather ask of them than of the non-native and plain
writers who pay for every false accusation with work they actually did.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
