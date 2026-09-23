# -*- coding: utf-8 -*-
"""Builds TastyBox_RawData.xlsx: a fully formula-driven export of the dataset
behind the TastyBox Channel Explorer, for the instructor to explore, audit,
or extend. Editing the blue assumption cells recalculates everything else."""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from data import CHANNELS, CHANNEL_ORDER, MARGIN, MONTHS

# ---------------------------------------------------------------------
# Styling constants
# ---------------------------------------------------------------------
FONT_NAME = "Arial"
NAVY = "13233B"
TEAL = "0E7C7B"
INPUT_BLUE = "0000FF"
HEADER_FILL = PatternFill("solid", fgColor=NAVY)
SECTION_FILL = PatternFill("solid", fgColor="F3F5F7")
HEADER_FONT = Font(name=FONT_NAME, bold=True, color="FFFFFF", size=11)
SECTION_FONT = Font(name=FONT_NAME, bold=True, color=NAVY, size=11)
TITLE_FONT = Font(name=FONT_NAME, bold=True, color=NAVY, size=16)
LABEL_FONT = Font(name=FONT_NAME, color="3A4552", size=10.5)
INPUT_FONT = Font(name=FONT_NAME, color=INPUT_BLUE, size=10.5)
BODY_FONT = Font(name=FONT_NAME, color="3A4552", size=10.5)
THIN = Side(style="thin", color="E1E6EA")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

CURRENCY = '$#,##0.00'
CURRENCY0 = '$#,##0'
INT0 = '#,##0'
PCT1 = '0.0%'
MULT = '0.00"x"'


def style_header_row(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = BORDER


def autofit(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


wb = Workbook()

# =======================================================================
# Sheet 1: Read Me
# =======================================================================
ws = wb.active
ws.title = "Read Me"
WRAP_COLS = 6          # merge A:F for every wrapped paragraph
COL_WIDTH_CHARS = 118  # approx. characters per wrapped line at this width

ws["A1"] = "TastyBox Channel Explorer — Raw Data"
ws["A1"].font = TITLE_FONT
ws.merge_cells("A1:F1")
ws["A2"] = "Customer Analytics (MARK 6580) · TastyBox case"
ws["A2"].font = Font(name=FONT_NAME, color=TEAL, bold=True, size=10.5)
ws.merge_cells("A2:F2")

import math


def add_section(ws, row, text):
    ws.cell(row=row, column=1, value=text).font = SECTION_FONT
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=WRAP_COLS)
    return row + 1


def add_para(ws, row, text):
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = BODY_FONT
    cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=WRAP_COLS)
    n_lines = max(1, math.ceil(len(text) / COL_WIDTH_CHARS))
    ws.row_dimensions[row].height = 15 * n_lines + 8
    return row + 1


def add_bullet(ws, row, label, note):
    cell = ws.cell(row=row, column=1, value=f"{label} — {note}")
    cell.font = BODY_FONT
    cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=WRAP_COLS)
    n_lines = max(1, math.ceil(len(label + " — " + note) / COL_WIDTH_CHARS))
    ws.row_dimensions[row].height = 15 * n_lines + 8
    return row + 1


