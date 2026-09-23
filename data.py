# -*- coding: utf-8 -*-
"""
TastyBox Channel Explorer — dataset and derived metrics.

Five acquisition channels, 12 months of retention data each, built from two
underlying sub-segments (New-to-brand / Existing) that blend into the
"headline" curve students see by default. Every number here was verified
programmatically to produce four specific analytical reversals when
explored through the widget's toggles — see BUSINESS_QUESTIONS at the
bottom for what each one is testing, and INSTRUCTOR_CODE below for the
sidebar passcode that unlocks the debrief notes.
"""

MARGIN = 15  # $ margin per active customer per month
MONTHS = 12

# Passcode that unlocks the instructor debrief notes in the sidebar.
# Change this before class to whatever you'll actually use/remember.
INSTRUCTOR_CODE = "tastybox-debrief"

# name -> (acquired customers, CAC per acquired customer $, segments)
# each segment: (label, floor retention, monthly decay, share of channel's acquisitions)
CHANNELS = {
    "Organic": dict(
        acquired=500, cac=2,
        segs=[("New-to-brand", 0.24, 0.75, 0.40), ("Existing", 0.30, 0.80, 0.60)],
    ),
    "Paid Search": dict(
        acquired=900, cac=28,
        segs=[("New-to-brand", 0.10, 0.68, 0.90), ("Existing", 0.25, 0.75, 0.10)],
    ),
    "Influencer": dict(
        acquired=350, cac=45,
        segs=[("New-to-brand", 0.04, 0.84, 0.65), ("Existing", 0.07, 0.87, 0.35)],
    ),
    "Holiday Promo": dict(
        acquired=480, cac=18,
        segs=[("New-to-brand", 0.47, 0.58, 0.55), ("Existing", 0.54, 0.63, 0.45)],
    ),
    "Referral": dict(
        acquired=300, cac=8,
        segs=[("New-to-brand", 0.06, 0.55, 0.65), ("Existing", 0.78, 0.96, 0.35)],
    ),
}

CHANNEL_ORDER = ["Organic", "Paid Search", "Influencer", "Holiday Promo", "Referral"]

COLORS = {
    "Organic": "#0E7C7B",
    "Paid Search": "#C8534A",
    "Influencer": "#8A5A2A",
    "Holiday Promo": "#13233B",
    "Referral": "#6C4FA1",
}


def _curve(floor, decay, months=MONTHS):
    return [floor + (1 - floor) * decay ** t for t in range(1, months + 1)]


def _blend(curve_a, curve_b, share_a):
    return [share_a * a + (1 - share_a) * b for a, b in zip(curve_a, curve_b)]


def _cum_clv(frac_curve, margin=MARGIN):
    running = 0.0
    out = []
    for f in frac_curve:
        running += f * margin
        out.append(running)
    return out


def build_dataset():
    """Returns a dict keyed by channel name with every derived series needed
    by the app: blended + per-segment fraction curves and cumulative CLV
    curves, acquired counts, and CAC."""
    out = {}
    for name, d in CHANNELS.items():
        (n1, f1, dc1, s1), (n2, f2, dc2, s2) = d["segs"]
        c1, c2 = _curve(f1, dc1), _curve(f2, dc2)
        blended = _blend(c1, c2, s1)
        out[name] = dict(
            acquired=d["acquired"],
            cac=d["cac"],
            blended_frac=blended,
            blended_clv=_cum_clv(blended),
            segments=[
                dict(name=n1, share=s1, frac=c1, clv=_cum_clv(c1)),
                dict(name=n2, share=s2, frac=c2, clv=_cum_clv(c2)),
            ],
        )
    return out


DATA = build_dataset()


