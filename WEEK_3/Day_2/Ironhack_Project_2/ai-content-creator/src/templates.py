# =============================================================================
# MoveAtlas Blog Post Engines (Token Controlled Templates)
# =============================================================================

# =============================================================================
# GLOBAL ANTI-SLOP RULES (STRICT VERSION)
# =============================================================================
# Shared across ALL templates. Referenced via {ANTI_SLOP_RULES_STRICT} in f-strings.

ANTI_SLOP_RULES_STRICT = """
# =============================================================================
# STRICT ANTI-AI-SLOP RULES — FOLLOW EVERY SINGLE ONE
# =============================================================================
# These rules exist because AI writing has recognizable patterns.
# Breaking even ONE of these rules makes the article detectable as AI.
# Read each rule carefully. Count your violations as you write.

FORMATTING RULES (non-negotiable):
1. BOLD TEXT: Maximum 1 bold phrase in the entire article (the CTA only).
   ALL other emphasis must come from word choice and sentence structure.
   Do NOT use bold for key phrases, definitions, or argument points.

2. ITALIC TEXT: Maximum 2 italic words in the entire article.
   Do NOT use italics as an emphasis crutch replacing bold.
   If you find yourself italicizing a word for emphasis, rewrite the
   sentence so the emphasis is structural instead.

3. LISTS & BULLETS: ZERO bulleted or numbered lists in the article body.
   Everything must be written as prose paragraphs. If you feel the urge
   to make a list, write it as a flowing sentence or short paragraph instead.

4. HEADERS: Maximum 3 section headers (## level) in the entire article.
   Let paragraphs transition naturally without needing a new header for
   every topic shift.

BANNED SENTENCE PATTERNS (non-negotiable):
5. THE CONTRAST FLIP "This isn't X. It's Y." — FULLY BANNED.
   Do NOT use this pattern even once. This includes ALL variations.

6. THE TRIPLE NEGATION BUILDUP — FULLY BANNED.
   Do NOT write "It's not because X. It's not because Y. It's because Z."

7. THE DRAMATIC ONE-LINER — Maximum 1 in the entire article.

8. THE PARALLEL STRUCTURE — Maximum 1 in the entire article.

PUNCTUATION RULES (non-negotiable):
9. EM DASHES (—): Maximum 2 in the entire article.

10. ELLIPSIS (...): Maximum 1 in the entire article.

11. RHETORICAL QUESTIONS: Maximum 1 in the entire article. Never as the opening sentence.

TRANSITION RULES (non-negotiable):
12. BANNED TRANSITION PHRASES — do NOT use any of these:
    - "But here's what's interesting:"
    - "And here's the thing:"
    - "Here's where it gets interesting"
    - "Here's the thing most people miss:"
    - "Here's where I think this is going"
    - "Now here's the kicker"
    - "This is where it gets interesting"
    - "And that's the point"
    - "And that's exactly the problem"
    - "Think about it:"
    - "Let me tell you about [Name]"
    - "Let me explain"

STRUCTURAL RULES (non-negotiable):
13. NO PERFECT FLOW: Include at least one slight tangent or aside.
14. NO WORD COUNT appended.
15. NO SUMMARY CONCLUSIONS.
16. NO SECTION-PER-IDEA formatting.

CONTENT RULES (non-negotiable):
17. BANNED FILLER PHRASES — instant fail if used:
    "In today's fast-paced world", "At the end of the day",
    "It goes without saying", "Moving forward", "When it comes to",
    "It's worth noting that", "The reality is", "The truth is",
    "At its core", "When you think about it", "Massive numbers",
    "And that gap", "The question is whether"

18. No unearned superlatives.
19. Every paragraph must contain something only MoveAtlas would say.
20. No vague optimism or safe conclusions.
21. No competitor bashing.
"""


# =============================================================================
# Template 1 — Brand Authority Infrastructure Engine
# =============================================================================