r = 4
r = add_section(ws, r, "What this is")
r = add_para(ws, r, (
    "This workbook is the same dataset that powers the TastyBox Channel Explorer "
    "Streamlit widget, fully broken out and formula-driven so you can audit it, "
    "pivot it, or extend it."
))
r = add_para(ws, r, (
    "Every derived number — retention rate, active customers, cumulative CLV, "
    "LTV:CAC — is a live formula, not a pasted value. Edit any blue cell on the "
    "Assumptions tab (margin, retention floor, decay, segment share, acquired "
    "customers, CAC) and everything downstream recalculates."
))
r += 1
r = add_section(ws, r, "How the retention model works")
r = add_para(ws, r, (
    "Each channel is built from two sub-segments (New-to-brand / Existing) that "
    "blend into the headline curve. Each segment's retention rate at month t "
    "follows Floor + (1 − Floor) × Decay^t — it decays geometrically toward a "
    "floor rather than to zero, a reasonable approximation for a subscription "
    "business with a loyal core."
))
r = add_para(ws, r, (
    "Cumulative CLV per acquired customer at month t = the running sum of "
    "(retention rate × margin per active customer) from month 1 to t. No "
    "discounting is applied — this mirrors the exercise's pen-and-paper CLV "
    "formula, not the deck's infinite-horizon perpetuity formula."
))
r += 1
r = add_section(ws, r, "Tabs in this workbook")
r = add_bullet(ws, r, "Channel Summary", "one row per channel: acquired, CAC, CLV at months 3/6/12, net value, total value created, LTV:CAC ratio.")
r = add_bullet(ws, r, "Monthly Data - Blended", "60 rows (5 channels x 12 months): the headline retention/CLV curve per channel, as shown in the widget by default.")
r = add_bullet(ws, r, "Monthly Data - By Segment", "120 rows (5 channels x 2 segments x 12 months): the New-to-brand / Existing split behind each blended curve — what the widget's 'Split by segment' toggle reveals.")
r = add_bullet(ws, r, "Assumptions", "the model's actual inputs: margin, and each channel/segment's acquired count, CAC, segment share, retention floor, and monthly decay. Edit here to explore scenarios.")
r += 1
r = add_section(ws, r, "A note on precision")
r = add_para(ws, r, (
    "The Channel Summary and Monthly Data - Blended tabs compute retention "
    "directly from the curve parameters (matching the widget's figures to the "
    "cent). The Active Customers column is a rounded, realistic headcount shown "
    "for readability — it is derived from the precise retention rate, not the "
    "other way round, so rounding never compounds into the CLV figures."
))
r += 1
r = add_section(ws, r, "Caveat")
r = add_para(ws, r, (
    "All figures are simplified, internally consistent teaching data — not real "
    "TastyBox financials. Margin is a flat $%d per active customer per month "
    "across all channels and segments." % MARGIN
))

autofit(ws, [20, 20, 20, 20, 20, 20])

# =======================================================================
# Sheet 2: Assumptions
# =======================================================================
asm = wb.create_sheet("Assumptions")
asm["A1"] = "Model Assumptions — edit the blue cells to explore scenarios"
asm["A1"].font = TITLE_FONT
asm.merge_cells("A1:G1")

asm["A3"] = "Margin per active customer per month ($)"
asm["A3"].font = LABEL_FONT
asm["B3"] = MARGIN
asm["B3"].font = INPUT_FONT
asm["B3"].number_format = CURRENCY0

asm["A4"] = "Months modeled"
asm["A4"].font = LABEL_FONT
asm["B4"] = MONTHS
asm["B4"].font = INPUT_FONT
asm["B4"].number_format = INT0

asm["A6"] = "CHANNEL TOTALS"
asm["A6"].font = SECTION_FONT
ch_header_row = 7
headers1 = ["Channel", "Customers Acquired", "CAC ($)"]
for i, h in enumerate(headers1, start=1):
    asm.cell(row=ch_header_row, column=i, value=h)
style_header_row(asm, ch_header_row, len(headers1))

ch_start = ch_header_row + 1
for i, name in enumerate(CHANNEL_ORDER):
    r = ch_start + i
    d = CHANNELS[name]
    asm.cell(row=r, column=1, value=name).font = BODY_FONT
    c = asm.cell(row=r, column=2, value=d["acquired"])
    c.font = INPUT_FONT
    c.number_format = INT0
    c = asm.cell(row=r, column=3, value=d["cac"])
    c.font = INPUT_FONT
    c.number_format = CURRENCY0
    for col in range(1, 4):
        asm.cell(row=r, column=col).border = BORDER
ch_end = ch_start + len(CHANNEL_ORDER) - 1

seg_section_row = ch_end + 2
asm.cell(row=seg_section_row, column=1, value="SEGMENT CURVE PARAMETERS").font = SECTION_FONT
seg_header_row = seg_section_row + 1
headers2 = ["Channel", "Segment", "Segment Share", "Retention Floor", "Monthly Decay"]
for i, h in enumerate(headers2, start=1):
    asm.cell(row=seg_header_row, column=i, value=h)
style_header_row(asm, seg_header_row, len(headers2))

seg_start = seg_header_row + 1
r = seg_start
for name in CHANNEL_ORDER:
    for seg_name, floor, decay, share in CHANNELS[name]["segs"]:
        asm.cell(row=r, column=1, value=name).font = BODY_FONT
        asm.cell(row=r, column=2, value=seg_name).font = BODY_FONT
        c = asm.cell(row=r, column=3, value=share)
        c.font = INPUT_FONT
        c.number_format = PCT1
        c = asm.cell(row=r, column=4, value=floor)
        c.font = INPUT_FONT
        c.number_format = PCT1
        c = asm.cell(row=r, column=5, value=decay)
        c.font = INPUT_FONT
        c.number_format = PCT1
        for col in range(1, 6):
            asm.cell(row=r, column=col).border = BORDER
        r += 1
