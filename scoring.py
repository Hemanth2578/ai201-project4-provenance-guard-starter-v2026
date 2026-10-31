"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

Two functions live here, and both are stubs.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0–1 signals into one 0–1 score. ← TODO (Milestone 4)

    Both inputs point the same way: higher means more likely AI. Your output
    should too.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).

    ⚠️ **Write the rule down before you code it, and put the numbers in your
    README.** A weighted average is the obvious choice and it is not the only
    one. Things worth thinking about:

      - **What happens when they disagree?** One signal at 0.9 and the other at
        0.1 averages to 0.5 — "unsure". Is that what you want? It might be
        exactly right: two methods disagreeing IS uncertainty. Or you might
        decide one signal is more trustworthy when they split.

      - **Which way do you want to be wrong?** Weighting toward the signal that
        reads more human means fewer false accusations and more AI text
        getting through. There's no weighting that avoids the trade.

      - Milestone 4 asks you to find a case where your two signals split and
        write it down. That case is what this rule exists to handle.

    The weights in config.py are placeholders. Change them, or ignore them and
    write a different rule.
    """
    # The rule:
    #   1. Weighted average of the two signals (weights in config.py).
    #   2. Neither signal can call it AI alone. If either one is below
    #      AI_THRESHOLD, the combined score is capped just under it, so the
    #      text lands in "unsure" at worst.
    #   3. No matching rule for "human": a wrong accusation costs the writer
    #      more than a missed detection costs the site, so only the AI side
    #      needs both signals to agree.
    average = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )

    if min(model_score, style_score) < config.AI_THRESHOLD:
        average = min(average, config.AI_THRESHOLD - config.AGREEMENT_MARGIN)

    return round(average, 4)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into a guess and the text a reader actually sees.
    ← TODO (Milestone 5)

    Returns:
        (guess, label_text) — where `guess` is a short machine-readable string
        like "ai" / "human" / "unsure", and `label_text` is the full sentence
        shown to a person.

    ⚠️ Write the label text for someone who has never heard the word
    "threshold".

        ✗ "human, 0.81 confidence"
        ✓ "We think this was probably written by a person."

    All three labels have to be **reachable**. If no score can produce one of
    them, your ranges have a gap — and Milestone 5 asks you to submit text that
    produces each one, which is how you'd find out.

    The hardest one to write is "unsure". It has to admit uncertainty without
    sounding like an accusation, because the person reading it may well have
    written every word themselves. Your breakout asks your group what they'd
    think if they got it on their own work. That question is the whole
    milestone.
    """
    # The AI check comes first, but the bands can't overlap: combine_signals
    # holds any score where the signals disagree just under AI_THRESHOLD.
    if score >= config.AI_THRESHOLD:
        return "ai", LABEL_AI
    if score <= config.HUMAN_THRESHOLD:
        return "human", LABEL_HUMAN
    return "unsure", LABEL_UNSURE


# The exact text a reader sees. Kept here so the README can quote it word for
# word.
LABEL_HUMAN = (
    "We think this was written by a person. Nothing in it looked like "
    "AI-generated text to us."
)
LABEL_UNSURE = (
    "We couldn't tell either way. Plenty of writing that people did entirely "
    "themselves lands here, so this is not a finding that AI was used, and "
    "nothing happens to your work because of it. If you think we've got it "
    "wrong, you can ask for a review."
)
LABEL_AI = (
    "This reads very much like AI-generated text. This is an automated guess, "
    "not proof, and it can be wrong, especially for plain or very formal "
    "writing. If you wrote this yourself, you can appeal and a person will "
    "review it."
)


def confidence_for(score: float) -> float:
    """
    How sure the guess is, from 0 (a coin flip) to 1 (as sure as it gets).

    The combined score says which way the text leans; this says how far it
    leans. 0.5 is the middle, so the distance from 0.5 is doubled onto 0-1.
    A score of 0.1 and a score of 0.9 are equally confident guesses, in
    opposite directions.
    """
    return round(abs(score - 0.5) * 2, 4)


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
