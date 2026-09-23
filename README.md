# TastyBox Channel Explorer

An interactive Streamlit widget for the Customer Analytics (MARK 6580) TastyBox
case. Students toggle time horizon, acquisition cost, comparison metric, and
segment split to work through four guided business questions, each with a
naive first answer that turns out to be wrong once you dig in.

## What it's testing

Five acquisition channels, twelve months of (synthetic, internally
consistent) retention data:

1. **Early-decision trap** — the channel that looks best after one quarter
   is not the channel that's best after a year.
2. **CAC-blind trap** — a channel's raw CLV looks fine until you net out
   what it cost to acquire those customers.
3. **Vanity-metric trap** — the channel with the most customers acquired
   is not the channel that created the most total value.
4. **Simpson's paradox trap** — a channel that looks mediocre blended is
   hiding one great sub-segment and one terrible one.

All underlying numbers are simplified teaching data, not real TastyBox
financials, but they were verified programmatically so all four traps hold
at once and nothing contradicts anything else in the dataset.

## Running it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## Deploying to Streamlit Community Cloud (free, ~2 minutes)

1. Create a new GitHub repository and push this folder to it. **Make the
   repository Private** — see "Keep the repo private" below for why —
   then:

   ```bash
   git init
   git add .
   git commit -m "TastyBox Channel Explorer"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with
   your GitHub account. When it asks for repository access, grant it access
   to your private repos too (Streamlit Community Cloud can deploy from
   private repos — it just needs the permission).
3. Click **New app**, pick this repository/branch, and set the main file
   path to `app.py`.
4. Click **Deploy**. Streamlit installs `requirements.txt` automatically and
   gives you a public URL (e.g. `https://<something>.streamlit.app`) you can
   share with students — no login required for them to use it. The deployed
   *app* is reachable by anyone with the link even though the *repo* is
   private; only the source code stays private.

Any time you push a change to the `main` branch, the deployed app updates
automatically within a minute or two.

### Keep the repo private

The instructor debrief notes are gated behind a passcode typed into the
app's sidebar (see below) — but that passcode is stored as plain text in
`data.py`. The app itself never exposes it (Streamlit runs server-side, so
nothing in a browser's dev tools can reveal it), but if the GitHub
**repository** is public, anyone who finds it can simply open `data.py` on
GitHub and read the code directly. Keep the repo Private and this isn't a
concern — only you (and anyone you explicitly invite as a collaborator)
can see the source.

## Files

- `app.py` — the Streamlit app (UI, charts, controls, question reveals)
- `data.py` — the dataset and the four business questions' setup/reveal text
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — theme (matches the course's navy/teal brand)

## Editing the data or questions

Everything about the five channels — acquired counts, CAC, retention curve
parameters, segment splits — lives in `CHANNELS` at the top of `data.py`.
The four question prompts and reveal text live in `BUSINESS_QUESTIONS` in
the same file. Change either and redeploy; no changes to `app.py` are
needed unless you're adding a new control or chart.

## Instructor debrief passcode

Each of the four questions is open-ended in the app itself — a scenario and
a question, no hint about which toggle "solves" it, and no answer key
attached. The write-ups for each one (what the naive read misses, and why)
live behind a small, unlabeled passcode box collapsed into the sidebar
(click the `>>` chevron, top-left, to open it). Type the code and press
Enter; a "Debrief" section with all four write-ups appears below the
questions. Nothing on the page hints that this exists until you open the
sidebar.

The default code is `tastybox-debrief`, set at the top of `data.py` as
`INSTRUCTOR_CODE`. Change it, save, then `git add .`, `git commit`, `git
push` — the deployed app redeploys automatically within a minute or two.

## Raw data workbook (Excel fallback)

`build_raw_data.py` generates `TastyBox_RawData.xlsx` — the whole exercise
reproduced in Excel in case you ever need to run it without the widget
(no wifi, no laptops, whatever). Seven tabs:

- **Discussion Questions** — the same four open-ended prompts as the
  widget. Safe to hand to students along with Channel Summary and the
  Monthly Data tabs.
- **Channel Summary**, **Monthly Data - Blended**, **Monthly Data - By
  Segment**, **Assumptions** — the same formula-driven dataset as before,
  computed live from the underlying curve parameters.
- **Instructor Notes** — the debrief write-up for each question. Not
  gated the way the widget's version is (Excel doesn't have a clean
  equivalent to the sidebar passcode) — it's just the last tab. Keep this
  file off any share you hand out before the exercise if you don't want
  it visible.

Not part of the deployed app; regenerate it any time after editing
`data.py` with:

```bash
pip install openpyxl
python build_raw_data.py
```
