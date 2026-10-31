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

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