seg_end = r - 1

autofit(asm, [16, 16, 15, 16, 15])

# =======================================================================
# Sheet 3: Monthly Data - By Segment (build first; Blended sheet sums it)
# =======================================================================
seg_ws = wb.create_sheet("Monthly Data - By Segment")
headers = ["Channel", "Segment", "Month", "Retention Rate", "Segment Acquired", "Active Customers", "Cumulative CLV ($)"]
for i, h in enumerate(headers, start=1):
    seg_ws.cell(row=1, column=i, value=h)
style_header_row(seg_ws, 1, len(headers))

CH_TOT = f"Assumptions!$B${ch_start}:$B${ch_end}"
CH_NAMES = f"Assumptions!$A${ch_start}:$A${ch_end}"
SEG_SHARE = f"Assumptions!$C${seg_start}:$C${seg_end}"
SEG_FLOOR = f"Assumptions!$D${seg_start}:$D${seg_end}"
SEG_DECAY = f"Assumptions!$E${seg_start}:$E${seg_end}"
SEG_CH = f"Assumptions!$A${seg_start}:$A${seg_end}"
SEG_SEG = f"Assumptions!$B${seg_start}:$B${seg_end}"

row = 2
seg_first_row = row
for name in CHANNEL_ORDER:
    for seg_name, floor, decay, share in CHANNELS[name]["segs"]:
        for month in range(1, MONTHS + 1):
            seg_ws.cell(row=row, column=1, value=name).font = BODY_FONT
            seg_ws.cell(row=row, column=2, value=seg_name).font = BODY_FONT
            seg_ws.cell(row=row, column=3, value=month).font = BODY_FONT

            floor_lookup = f"SUMIFS({SEG_FLOOR},{SEG_CH},$A{row},{SEG_SEG},$B{row})"
            decay_lookup = f"SUMIFS({SEG_DECAY},{SEG_CH},$A{row},{SEG_SEG},$B{row})"
            share_lookup = f"SUMIFS({SEG_SHARE},{SEG_CH},$A{row},{SEG_SEG},$B{row})"
            acquired_lookup = f"SUMIFS({CH_TOT},{CH_NAMES},$A{row})"

            d_cell = seg_ws.cell(row=row, column=4)
            d_cell.value = f"={floor_lookup}+(1-{floor_lookup})*{decay_lookup}^$C{row}"
            d_cell.number_format = PCT1
            d_cell.font = BODY_FONT

            e_cell = seg_ws.cell(row=row, column=5)
            e_cell.value = f"=ROUND({acquired_lookup}*{share_lookup},0)"
            e_cell.number_format = INT0
            e_cell.font = BODY_FONT

            f_cell = seg_ws.cell(row=row, column=6)
            f_cell.value = f"=ROUND(D{row}*E{row},0)"
            f_cell.number_format = INT0
            f_cell.font = BODY_FONT

            g_cell = seg_ws.cell(row=row, column=7)
            if month == 1:
                g_cell.value = f"=D{row}*Assumptions!$B$3"
            else:
                g_cell.value = f"=G{row-1}+D{row}*Assumptions!$B$3"
            g_cell.number_format = CURRENCY
            g_cell.font = BODY_FONT

            for col in range(1, 8):
                seg_ws.cell(row=row, column=col).border = BORDER
            row += 1
seg_last_row = row - 1

seg_ws.freeze_panes = "A2"
autofit(seg_ws, [15, 16, 8, 15, 16, 16, 18])

# =======================================================================
# Sheet 4: Monthly Data - Blended
# =======================================================================
bl_ws = wb.create_sheet("Monthly Data - Blended")
headers = ["Channel", "Month", "Retention Rate", "Active Customers", "Cumulative CLV ($)"]
for i, h in enumerate(headers, start=1):
    bl_ws.cell(row=1, column=i, value=h)
style_header_row(bl_ws, 1, len(headers))

