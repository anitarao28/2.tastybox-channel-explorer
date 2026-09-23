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

1. Create a new GitHub repository and push this folder to it:

   ```bash
   git init
   git add .
   git commit -m "TastyBox Channel Explorer"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with
   your GitHub account.
3. Click **New app**, pick this repository/branch, and set the main file
   path to `app.py`.
4. Click **Deploy**. Streamlit installs `requirements.txt` automatically and
   gives you a public URL (e.g. `https://<something>.streamlit.app`) you can
   share with students — no login required for them to use it.

Any time you push a change to the `main` branch, the deployed app updates
automatically within a minute or two.

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

## Raw data workbook (optional)

`build_raw_data.py` generates `TastyBox_RawData.xlsx` — a fully
formula-driven export of the same dataset (retention rate, active
customers, cumulative CLV, all computed live from the underlying curve
parameters) for exploring, pivoting, or auditing outside the widget. It's
not part of the deployed app; regenerate it any time with:

```bash
pip install openpyxl
python build_raw_data.py
```