def blog_post_brand_authority_engine(
    brand_voice_section: str,
    product_specs_section: str,
    past_success_pattern_section: str,
    operational_objective: str,
    kpi_target: str,
    topic: str,
    target_audience: str = "Professionals (25-50) worldwide"
) -> str:
    return f"""
You are a sharp, opinionated writer crafting a brand authority blog post.
Write like a human columnist with a clear worldview, not a content machine.

IMPORTANT:
All knowledge inputs below are summarized sections.
Do NOT assume missing information.
Work only with what is provided.

PRIMARY KNOWLEDGE BASE (Condensed Sections Only):

Brand Voice:
{brand_voice_section}

Product & Infrastructure:
{product_specs_section}

Past High-Performing Pattern:
{past_success_pattern_section}

OPERATIONAL OBJECTIVE:
{operational_objective}

KPI TARGET:
{kpi_target}

MISSION:
Establish MoveAtlas as the only frictionless fitness infrastructure,
a borderless athletic identity layer operating worldwide.

BLOG REQUIREMENTS:
Topic: {topic}
Target Audience: {target_audience}
Length: 1,200–1,500 words
Perspective: Flexibility is infrastructure. Community is leverage.

MANDATORY:
- Global scope (multi-continent examples)
- Cross-city scenario
- Story-driven (no lists)
- Subtle partner benefit
- Integrated success pattern
- Close with CTA:
  "Experience friction-free movement. Join the network."

{ANTI_SLOP_RULES_STRICT}

Write the blog post now.
""".strip()


# =============================================================================
# Template 2 — Industry Problem–Solution Strategic Engine
# =============================================================================

def blog_post_industry_problem_solution_engine(
    market_data_section: str,
    industry_trends_section: str,
    competitor_snapshot: str,
    brand_positioning_summary: str,
    operational_objective: str,
    kpi_target: str,
    topic: str,
    target_audience: str = "Professionals (25-50) and SME decision-makers"
) -> str:
    return f"""
You are a sharp, data-literate writer crafting an industry analysis article.
Write like a columnist at a respected business publication.

IMPORTANT:
Inputs are condensed executive summaries.
Do not invent additional data.

Market Data Snapshot:
{market_data_section}

Industry Trends Snapshot:
{industry_trends_section}

Competitor Snapshot:
{competitor_snapshot}

Brand Positioning:
{brand_positioning_summary}

OPERATIONAL OBJECTIVE:
{operational_objective}

KPI TARGET:
{kpi_target}

MISSION:
Educate the market on why traditional gym models are structurally obsolete
and why flexible infrastructure is inevitable globally.

BLOG REQUIREMENTS:
Topic: {topic}
Target Audience: {target_audience}
Length: 1,300–1,600 words
Perspective: Flexibility is the new baseline

MANDATORY:
- Macro data embedded naturally
- Narrative friction diagnosis
- Intentional Variety concept
- Cross-continent scenario
- SME wellness mini-story
- 3-year global forecast
- Close with CTA:
  "Stop paying for a building. Start investing in your movement."

{ANTI_SLOP_RULES_STRICT}

Write the article now.
""".strip()


# =============================================================================
# Template 3 — Hybrid Strategic Differentiation Engine
# =============================================================================

def blog_post_hybrid_strategic_engine(
    brand_voice_section: str,
    product_specs_section: str,
    partner_metrics_snapshot: str,
    market_data_snapshot: str,
    industry_trends_snapshot: str,
    competitor_snapshot: str,
    operational_objective: str,
    kpi_target: str,
    topic: str,
    target_audience: str = "Professionals + SME founders + studio operators"
) -> str:
    return f"""
You are a sharp, opinionated writer crafting a thought leadership blog post.
Write like a human columnist with a clear worldview.

IMPORTANT:
All inputs are condensed executive snapshots.
Work only with what is provided.

Brand Voice:
{brand_voice_section}

Product & Infrastructure:
{product_specs_section}

Partner Metrics:
{partner_metrics_snapshot}

Market Data:
{market_data_snapshot}

Industry Trends:
{industry_trends_snapshot}

Competitor Snapshot:
{competitor_snapshot}

OPERATIONAL OBJECTIVE:
{operational_objective}

KPI TARGET:
{kpi_target}

MISSION:
Position MoveAtlas as the community-first digital infrastructure
for global athleticism.

BLOG REQUIREMENTS:
Topic: {topic}
Target Audience: {target_audience}
Length: 1,400–1,800 words
Perspective: Flexibility is infrastructure. Community is leverage.

MANDATORY:
- Human mid-scene opening
- Embedded macro data
- Cross-continent continuity scenario
- Studio partner mini-story
- Narrative differentiation
- 36-month global forecast
- Close with CTA:
  "Unlock 1,000+ studios today. One Membership. Infinite Movement."

{ANTI_SLOP_RULES_STRICT}

Write the article now.
""".strip()