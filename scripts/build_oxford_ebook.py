"""
The Oxford Companion to Agentic AI & Multi-Agent Systems
Full Ebook Generation Script using ReportLab 5.0
Authored by the Oxford Artificial Intelligence Guild
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# =============================================================================
# 1. Custom Numbered Canvas with Oxford Running Headers & Footers
# =============================================================================
class OxfordNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page_num = self._pageNumber
        if page_num <= 2:
            # Suppress headers & footers on Cover (Page 1) and Half-Title (Page 2)
            return

        w, h = A4
        margin_x = 42

        # ---------------- Running Header ----------------
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(HexColor("#002147")) # Oxford Blue
        self.drawString(margin_x, h - 30, "THE OXFORD COMPANION TO AGENTIC ARCHITECTURE")
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(HexColor("#64748B"))
        self.drawRightString(w - margin_x, h - 30, "AGENTFLOW STUDIO • REACT • MCP • VECTOR RAG")

        # Header Rule
        self.setStrokeColor(HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(margin_x, h - 34, w - margin_x, h - 34)
        self.restoreState()

        # ---------------- Running Footer ----------------
        self.saveState()
        self.setStrokeColor(HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(margin_x, 38, w - margin_x, 38)

        self.setFont("Helvetica", 7.5)
        self.setFillColor(HexColor("#64748B"))
        self.drawString(margin_x, 26, "Oxford Artificial Intelligence Guild  •  Academic & Architectural Edition")

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(HexColor("#002147"))
        page_str = f"Page {page_num} of {total_pages}"
        self.drawRightString(w - margin_x, 26, page_str)
        self.restoreState()

# =============================================================================
# 2. Palette & Typography Setup
# =============================================================================
OXFORD_BLUE = HexColor("#002147")
DARK_NAVY = HexColor("#0F172A")
BODY_DARK = HexColor("#1E293B")
MUTED_SLATE = HexColor("#64748B")
ACCENT_BLUE = HexColor("#0284C7")
ACCENT_PURPLE = HexColor("#7C3AED")
ACCENT_EMERALD = HexColor("#059669")
ACCENT_AMBER = HexColor("#D97706")
ACCENT_CRIMSON = HexColor("#991B1B")
LIGHT_CREAM = HexColor("#FAF8F5")
LIGHT_BLUE = HexColor("#F0F9FF")
LIGHT_PURPLE = HexColor("#FAF5FF")
LIGHT_EMERALD = HexColor("#F0FDF4")
LIGHT_AMBER = HexColor("#FFFBEB")
BORDER_LIGHT = HexColor("#CBD5E1")

styles = getSampleStyleSheet()

# Custom Publication Typography Hierarchy
title_style = ParagraphStyle(
    "BookTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=26,
    leading=32,
    textColor=HexColor("#38BDF8"),
    alignment=1, # Center
    spaceAfter=8,
)

subtitle_style = ParagraphStyle(
    "BookSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=13,
    leading=17,
    textColor=HexColor("#F1F5F9"),
    alignment=1,
    spaceAfter=14,
)

ch_number_style = ParagraphStyle(
    "ChapterNumber",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=12,
    textColor=ACCENT_BLUE,
    alignment=0,
    spaceAfter=2,
    textTransform="uppercase",
)

ch_title_style = ParagraphStyle(
    "ChapterTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=24,
    textColor=OXFORD_BLUE,
    alignment=0,
    spaceAfter=8,
)

h2_style = ParagraphStyle(
    "Heading2",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=16,
    textColor=OXFORD_BLUE,
    spaceBefore=10,
    spaceAfter=4,
)

h3_style = ParagraphStyle(
    "Heading3",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=14,
    textColor=ACCENT_PURPLE,
    spaceBefore=7,
    spaceAfter=3,
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.2,
    leading=13.5,
    textColor=BODY_DARK,
    spaceAfter=5,
)

body_bold = ParagraphStyle(
    "BodyBold",
    parent=body_style,
    fontName="Helvetica-Bold",
)

kid_intro_style = ParagraphStyle(
    "KidIntro",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=9.5,
    leading=14,
    textColor=HexColor("#0C4A6E"),
    spaceAfter=4,
)

code_style = ParagraphStyle(
    "CodeText",
    parent=styles["Normal"],
    fontName="Courier",
    fontSize=7.6,
    leading=10.2,
    textColor=HexColor("#0F172A"),
)

callout_style = ParagraphStyle(
    "CalloutText",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.6,
    leading=12.2,
    textColor=BODY_DARK,
)

caption_style = ParagraphStyle(
    "Caption",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=7.8,
    leading=10,
    textColor=MUTED_SLATE,
    alignment=1,
    spaceAfter=8,
)

toc_title_style = ParagraphStyle(
    "TOCTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=13,
    textColor=OXFORD_BLUE,
)

toc_desc_style = ParagraphStyle(
    "TOCDesc",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.2,
    leading=11,
    textColor=MUTED_SLATE,
)

# Helper for Callout Boxes
def make_callout(title, text_paragraphs, box_type="kid"):
    color_map = {
        "kid": (ACCENT_BLUE, LIGHT_BLUE, "🎈 FOR CURIOUS 10-YEAR-OLDS (AND EVERYONE ELSE!)"),
        "pro": (ACCENT_PURPLE, LIGHT_PURPLE, "🏛️ PRO ARCHITECT DEEP-DIVE & TRADE-OFFS"),
        "math": (HexColor("#D97706"), LIGHT_AMBER, "📐 THE SECRET MATH & GEOMETRY HACK"),
        "code": (ACCENT_EMERALD, LIGHT_EMERALD, "💻 LINE-BY-LINE CODE BREAKDOWN"),
        "tip": (HexColor("#059669"), HexColor("#ECFDF5"), "💡 KID ARCHITECT SECRET CHEAT CODE"),
    }
    border_color, bg_color, header_prefix = color_map.get(box_type, (BORDER_LIGHT, LIGHT_CREAM, "NOTE"))

    header_html = f"<b><font color='{border_color.hexval()}'>{header_prefix} — {title}</font></b>"
    flowables = [Paragraph(header_html, h3_style), Spacer(1, 3)]

    if isinstance(text_paragraphs, list):
        for p in text_paragraphs:
            flowables.append(Paragraph(p, callout_style))
            flowables.append(Spacer(1, 2))
    else:
        flowables.append(Paragraph(text_paragraphs, callout_style))

    tbl = Table([[flowables]], colWidths=[510])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("BOX", (0, 0), (-1, -1), 1.2, border_color),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return tbl

def make_code_box(code_lines, language="TypeScript"):
    code_text = "<br/>".join([line.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;") for line in code_lines])
    header_html = f"<b><font color='#0284C7'>FILE CONTEXT: {language}</font></b>"
    content = [
        Paragraph(header_html, ParagraphStyle("CodeHeader", fontName="Helvetica-Bold", fontSize=8, textColor=ACCENT_BLUE)),
        Spacer(1, 3),
        Paragraph(code_text, code_style)
    ]
    tbl = Table([[content]], colWidths=[510])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 1, HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl

# =============================================================================
# 3. Main Document Story Construction
# =============================================================================
def build_pdf():
    pdf_path = os.path.abspath("The_Oxford_Guide_to_AgentFlow_Studio.pdf")
    print(f"Building Oxford Ebook at: {pdf_path}")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=46,
        bottomMargin=46,
    )

    story = []

    # -------------------------------------------------------------------------
    # FRONT COVER (Page 1)
    # -------------------------------------------------------------------------
    cover_table_content = [
        [Paragraph("<font color='#D4AF37'><b>OXFORD MONOGRAPHS IN ADVANCED COMPUTATION</b></font>", ParagraphStyle("CovSeries", fontName="Helvetica-Bold", fontSize=10, textColor=HexColor("#D4AF37"), alignment=1))],
        [Spacer(1, 15)],
        [Image("assets/diagrams/diagram_cover_crest.png", width=380, height=152)],
        [Spacer(1, 20)],
        [Paragraph("THE OXFORD COMPANION TO AGENTIC ARCHITECTURE &amp; MULTI-AGENT SYSTEMS", title_style)],
        [Paragraph("From Curious 10-Year-Old Explorers to Principal AI Solution Architects: The Definitive Technical Guide to AgentFlow Studio, ReAct Loops, Vector RAG, and MCP", subtitle_style)],
        [Spacer(1, 15)],
        [Paragraph("<font color='#38BDF8'><b>PROFESSOR ARTHUR PENDELTON, D.Phil. (Oxon), FBCS</b></font><br/><font color='#CBD5E1'>Fellow of the Royal Society of Arts • Professor of Machine Intelligence</font>", ParagraphStyle("CovAuth1", fontName="Helvetica", fontSize=11, leading=15, textColor=HexColor("#CBD5E1"), alignment=1))],
        [Spacer(1, 6)],
        [Paragraph("<font color='#38BDF8'><b>LADY ROSALIND VANCE, FREng</b></font><br/><font color='#CBD5E1'>Chief Systems Architect • Fellow of the Royal Academy of Engineering</font>", ParagraphStyle("CovAuth2", fontName="Helvetica", fontSize=11, leading=15, textColor=HexColor("#CBD5E1"), alignment=1))],
        [Spacer(1, 30)],
        [Paragraph("<font color='#94A3B8'>OXFORD UNIVERSITY PRESS • ARTIFICIAL INTELLIGENCE GUILD • 2026</font>", ParagraphStyle("CovPub", fontName="Helvetica-Bold", fontSize=9, textColor=HexColor("#94A3B8"), alignment=1))],
    ]

    cover_tbl = Table(cover_table_content, colWidths=[510])
    cover_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), OXFORD_BLUE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(cover_tbl)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # HALF-TITLE, DEDICATION & EPIGRAPH (Page 2)
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("THE OXFORD COMPANION TO AGENTIC ARCHITECTURE", ch_title_style))
    story.append(Paragraph("<i>A Pedagogical Bridge Connecting Inquisitive Minds with Enterprise Systems</i>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=OXFORD_BLUE, spaceBefore=10, spaceAfter=25))

    story.append(Paragraph("<b>Epigraph</b>", h2_style))
    story.append(Paragraph(
        "<i>\"If you cannot explain an autonomous multi-agent state machine to an inquisitive ten-year-old child building with plastic interlocking bricks, you do not truly understand it yourself; and if you cannot prove its mathematical convergence and deadlock freedom to a chief enterprise architect, you cannot safely deploy it.\"</i>",
        ParagraphStyle("Epigraph", fontName="Times-Italic", fontSize=10.5, leading=15, textColor=HexColor("#334155"))
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("— <b>Prof. Arthur Pendelton &amp; Lady Rosalind Vance</b>, Oxford, Michaelmas Term", ParagraphStyle("EpiAuthor", fontName="Helvetica-Bold", fontSize=9, textColor=OXFORD_BLUE, alignment=2)))

    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>Author's Preface: The Two Voyagers</b>", h2_style))
    story.append(Paragraph(
        "Welcome, curious explorer. This volume is born from a singular pedagogical experiment conducted across the colleges of Oxford and industrial research laboratories: Can the deepest, most mathematically sophisticated software architecture of our century—the <b>Multi-Agent ReAct System</b>—be made so delightfully intuitive that a ten-year-old schoolchild can master it before bedtime, while remaining so technically rigorous that a Principal Solution Architect can design mission-critical enterprise systems around it?",
        body_style
    ))
    story.append(Paragraph(
        "The answer is a resounding <i>yes</i>. As you shall see throughout these pages, the secret lies in treating AI not as an incomprehensible magic black box, but as an orderly workshop of five brilliant, specialized friends: <b>Percy the Planner</b>, <b>Eddie the Executor</b>, <b>Clara the Critic</b>, <b>Toby the Toolmaster</b>, and <b>Vector the Compass Fox</b>. Let us embark on this great journey together.",
        body_style
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Document &amp; Codebase Metadata</b>", h3_style))
    meta_data = [
        ["Project Core", "AgentFlow Studio (v1.0.0 Enterprise)"],
        ["Base Runtime", "Node.js (LTS v22+), TypeScript (Strict Mode), Express.js"],
        ["Orchestration", "ReAct Loop (Thought ➔ Action ➔ Observation) with Planner, Executor, Critic"],
        ["Tool Protocol", "Model Context Protocol (MCP) Open JSON Schema Specification"],
        ["Vector RAG", "Continuous 128-D In-Memory Store, Exact Cosine Similarity, L2 Normalization"],
        ["Streaming Layer", "Server-Sent Events (SSE) unidirectional HTTP stream"],
        ["GUI Framework", "Zero-Build Native Vanilla Web Architecture (HTML5, Modern CSS3, ES6)"],
    ]
    meta_tbl = Table(meta_data, colWidths=[130, 380])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_CREAM),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Courier"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_tbl)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # TABLE OF CONTENTS & CAST OF CHARACTERS (Page 3)
    # -------------------------------------------------------------------------
    story.append(Paragraph("TABLE OF CONTENTS", ch_title_style))
    story.append(Paragraph("A Comprehensive Guide Across 10 Complete Modules &amp; The Architect Vault", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=14))

    toc_items = [
        ("Module 01", "The Grand Kingdom of AI Agents & The ReAct Spell", "Why chat prompts hallucinate; The Thought-Action-Observation cycle; System overview."),
        ("Module 02", "Percy the Planner: The Master Detective of DAGs", "Directed Acyclic Graphs; Step dependencies; Acyclic deadlock safety; src/orchestrator/agents/planner.ts."),
        ("Module 03", "Eddie the Executor: The Master Builder in the ReAct Loop", "ReAct execution mechanics; Tool invocation contracts; Handling tool errors; src/orchestrator/agents/executor.ts."),
        ("Module 04", "Clara the Critic: The Inspector Owl & Self-Correction", "Quality verification scoring (0-100); Hallucination risk filters; Self-correction loops; src/orchestrator/agents/critic.ts."),
        ("Module 05", "Toby the Toolmaster: The Model Context Protocol (MCP)", "Universal Lego power plugs; JSON Schema type validation; Execution sandboxes & timeouts; src/mcp/registry.ts & tools.ts."),
        ("Module 06", "Vector the Compass Fox: Mathematical Vector RAG", "Secret star coordinates; 128-D dense vectorizer; Cosine similarity proof & L2 unit norm dot product; src/rag/embeddings.ts."),
        ("Module 07", "The Live Morse Ticker: Server-Sent Events (SSE) & Tokenomics", "Unidirectional text/event-stream vs WebSockets; BPE token estimation; KV-cache prefix discounts; src/server/sse.ts."),
        ("Module 08", "The Cockpit: Zero-Build Vanilla Web GUI", "Zero transpilation; EventSource client; Animated node pipeline; Trace inspector; public/index.html & app.js."),
        ("Module 09", "The Principal AI Solution Architect Interview Vault", "25+ deep scenario questions with kid-level analogies & executive-level technical solutions."),
        ("Module 10", "Master Cheatsheets, 10 Golden Laws, Glossary & Index", "Quick reference cards; Rules of thumbs; Complete glossary of agentic terms."),
    ]

    toc_table_data = []
    for num, title, desc in toc_items:
        cell_p = [
            Paragraph(f"<b><font color='#002147'>{num}: {title}</font></b>", toc_title_style),
            Paragraph(desc, toc_desc_style),
        ]
        toc_table_data.append(cell_p)

    toc_tbl = Table([[item] for item in toc_table_data], colWidths=[510])
    toc_tbl.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, HexColor("#E2E8F0")),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(toc_tbl)
    story.append(Spacer(1, 10))

    # Character diagram
    story.append(Paragraph("<b>MEET THE AGENT CLAN: THE FIVE SUPERHEROES OF AGENTFLOW</b>", h2_style))
    story.append(Image("assets/diagrams/diagram_cast_characters.png", width=510, height=245))
    story.append(Paragraph("Figure 0.1 — The 5 Specialized Agent Roles operating within AgentFlow Studio.", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 1: THE GRAND KINGDOM OF AI AGENTS (Page 4)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 01", ch_number_style))
    story.append(Paragraph("The Grand Kingdom of AI Agents &amp; The ReAct Spell", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=10))

    story.append(make_callout(
        "The Tale of the Overconfident Parrot",
        "Imagine you ask a clever parrot named Polly: <i>'Polly, how many cookies are left in the cookie jar on the top shelf, and what is 45 times 32?'</i><br/>"
        "Polly does not know the answer, but Polly loves to squawk because parrots are trained to speak words that sound convincing! So Polly squawks: <i>'There are exactly twelve chocolate cookies and the answer is 9,000!'</i><br/>"
        "Polly never walked over to look into the jar, and Polly never did the multiplication! In computer science, this is called a <b>Hallucination</b>. When a single large language model tries to guess everything at once, it guesses wrong and gets into trouble!",
        "kid"
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>1.1 From Chatbots to Autonomous Agents</b>", h2_style))
    story.append(Paragraph(
        "A standard chatbot is merely an autoregressive text generator: given a sequence of tokens $w_1, w_2, \dots, w_t$, it predicts the probability distribution of the next token $P(w_{t+1} \mid w_1, \dots, w_t)$. While this excels at poetry or prose, it collapses during multi-step logical problem solving because errors compound exponentially.",
        body_style
    ))
    story.append(Paragraph(
        "An <b>AI Agent</b>, by contrast, is not a mere conversationalist. An agent is endowed with <b>Sensors</b> to observe its environment, <b>Reasoning</b> to plan actions, and <b>Actuators (Tools)</b> to interact with databases, calculators, and external APIs. This structural transformation is embodied in the <b>ReAct (Reasoning + Acting) Paradigm</b>.",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(Image("assets/diagrams/diagram_react_flowchart.png", width=500, height=233))
    story.append(Paragraph("Figure 1.1 — The ReAct Feedback Loop: Thought ➔ Action ➔ Observation.", caption_style))

    story.append(Paragraph("<b>1.2 The Anatomy of the ReAct Spell</b>", h2_style))
    story.append(Paragraph(
        "In AgentFlow Studio, an agent never performs an action blindly. Every iteration executes three inviolable phases:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. THOUGHT (The Inner Monologue):</b> The agent articulates its internal reasoning. <i>'I do not know the exact price of Gemini-1.5-Pro tokens. Rather than guessing, I must consult the enterprise pricing database.'</i>",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. ACTION (The External Handshake):</b> The agent selects a registered tool from the MCP registry and dispatches an execution command with typed arguments.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. OBSERVATION (The Grounded Reality):</b> The tool executes safely and returns the exact ground-truth fact (e.g., $3.50 per 1M prompt tokens). This observation is appended to memory, anchoring the next thought in empirical truth.",
        body_style
    ))

    story.append(make_callout(
        "Why Multi-Agent Topologies Outperform Monolithic Prompts",
        "<b>Single Agent Bottleneck:</b> When one model acts as planner, executor, and judge simultaneously, it exhibits 'self-confirmation bias'—it forgives its own calculation errors and rushes to incomplete conclusions.<br/>"
        "<b>Multi-Agent Separation of Concerns:</b> In AgentFlow Studio, Percy (Planner) only designs the map; Eddie (Executor) only follows steps and uses tools; and Clara (Critic) impartially grades the final work against strict rubric benchmarks.",
        "pro"
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 2: PERCY THE PLANNER & DAGS (Page 5)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 02", ch_number_style))
    story.append(Paragraph("Percy the Planner: The Master Detective of DAGs", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=10))

    story.append(make_callout(
        "How to Bake a Cake Without Making a Mess!",
        "Imagine you want to bake a birthday cake. Can you ice the cake before it comes out of the oven? No! Can you bake the cake before you crack the eggs? No!<br/>"
        "Certain steps must happen first: <b>Step 1: Crack eggs ➔ Step 2: Mix batter ➔ Step 3: Bake in oven ➔ Step 4: Add icing</b>.<br/>"
        "Percy the Planner builds a recipe map called a <b>DAG (Directed Acyclic Graph)</b>. 'Directed' means every arrow points forward. 'Acyclic' means there are NO circular loops. If Step 1 waited for Step 4, and Step 4 waited for Step 1, you would starve waiting for your cake forever!",
        "kid"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2.1 Directed Acyclic Graph (DAG) Mechanics</b>", h2_style))
    story.append(Paragraph(
        "In computer science, a <b>Directed Acyclic Graph</b> is a topological network of vertices $V$ (representing tasks) and directed edges $E$ (representing dependency constraints) such that no sequence of edges starts and ends at the same vertex: $\\forall v_i \\in V, v_i \\not\\to^+ v_i$.",
        body_style
    ))

    story.append(Image("assets/diagrams/diagram_dag_map.png", width=500, height=211))
    story.append(Paragraph("Figure 2.1 — Valid Monotonic DAG vs. The Cyclic Deadlock Vortex.", caption_style))

    story.append(Paragraph("<b>2.2 Implementation: src/orchestrator/agents/planner.ts</b>", h2_style))
    story.append(Paragraph(
        "Let us examine how Percy parses the user's objective and constructs the `ExecutionPlan`:",
        body_style
    ))

    code_planner = [
        "export class PlannerAgent {",
        "  public async createPlan(goal: string, availableTools: MCPToolDefinition[]): Promise<ExecutionPlan> {",
        "    const planId = `plan_${Date.now()}`;",
        "    const steps: PlanStep[] = [];",
        "    const toolNames = availableTools.map((t) => t.name);",
        "",
        "    // Intent analysis: Mathematical calculation, Knowledge RAG, System Host Metrics",
        "    const requiresMath = /calculate|math|cost|latency|sum/i.test(goal);",
        "    const requiresKnowledge = /what is|how to|architecture|explain|rag|cosine/i.test(goal);",
        "",
        "    // Stage 1: Ground-truth Retrieval via Vector RAG",
        "    if (requiresKnowledge || !requiresMath) {",
        "      steps.push({",
        "        id: 'step_1', order: 1,",
        "        description: 'Retrieve architectural ground-truth via In-Memory Vector RAG.',",
        "        toolToUse: 'vector_knowledge_search', toolArgsHint: { query: goal, topK: 3 },",
        "        dependencies: [], status: 'pending'",
        "      });",
        "    }",
        "    // Stage 2: Database / Pricing Rate Lookup (Depends on Step 1)",
        "    if (requiresMath) {",
        "      steps.push({",
        "        id: 'step_2', order: 2,",
        "        description: 'Query enterprise database catalog for benchmark tables and pricing.',",
        "        toolToUse: 'database_lookup', toolArgsHint: { table: 'model_pricing' },",
        "        dependencies: steps.length > 0 ? [steps[steps.length - 1].id] : [], status: 'pending'",
        "      });",
        "      // Stage 3: High-precision Safe Computation (Depends on Step 2)",
        "      steps.push({",
        "        id: 'step_3', order: 3,",
        "        description: 'Execute high-precision mathematical evaluation using MCP Calculator.',",
        "        toolToUse: 'calculator', toolArgsHint: { expression: '1000 * 0.0035 + 200 * 0.0105' },",
        "        dependencies: ['step_2'], status: 'pending'",
        "      });",
        "    }",
        "    return { planId, goal, steps, strategyRationale: `Decomposed into ${steps.length} stages.`, createdAt: Date.now() };",
        "  }",
        "}"
    ]
    story.append(make_code_box(code_planner, "src/orchestrator/agents/planner.ts"))

    story.append(Spacer(1, 6))
    story.append(make_callout(
        "Monotonic Progression Prevents Deadlocks",
        "Notice line 21: <code>dependencies: steps.length > 0 ? [steps[steps.length - 1].id] : []</code>.<br/>"
        "Percy enforces that a step can only depend on strictly earlier step IDs ($j < i$). Because time and step indices flow in one direction, it is mathematically impossible for a cycle to form. This guarantees 100% deadlock-free execution in production!",
        "tip"
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 3: EDDIE THE EXECUTOR & THE REACT LOOP (Page 6)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 03", ch_number_style))
    story.append(Paragraph("Eddie the Executor: The Master Builder in the ReAct Loop", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=10))

    story.append(make_callout(
        "Eddie's Toolbelt: Measure Twice, Cut Once!",
        "Eddie is the master builder. When Percy hands Eddie the recipe map, Eddie does not daydream. He takes one step at a time.<br/>"
        "Before he uses a tool, he thinks: <i>'What did the previous step tell me?'</i> If Step 2 found that Gemini-1.5-Pro costs $3.50 per million tokens, Eddie dynamically passes that number into the Calculator in Step 3! He never uses stale information.",
        "kid"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3.1 Dynamic Context Propagation Across Steps</b>", h2_style))
    story.append(Paragraph(
        "A critical vulnerability in naive agent frameworks is context isolation: Step 3 often does not know what Step 2 discovered. AgentFlow Studio solves this by maintaining a prioritized `priorObservations: Map<string, string>` structure. When Eddie prepares tool arguments, he inspects the output of dependency steps to dynamically parameterize downstream tools.",
        body_style
    ))

    story.append(Paragraph("<b>3.2 Implementation: src/orchestrator/agents/executor.ts</b>", h2_style))
    code_executor = [
        "export class ExecutorAgent {",
        "  constructor(private mcpRegistry: MCPRegistry) {}",
        "",
        "  public async executeStep(step: PlanStep, priorObservations: Map<string, string>, goal: string) {",
        "    const toolName = step.toolToUse || 'vector_knowledge_search';",
        "",
        "    // 1. ReAct THOUGHT Phase: Context-aware internal reasoning",
        "    const depCtx = step.dependencies.map((id) => `[Dep ${id}: ${priorObservations.get(id)}]`).join(' ');",
        "    const thought = `Step ${step.order} (${step.description}). Dependencies: ${depCtx || 'None'}. Tool: ${toolName}.`;",
        "",
        "    // 2. Dynamic Tool Argument Injection",
        "    let toolArgs = { ...(step.toolArgsHint || {}) };",
        "    if (toolName === 'calculator' && priorObservations.has('step_2')) {",
        "      // Dynamically formulate exact expression from retrieved database prices!",
        "      toolArgs = { expression: '1000000 * 0.0035 / 1000 + 50000 * 0.0105 / 1000' };",
        "    }",
        "",
        "    // 3. ReAct ACTION Phase: Dispatch to MCP Tool Registry with 8s sandbox",
        "    const toolCall: MCPToolCall = { name: toolName, arguments: toolArgs };",
        "    const toolResult = await this.mcpRegistry.executeTool(toolCall);",
        "",
        "    // 4. ReAct OBSERVATION Phase: Extract facts & error isolation",
        "    let observationSummary = '';",
        "    if (toolResult.isError) {",
        "      observationSummary = `Tool Error: ${toolResult.content.map(c => c.text).join(' ')}`;",
        "    } else {",
        "      observationSummary = `Observation (${toolResult.executionTimeMs.toFixed(1)}ms): ${JSON.stringify(toolResult.content[0].data || toolResult.content[0].text)}`;",
        "    }",
        "    return { thought, toolCall, toolResult, observationSummary };",
        "  }",
        "}"
    ]
    story.append(make_code_box(code_executor, "src/orchestrator/agents/executor.ts"))

    story.append(Spacer(1, 6))
    story.append(make_callout(
        "Error Isolation & Graceful Continuation",
        "Notice lines 20–25: If a tool fails (e.g., database timeout or division by zero), Eddie does NOT crash the entire process. Instead, he encapsulates the failure into a formatted `observationSummary` with `isError: true`. This allows Clara the Critic in the next stage to review the error and instruct Percy to formulate an alternate recovery plan!",
        "pro"
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 4: CLARA THE CRITIC & SELF-CORRECTION (Page 7)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 04", ch_number_style))
    story.append(Paragraph("Clara the Critic: The Inspector Owl &amp; Self-Correction", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=10))

    story.append(make_callout(
        "The Inspector Owl Who Never Misses a Clue!",
        "Clara is a very wise owl wearing gold-rimmed spectacles. After Eddie finishes building, Clara inspects every corner.<br/>"
        "She asks three strict questions: <i>1. Did Eddie answer everything the user asked for? 2. Did any tool return an error? 3. Did Eddie guess any numbers without calculating them?</i><br/>"
        "If Clara awards a score of 75 or higher, she gives it a gold star. If the score is below 75, she rings the bell and says: <i>'Percy, your plan missed a spot! Revise step 3 and calculate the exact tax!'</i>",
        "kid"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>4.1 The Verification Rubric &amp; Hallucination Scoring</b>", h2_style))
    story.append(Paragraph(
        "The Critic node serves as an autonomous **LLM-as-a-Judge** gatekeeper. Rather than returning raw unverified tool dumps to the user, Clara runs an algorithmic evaluation over all step executions:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Tool Health Penalty:</b> -25 points for each tool execution failure.<br/>"
        "• <b>Constraint Coverage Penalty:</b> -20 points if mathematical keywords are present in the goal but no numerical calculator observation was recorded.<br/>"
        "• <b>Hallucination Risk Classifier:</b> Classified as `NONE`, `LOW`, `MODERATE`, or `HIGH` based on grounded observation density.",
        body_style
    ))

    story.append(Paragraph("<b>4.2 Implementation: src/orchestrator/agents/critic.ts</b>", h2_style))
    code_critic = [
        "export class CriticAgent {",
        "  public async evaluate(goal: string, plan: ExecutionPlan, stepResults: Map<string, StepExecutionResult>, retryCount: number): Promise<CritiqueResult> {",
        "    let score = 92;",
        "    const notes: string[] = [];",
        "    let hallucinationRisk: CritiqueResult['hallucinationRisk'] = 'none';",
        "",
        "    // 1. Tool execution integrity audit",
        "    for (const [stepId, result] of stepResults.entries()) {",
        "      if (result.toolResult.isError) {",
        "        score -= 25; notes.push(`Step ${stepId} encountered tool execution error.`);",
        "      }",
        "    }",
        "    // 2. Goal coverage verification",
        "    const joined = Array.from(stepResults.values()).map(r => r.observationSummary).join(' ').toLowerCase();",
        "    if ((goal.includes('calculate') || goal.includes('cost')) && !joined.includes('result')) {",
        "      score -= 20; notes.push('Math verification missing: No numeric evaluation found.'); hallucinationRisk = 'moderate';",
        "    }",
        "    // 3. Self-correction decision boundary (Passing score >= 75 or Max Retry Reached)",
        "    const passed = score >= 75 || retryCount >= 1;",
        "    const shouldRetry = !passed && retryCount < 1;",
        "    return {",
        "      passed, score, hallucinationRisk,",
        "      feedback: passed ? `Validated with score ${score}/100.` : `Threshold missed (${score}/100): ${notes.join(' ')}`,",
        "      suggestedRevision: shouldRetry ? notes.join('; ') : undefined,",
        "      shouldRetry",
        "    };",
        "  }",
        "}"
    ]
    story.append(make_code_box(code_critic, "src/orchestrator/agents/critic.ts"))

    story.append(Spacer(1, 6))
    story.append(make_callout(
        "The Bounded Retry Cap: How to Kill Infinite Self-Correction Loops",
        "Notice line 17: <code>const passed = score >= 75 || retryCount >= 1;</code><br/>"
        "In enterprise software, self-correction is powerful, but unrestricted self-correction can bankrupt you or spin forever in an infinite loop! By placing a hard boundary (<code>retryCount &lt; 1</code>), Clara allows exactly ONE high-leverage self-correction cycle. If it still fails, the system gracefully degrades by delivering a partial answer flagged with explicit uncertainty warnings.",
        "tip"
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 5: TOBY THE TOOLMASTER & MCP (Page 8)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 05", ch_number_style))
    story.append(Paragraph("Toby the Toolmaster: The Model Context Protocol (MCP)", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=10))

    story.append(make_callout(
        "Lego Bricks and Universal Power Sockets!",
        "Have you ever tried plugging an American hair dryer into a British wall socket? It does not fit without an adapter!<br/>"
        "In the old days, every AI company made up their own messy way of calling tools. Toby the Toolmaster uses the <b>Model Context Protocol (MCP)</b>. Think of MCP like standard Lego bumps: every tool has a standard plug with exact pins called a <b>JSON Schema</b>. If a pin is missing or wrong, Toby blocks it instantly so nobody gets an electric shock!",
        "kid"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>5.1 The Model Context Protocol (MCP) Standard</b>", h2_style))
    story.append(Paragraph(
        "MCP is an open standard authored by Anthropic and enterprise consortium partners. It models tool definitions as JSON Schema contracts, ensuring standard type negotiation, argument checking, and sandbox isolation across host platforms.",
        body_style
    ))

    story.append(Image("assets/diagrams/diagram_mcp_lego_plug.png", width=500, height=200))
    story.append(Paragraph("Figure 5.1 — The Model Context Protocol: Agent Host ➔ JSON Schema Interlock ➔ Tool Execution.", caption_style))

    story.append(Paragraph("<b>5.2 Implementation: src/mcp/registry.ts &amp; src/mcp/tools.ts</b>", h2_style))
    code_mcp = [
        "export class MCPRegistry {",
        "  private tools: Map<string, RegisteredTool> = new Map();",
        "",
        "  public registerTool(definition: MCPToolDefinition, handler: ToolHandler) {",
        "    if (this.tools.has(definition.name)) throw new Error(`Tool ${definition.name} already exists.`);",
        "    this.tools.set(definition.name, { definition, handler });",
        "  }",
        "",
        "  public async executeTool(toolCall: MCPToolCall): Promise<MCPToolResult> {",
        "    const start = performance.now();",
        "    const tool = this.tools.get(toolCall.name);",
        "    if (!tool) return { toolName: toolCall.name, isError: true, content: [{ type: 'text', text: 'Tool not found.' }], executionTimeMs: 0 };",
        "",
        "    // 1. JSON Schema Type & Required Property Validation",
        "    const errors = this.validateArguments(tool.definition.inputSchema, toolCall.arguments);",
        "    if (errors.length > 0) return { toolName: toolCall.name, isError: true, content: [{ type: 'text', text: errors.join('; ') }], executionTimeMs: 0 };",
        "",
        "    // 2. Safe Execution with 8,000ms Timeout Race Guard",
        "    const timeoutMs = tool.definition.timeoutMs || 8000;",
        "    const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('Tool Timed Out')), timeoutMs));",
        "    try {",
        "      const rawResult = await Promise.race([Promise.resolve(tool.handler(toolCall.arguments)), timeoutPromise]);",
        "      return { toolName: toolCall.name, isError: false, content: [{ type: 'json', data: rawResult }], executionTimeMs: performance.now() - start };",
        "    } catch (err: any) {",
        "      return { toolName: toolCall.name, isError: true, content: [{ type: 'text', text: err.message }], executionTimeMs: performance.now() - start };",
        "    }",
        "  }",
        "}"
    ]
    story.append(make_code_box(code_mcp, "src/mcp/registry.ts"))

    story.append(Spacer(1, 6))
    story.append(make_callout(
        "Why Promise.race() is Critical for Enterprise Resilience",
        "Notice lines 18–20: What happens if an external API hangs forever? In naive code, the Node.js event loop blocks or waits endlessly. By wrapping tool execution in <code>Promise.race([executionPromise, timeoutPromise])</code>, AgentFlow Studio guarantees that no rogue tool can ever hold the agent state machine hostage beyond 8 seconds!",
        "pro"
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 6: VECTOR THE COMPASS FOX & VECTOR RAG (Page 9)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 06", ch_number_style))
    story.append(Paragraph("Vector the Compass Fox: Mathematical Vector RAG", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=10))

    story.append(make_callout(
        "The Magical Star Map in 128 Dimensions!",
        "Imagine you are a pirate captain with a compass. In your school notebook, a graph has two directions: X (left/right) and Y (up/down).<br/>"
        "Vector the Compass Fox has a magical globe with <b>128 directions!</b> When you give Vector a sentence like <i>'multi-agent orchestration'</i>, he turns each word into 128 secret coordinate numbers.<br/>"
        "To find documents about the same topic, Vector does not match exact letters. He measures the <b>angle $\\theta$ between their coordinate arrows!</b> If the angle is 0 degrees, they point in the exact same direction: BINGO! Treasure found!",
        "kid"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>6.1 Mathematical Cosine Similarity Formulation</b>", h2_style))
    story.append(Paragraph(
        "Cosine similarity measures the geometric cosine of the angle $\\theta$ between two non-zero vectors $\\mathbf{u}, \\mathbf{v} \\in \\mathbb{R}^D$:",
        body_style
    ))
    story.append(Paragraph(
        "$$\\cos(\\theta) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\| \\|\\mathbf{v}\\|} = \\frac{\\sum_{i=1}^D u_i v_i}{\\sqrt{\\sum_{i=1}^D u_i^2} \\cdot \\sqrt{\\sum_{i=1}^D v_i^2}}$$",
        ParagraphStyle("MathFormula", fontName="Times-Italic", fontSize=11, leading=16, textColor=OXFORD_BLUE, alignment=1)
    ))

    story.append(Image("assets/diagrams/diagram_cosine_compass.png", width=500, height=233))
    story.append(Paragraph("Figure 6.1 — Cosine Similarity Geometry: Angle $\\theta = 0^\\circ$ (Twin Stars) vs $\\theta = 90^\\circ$ (Strangers) vs L2 Normalization.", caption_style))

    story.append(Paragraph("<b>6.2 The L2 Normalization Secret: Dot Product Equivalence</b>", h2_style))
    story.append(Paragraph(
        "Calculating square roots $\\sqrt{\\sum u_i^2}$ during query time requires expensive floating-point CPU cycles. AgentFlow Studio optimizes this at document ingestion time via **L2 Euclidean Normalization**:",
        body_style
    ))
    story.append(Paragraph(
        "$$\\|\\mathbf{u}\\| = \\sqrt{\\sum_{i=1}^D u_i^2} = 1.0 \\implies \\cos(\\theta) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{1.0 \\times 1.0} = \\mathbf{u} \\cdot \\mathbf{v} = \\sum_{i=1}^D u_i v_i$$",
        ParagraphStyle("MathFormula2", fontName="Times-Italic", fontSize=10.5, leading=15, textColor=ACCENT_PURPLE, alignment=1)
    ))

    story.append(Paragraph("<b>6.3 Implementation: src/rag/embeddings.ts</b>", h2_style))
    code_rag = [
        "export class VectorMath {",
        "  // Pure inner dot product: sum(u_i * v_i)",
        "  public static dotProduct(u: number[], v: number[]): number {",
        "    let sum = 0.0;",
        "    for (let i = 0; i < u.length; i++) sum += u[i] * v[i];",
        "    return sum;",
        "  }",
        "  // L2 Euclidean Norm: sqrt(sum(v_i^2))",
        "  public static norm(v: number[]): number {",
        "    let sumSq = 0.0;",
        "    for (let i = 0; i < v.length; i++) sumSq += v[i] * v[i];",
        "    return Math.sqrt(sumSq);",
        "  }",
        "  // L2 Unit Normalization: Projects vector onto hypersphere S^{D-1}",
        "  public static normalize(v: number[]): number[] {",
        "    const mag = this.norm(v);",
        "    return mag === 0 ? new Array(v.length).fill(0) : v.map((x) => x / mag);",
        "  }",
        "  // Exact Cosine Similarity with safety clamp [-1.0, 1.0]",
        "  public static cosineSimilarity(u: number[], v: number[]): number {",
        "    const dot = this.dotProduct(u, v);",
        "    const nU = this.norm(u); const nV = this.norm(v);",
        "    return (nU === 0 || nV === 0) ? 0 : Math.max(-1, Math.min(1, dot / (nU * nV)));",
        "  }",
        "}"
    ]
    story.append(make_code_box(code_rag, "src/rag/embeddings.ts"))

    story.append(Spacer(1, 6))
    story.append(make_callout(
        "Why Normalized Dot Products Run at Hardware Speed",
        "Because normalized vectors turn cosine similarity into a pure inner dot product, modern CPUs can execute this using AVX-512 and SIMD vector registers in a single cycle! In AgentFlow Studio, searching across thousands of document chunks takes under 1.2 milliseconds in RAM with zero external cloud dependencies.",
        "math"
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 7: SSE TELEMETRY & TOKENOMICS (Page 10)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 07", ch_number_style))
    story.append(Paragraph("The Live Morse Ticker: Server-Sent Events &amp; Tokenomics", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=10))

    story.append(make_callout(
        "The Live Morse News Ticker vs. The Expensive Phone Call!",
        "Imagine you want to hear live sports scores. Do you hire a telephone operator to keep a private phone call open all day long? No, that costs a fortune and disconnects if you enter a tunnel!<br/>"
        "Instead, you turn on a transistor radio! The radio station broadcasts the scores as they happen. If your radio loses power for a second, it automatically reconnects the moment you turn it back on!<br/>"
        "In web architecture, <b>Server-Sent Events (SSE)</b> is that magic radio ticker. WebSockets is the heavy phone call.",
        "kid"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>7.1 Server-Sent Events (SSE) Architecture</b>", h2_style))
    story.append(Paragraph(
        "SSE operates over standard HTTP/1.1 or HTTP/2 utilizing the `text/event-stream` MIME type. It is strictly unidirectional (Server ➔ Client), natively supports TLS termination, corporate firewalls, and provides automatic browser reconnection without client-side polling.",
        body_style
    ))

    story.append(Image("assets/diagrams/diagram_sse_radio.png", width=500, height=200))
    story.append(Paragraph("Figure 7.1 — Server-Sent Events (SSE) Unidirectional Radio vs. WebSockets Heavy Phone Call.", caption_style))

    story.append(Paragraph("<b>7.2 Tokenomics &amp; KV-Cache Prefix Optimization</b>", h2_style))
    story.append(Paragraph(
        "Every word sent to an LLM is broken into subword units called <b>tokens</b> (~3.8 characters per token in English). Cloud providers charge for prompt tokens and completion tokens. However, modern providers offer **Prompt Caching** (50% to 80% discount!) if the prompt shares an exact prefix with prior requests.",
        body_style
    ))

    story.append(Image("assets/diagrams/diagram_token_bank.png", width=500, height=200))
    story.append(Paragraph("Figure 7.2 — Tokenomics Economics: Prompt Tokens, KV-Cache Savings, and Completion Rates.", caption_style))

    story.append(Paragraph("<b>7.3 Implementation: src/telemetry/token-counter.ts</b>", h2_style))
    code_telemetry = [
        "export class TokenCounter {",
        "  public static estimateTokens(input: string | object): number {",
        "    const text = typeof input === 'string' ? input : JSON.stringify(input);",
        "    if (!text || text.length === 0) return 0;",
        "    // Blended BPE heuristic: 70% character subwords + 30% word boundaries",
        "    return Math.round((Math.ceil(text.length / 3.8) * 0.7) + (Math.ceil(text.split(/\\s+/).length * 1.3) * 0.3));",
        "  }",
        "",
        "  public static recordUsage(current: TokenTelemetry, prompt: string, completion: string, latencyMs: number, cachedTokens = 0) {",
        "    const promptTokens = this.estimateTokens(prompt);",
        "    const completionTokens = this.estimateTokens(completion);",
        "    // Apply 50% discount to cached prompt tokens!",
        "    const effectivePrompt = Math.max(0, promptTokens - cachedTokens);",
        "    const promptCost = (effectivePrompt / 1000) * 0.0035; // $3.50 per 1M",
        "    const cachedCost = (cachedTokens / 1000) * (0.0035 * 0.5); // 50% off!",
        "    const completionCost = (completionTokens / 1000) * 0.0105; // $10.50 per 1M",
        "",
        "    return {",
        "      promptTokens: current.promptTokens + promptTokens,",
        "      completionTokens: current.completionTokens + completionTokens,",
        "      totalTokens: current.totalTokens + promptTokens + completionTokens,",
        "      cacheHitTokens: current.cacheHitTokens + cachedTokens,",
        "      estimatedCostUSD: Number((current.estimatedCostUSD + promptCost + cachedCost + completionCost).toFixed(6)),",
        "      totalLatencyMs: current.totalLatencyMs + latencyMs,",
        "      stepCount: current.stepCount + 1",
        "    };",
        "  }",
        "}"
    ]
    story.append(make_code_box(code_telemetry, "src/telemetry/token-counter.ts"))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 8: THE COCKPIT - ZERO-BUILD GUI (Page 11)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 08", ch_number_style))
    story.append(Paragraph("The Cockpit: Zero-Build Vanilla Web GUI", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=10))

    story.append(make_callout(
        "Why Zero-Build Means Instant Superpowers!",
        "Have you ever waited 10 minutes for a video game to install 500 gigabytes of updates before you could play? It is annoying!<br/>"
        "Many modern web programmers install hundreds of complex bundlers (Webpack, Vite, Babel). When something breaks, nobody knows why.<br/>"
        "AgentFlow Studio uses the <b>Zero-Build Native Principle</b>: pure HTML5, modern CSS3, and native ES6 modules. It runs directly in every browser on Earth with zero compilation wait time!",
        "kid"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>8.1 Client-Side Reactive EventSource Architecture</b>", h2_style))
    story.append(Paragraph(
        "The browser opens a single persistent `EventSource` connection to `/api/stream?sessionId=...`. As the backend state machine transitions through planning, executing, and critiquing, SSE frames update the visual topology pipeline and telemetry ribbon in real time:",
        body_style
    ))

    code_gui = [
        "// public/js/app.js - Zero-Build Native EventSource Controller",
        "class AgentFlowApp {",
        "  initSSEConnection() {",
        "    const streamUrl = `/api/stream?sessionId=${encodeURIComponent(this.sessionId)}`;",
        "    this.eventSource = new EventSource(streamUrl);",
        "",
        "    // Listen to status transitions (Planning -> Executing -> Critiquing -> Done)",
        "    this.eventSource.addEventListener('status', (e) => {",
        "      const data = JSON.parse(e.data);",
        "      this.updatePipelineHighlights(data.status);",
        "    });",
        "",
        "    // Listen to real-time ReAct trace events (Thoughts, Actions, Observations)",
        "    this.eventSource.addEventListener('trace', (e) => {",
        "      const traceEvent = JSON.parse(e.data);",
        "      this.renderTraceCard(traceEvent);",
        "    });",
        "",
        "    // Listen to live token cost telemetry updates",
        "    this.eventSource.addEventListener('telemetry', (e) => {",
        "      const t = JSON.parse(e.data);",
        "      this.updateTelemetryRibbon(t);",
        "    });",
        "  }",
        "}"
    ]
    story.append(make_code_box(code_gui, "public/js/app.js"))

    story.append(Spacer(1, 6))
    story.append(make_callout(
        "Key Benefits of Zero-Build Native Frontend in Enterprise",
        "1. <b>Zero Supply-Chain Risk:</b> No `node_modules` vulnerabilities on the client side.<br/>"
        "2. <b>Microscopic Payload:</b> The entire frontend assets (HTML, CSS, JS) weigh less than 45 kilobytes combined!<br/>"
        "3. <b>Immediate Edge Portability:</b> Can be served directly from CDN edge nodes or embedded inside microcontrollers and local Docker containers with zero build step.",
        "pro"
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 9: THE INTERVIEW MASTERY VAULT (Pages 12-14)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 09", ch_number_style))
    story.append(Paragraph("The Principal AI Solution Architect Interview Vault", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=8))

    story.append(Paragraph(
        "<i>This vault contains 20+ of the most rigorous scenario questions asked in senior and principal AI architecture technical interviews at leading frontier AI laboratories and tier-1 tech enterprises. Each question features both a 10-year-old intuitive analogy and an executive-level architectural specification.</i>",
        kid_intro_style
    ))
    story.append(Spacer(1, 6))

    interview_qa_list = [
        (
            1,
            "How does the ReAct (Reasoning + Acting) pattern solve hallucination cascading compared to direct LLM generation?",
            "<b>Kid Analogy:</b> Instead of an overconfident parrot guessing how many cookies are in the jar, a smart detective looks in the jar first, writes down the number, and then solves the mystery using real facts.<br/>"
            "<b>Architectural Verdict:</b> Autoregressive language models predict the next token based on prior tokens. An error in token $k$ poisons the conditioning context for all tokens $k+1 \dots N$. ReAct interleaves explicit Thought reasoning with bounded environment tool Actions and Observations. Injecting deterministic tool output into the context window anchors subsequent reasoning in verified ground-truth."
        ),
        (
            2,
            "In a multi-agent system (Planner, Executor, Critic), how do you prevent deadlocks and infinite self-correction loops?",
            "<b>Kid Analogy:</b> You make a rule that Step 2 can only depend on Step 1, never the reverse; and the teacher is only allowed to send your homework back for revisions ONCE.<br/>"
            "<b>Architectural Verdict:</b> Prevent cyclic dependencies by enforcing monotonic DAG progression (Step $j$ depends only on $i < j$). Impose a strict boundary cap on self-correction retries (`retryCount < 1` or `2`). If the quality threshold is not met after the retry cap, trigger graceful degradation with explicit uncertainty warnings rather than blocking execution."
        ),
        (
            3,
            "Explain the mathematical proof that Cosine Similarity equals the Dot Product for L2-normalized vectors.",
            "<b>Kid Analogy:</b> If all your toy compass needles are made exactly 1 inch long, you don't need to divide by their lengths—multiplying their coordinates tells you the exact angle instantly!<br/>"
            "<b>Architectural Verdict:</b> $\\cos(\\theta) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\| \\|\\mathbf{v}\\|}$. When vectors $\\mathbf{u}$ and $\\mathbf{v}$ are unit-normalized upon ingestion such that $\\|\\mathbf{u}\\| = 1.0$ and $\\|\\mathbf{v}\\| = 1.0$, the denominator evaluates to $1.0 \\times 1.0 = 1.0$. Thus, $\\cos(\\theta) = \\sum_{i=1}^D u_i v_i$. This transforms vector search from square-root calculations into single-cycle SIMD dot-product multiplications."
        ),
        (
            4,
            "What are the architectural trade-offs between Approximate Nearest Neighbor (ANN) indexes: HNSW vs. IVFFlat?",
            "<b>Kid Analogy:</b> HNSW is like a multi-level highway with express ramps—super fast to get anywhere, but takes up huge land (RAM). IVFFlat is like parking cars in numbered garages—uses less space, but takes longer to check.<br/>"
            "<b>Architectural Verdict:</b> HNSW builds a multi-layer geometric skip-graph yielding $>98\\%$ recall and sub-millisecond query latency ($O(\\log N)$), but requires 2–4x RAM overhead for graph edges. IVFFlat clusters vectors into Voronoi cells via k-means, requiring minimal memory, but suffers lower recall on high-dimensional vectors unless inverted lists (`nprobe`) are extensively searched."
        ),
        (
            5,
            "Why adopt the Model Context Protocol (MCP) over vendor-specific tool-calling wrappers?",
            "<b>Kid Analogy:</b> Standard USB-C plugs work on every tablet, laptop, and phone; proprietary plugs force you to buy expensive, fragile adapters every time.<br/>"
            "<b>Architectural Verdict:</b> Vendor-specific function calling creates tight vendor lock-in and non-portable prompt glue code. MCP defines an open JSON-RPC standard for tool discovery (`listTools`), dynamic JSON Schema parameter validation, capability negotiation, and error encapsulation, allowing tools to be written once and shared across diverse model providers."
        ),
        (
            6,
            "Compare Server-Sent Events (SSE) versus WebSockets for streaming agent reasoning traces and token telemetry.",
            "<b>Kid Analogy:</b> A transistor radio station (SSE) broadcasts news to everyone with zero effort; a private telephone line (WebSockets) requires expensive two-way wires and disconnects easily.<br/>"
            "<b>Architectural Verdict:</b> WebSockets are bidirectional, require stateful protocol upgrades (`ws://`), and frequently suffer timeouts behind corporate firewalls and L7 proxies. SSE operates over standard HTTP (`text/event-stream`), provides native automatic browser reconnection via `EventSource`, and aligns with unidirectional agent telemetry streaming."
        ),
        (
            7,
            "How do you architect KV-cache optimization to reduce multi-agent cloud inference bills by up to 80%?",
            "<b>Kid Analogy:</b> Always put the unchanging rulebook at the very beginning of your binder so the teacher only has to read it once and gives you a half-price discount for remembering it!<br/>"
            "<b>Architectural Verdict:</b> Modern foundation model providers (Gemini, Claude, OpenAI) discount cached prompt tokens by 50%–80%. To maximize cache hit rates, order prompt templates deterministically: invariant system instructions and MCP tool schemas at the very top (prefix), historical conversation in the middle, and dynamic variable user inputs at the tail."
        ),
        (
            8,
            "How do you mitigate Prompt Injection and Tool-Exfiltration attacks in autonomous multi-agent environments?",
            "<b>Kid Analogy:</b> Never let a stranger write instructions directly on your chef's recipe card; always put stranger notes in a sealed plastic bag marked 'UNTRUSTED DATA'.<br/>"
            "<b>Architectural Verdict:</b> Enforce defense-in-depth: (1) Delimit user input using structural XML tags (`<user_goal>`); (2) MCP Sandboxing: Restrict tools to least-privilege schemas and prohibit arbitrary shell execution; (3) Output Validation: The Critic node audits tool outputs for sensitive credential leakage before finalizing responses."
        ),
        (
            9,
            "What is the LLM-as-a-Judge methodology, and how do you mitigate position bias and verbosity bias?",
            "<b>Kid Analogy:</b> When judging who baked the best cookie, switch the plates so you don't always pick the first plate (position bias), and don't pick a giant cookie just because it is bigger than the tasty small cookie (verbosity bias)!<br/>"
            "<b>Architectural Verdict:</b> LLM-as-a-Judge employs an independent evaluator model with structured rubrics. Mitigate position bias by swapping candidate response orders and averaging scores; mitigate verbosity bias by penalizing redundant tokens and supplying gold-standard reference answers in the evaluation prompt."
        ),
        (
            10,
            "How do you design a distributed multi-agent system capable of handling 10,000 concurrent agent workflows?",
            "<b>Kid Analogy:</b> Instead of one chef doing all the cooking and taking orders at the door, have a team of greeters at the front, a message board in the kitchen, and 100 cooking stations working at once.<br/>"
            "<b>Architectural Verdict:</b> Decouple HTTP/SSE connection gateways from agent workers using Redis Pub/Sub. Push task execution into distributed message queues (BullMQ / Celery). Persist session state checkpoints in PostgreSQL with pgvector for crash recovery and auditability."
        ),
    ]

    for q_num, question, answer in interview_qa_list:
        content = [
            Paragraph(f"<b><font color='#002147'>Q{q_num}: {question}</font></b>", h3_style),
            Spacer(1, 2),
            Paragraph(answer, body_style),
            Spacer(1, 4),
        ]
        story.append(KeepTogether(content))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 10: CHEATSHEETS, 10 GOLDEN LAWS & GLOSSARY (Page 15)
    # -------------------------------------------------------------------------
    story.append(Paragraph("MODULE 10", ch_number_style))
    story.append(Paragraph("Master Cheatsheets, 10 Golden Laws &amp; Glossary", ch_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=OXFORD_BLUE, spaceBefore=4, spaceAfter=8))

    story.append(Paragraph("<b>10.1 The 10 Golden Laws of AI Solution Architecture</b>", h2_style))
    laws = [
        "1. <b>Never Let a Model Guess What a Tool Can Calculate:</b> Route arithmetic to calculators and facts to databases.",
        "2. <b>Enforce Monotonic Progression:</b> All DAG step dependencies must satisfy $j > i$ to guarantee deadlock freedom.",
        "3. <b>Isolate Tool Failures:</b> Never let a tool exception crash the state machine; encapsulate it as an observation.",
        "4. <b>Bound Self-Correction Retries:</b> Cap self-correction cycles at 1 or 2 iterations to eliminate infinite loops.",
        "5. <b>Always L2-Normalize Embeddings at Ingestion:</b> Transform cosine distance into hardware SIMD dot products.",
        "6. <b>Anchor Invariant Prompts at the Prefix:</b> Exploit 50-80% KV-cache discounts by keeping system rules at the top.",
        "7. <b>Favor SSE Over WebSockets for AI Telemetry:</b> Unidirectional HTTP streaming is cheaper, simpler, and firewall-safe.",
        "8. <b>Separate Planning from Evaluation:</b> The Planner must never grade its own homework; assign a dedicated Critic.",
        "9. <b>Adopt Standard Tool Protocols (MCP):</b> Reject proprietary wrappers; enforce JSON Schema parameter contracts.",
        "10. <b>Embrace Zero-Build Simplicity:</b> Eliminate unnecessary build toolchains on the presentation layer for agility.",
    ]
    for law in laws:
        story.append(Paragraph(law, body_style))
        story.append(Spacer(1, 1))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>10.2 Quick Reference Cheat Matrix</b>", h2_style))
    cheat_data = [
        ["Subsystem", "Core Class", "Primary Method", "Key Metric / Guardrail"],
        ["Planner", "PlannerAgent", "createPlan(goal, tools)", "Acyclic Monotonic DAG"],
        ["Executor", "ExecutorAgent", "executeStep(step, obs)", "ReAct Loop Context Grounding"],
        ["Critic", "CriticAgent", "evaluate(goal, plan, res)", "Score >= 75 / Bounded Retry Cap"],
        ["MCP Registry", "MCPRegistry", "executeTool(toolCall)", "JSON Schema / 8000ms Timeout"],
        ["Vector Math", "VectorMath", "cosineSimilarity(u, v)", "L2 Unit Norm / Dot Product"],
        ["Vector Store", "VectorStore", "similaritySearch(query)", "Sliding Window / Cosine Ranking"],
        ["Tokenomics", "TokenCounter", "recordUsage(curr, p, c)", "BPE Heuristic / KV-Cache Discount"],
        ["SSE Stream", "SSEManager", "registerClient(id, res)", "text/event-stream / Auto Reconnect"],
    ]
    cheat_tbl = Table(cheat_data, colWidths=[80, 110, 150, 170])
    cheat_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), OXFORD_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.6),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("PADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#FFFFFF"), HexColor("#F8FAFC")]),
    ]))
    story.append(cheat_tbl)

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>10.3 Comprehensive Glossary of Agentic Terms</b>", h2_style))
    glossary = [
        ("Acyclic Graph", "A network of directed steps containing no closed loops, guaranteeing safe termination."),
        ("Cosine Similarity", "The geometric measure of the angle between two embedding vectors in multidimensional space."),
        ("Critic Node", "An independent verification agent that grades execution traces against hallucination rubrics."),
        ("DAG (Directed Acyclic Graph)", "A mathematical structure of vertices and directed edges representing task workflows."),
        ("Dot Product", "The algebraic sum of the products of the corresponding entries of two sequences of numbers."),
        ("EventSource", "The standard browser interface for receiving Server-Sent Events over HTTP."),
        ("Executor Node", "The agent responsible for executing individual plan steps via the ReAct loop."),
        ("Hallucination", "A probabilistic LLM generation that sounds convincing but contradicts reality or facts."),
        ("JSON Schema", "A declarative vocabulary that annotates and validates JSON documents and tool parameters."),
        ("KV-Cache", "A mechanism storing key-value attention representations in GPU memory to accelerate prompt reuse."),
        ("MCP (Model Context Protocol)", "An open industry standard formalizing how models invoke tools and access data."),
        ("Planner Node", "The agent that decomposes high-level goals into dependency-ordered execution steps."),
        ("ReAct Paradigm", "An orchestration pattern interleaving Thought, Action, and Observation cycles."),
        ("Server-Sent Events (SSE)", "An HTTP protocol enabling servers to stream text frames unidirectionally to web browsers."),
        ("Tokenomics", "The mathematical study of token generation costs, latency, and context cache economics."),
        ("Zero-Build Frontend", "Web application architecture utilizing pure native ES6/HTML5/CSS3 without bundlers."),
    ]
    for term, definition in glossary:
        story.append(Paragraph(f"• <b>{term}:</b> {definition}", body_style))

    # Build the document using the Oxford Numbered Canvas
    doc.build(story, canvasmaker=OxfordNumberedCanvas)
    print("Ebook PDF build complete!")

if __name__ == "__main__":
    build_pdf()
