"""
Main application entry point (Production Refactor).
Orchestrates the flow between Interface, Knowledge, and LLM layers.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Project modules
from llm_integration import LLMFactory 
from knowledge_base import (
    build_brand_knowledge,
    build_product_knowledge,
    build_competitor_knowledge,
    build_industry_trends_knowledge,
    build_market_overview_knowledge,
)
import templates 
from interface import CLIInterface

# Resolve project paths
BASE_DIR = Path(__file__).resolve().parent.parent

def main() -> None:
    load_dotenv()
    
    # Initialize Interface
    ui = CLIInterface()
    ui.show_header()
    
    # 1. Setup Provider
    provider_key = ui.get_provider_choice()
    try:
        llm = LLMFactory.get_provider(provider_key)
    except Exception as e:
        print(f"Error: {e}")
        return

    # 2. Get User Intent
    t_choice = ui.get_template_choice()
    params = ui.get_content_params()

    # 3. Process Data (The "Layers Below")
    ui.notify_loading("Building Knowledge Base")
    brand_path = BASE_DIR / "knowledge_base/primary/brand_guidelines.md"
    product_path = BASE_DIR / "knowledge_base/primary/product_specs.md"
    market_path = BASE_DIR / "knowledge_base/secondary/market_trends.md"
    competitor_path = BASE_DIR / "knowledge_base/secondary/competitor_analysis.md"

    kb = {
        "brand": build_brand_knowledge(str(brand_path)),
        "product": build_product_knowledge(str(product_path)),
        "market": build_market_overview_knowledge(str(market_path)),
        "industry": build_industry_trends_knowledge(str(competitor_path)),
        "competitor": build_competitor_knowledge(str(competitor_path))
    }

    # 4. Map to Template
    ui.notify_loading("Constructing Strategic Prompt")
    if t_choice == "1":
        prompt_text = templates.blog_post_brand_authority_engine(
            brand_voice_section=kb["brand"].get("brand_voice", ""),
            product_specs_section=kb["product"].get("product_overview", ""),
            past_success_pattern_section="Berlin expansion framework",
            operational_objective=params["objective"],
            kpi_target=params["kpi"],
            topic=params["topic"]
        )
    elif t_choice == "2":
        prompt_text = templates.blog_post_industry_problem_solution_engine(
            market_data_section=kb["market"].get("industry_overview", ""),
            industry_trends_section=kb["industry"].get("macro_trends", ""),
            competitor_snapshot=kb["competitor"].get("competitive_overview", ""),
            brand_positioning_summary=kb["brand"].get("brand_voice", ""),
            operational_objective=params["objective"],
            kpi_target=params["kpi"],
            topic=params["topic"]
        )
    else:
        prompt_text = templates.blog_post_hybrid_strategic_engine(
            brand_voice_section=kb["brand"].get("brand_voice", ""),
            product_specs_section=kb["product"].get("product_overview", ""),
            partner_metrics_snapshot=kb["product"].get("customer_results", ""),
            market_data_snapshot=kb["market"].get("industry_overview", ""),
            industry_trends_snapshot=kb["industry"].get("macro_trends", ""),
            competitor_snapshot=kb["competitor"].get("competitive_overview", ""),
            operational_objective=params["objective"],
            kpi_target=params["kpi"],
            topic=params["topic"]
        )

    # 5. Generation
    ui.notify_loading(f"Generating Content with {provider_key.upper()}")
    blog_output = llm.generate(prompt_text, temperature=0.7)

    # 6. Output
    output_path = BASE_DIR / "blog_output.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(blog_output)

    ui.notify_success(output_path)

if __name__ == "__main__":
    main()