# Blended retention is computed straight from the Assumptions curve
# parameters (a share-weighted SUMPRODUCT across each channel's two
# segment rows), NOT by summing the segment sheet's rounded headcounts —
# that keeps this sheet numerically identical to the widget's own math
# instead of drifting from compounded rounding over 12 months. Active
# Customers is still shown as a rounded, realistic headcount, but it's
# derived from the precise retention rate rather than the other way round.
row = 2
bl_first_row = row
for name in CHANNEL_ORDER:
    for month in range(1, MONTHS + 1):
        bl_ws.cell(row=row, column=1, value=name).font = BODY_FONT
        bl_ws.cell(row=row, column=2, value=month).font = BODY_FONT

        acquired_lookup = f"SUMIFS({CH_TOT},{CH_NAMES},$A{row})"

        b_cell = bl_ws.cell(row=row, column=3)  # Retention Rate
        b_cell.value = (
            f"=SUMPRODUCT(({SEG_CH}=$A{row})*({SEG_SHARE})*"
            f"({SEG_FLOOR}+(1-{SEG_FLOOR})*{SEG_DECAY}^$B{row}))"
        )
        b_cell.number_format = PCT1
        b_cell.font = BODY_FONT

        c_cell = bl_ws.cell(row=row, column=4)  # Active Customers
        c_cell.value = f"=ROUND(C{row}*({acquired_lookup}),0)"
        c_cell.number_format = INT0
        c_cell.font = BODY_FONT

        e_cell = bl_ws.cell(row=row, column=5)  # Cumulative CLV
        if month == 1:
            e_cell.value = f"=C{row}*Assumptions!$B$3"
        else:
            e_cell.value = f"=E{row-1}+C{row}*Assumptions!$B$3"
        e_cell.number_format = CURRENCY
        e_cell.font = BODY_FONT

        for col in range(1, 6):
            bl_ws.cell(row=row, column=col).border = BORDER
        row += 1
bl_last_row = row - 1

bl_ws.freeze_panes = "A2"
autofit(bl_ws, [15, 8, 15, 16, 18])

# =======================================================================
# Sheet 5: Channel Summary
# =======================================================================
cs_ws = wb.create_sheet("Channel Summary")
headers = [
    "Channel", "Customers Acquired", "CAC ($)", "Month 3 CLV", "Month 6 CLV",
    "Month 12 CLV", "Net Value (CLV12 - CAC)", "Total Value Created ($)", "LTV:CAC Ratio",
]
for i, h in enumerate(headers, start=1):
    cs_ws.cell(row=1, column=i, value=h)
style_header_row(cs_ws, 1, len(headers))

BLSHEET = "'Monthly Data - Blended'"
BL_CH_COL = f"{BLSHEET}!$A${bl_first_row}:$A${bl_last_row}"
BL_MONTH_COL = f"{BLSHEET}!$B${bl_first_row}:$B${bl_last_row}"
BL_CLV_COL = f"{BLSHEET}!$E${bl_first_row}:$E${bl_last_row}"

for i, name in enumerate(CHANNEL_ORDER):
    r = 2 + i
    cs_ws.cell(row=r, column=1, value=name).font = BODY_FONT

    b = cs_ws.cell(row=r, column=2)
    b.value = f"=SUMIFS({CH_TOT},{CH_NAMES},A{r})"
    b.number_format = INT0
    b.font = BODY_FONT

    c = cs_ws.cell(row=r, column=3)
    c.value = f"=SUMIFS(Assumptions!$C${ch_start}:$C${ch_end},{CH_NAMES},A{r})"
    c.number_format = CURRENCY0
    c.font = BODY_FONT

    for col, month in ((4, 3), (5, 6), (6, 12)):
        cell = cs_ws.cell(row=r, column=col)
        cell.value = f"=SUMIFS({BL_CLV_COL},{BL_CH_COL},$A{r},{BL_MONTH_COL},{month})"
        cell.number_format = CURRENCY
        cell.font = BODY_FONT

    net = cs_ws.cell(row=r, column=7)
    net.value = f"=F{r}-C{r}"
    net.number_format = CURRENCY
    net.font = BODY_FONT

    total = cs_ws.cell(row=r, column=8)
    total.value = f"=F{r}*B{r}"
    total.number_format = CURRENCY0
    total.font = BODY_FONT

    ratio = cs_ws.cell(row=r, column=9)
    ratio.value = f"=IFERROR(F{r}/C{r},0)"
    ratio.number_format = MULT
    ratio.font = BODY_FONT

    for col in range(1, 10):
        cs_ws.cell(row=r, column=col).border = BORDER

cs_ws.freeze_panes = "A2"
autofit(cs_ws, [15, 17, 10, 13, 13, 13, 20, 20, 13])

# reorder sheets: Read Me, Channel Summary, Monthly Blended, Monthly Segment, Assumptions
wb._sheets = [
    wb["Read Me"], wb["Channel Summary"], wb["Monthly Data - Blended"],
    wb["Monthly Data - By Segment"], wb["Assumptions"],
]

wb.save("TastyBox_RawData.xlsx")
print("saved")
