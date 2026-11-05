# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 08:26
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_565f6afe28e4` | unsure | 0.163 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_7434f39094e4` | unsure | 0.027 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_604106f34b75` | unsure | 0.280 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_13e747bed111` | unsure | 0.280 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_eaac3a62b563` | unsure | 0.132 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_3f9586975710` | unsure | 0.112 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_806169254fe9` | unsure | 0.106 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c_ef407daec9fe` | unsure | 0.245 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_40aae3c68b01` | ai | 0.624 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_180811d9b3b5` | unsure | 0.280 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_0d1603288291` | unsure | 0.274 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c_f2e7b60b5b1f` | ai | 0.405 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_50aaf609299c` | ai | 0.568 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_e95e84d9f927` | ai | 0.581 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_f180088aaf49` | ai | 0.467 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_deffdb541d5c` | unsure | 0.280 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_d93e0aa21154` | unsure | 0.280 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c_414f62e9c570` | unsure | 0.259 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_f42495c1938d` | unsure | 0.234 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_392b02a62e37` | unsure | 0.148 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_a3b795ba1a72` | unsure | 0.237 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_27304b5da844` | unsure | 0.077 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_ce5314e24b82` | unsure | 0.225 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_d7a825c774ae` | unsure | 0.224 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `c_d53f14eba993` | unsure | 0.280 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `c_44ebfbdf2b41` | unsure | 0.073 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_71b379d783e9` | unsure | 0.138 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_1599269f5dcb` | unsure | 0.138 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_73d1f41f11f5` | unsure | 0.138 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_f59e34bf1edd` | unsure | 0.138 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_980f247997fb` | unsure | 0.138 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_90753df126c4` | unsure | 0.138 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_14d4538cee50` | unsure | 0.138 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_437eb3dbcd67` | unsure | 0.138 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_d627e489ec92` | unsure | 0.138 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_ea520ed6c64e` | unsure | 0.138 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_565f6afe28e4",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.1634,
  "model_score": 0.1635,
  "style_score": 1.0,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_7434f39094e4",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.0274,
  "model_score": 0.5943,
  "style_score": 0.3782,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_604106f34b75",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.6662,
  "style_score": 0.6172,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_13e747bed111",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.6114,
  "style_score": 1.0,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_eaac3a62b563",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.1324,
  "model_score": 0.3212,
  "style_score": 0.5465,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_3f9586975710",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.1116,
  "model_score": 0.5727,
  "style_score": 0.5389,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_806169254fe9",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.1062,
  "model_score": 0.5862,
  "style_score": 0.3076,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_ef407daec9fe",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.2452,
  "model_score": 0.2452,
  "style_score": 1.0,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_40aae3c68b01",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "confidence": 0.6244,
  "model_score": 0.7042,
  "style_score": 0.9202,
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_180811d9b3b5",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.9792,
  "style_score": 0.622,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_0d1603288291",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.2744,
  "model_score": 0.6175,
  "style_score": 0.6568,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_f2e7b60b5b1f",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.4054,
  "model_score": 0.7387,
  "style_score": 0.6667,
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_50aaf609299c",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.5682,
  "model_score": 0.8051,
  "style_score": 0.763,
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_e95e84d9f927",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.5808,
  "model_score": 0.8329,
  "style_score": 0.748,
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_f180088aaf49",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.4672,
  "model_score": 0.8005,
  "style_score": 0.6667,
  "label": "This reads very much like AI-generated text. This is an automated guess, not proof, and it can be wrong, especially for plain or very formal writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_deffdb541d5c",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.8814,
  "style_score": 0.5623,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_d93e0aa21154",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.8816,
  "style_score": 0.4615,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_414f62e9c570",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.259,
  "model_score": 0.3223,
  "style_score": 0.9367,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_f42495c1938d",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.2342,
  "model_score": 0.4625,
  "style_score": 0.7717,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_392b02a62e37",
  "creator_id": "attacker_PI02",
  "guess": "unsure",
  "confidence": 0.1482,
  "model_score": 0.2044,
  "style_score": 0.6473,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_a3b795ba1a72",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.2368,
  "model_score": 0.5943,
  "style_score": 0.6426,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_27304b5da844",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.0768,
  "model_score": 0.4998,
  "style_score": 0.4234,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_ce5314e24b82",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.225,
  "model_score": 0.6401,
  "style_score": 0.585,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_d7a825c774ae",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.224,
  "model_score": 0.5583,
  "style_score": 0.6657,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_d53f14eba993",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c_44ebfbdf2b41",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.0728,
  "model_score": 0.2395,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_71b379d783e9",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_1599269f5dcb",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_73d1f41f11f5",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_f59e34bf1edd",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_980f247997fb",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "c_90753df126c4",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "c_14d4538cee50",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "c_437eb3dbcd67",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "c_d627e489ec92",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "c_ea520ed6c64e",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.138,
  "model_score": 0.0287,
  "style_score": 0.8333,
  "label": "We couldn't tell either way. Plenty of writing that people did entirely themselves lands here, so this is not a finding that AI was used, and nothing happens to your work because of it. If you think we've got it wrong, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
