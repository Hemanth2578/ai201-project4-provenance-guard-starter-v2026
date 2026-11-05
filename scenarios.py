"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# ── Human-written pieces ─────────────────────────────────────────────────────
# Public reader reviews of The Hunger Games, written by people (not by me and
# not by AI). Split by style: plain, simple writing goes to criterion 1; the
# rest is ordinary writing for criterion 2. No piece is in both sets.

PLAIN_HUMAN = [
    # review 1: short sentences, simple opinions
    "Sorry, guys. I know that this book has been such a huge hit, but I just didn't think it was that impressive. The plot wasn't that suspenseful; the whole idea of Capitol and Panem just was too 1984 for me. And the ending with all the dead tributes coming back as mutts? Just made the entire novel worse. Will not be reading the rest of this series. Sad. I thought it would have been better! Just not my cup of tea.",
    # review 4: short, simple exclamations
    "This book was amazing! From the moment you started reading it, you were sitting on the edge of your seat, heart pounding, and not wanting to put the book down! I felt so connected to the characters and felt involved with their lives. I laughed, cried, and gasped my way to the end!",
    # review 5: spelling and grammar slips, likely a second-language or young writer
    "This is disturbing and entrancing all at the same time. Collins charater development was amazing. Within the first few chapter I felt like I had know the charater forever. I love the writing I was hook from the first chapter. I can't wait for the second book.",
    # The rest are reader reviews of The 5 Types of Wealth.
    # review 1: simple sentences, typos ("recieved", "couldnt", "every is")
    "The subtitle nails this one...transformative! Given the current economic situation, every is re-evaluating their lives. Bloom provides a much needed perspective shift in how we think about wealth. More of the popular thinking is shifting away from wealth in terms of finances, and more towards wealth in other aspects of life, and this couldnt be needed. This is in the top 5 books I've read this year.\n\nI recieved an advanced copy of this book in exchange for my honest review...thank you NetGalley and Harriman House",
    # review 2: light, plain recommendation
    "Received an advanced copy of this book, and I highly recommend it.\n\nA great compendium of all tips, tricks and hacks (along with lots of new ones) that you might have pieced over the years if you watched, read or listened to the works of Jordan Peterson, Naval Ravikant, Sam Harris, Andrew Huberman, Tim Ferris, Joe Rogan and Lex Fridman.\n\nThe writing is light, easy to follow and not-preachy, the chapters are structured well and I constantly found myself taking notes and breezing through the 400 pages, so that must mean it's a winner.",
    # review 4: simple and enthusiastic
    "The 5 Types of Wealth is the best book that I have read in 2024! This is not another self help book. This is a how to guide for looking at Time Wealth, Social Wealth, Mental Wealth, Physical Wealth, and Financial Wealth and how to analyze and improve all aspects of life. Each section helps to measure your wealth and then give meaningful steps to improve.\n\nSahil Bloom combines storytelling, interviews, questions, exercises and insight in a guide to living your best life.\n\nThank you to NetGalley for providing an advanced reader copy in exchange for an honest review. I have also pre-ordered books for my adult children!",
    # review 8: short and plain
    "I liked this book. There were not a lot of new things for me to learn but everything was consolidated very well and I found some of the practical exercises useful. I didn’t always 100% agree with all the advice but the author had quite a pragmatic approach and there were definitely some things that worked for me. Definitely worth a read. Thanks to NetGalley for the early copy.",
    # review 9: two short sentences
    "Couldn't even finish. Dude set out to prioritize what was important in life after he already made millions. Not relatable at all",
]

