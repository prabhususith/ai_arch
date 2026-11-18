"""
Generate high-resolution visual diagrams and illustrations for the Oxford AI Ebook.
Uses Pillow to create clean, colorful, pedagogical diagrams suitable for age 10 to pro.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

os.makedirs('assets/diagrams', exist_ok=True)

def get_font(size, bold=False):
    # Try common Windows TrueType fonts, fallback to default
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
    ]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default()
    except Exception:
        return None

# Palette
OXFORD_BLUE = (0, 33, 71)
DARK_NAVY = (15, 23, 42)
LIGHT_BG = (248, 250, 252)
ACCENT_BLUE = (2, 132, 199)
ACCENT_CYAN = (6, 182, 212)
ACCENT_PURPLE = (124, 58, 237)
ACCENT_EMERALD = (16, 185, 129)
ACCENT_AMBER = (245, 158, 11)
ACCENT_ROSE = (244, 63, 94)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
BORDER_COLOR = (203, 213, 225)
TEXT_DARK = (30, 41, 59)
TEXT_MUTED = (100, 116, 139)

# -----------------------------------------------------------------------------
# 1. Academic Crest / Seal for Title Page
# -----------------------------------------------------------------------------
def make_crest():
    img = Image.new("RGBA", (800, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    cx, cy = 400, 150
    r = 110

    # Outer gold ring
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=OXFORD_BLUE, outline=GOLD, width=6)
    d.ellipse((cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10), outline=GOLD, width=2)

    # Academic Shield
    shield_pts = [
        (cx - 55, cy - 50),
        (cx + 55, cy - 50),
        (cx + 55, cy + 15),
        (cx, cy + 65),
        (cx - 55, cy + 15),
    ]
    d.polygon(shield_pts, fill=(10, 45, 95), outline=GOLD, width=3)

    # Symbols inside shield: Open Book + Robotic Gear + Spark
    # Open Book
    d.rectangle((cx - 32, cy - 35, cx - 4, cy - 10), fill=WHITE, outline=GOLD, width=2)
    d.rectangle((cx + 4, cy - 35, cx + 32, cy - 10), fill=WHITE, outline=GOLD, width=2)
    # Lines on book
    d.line((cx - 28, cy - 28, cx - 8, cy - 28), fill=OXFORD_BLUE, width=2)
    d.line((cx - 28, cy - 22, cx - 8, cy - 22), fill=OXFORD_BLUE, width=2)
    d.line((cx - 28, cy - 16, cx - 8, cy - 16), fill=OXFORD_BLUE, width=2)
    d.line((cx + 8, cy - 28, cx + 28, cy - 28), fill=OXFORD_BLUE, width=2)
    d.line((cx + 8, cy - 22, cx + 28, cy - 22), fill=OXFORD_BLUE, width=2)
    d.line((cx + 8, cy - 16, cx + 28, cy - 16), fill=OXFORD_BLUE, width=2)

    # Compass / Gear symbol
    d.ellipse((cx - 16, cy + 5, cx + 16, cy + 37), fill=GOLD, outline=WHITE, width=2)
    d.ellipse((cx - 7, cy + 14, cx + 7, cy + 28), fill=(10, 45, 95))

    # Text Banner below
    f_latin = get_font(18, bold=True)
    f_sub = get_font(13, bold=False)
    d.text((cx, 285), "SAPIENTIA PER SYNTHESIM", fill=GOLD, font=f_latin, anchor="mm")
    d.text((cx, 305), "OXFORD ARTIFICIAL INTELLIGENCE GUILD", fill=TEXT_MUTED, font=f_sub, anchor="mm")

    img.save("assets/diagrams/diagram_cover_crest.png")
    print("Generated: diagram_cover_crest.png")

# -----------------------------------------------------------------------------
# 2. Character Profile Cards (Meet the Agent Clan)
# -----------------------------------------------------------------------------
def make_characters_card():
    w, h = 1000, 480
    img = Image.new("RGBA", (w, h), LIGHT_BG)
    d = ImageDraw.Draw(img)

    # Title
    f_title = get_font(26, bold=True)
    f_sub = get_font(14, bold=False)
    d.text((500, 35), "MEET THE AGENT CLAN: THE 5 SUPERHEROES OF AGENTFLOW", fill=OXFORD_BLUE, font=f_title, anchor="mm")
    d.text((500, 65), "Every great system is run by specialized teammates who collaborate like clockwork!", fill=TEXT_MUTED, font=f_sub, anchor="mm")

    cards = [
        {
            "name": "PERCY",
            "title": "The Master Detective (Planner)",
            "color": ACCENT_BLUE,
            "badge": "PLANNER",
            "icon": "MAP & DAG",
            "desc": "Breaks big impossible goals into small, easy step-by-step recipes called a DAG (Directed Acyclic Graph). Never gets dizzy in circles!",
            "superpower": "Superpower: X-Ray Goal Decomposition",
        },
        {
            "name": "EDDIE",
            "title": "The Master Builder (Executor)",
            "color": ACCENT_PURPLE,
            "badge": "EXECUTOR",
            "icon": "REACT LOOP",
            "desc": "Follows Percy's recipe step-by-step. Uses the ReAct loop: THINKS about the goal, ACTS by using tools, and OBSERVES the real results!",
            "superpower": "Superpower: Hands-on Tool Execution",
        },
        {
            "name": "CLARA",
            "title": "The Inspector Owl (Critic)",
            "color": ACCENT_AMBER,
            "badge": "CRITIC",
            "icon": "OWL OF TRUTH",
            "desc": "Checks Eddie's work with a magnifying glass. Spots tricky hallucinations, scores answers from 0-100, and triggers self-correction when needed!",
            "superpower": "Superpower: Zero Hallucination Shield",
        },
        {
            "name": "TOBY",
            "title": "The Toolmaster (MCP Registry)",
            "color": ACCENT_EMERALD,
            "badge": "MCP REGISTRY",
            "icon": "POWER PLUG",
            "desc": "Hands out certified tools (Calculators, Vector RAG, Databases) with safe standard Lego-like power plugs. Enforces safety and timeouts!",
            "superpower": "Superpower: Universal Tool Interlock",
        },
        {
            "name": "VECTOR",
            "title": "The Compass Fox (RAG Engine)",
            "color": ACCENT_CYAN,
            "badge": "VECTOR RAG",
            "icon": "128-D COMPASS",
            "desc": "Turns ordinary words into secret star coordinates in 128 dimensions! Uses Cosine Similarity to find matching treasure in microseconds!",
            "superpower": "Superpower: Exact Mathematical Cosine",
        },
    ]

    card_w = 180
    card_h = 360
    start_x = 20
    gap = 15

    f_cname = get_font(18, bold=True)
    f_badge = get_font(10, bold=True)
    f_ctitle = get_font(11, bold=True)
    f_cdesc = get_font(11, bold=False)
    f_super = get_font(10, bold=True)

    for i, c in enumerate(cards):
        cx = start_x + i * (card_w + gap)
        cy = 95

        # Card container
        d.rounded_rectangle((cx, cy, cx + card_w, cy + card_h), radius=12, fill=WHITE, outline=BORDER_COLOR, width=2)
        
        # Header banner
        d.rounded_rectangle((cx, cy, cx + card_w, cy + 65), radius=12, fill=c["color"])
        d.rectangle((cx, cy + 50, cx + card_w, cy + 65), fill=c["color"]) # square bottom

        # Badge
        d.rounded_rectangle((cx + 10, cy + 8, cx + card_w - 10, cy + 24), radius=6, fill=(255, 255, 255, 60))
        d.text((cx + card_w // 2, cy + 16), c["badge"], fill=WHITE, font=f_badge, anchor="mm")
        d.text((cx + card_w // 2, cy + 45), c["name"], fill=WHITE, font=f_cname, anchor="mm")

        # Icon circle
        ic_y = cy + 95
        d.ellipse((cx + card_w//2 - 25, ic_y - 25, cx + card_w//2 + 25, ic_y + 25), fill=LIGHT_BG, outline=c["color"], width=2)
        d.text((cx + card_w // 2, ic_y), c["icon"][:5], fill=c["color"], font=f_badge, anchor="mm")

        # Title
        d.text((cx + 12, cy + 130), c["title"], fill=TEXT_DARK, font=f_ctitle)

        # Description text wrapping
        words = c["desc"].split()
        lines = []
        cur = ""
        for wrd in words:
            if len(cur + " " + wrd) < 22:
                cur += (" " if cur else "") + wrd
            else:
                lines.append(cur)
                cur = wrd
        if cur:
            lines.append(cur)

        y_txt = cy + 165
        for l in lines[:7]:
            d.text((cx + 12, y_txt), l, fill=TEXT_MUTED, font=f_cdesc)
            y_txt += 17

        # Superpower box at bottom
        d.rounded_rectangle((cx + 8, cy + card_h - 45, cx + card_w - 8, cy + card_h - 10), radius=6, fill=(240, 245, 250), outline=c["color"], width=1)
        d.text((cx + card_w // 2, cy + card_h - 28), c["superpower"], fill=c["color"], font=f_super, anchor="mm")

    img.save("assets/diagrams/diagram_cast_characters.png")
    print("Generated: diagram_cast_characters.png")

# -----------------------------------------------------------------------------
# 3. ReAct Flowchart (Thought -> Action -> Observation Loop)
# -----------------------------------------------------------------------------
def make_react_flowchart():
    w, h = 900, 420
    img = Image.new("RGBA", (w, h), WHITE)
    d = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(13, bold=False)
    f_box_h = get_font(15, bold=True)
    f_box_p = get_font(11, bold=False)
    f_arrow = get_font(13, bold=True)

    d.text((450, 30), "THE REACT CYCLE: THOUGHT ➔ ACTION ➔ OBSERVATION", fill=OXFORD_BLUE, font=f_title, anchor="mm")
    d.text((450, 58), "How Eddie the Executor thinks like a scientist to solve problems without guessing!", fill=TEXT_MUTED, font=f_sub, anchor="mm")

    # Step 1: User Goal
    d.rounded_rectangle((40, 110, 190, 260), radius=12, fill=(240, 249, 255), outline=ACCENT_BLUE, width=3)
    d.text((115, 135), "1. GOAL / CONTEXT", fill=ACCENT_BLUE, font=f_box_h, anchor="mm")
    d.text((115, 175), "User asks:\n'Calculate cost for\n1M prompt tokens & \nexplain RAG.'", fill=TEXT_DARK, font=f_box_p, anchor="mm")
    d.text((115, 235), "Input Trigger", fill=TEXT_MUTED, font=get_font(10, True), anchor="mm")

    # Arrow 1 -> 2
    d.line((190, 185, 240, 185), fill=BORDER_COLOR, width=4)
    d.polygon([(240, 185), (230, 178), (230, 192)], fill=BORDER_COLOR)

    # Step 2: Thought (Purple)
    d.rounded_rectangle((240, 110, 420, 260), radius=12, fill=(250, 245, 255), outline=ACCENT_PURPLE, width=3)
    d.text((330, 135), "2. THOUGHT (Reasoning)", fill=ACCENT_PURPLE, font=f_box_h, anchor="mm")
    d.text((330, 180), "Eddie reflects:\n'I need exact rates.\nLet me look up the\npricing DB first,\nnot invent numbers!'", fill=TEXT_DARK, font=f_box_p, anchor="mm")
    d.text((330, 235), "Prevents Hallucination", fill=ACCENT_PURPLE, font=get_font(10, True), anchor="mm")

    # Arrow 2 -> 3
    d.line((420, 185, 470, 185), fill=BORDER_COLOR, width=4)
    d.polygon([(470, 185), (460, 178), (460, 192)], fill=BORDER_COLOR)

    # Step 3: Action (Blue)
    d.rounded_rectangle((470, 110, 650, 260), radius=12, fill=(240, 253, 250), outline=ACCENT_EMERALD, width=3)
    d.text((560, 135), "3. ACTION (MCP Tool)", fill=ACCENT_EMERALD, font=f_box_h, anchor="mm")
    d.text((560, 180), "Dispatches JSON call:\ndatabase_lookup({\n  table: 'pricing',\n  model: 'gemini'\n})", fill=TEXT_DARK, font=f_box_p, anchor="mm")
    d.text((560, 235), "Bounded & Sandboxed", fill=ACCENT_EMERALD, font=get_font(10, True), anchor="mm")

    # Arrow 3 -> 4
    d.line((650, 185, 700, 185), fill=BORDER_COLOR, width=4)
    d.polygon([(700, 185), (690, 178), (690, 192)], fill=BORDER_COLOR)

    # Step 4: Observation (Cyan)
    d.rounded_rectangle((700, 110, 870, 260), radius=12, fill=(255, 251, 235), outline=ACCENT_AMBER, width=3)
    d.text((785, 135), "4. OBSERVATION", fill=ACCENT_AMBER, font=f_box_h, anchor="mm")
    d.text((785, 180), "Real World Answer:\nInput: $3.50 / 1M\nOutput: $10.50 / 1M\nLat: 850ms", fill=TEXT_DARK, font=f_box_p, anchor="mm")
    d.text((785, 235), "Grounded Truth", fill=ACCENT_AMBER, font=get_font(10, True), anchor="mm")

    # Bottom Loop Arrow: Observation feeds back to Thought!
    d.line((785, 260, 785, 330), fill=ACCENT_PURPLE, width=3)
    d.line((785, 330, 330, 330), fill=ACCENT_PURPLE, width=3)
    d.line((330, 330, 330, 260), fill=ACCENT_PURPLE, width=3)
    d.polygon([(330, 260), (324, 270), (336, 270)], fill=ACCENT_PURPLE)

    d.text((560, 345), "FEEDBACK LOOP: Real facts feed into the NEXT Thought until Goal is Fully Solved!", fill=ACCENT_PURPLE, font=f_arrow, anchor="mm")

    img.save("assets/diagrams/diagram_react_flowchart.png")
    print("Generated: diagram_react_flowchart.png")

# -----------------------------------------------------------------------------
# 4. DAG (Directed Acyclic Graph) Treasure Map
# -----------------------------------------------------------------------------
def make_dag_map():
    w, h = 900, 380
    img = Image.new("RGBA", (w, h), WHITE)
    d = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_node = get_font(13, bold=True)
    f_txt = get_font(10, bold=False)

    d.text((450, 25), "DIRECTED ACYCLIC GRAPH (DAG): PERCY'S RECIPE MAP", fill=OXFORD_BLUE, font=f_title, anchor="mm")
    d.text((450, 50), "Every step points forward to the treasure. No circular loops allowed!", fill=TEXT_MUTED, font=f_sub, anchor="mm")

    # Side A: The Right Way (Acyclic DAG)
    d.rounded_rectangle((30, 80, 480, 350), radius=10, fill=(248, 250, 252), outline=ACCENT_EMERALD, width=2)
    d.text((255, 105), "✅ VALID DAG: Clean Forward Progress", fill=ACCENT_EMERALD, font=get_font(15, True), anchor="mm")

    # Node 1
    d.rounded_rectangle((50, 150, 180, 210), radius=8, fill=WHITE, outline=ACCENT_BLUE, width=2)
    d.text((115, 170), "Step 1: RAG Search", fill=ACCENT_BLUE, font=f_node, anchor="mm")
    d.text((115, 190), "Gathers knowledge", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    # Node 2
    d.rounded_rectangle((230, 130, 350, 190), radius=8, fill=WHITE, outline=ACCENT_PURPLE, width=2)
    d.text((290, 150), "Step 2: DB Lookup", fill=ACCENT_PURPLE, font=f_node, anchor="mm")
    d.text((290, 170), "Gets exact rates", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    # Node 3
    d.rounded_rectangle((230, 215, 350, 275), radius=8, fill=WHITE, outline=ACCENT_AMBER, width=2)
    d.text((290, 235), "Step 3: Host Metrics", fill=ACCENT_AMBER, font=f_node, anchor="mm")
    d.text((290, 255), "Checks memory", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    # Node 4 (Finish)
    d.rounded_rectangle((380, 170, 460, 235), radius=8, fill=(240, 253, 250), outline=ACCENT_EMERALD, width=2)
    d.text((420, 195), "Step 4: Math", fill=ACCENT_EMERALD, font=f_node, anchor="mm")
    d.text((420, 215), "Final cost sum", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    # Arrows for Valid DAG
    d.line((180, 175, 230, 160), fill=BORDER_COLOR, width=3)
    d.polygon([(230, 160), (220, 156), (223, 166)], fill=BORDER_COLOR)

    d.line((180, 185, 230, 235), fill=BORDER_COLOR, width=3)
    d.polygon([(230, 235), (223, 228), (220, 238)], fill=BORDER_COLOR)

    d.line((350, 160, 380, 195), fill=BORDER_COLOR, width=3)
    d.polygon([(380, 195), (372, 187), (370, 198)], fill=BORDER_COLOR)

    d.line((350, 245, 380, 210), fill=BORDER_COLOR, width=3)
    d.polygon([(380, 210), (370, 207), (372, 218)], fill=BORDER_COLOR)

    d.text((255, 315), "Progress is monotonic: Step N depends only on Step < N", fill=TEXT_DARK, font=f_txt, anchor="mm")

    # Side B: The Danger Zone (Cyclic Dependency - The Infinite Loop of Doom)
    d.rounded_rectangle((510, 80, 870, 350), radius=10, fill=(255, 245, 245), outline=ACCENT_ROSE, width=2)
    d.text((690, 105), "❌ CYCLIC ERROR: The Spinning Vortex!", fill=ACCENT_ROSE, font=get_font(15, True), anchor="mm")

    d.rounded_rectangle((540, 165, 660, 225), radius=8, fill=WHITE, outline=ACCENT_ROSE, width=2)
    d.text((600, 185), "Step A: Wait for B", fill=TEXT_DARK, font=f_node, anchor="mm")
    d.text((600, 205), "'Need B's answer!'", fill=ACCENT_ROSE, font=f_txt, anchor="mm")

    d.rounded_rectangle((720, 165, 840, 225), radius=8, fill=WHITE, outline=ACCENT_ROSE, width=2)
    d.text((780, 185), "Step B: Wait for A", fill=TEXT_DARK, font=f_node, anchor="mm")
    d.text((780, 205), "'Need A's answer!'", fill=ACCENT_ROSE, font=f_txt, anchor="mm")

    # Circular arrows
    d.line((660, 180, 720, 180), fill=ACCENT_ROSE, width=3)
    d.polygon([(720, 180), (710, 174), (710, 186)], fill=ACCENT_ROSE)

    d.line((780, 225, 780, 270), fill=ACCENT_ROSE, width=3)
    d.line((780, 270, 600, 270), fill=ACCENT_ROSE, width=3)
    d.line((600, 270, 600, 225), fill=ACCENT_ROSE, width=3)
    d.polygon([(600, 225), (594, 235), (606, 235)], fill=ACCENT_ROSE)

    d.text((690, 295), "DEADLOCK! Both wait forever! Never happens in AgentFlow", fill=ACCENT_ROSE, font=get_font(11, True), anchor="mm")
    d.text((690, 320), "because Percy enforces monotonic IDs step_1 < step_2", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    img.save("assets/diagrams/diagram_dag_map.png")
    print("Generated: diagram_dag_map.png")

# -----------------------------------------------------------------------------
# 5. MCP Universal Lego Power Plug
# -----------------------------------------------------------------------------
def make_mcp_sockets():
    w, h = 900, 360
    img = Image.new("RGBA", (w, h), WHITE)
    d = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_bold = get_font(14, bold=True)
    f_txt = get_font(11, bold=False)

    d.text((450, 25), "MODEL CONTEXT PROTOCOL (MCP): UNIVERSAL POWER PLUGS", fill=OXFORD_BLUE, font=f_title, anchor="mm")
    d.text((450, 50), "Standard sockets mean any AI Agent can plug into any tool in the world!", fill=TEXT_MUTED, font=f_sub, anchor="mm")

    # Agent side (Left Plug)
    d.rounded_rectangle((50, 90, 320, 300), radius=12, fill=(240, 245, 255), outline=ACCENT_BLUE, width=3)
    d.text((185, 120), "AGENT HOST (LLM)", fill=ACCENT_BLUE, font=f_bold, anchor="mm")
    d.text((185, 150), "• Issues tool calls\n• Sends JSON payload\n• Expects structured result", fill=TEXT_DARK, font=f_txt, anchor="mm")
    
    # 3 Socket Pins protruding to the right
    for py in [195, 235, 275]:
        d.rounded_rectangle((310, py - 10, 350, py + 10), radius=4, fill=GOLD, outline=OXFORD_BLUE, width=2)

    # Middle Interlock (The MCP Contract)
    d.rounded_rectangle((360, 90, 540, 300), radius=12, fill=(255, 251, 235), outline=GOLD, width=3)
    d.text((450, 120), "MCP PROTOCOL", fill=GOLD, font=f_bold, anchor="mm")
    d.text((450, 160), "1. Tool Discovery\n   (listTools)\n2. JSON Schema Pin\n   (Type Validation)\n3. Timeout Guard\n   (8,000ms sandbox)", fill=TEXT_DARK, font=f_txt, anchor="mm")
    d.text((450, 260), "NO SPYING & NO LEAKS", fill=ACCENT_EMERALD, font=get_font(10, True), anchor="mm")

    # Receiving Sockets on Tool side
    for py in [195, 235, 275]:
        d.rounded_rectangle((550, py - 12, 590, py + 12), radius=4, fill=(240, 240, 240), outline=ACCENT_EMERALD, width=2)
        d.line((550, py, 590, py), fill=ACCENT_EMERALD, width=3)

    # Tool side (Right Socket)
    d.rounded_rectangle((580, 90, 850, 300), radius=12, fill=(240, 253, 250), outline=ACCENT_EMERALD, width=3)
    d.text((715, 120), "MCP TOOL REGISTRY", fill=ACCENT_EMERALD, font=f_bold, anchor="mm")
    d.text((715, 160), "• calculator\n• vector_knowledge_search\n• database_lookup\n• system_metrics", fill=TEXT_DARK, font=f_txt, anchor="mm")
    d.text((715, 245), "Executes real code securely\nin a protected sandbox!", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    img.save("assets/diagrams/diagram_mcp_lego_plug.png")
    print("Generated: diagram_mcp_lego_plug.png")

# -----------------------------------------------------------------------------
# 6. Cosine Similarity Angle Compass
# -----------------------------------------------------------------------------
def make_cosine_compass():
    w, h = 900, 420
    img = Image.new("RGBA", (w, h), WHITE)
    d = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_bold = get_font(13, bold=True)
    f_math = get_font(14, bold=True)
    f_txt = get_font(11, bold=False)

    d.text((450, 25), "THE ANGLE COMPASS: HOW COSINE SIMILARITY FINDS SECRETS", fill=OXFORD_BLUE, font=f_title, anchor="mm")
    d.text((450, 50), "Vector the Fox doesn't read words—he measures the angle between treasure coordinates!", fill=TEXT_MUTED, font=f_sub, anchor="mm")

    # Case 1: Angle = 0 deg (Identical Meaning, Cos = 1.0)
    d.rounded_rectangle((30, 90, 290, 380), radius=12, fill=(240, 253, 250), outline=ACCENT_EMERALD, width=3)
    d.text((160, 115), "MATCH: cos(0°) = 1.0", fill=ACCENT_EMERALD, font=f_bold, anchor="mm")
    
    # Coordinate axis
    d.line((70, 240, 250, 240), fill=BORDER_COLOR, width=2)
    d.line((80, 250, 80, 140), fill=BORDER_COLOR, width=2)
    # Vectors u and v overlapping
    d.line((80, 240, 220, 160), fill=ACCENT_BLUE, width=4) # u
    d.line((80, 240, 240, 150), fill=ACCENT_EMERALD, width=3) # v
    d.text((230, 145), "u (query)", fill=ACCENT_BLUE, font=f_txt)
    d.text((250, 160), "v (doc)", fill=ACCENT_EMERALD, font=f_txt)
    d.text((160, 260), "Angle θ ≈ 0° (Twin Stars)", fill=ACCENT_EMERALD, font=f_bold, anchor="mm")
    d.text((160, 295), "'multi-agent' ➔ 'agentic system'\nExact same conceptual direction!\nCosine score: 0.95 to 1.0", fill=TEXT_DARK, font=f_txt, anchor="mm")

    # Case 2: Angle = 90 deg (Unrelated, Cos = 0.0)
    d.rounded_rectangle((310, 90, 580, 380), radius=12, fill=(248, 250, 252), outline=ACCENT_BLUE, width=3)
    d.text((445, 115), "ORTHOGONAL: cos(90°) = 0.0", fill=ACCENT_BLUE, font=f_bold, anchor="mm")
    
    # Coordinate axis
    d.line((350, 240, 530, 240), fill=BORDER_COLOR, width=2)
    d.line((370, 250, 370, 140), fill=BORDER_COLOR, width=2)
    # Vectors at right angle
    d.line((370, 240, 510, 240), fill=ACCENT_BLUE, width=4) # horizontal u
    d.line((370, 240, 370, 150), fill=ACCENT_PURPLE, width=4) # vertical v
    # Right angle marker
    d.rectangle((370, 225, 385, 240), outline=TEXT_MUTED, width=1)
    d.text((515, 245), "u", fill=ACCENT_BLUE, font=f_txt)
    d.text((375, 145), "v", fill=ACCENT_PURPLE, font=f_txt)
    d.text((445, 260), "Angle θ = 90° (Strangers)", fill=ACCENT_BLUE, font=f_bold, anchor="mm")
    d.text((445, 295), "'quantum physics' ➔ 'apple pie'\nCompletely unrelated topics!\nCosine score: 0.00", fill=TEXT_DARK, font=f_txt, anchor="mm")

    # Case 3: The Magic Trick: L2 Unit Normalization (Dot Product Speed!)
    d.rounded_rectangle((600, 90, 870, 380), radius=12, fill=(255, 251, 235), outline=GOLD, width=3)
    d.text((735, 115), "THE MAGIC TRICK: L2 NORM", fill=GOLD, font=f_bold, anchor="mm")
    
    # Formula box
    d.rounded_rectangle((620, 145, 850, 235), radius=8, fill=WHITE, outline=BORDER_COLOR, width=1)
    d.text((735, 165), "General Cosine Formula:", fill=TEXT_MUTED, font=f_txt, anchor="mm")
    d.text((735, 185), "cos(θ) = (u · v) / (||u|| * ||v||)", fill=OXFORD_BLUE, font=f_math, anchor="mm")
    d.text((735, 210), "When ||u|| = 1.0 and ||v|| = 1.0:", fill=ACCENT_EMERALD, font=get_font(10, True), anchor="mm")
    d.text((735, 225), "cos(θ) = u · v = Σ (u_i * v_i)", fill=ACCENT_PURPLE, font=f_math, anchor="mm")

    d.text((735, 260), "Why this matters to a 10yo:", fill=TEXT_DARK, font=get_font(11, True), anchor="mm")
    d.text((735, 300), "No scary square roots at search time!\nJust multiply and add.\nComputers can do this 10,000,000\ntimes a second in RAM!", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    img.save("assets/diagrams/diagram_cosine_compass.png")
    print("Generated: diagram_cosine_compass.png")

# -----------------------------------------------------------------------------
# 7. SSE vs WebSockets (The Radio vs Phone Call)
# -----------------------------------------------------------------------------
def make_sse_radio():
    w, h = 900, 360
    img = Image.new("RGBA", (w, h), WHITE)
    d = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_bold = get_font(14, bold=True)
    f_txt = get_font(11, bold=False)

    d.text((450, 25), "SERVER-SENT EVENTS (SSE) vs WEBSOCKETS", fill=OXFORD_BLUE, font=f_title, anchor="mm")
    d.text((450, 50), "Why a one-way live radio ticker is 10x better than an expensive two-way phone call for AI!", fill=TEXT_MUTED, font=f_sub, anchor="mm")

    # Side A: SSE (The Radio Morse Ticker)
    d.rounded_rectangle((30, 85, 430, 330), radius=12, fill=(240, 253, 250), outline=ACCENT_EMERALD, width=3)
    d.text((230, 115), "SERVER-SENT EVENTS (SSE)", fill=ACCENT_EMERALD, font=f_bold, anchor="mm")
    d.text((230, 138), "📻 The Live Morse Radio Station", fill=TEXT_DARK, font=get_font(12, True), anchor="mm")

    # Graphic representation: Server emitting waves to Client
    d.rounded_rectangle((50, 165, 130, 225), radius=8, fill=WHITE, outline=ACCENT_EMERALD, width=2)
    d.text((90, 195), "Agent\nServer", fill=ACCENT_EMERALD, font=f_txt, anchor="mm")

    # Stream of waves
    for i, wx in enumerate([160, 200, 240, 280]):
        d.line((wx, 175, wx + 20, 195), fill=ACCENT_EMERALD, width=3)
        d.line((wx + 20, 195, wx, 215), fill=ACCENT_EMERALD, width=3)

    d.rounded_rectangle((330, 165, 410, 225), radius=8, fill=WHITE, outline=ACCENT_BLUE, width=2)
    d.text((370, 195), "User\nBrowser", fill=ACCENT_BLUE, font=f_txt, anchor="mm")

    d.text((230, 250), "• One-way stream over standard HTTP/1.1 or HTTP/2\n• Free automatic reconnection if WiFi hiccups!\n• Traverses all firewalls and corporate proxies easily", fill=TEXT_DARK, font=f_txt, anchor="mm")
    d.text((230, 305), "Winner for AI Token & Trace Telemetry!", fill=ACCENT_EMERALD, font=get_font(11, True), anchor="mm")

    # Side B: WebSockets (The Heavy 2-Way Phone Call)
    d.rounded_rectangle((470, 85, 870, 330), radius=12, fill=(255, 245, 245), outline=ACCENT_AMBER, width=2)
    d.text((670, 115), "WEBSOCKETS (WS)", fill=ACCENT_AMBER, font=f_bold, anchor="mm")
    d.text((670, 138), "☎️ The Two-Way Walkie-Talkie", fill=TEXT_DARK, font=get_font(12, True), anchor="mm")

    d.rounded_rectangle((490, 165, 570, 225), radius=8, fill=WHITE, outline=ACCENT_AMBER, width=2)
    d.text((530, 195), "Server", fill=ACCENT_AMBER, font=f_txt, anchor="mm")

    # Bidirectional arrows
    d.line((585, 185, 755, 185), fill=ACCENT_AMBER, width=3)
    d.polygon([(755, 185), (745, 180), (745, 190)], fill=ACCENT_AMBER)
    d.line((755, 205, 585, 205), fill=ACCENT_AMBER, width=3)
    d.polygon([(585, 205), (595, 200), (595, 210)], fill=ACCENT_AMBER)

    d.rounded_rectangle((770, 165, 850, 225), radius=8, fill=WHITE, outline=TEXT_MUTED, width=2)
    d.text((810, 195), "Client", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    d.text((670, 250), "• Requires stateful custom protocol upgrade\n• Firewalls often block or drop idle sockets\n• Overkill when client only listens to token streams!", fill=TEXT_MUTED, font=f_txt, anchor="mm")
    d.text((670, 305), "Great for multiplayer games, unnecessary for AI streams", fill=TEXT_MUTED, font=get_font(11, False), anchor="mm")

    img.save("assets/diagrams/diagram_sse_radio.png")
    print("Generated: diagram_sse_radio.png")

# -----------------------------------------------------------------------------
# 8. Tokenomics Piggy Bank & KV-Cache
# -----------------------------------------------------------------------------
def make_token_bank():
    w, h = 900, 360
    img = Image.new("RGBA", (w, h), WHITE)
    d = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_bold = get_font(13, bold=True)
    f_txt = get_font(11, bold=False)

    d.text((450, 25), "TOKEN ECONOMICS: THE MAGIC PIGGY BANK & KV-CACHE", fill=OXFORD_BLUE, font=f_title, anchor="mm")
    d.text((450, 50), "How smart architects save 80% on cloud AI bills by reusing memory prefixes!", fill=TEXT_MUTED, font=f_sub, anchor="mm")

    # Prompt Tokens
    d.rounded_rectangle((30, 90, 290, 320), radius=12, fill=(240, 245, 255), outline=ACCENT_BLUE, width=3)
    d.text((160, 120), "1. PROMPT TOKENS", fill=ACCENT_BLUE, font=f_bold, anchor="mm")
    d.text((160, 150), "The Question Words\n(~3.8 chars per subword token)", fill=TEXT_DARK, font=f_txt, anchor="mm")
    d.rounded_rectangle((50, 185, 270, 245), radius=8, fill=WHITE, outline=BORDER_COLOR, width=1)
    d.text((160, 215), "1,000,000 Tokens\nStandard Price: $3.50 / 1M", fill=OXFORD_BLUE, font=get_font(12, True), anchor="mm")
    d.text((160, 280), "Every prompt sends system rules\n+ tools + your question", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    # KV-Cache Hits (The Magic Piggy Bank)
    d.rounded_rectangle((310, 90, 580, 320), radius=12, fill=(240, 253, 250), outline=ACCENT_EMERALD, width=3)
    d.text((445, 120), "2. KV-CACHE DISCOUNT", fill=ACCENT_EMERALD, font=f_bold, anchor="mm")
    d.text((445, 150), "The 'Already Read' Memory\n(50% to 80% Discount!)", fill=ACCENT_EMERALD, font=f_txt, anchor="mm")
    d.rounded_rectangle((330, 185, 560, 245), radius=8, fill=WHITE, outline=ACCENT_EMERALD, width=2)
    d.text((445, 215), "500,000 Cached Tokens\nCached Price: $1.75 / 1M!", fill=ACCENT_EMERALD, font=get_font(12, True), anchor="mm")
    d.text((445, 280), "Golden Rule: Always put STATIC\nrules at the very TOP of prompt!", fill=TEXT_DARK, font=get_font(11, True), anchor="mm")

    # Output Completion Tokens
    d.rounded_rectangle((600, 90, 870, 320), radius=12, fill=(255, 251, 235), outline=ACCENT_AMBER, width=3)
    d.text((735, 120), "3. COMPLETION TOKENS", fill=ACCENT_AMBER, font=f_bold, anchor="mm")
    d.text((735, 150), "The Answer Words\n(Costs 3x more to write!)", fill=TEXT_DARK, font=f_txt, anchor="mm")
    d.rounded_rectangle((620, 185, 850, 245), radius=8, fill=WHITE, outline=BORDER_COLOR, width=1)
    d.text((735, 215), "50,000 Answer Tokens\nStandard Price: $10.50 / 1M", fill=OXFORD_BLUE, font=get_font(12, True), anchor="mm")
    d.text((735, 280), "Keep agent answers concise\nand grounded in facts!", fill=TEXT_MUTED, font=f_txt, anchor="mm")

    img.save("assets/diagrams/diagram_token_bank.png")
    print("Generated: diagram_token_bank.png")

if __name__ == "__main__":
    make_crest()
    make_characters_card()
    make_react_flowchart()
    make_dag_map()
    make_mcp_sockets()
    make_cosine_compass()
    make_sse_radio()
    make_token_bank()
    print("All 8 publication diagrams successfully generated!")
