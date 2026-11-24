#!/usr/bin/env python3
"""Draw "The World in One Picture" — a one-image newspaper front page
summarising the world news of Monday 23 November 2026.

Deterministic: the same run always produces byte-identical entry.png.
Run:  python3 draw.py
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants

SIZE = 1024
MARGIN = 36
CONTENT_W = SIZE - 2 * MARGIN

PAPER = (250, 247, 240)
INK = (18, 18, 18)
GREY = (90, 86, 78)
RULE = (30, 30, 30)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

OUT = "entry.png"

# ---------------------------------------------------------------- content
# Every fact below is taken from the verified content spec for this date.

MASTHEAD = "THE WORLD IN ONE PICTURE"
DATELINE = "Monday 23 November 2026"
TAGLINE = "One image. One day. The whole world."

LEAD_LABEL = "LEAD STORY — BRUSSELS"
LEAD_HEADLINE = (
    "EU Unveils 22nd Sanctions Package: 60 Banks Cut From SWIFT, "
    "Sports Ban for Russia"
)
LEAD_BODY = (
    "The European Commission proposed its 22nd package of sanctions on "
    "Russia: some 60 banks cut from the SWIFT system, a crackdown on the "
    "crypto networks financing the war, more than 70 shadow-fleet vessels "
    "listed, and a ban on Russian-flag teams at European sporting and "
    "cultural events. The plan still needs unanimous approval from all "
    "27 member states."
)

PANELS = [
    (
        "Ukraine Confirms Sea Drones Sank Russian Corvette in Libya",
        "Zelenskyy confirmed seven Ukrainian naval drones sank the "
        "corvette Merkury in Benghazi port and hit the cargo ship "
        "Angara in the same operation.",
    ),
    (
        "Russian Strikes Kill at Least 14 in Kyiv Region",
        "Overnight attacks killed at least 14 people: ten in Dymer, "
        "where a five-storey block partly collapsed, three at a "
        "Vyshneve supermarket, and one in Bila Tserkva.",
    ),
    (
        "NATO Sends AWACS to Poland After Russian Missiles Land on Its Soil",
        "NATO will deploy an AWACS early-warning aircraft to Poland "
        "after three Russian Kh-101 missiles landed on Polish "
        "territory during Friday's mass attack on Ukraine.",
    ),
    (
        "Iran Flogs Singer Parastoo Ahmadi and Four of Her Team",
        "Ahmadi and four members of her team each received 74 lashes "
        "in Qom over her hijab-free online concert, and were banned "
        "from artistic work and travel for two years.",
    ),
    (
        "Markets Roar Back as Nvidia Reinstates Jensen Huang",
        "Nvidia surged about 31% as Huang returned as CEO. The Nasdaq "
        "jumped 6.5% and the S&P 500 rose 4.7%, snapping a "
        "seven-session losing streak.",
    ),
    (
        "COP31 Fallout: Erdogan Defends Summit That Ended Without a Deal",
        "Erdogan said COP31 laid a 'very valuable foundation' after "
        "the Antalya talks collapsed without a deal — the first such "
        "breakdown since Copenhagen in 2009.",
    ),
]

TICKER = (
    "FINLAND SUMMONS RUSSIA'S AMBASSADOR  •  EU SIGNS TRADE DEAL WITH "
    "INDONESIA  •  CROWDSTRIKE TO ACQUIRE ZSCALER IN ~$44BN DEAL"
)

# ---------------------------------------------------------------- helpers


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap measured with the real font metrics."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, leading, fill=INK):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, text, y, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text(((SIZE - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


# ---------------------------------------------------------------- layout


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    y = 26
    # top rule
    d.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RULE, width=3)
    y += 14

    # masthead
    y = centred(d, MASTHEAD, y, font(SERIF_BOLD, 50))
    y += 8
    y = centred(d, DATELINE + "   ·   " + TAGLINE, y, font(SANS_BOLD, 17), GREY)
    y += 12
    # double rule under the masthead
    d.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RULE, width=4)
    d.line([(MARGIN, y + 7), (SIZE - MARGIN, y + 7)], fill=RULE, width=1)
    y += 24

    # lead story
    d.text((MARGIN, y), LEAD_LABEL, font=font(SANS_BOLD, 15), fill=GREY)
    y += 24
    lead_head = wrap(d, LEAD_HEADLINE, font(SERIF_BOLD, 37), CONTENT_W)
    y = draw_lines(d, lead_head, MARGIN, y, font(SERIF_BOLD, 37), 45)
    y += 8
    lead_body = wrap(d, LEAD_BODY, font(SERIF, 19), CONTENT_W)
    y = draw_lines(d, lead_body, MARGIN, y, font(SERIF, 19), 26)
    y += 16
    d.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RULE, width=2)
    y += 18

    # panel grid: two columns, three rows
    gap = 28
    col_w = (CONTENT_W - gap) // 2
    row_top = y
    panel_h_max = 0
    positions = []
    for i, (head, body) in enumerate(PANELS):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + gap)
        positions.append((x, row, head, body))

    row_heights = [0, 0, 0]
    rendered = []
    for x, row, head, body in positions:
        head_lines = wrap(d, head, font(SERIF_BOLD, 20), col_w)
        body_lines = wrap(d, body, font(SERIF, 16), col_w)
        h = len(head_lines) * 25 + 4 + len(body_lines) * 21
        row_heights[row] = max(row_heights[row], h)
        rendered.append((x, row, head_lines, body_lines))

    row_y = [row_top]
    for r in range(2):
        row_y.append(row_y[-1] + row_heights[r] + 16)

    for x, row, head_lines, body_lines in rendered:
        py = row_y[row]
        py = draw_lines(d, head_lines, x, py, font(SERIF_BOLD, 20), 25)
        py += 4
        draw_lines(d, body_lines, x, py, font(SERIF, 16), 21)

    # vertical divider between the columns
    mid_x = MARGIN + col_w + gap // 2
    grid_bottom = row_y[2] + row_heights[2]
    d.line([(mid_x, row_top), (mid_x, grid_bottom)], fill=(170, 164, 150), width=1)
    # horizontal rules between rows
    for r in range(2):
        ry = row_y[r] + row_heights[r] + 8
        d.line([(MARGIN, ry), (SIZE - MARGIN, ry)], fill=(170, 164, 150), width=1)

    # ticker strip at the bottom
    strip_h = 74
    strip_y = SIZE - MARGIN - strip_h
    assert grid_bottom + 14 <= strip_y, f"layout overflow: grid ends {grid_bottom}"
    d.rectangle([(0, strip_y), (SIZE, SIZE - MARGIN + 6)], fill=(16, 16, 16))
    tick_lines = wrap(d, TICKER, font(SANS_BOLD, 17), CONTENT_W)
    ty = strip_y + (strip_h - len(tick_lines) * 24) // 2
    for line in tick_lines:
        w = d.textlength(line, font=font(SANS_BOLD, 17))
        d.text(((SIZE - w) / 2, ty), line, font=font(SANS_BOLD, 17), fill=(245, 242, 235))
        ty += 24

    img.save(OUT)
    print(f"wrote {OUT}: grid_bottom={grid_bottom} strip_y={strip_y}")


if __name__ == "__main__":
    build()