ORDINARY_HUMAN = [
    # review 2
    "I was always put off reading this book due to the astounding similarities which the synopsis has to one of my favourite novels, \"Battle Royale\" by Koushon Takami. These similarities are not only found in the synopsis but do tend to resurface throughout the whole book.  It's difficult to believe that Suzanne Collins has not read Battle Royale and taken incredibly heavy inspiration from it, yet apparently she had no knowledge of it. Regardless, The Hunger Games does tell a new story, just within a familiar framework. Conceptual similarities aside there is genuinely gripping storytelling to be discovered, shockingly basic prose and minuscule sentences encapsulate the feelings of the main characters, and there are more than enough hints at a bigger picture to make me interested to read the next in the series. The Orwellian politics that plays as a subtext to the action is interesting and has great potential; thus far in the series it seems sorely under-utilised, but then again, this is essentially a children's book and grand ideas aren't expected to be dissected (no disrespect to children's books intended, I'm a huge fan). Characters are well presented and have great potential to develop in the sequels. The large typeface of simple language which spans 400+ pages is incredibly easy to read and therefore addictive. Surprisingly, it only took me three days to consume without any binging. The Hunger Games is great fun, easy to read yet with subtle hints at something grand, and for these reasons I recommend it. But while we're on the subject of a government that makes teenagers fight to the death as punishment for social rebellion, you should definitely read Battle Royale.",
    # review 3
    "All the bloggers have recommended this and I can see why. Very engrossing and suspenseful, a must-read if you like dystopian adventure. It's \"The Lottery\" crossed with Survivor, and not for the faint of heart. Two kids at school have read it so far and each one, when he returned it, said to me, \"That book was GOOD.\" I was so engrossed in reading that I forgot this is the first in a planned trilogy; the end left me hanging. It's not unlike Marsden's Tomorrow, When the War Began series; the characters are teenagers who must use weapons and ingenuity to defeat (okay, kill) their adversaries.",
    # review 6
    "\"The Most Dangerous Game\" meets Survivor. I loved it: deft characterization wrapped tightly around this lean, brutal plot that absolutely grabbed me and hung on. This was one that I started reading in the morning and snarled at all comers until I had finished it in the evening. HIGHLY RECOMMEND.",
    # review 7
    "allow me to be relevant for a moment: oh my god, this book is outstanding!! it is all good things; battle royale, blood of heroes (one of the best movies ever made - dont argue with me), and all the best elements of this survivalist gary paulsen jag i am on. it kept me up way past my bedtime last night, because i could not stop reading, even though my eyes did not want to be awake. and now we veer, as ever, into the personal. this book is my comeuppance. i suppose it is factually my second comeuppance. i used to be a sneerer at grownups reading harry potter and twilight and all the stuff that is supposed to be for the kiddies, and was disgusted by the infantilizing of our adults tastes. and then i decided to take a teen lit class this summer for my mls degree, so i could have a class with greg before he graduated. i figured it would be easy reading and not too challenging and a nice way to spend my summer; getting A pluses and hanging out with my friend. but of course, after i had read a few books from the syllabus, we realized that we had signed up for the wrong class, and all the teen books i had been reading (and for the most part enjoying) were not for our class. and the books i was actually supposed to be reading were for much much younger readers. and then i was disappointed that i wouldnt be reading all those teen books after all. first comeuppance: regretting mocking teen fiction because now i have to read actual books for babies, which is so much more infantilizing. and now, my second comeuppance, i read this book and its not on either of the reading lists, and i dont even know if i can use it for this 10-book annotated bibliography because it might be for too old of a reading age, but i dont even care. i am now an adult who reads teen fiction. i have to reevaluate everything i thought i stood for. i still wont read harry potter, because i am stubborn, but i might have to sneer a little less at others. and that,i assure you, that is going to hurt.",
    # review 8
    "The Hunger Games felt like the dawning of an era; it was my introduction to dystopian sci-fi and was the first book, in my teens, that made me legitimately reconsider the things I’d always been taught about the US government, politics, and society at large. I’d grown up in a solidly sheltered, religious, and politically conservative home, and had never questioned much of what I’d been told up to that point. I’ll never forget reading this book for the first time, and that moment of wondering if this could all become a reality, and weighing my own mortality a little more heavily than I had before.",
    # The rest are reader reviews of The 5 Types of Wealth.
    # review 3
    "Having had the privilege of reading an advanced copy, I can confidently say this book is a masterfully crafted roadmap to building a rich life in every sense. Sahil's authentic approach to each type of wealth combines inspiring anecdotes, practical exercises, and actionable insights.\n\nEach section empowers readers to reject the default path society often sets and instead encourages designing a dream life with intentionality. Sahil’s writing is both motivating and deeply introspective, making it easy to connect with his vision.\n\nA must-read for anyone ready to redefine their priorities, harness their potential, and create a life of true abundance.",
    # review 5
    "This is an engaging and accessible exploration of how to think about and (re)define wealth. The book explores five types of wealth - financial, mental, physical, social, and time. It is full of practical advice and prompts to reflect and assess various aspects of wealth. I appreciated the structure of the book which is organized around asking a “big question”, offering conceptualizations of the different types of wealth, outlining three pillars of each aspect of wealth, and providing guidance and summaries.\n\nThank you to Random House Ballantine and NetGalley for the opportunity to read a copy.",
    # review 6
    "A book to be read in your 20s, 30s and beyond...more than once!\n\nAs someone who feels I know what my goals are, what I want out of life and feel good about the balance I have achieved thus far, I felt light bulb moments going off throughout reading The 5 Types of Wealth. Sahil has the reader asking themselves questions that will make you think twice about what \"enough\" is, how you're spending your time and what it is you want out of life.\n\nThere are great guides, tips and hacks for each chapter that are applicable whether you are just starting out when it comes to a certain type of wealth or have been going at it for decades.\n\nSahil is a definite inspiration and wealth of knowledge!",
    # review 7
    "I found The 5 Types of Wealth enjoyable to read and picked up several ideas that I think will be useful for me to incorporate into my routine. Was every chapter full of new info or insights? No. Were all five sections equally useful? No, I found two of the five sections more interesting than the other three. But I highlighted several ideas or frameworks that were unique and I want to reference later. The author doesn’t address faith or the spiritual dimension of our lives but I could still find connections to my faith practice and priorities (example, the chapter on mental wealth gave me some insight on scripture memorization, which is important to me but much harder than it used to be).\n\nThis book reminded me of attending development courses when I was in the corporate world and sitting in a comfortable learning environment and finding one or two nuggets over the course of a couple of days that I could take away and do something with. If you like books like Atomic Habits, you would probably appreciate this one too. Thanks to Amy at Random House for pointing me to this book and to NetGalley for providing an e-galley to read and review. This book will come out on February 4, 2025.",
    # review 10
    "It’s not a bad book per se. On one hand, there are good ideas for self-reflection and genuine advice for a happier, healthier life. On the other, most of the content is straight up taken from other modern non-fiction books. To his credit, the author quotes the original creators, but does so to death. Some chapters are even explicit collaborations with said creators. Having gone through many of these books, I cannot help but feel like the content is repetitive, including word for word copies such as \"the fisherman parable\". There is also the occasional nonsense, like the claim that drinking water first thing in the morning will \"flush out the toxins\" from your body. The author is deeply entitled, and even though he is somewhat aware, the narrative often falls flat because of it.",
]

