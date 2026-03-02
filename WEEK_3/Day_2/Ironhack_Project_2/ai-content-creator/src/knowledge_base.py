# src/knowledge_base.py

# Import helper functions from document_processor
from document_processor import load_markdown, extract_section


# ------------------------------
# BRAND KNOWLEDGE
# ------------------------------

def build_brand_knowledge(file_path):
    """
    This function reads the brand_guidelines markdown file
    and extracts its main sections into a dictionary.
    """

    # Load the full markdown file content
    content = load_markdown(file_path)

    # Extract specific sections using their headers
    brand_voice = extract_section(content, "## 1. Brand Voice", "## 2.")
    tone_guidelines = extract_section(content, "## 2. Tone Guidelines", "## 3.")
    messaging = extract_section(content, "## 3. Key Messaging Framework", "## 4.")
    audience = extract_section(content, "## 4. Target Audience Personas", "## 5.")

    # Return structured data as a dictionary
    return {
        "brand_voice": brand_voice,
        "tone_guidelines": tone_guidelines,
        "messaging_framework": messaging,
        "target_audience": audience
    }


# ------------------------------
# PRODUCT KNOWLEDGE
# ------------------------------

def build_product_knowledge(file_path):
    """
    Extracts product-related information from product_specs markdown file.
    """

    content = load_markdown(file_path)

    product_overview = extract_section(content, "## 1. Product Overview", "## 2.")
    core_features = extract_section(content, "## 2. Core Features & Benefits", "## 3.")
    use_cases = extract_section(content, "## 3. Use Cases", "## 4.")
    pricing = extract_section(content, "## 4. Pricing & Plans", "## 5.")
    technical_specs = extract_section(content, "## 5. Technical Specifications", "## 6.")
    usps = extract_section(content, "## 6. Unique Selling Propositions (USPs)", "## 7.")
    social_proof = extract_section(content, "## 7. Customer Results & Social Proof", "## 8.")
    roadmap = extract_section(content, "## 8. Roadmap & Future Development")

    return {
        "product_overview": product_overview,
        "core_features": core_features,
        "use_cases": use_cases,
        "pricing_plans": pricing,
        "technical_specifications": technical_specs,
        "unique_selling_points": usps,
        "customer_results": social_proof,
        "roadmap": roadmap
    }


# ------------------------------
# COMPETITOR ANALYSIS
# ------------------------------

def build_competitor_knowledge(file_path):
    """
    Extracts competitor analysis sections from markdown file.
    """

    content = load_markdown(file_path)

    competitive_overview = extract_section(content, "## 1. Competitive Overview", "## 2.")
    competitor_profiles = extract_section(content, "## 2. Detailed Competitor Profiles", "## 3.")
    feature_matrix = extract_section(content, "## 3. Feature Comparison Matrix", "## 4.")
    market_dynamics = extract_section(content, "## 4. Market Dynamics", "## 5.")
    differentiation = extract_section(content, "## 5. Differentiation Opportunities", "## 6.")
    content_strategy = extract_section(content, "## 6. Competitive Content Strategy")

    return {
        "competitive_overview": competitive_overview,
        "competitor_profiles": competitor_profiles,
        "feature_comparison_matrix": feature_matrix,
        "market_dynamics": market_dynamics,
        "differentiation_opportunities": differentiation,
        "competitive_content_strategy": content_strategy
    }


# ------------------------------
# INDUSTRY TRENDS
# ------------------------------

def build_industry_trends_knowledge(file_path):
    """
    Extracts high-level industry trend sections.
    """

    content = load_markdown(file_path)

    macro_trends = extract_section(content, "## 1. Macro Trends", "## 2.")
    technology_shifts = extract_section(content, "## 2. Technology Shifts", "## 3.")
    customer_behavior = extract_section(content, "## 3. Customer Behavior Changes", "## 4.")
    regulatory_trends = extract_section(content, "## 4. Regulatory Trends")

    return {
        "macro_trends": macro_trends,
        "technology_shifts": technology_shifts,
        "customer_behavior_changes": customer_behavior,
        "regulatory_trends": regulatory_trends
    }


# ------------------------------
# MARKET OVERVIEW
# ------------------------------

def build_market_overview_knowledge(file_path):
    """
    Extracts structured market overview sections.
    """

    content = load_markdown(file_path)

    industry_overview = extract_section(content, "## 1. Industry Overview", "## 2.")
    market_segments = extract_section(content, "## 2. Market Segments", "## 3.")
    growth_drivers = extract_section(content, "## 3. Growth Drivers", "## 4.")
    key_statistics = extract_section(content, "## 4. Key Statistics & Data Points", "## 5.")
    regulatory_economic = extract_section(content, "## 5. Regulatory & Economic Factors", "## 6.")
    geographic_analysis = extract_section(content, "## 6. Geographic Analysis", "## 7.")
    market_outlook = extract_section(content, "## 7. Market Outlook & Predictions")

    return {
        "industry_overview": industry_overview,
        "market_segments": market_segments,
        "growth_drivers": growth_drivers,
        "key_statistics": key_statistics,
        "regulatory_economic_factors": regulatory_economic,
        "geographic_analysis": geographic_analysis,
        "market_outlook_predictions": market_outlook
    }