# ---------------------------------------------------------------------
# The four guided business questions. Each is an open scenario with a
# question for the group to argue through using the widget's controls —
# no hint at which toggle "solves" it, and no per-question answer key.
# The write-ups in `reveal` are for the instructor debrief after
# discussion; the app surfaces them only behind a passcode, never
# attached to the question itself. See BUSINESS_QUESTIONS below.
# ---------------------------------------------------------------------
BUSINESS_QUESTIONS = [
    dict(
        id="q1",
        title="Q1 — The CMO wants a budget call off Q1 results. What do you tell her?",
        setup=(
            "It's the end of the first quarter (month 3), and the CMO is locking in "
            "next year's channel budget off early performance. She wants a one-line "
            "read: which channel is winning so far? Set the month slider to 3 and "
            "look at the ranking."
        ),
        prompt="What would you caution against before she locks in that budget?",
        reveal=(
            "**The trap:** at month 3, Influencer is in a near-tie for the lead — a "
            "defensible pick if you're locking in a budget off one quarter.\n\n"
            "**The reveal:** by month 6, Holiday Promo overtakes every channel and "
            "never gives the lead back, while Influencer's early spike fades fast as "
            "its retention curve flattens out. A budget set after Q1 would have "
            "overfunded the channel about to fade and starved the one about to "
            "compound — the standard argument for waiting through at least two full "
            "retention cycles before reallocating spend."
        ),
    ),
    dict(
        id="q2",
        title="Q2 — Influencer posts a solid CLV. Do you recommend scaling it?",
        setup=(
            "Influencer's 12-month CLV per customer is $78.70 — respectable, mid-pack, "
            "and it was even the Q1 leader. The growth team's draft memo recommends "
            "doubling Influencer spend next year on the strength of that number."
        ),
        prompt="What would you want to check before signing off on that memo?",
        reveal=(
            "**The trap:** CLV alone makes Influencer look like a safe channel to "
            "scale — nothing in that number signals a problem.\n\n"
            "**The reveal:** Influencer's CAC is $45, by far the highest of the "
            "five, putting its LTV:CAC ratio at roughly 1.75:1 — well under the 3:1 "
            "most marketing teams use as a floor for a channel worth scaling. Net of "
            "acquisition cost, its value falls to $33.70, second-to-last of all "
            "five. The memo's recommendation reverses once cost enters the model: "
            "no scaling call should be made on CLV alone."
        ),
    ),
    dict(
        id="q3",
        title="Q3 — Paid Search drove the most volume. Is it the growth engine?",
        setup=(
            "Paid Search acquired 900 customers this year — nearly double any other "
            "channel, and almost twice Holiday Promo's 480. In the year-end growth "
            "review, it's the headline number: Paid Search built the base."
        ),
        prompt="What's missing from that headline number?",
        reveal=(
            "**The trap:** 900 new customers is the biggest number on the page, and "
            "headcount is the easiest metric to lead a growth review with.\n\n"
            "**The reveal:** Paid Search's per-customer CLV ($49.53) is the worst of "
            "all five channels, and in total dollars it's actually beaten by Holiday "
            "Promo ($48,752 vs. $44,581) — a channel that acquired little more than "
            "half as many customers. Volume and value answer different questions; a "
            "growth review that tracks acquisition count alone keeps funding the "
            "channel that looks biggest, not the one that's paying back."
        ),
    ),
    dict(
        id="q4",
        title="Q4 — Referral is mediocre everywhere. Do you cut it from the mix?",
        setup=(
            "Referral ranks 4th of 5 on CLV, 3rd on net value, and last on total "
            "value created. Nothing in the blended numbers argues for protecting its "
            "budget line, and it's the easiest channel to cut without a fight."
        ),
        prompt="Would you defend that call? What would make you dig further first?",
        reveal=(
            "**The trap:** the blended number is genuinely unremarkable on every "
            "measure, so \"deprioritize Referral\" reads as the safe, low-risk "
            "call.\n\n"
            "**The reveal:** Referral is actually two very different customer "
            "populations averaged together. Referrals from **existing customers** "
            "are worth $171.07 — the single best number in the entire dataset, ahead "
            "of every other channel outright. Referrals that bring in **new-to-brand** "
            "customers are worth only $28.02 — the worst. Averaging hid a targeting "
            "decision as a channel decision: the fix isn't to cut Referral, it's to "
            "redesign the program so it targets existing customers' networks instead "
            "of cold new-to-brand traffic."
        ),
    ),
]