# ── AI-generated pieces (criterion 3) ────────────────────────────────────────
# Unedited chatbot output from a one-line prompt. These are short fiction
# vignettes while the human set is book reviews, so genre differs between the
# two groups; the README notes that as a limit on what the gap shows.

CLEAR_AI = [
    "At the edge of a quiet seaside town, a tiny bookstore opened only when it rained. Nobody knew who owned it, but visitors always discovered exactly the book they needed tucked somewhere among its crooked wooden shelves.",
    "The robot had been designed to organize kitchen cabinets, yet it developed an unusual fascination with jazz. Every evening at precisely seven, it abandoned the dishes and tapped complicated rhythms against pots and pans.",
    "Sunlight poured through the greenhouse roof, illuminating rows of plants in brilliant shades of green. Hidden between the tomatoes and basil, a single purple flower had appeared overnight, surprising everyone who passed it.",
    "Marcus kept a notebook filled entirely with ideas he considered too strange to pursue. There were plans for underwater cafés, umbrellas that collected drinking water, and a mysterious final page containing nothing except a carefully drawn circle.",
    "By midnight, the city streets were almost empty. A delivery cyclist glided through the intersections while apartment windows flickered above, each glowing rectangle suggesting a completely different story unfolding inside.",
    "Scientists aboard the research station expected the experiment to take months. Instead, their computer displayed a result after only seventeen minutes, leaving everyone staring silently at the screen and wondering which assumption had been wrong.",
    "The old coffee mug wasn't particularly valuable, but Elena refused to replace it. Its faded paint and chipped handle reminded her of early mornings, ambitious plans, and the small apartment where she had first learned to trust her own decisions.",
    "Somewhere deep in the mountains, melting snow gathered into a narrow stream that wound between stones and pine trees. It seemed insignificant there, but mile after mile the water joined other streams, eventually becoming a river wide enough to shape entire landscapes.",
]

