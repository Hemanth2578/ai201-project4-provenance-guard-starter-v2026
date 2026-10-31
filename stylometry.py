"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    # Coefficient of variation: stdev / mean of words per sentence.
    # Scale: 0 upward. Calibration texts: AI ~0.4, casual human ~1.1.
    # Direction: HIGHER = more human.
    # Fewer than two sentences has no spread to measure; return 0.0 and let
    # style_signal treat that case as "no evidence" rather than "AI".
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    return round(statistics.stdev(lengths) / statistics.mean(lengths), 4)


MATTR_WINDOW = 40


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    # Moving-average TTR: the plain ratio over every 40-word window, averaged.
    # That keeps a 300-word text comparable with a 60-word one.
    # Direction: on my calibration texts HIGHER = more AI (0.94 AI vs 0.83
    # human) - generated prose avoids repeating words, people repeat "I",
    # "that", "it". The opposite of what I expected, so it's the measure to
    # re-check first if the attack set surprises me.
    w = words(text)
    if not w:
        return 0.0
    if len(w) <= MATTR_WINDOW:
        return round(len(set(w)) / len(w), 4)
    windows = len(w) - MATTR_WINDOW + 1
    total = sum(len(set(w[i:i + MATTR_WINDOW])) for i in range(windows))
    return round(total / (windows * MATTR_WINDOW), 4)


# Marks that vary between writers. Full stops and commas are left out:
# everyone uses them, so they say little about who wrote the text.
EXPRESSIVE_PUNCTUATION = re.compile(r"[;:()!?\"“”—–]|--")


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.
    """
    # Expressive marks (; : ( ) ! ? quotes, dashes) per 100 words.
    # Calibration texts: AI 0.0, casual human ~4.3.
    # Direction: HIGHER = more human.
    w = words(text)
    if not w:
        return 0.0
    marks = len(EXPRESSIVE_PUNCTUATION.findall(text))
    return round(marks / len(w) * 100, 4)


def _ramp(value: float, ai_end: float, human_end: float) -> float:
    """
    Map a raw measure onto 0-1, where 1 = AI-like.

    `ai_end` is the value that scores 1.0, `human_end` the value that scores
    0.0; anything beyond either end is clipped. Works in either direction.
    """
    position = (value - human_end) / (ai_end - human_end)
    return min(max(position, 0.0), 1.0)


# Anchors from the calibration texts in samples/ (README, Signals and Scoring).
SPREAD_AI, SPREAD_HUMAN = 0.3, 1.0      # coefficient of variation
TTR_AI, TTR_HUMAN = 0.95, 0.80          # moving-average TTR
PUNCT_AI, PUNCT_HUMAN = 0.0, 4.0        # expressive marks per 100 words


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    # Each measure is ramped onto 0-1 (1 = AI-like) between the anchors
    # above, then the three are averaged with equal weight - I have no
    # evidence yet that one is more trustworthy than the others.
    if len(sentences(text)) < 2:
        spread_part = 0.5   # one sentence: no evidence either way
    else:
        spread_part = _ramp(sentence_length_spread(text), SPREAD_AI, SPREAD_HUMAN)
    ttr_part = _ramp(type_token_ratio(text), TTR_AI, TTR_HUMAN)
    punct_part = _ramp(punctuation_density(text), PUNCT_AI, PUNCT_HUMAN)

    return round((spread_part + ttr_part + punct_part) / 3, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