# ── Long bodies (criterion 5) ────────────────────────────────────────────────
# Real sentences repeated to an exact word count, so the only thing that varies
# is length.

_FILLER = ("The district held its breath as the names were drawn, and nobody "
           "in the square said a word until the second name was read out loud.").split()


def _words(n: int) -> str:
    return " ".join(_FILLER[i % len(_FILLER)] for i in range(n))


SCENARIOS = [
    {
        "name": "plain-style human writing",
        "criterion": 1,
        # Target: at most 1 of 8 labelled high-confidence AI, in any trial.
        "texts": PLAIN_HUMAN,
    },
    {
        "name": "ordinary human writing",
        "criterion": 2,
        # Target: at least 7 of 10 labelled high-confidence human, every trial.
        "texts": ORDINARY_HUMAN,
    },
    {
        "name": "AI vs human gap",
        "criterion": 3,
        # Target: mean combined_score of the 8 AI pieces at least 0.30 above the
        # mean of the 8 human pieces, every trial. AI first, human second.
        "texts": CLEAR_AI + ORDINARY_HUMAN[:8],
    },
    {
        "name": "every label reachable",
        "criterion": 4,
        # Target: each label produced by both of its inputs in all 3 trials.
        # Chosen before the first run. Order: human, human, unsure, unsure,
        # ai, ai. The unsure pieces are AI text with about half the sentences
        # rewritten by hand.
        "texts": [
            # expected: human
            "'Fiction' is the most beloved genre to the young generation. Whether it could be in movies or books because it let's one explore the dream of an extrodinary stuff is possible if one had them in real life.",
            "If there is one dish for breakfast that everyone loves here is Bangalore is the Dosa. Dosa combined with coconut chutney and sambar is all that need to energize the boring day.",
            # expected: unsure
            "My name is John. I'm a Software Engineer at Google. Outside work, I spend most of my time playing tennies and watching movies.",
            # Written by Claude: sentences 1, 3 and 5 in a generated register,
            # 2 and 4 rewritten casually. The "rewrite" is also AI-written,
            # not by hand as criterion 4 specifies; the README says so.
            "The community garden behind the library reopened this spring after a long winter break. honestly half the beds were still mud the first week lol. Volunteers organized weekly workshops on composting and seasonal planting. My neighbour went once and now she wont stop talking about her tomatoes. The garden committee hopes to expand the space next year to include a small greenhouse.",
            # expected: ai
            "The train arrived at a station that didn’t appear on any map. Curious passengers stared through the windows at golden streetlights, empty platforms, and a clock whose hands seemed to be moving backward.",
            "Every morning, a red balloon appeared outside Daniel’s apartment window, floating perfectly still despite the wind. He ignored it for weeks, until one day a small envelope was tied to its string.",
        ],
    },
    {
        "name": "long text never scored in secret",
        "criterion": 5,
        # Target: over 250 words -> 413 and logged; 249 words -> scored (200).
        "bodies": [
            {"text": _words(249), "creator_id": "eval_long_249"},
            {"text": _words(251), "creator_id": "eval_long_251"},
            {"text": _words(1000), "creator_id": "eval_long_1000"},
            {"text": _words(10000), "creator_id": "eval_long_10000"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
