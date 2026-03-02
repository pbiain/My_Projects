"""
Interface Layer for AI Content Creator.
Handles all user interactions and terminal formatting.
"""

class CLIInterface:
    def __init__(self):
        self.width = 50

    def show_header(self):
        print("\n" + "=" * self.width)
        print("🚀 MOVEATLAS STRATEGIC CONTENT ENGINE".center(self.width))
        print("=" * self.width)

    def get_provider_choice(self) -> str:
        print("\n[1] SELECT PROVIDER")
        print("  1. OpenAI (GPT-4o-mini)")
        print("  2. Anthropic (Claude 3.5 Sonnet)")
        choice = input("  Select (1/2): ").strip()
        return "openai" if choice == "1" else "anthropic"

    def get_template_choice(self) -> str:
        print("\n[2] SELECT CONTENT STRATEGY")
        print("  1. Brand Authority (Identity focus)")
        print("  2. Industry Analysis (Data focus)")
        print("  3. Hybrid Strategic (Community focus)")
        return input("  Select (1/2/3): ").strip()

    def get_content_params(self) -> dict:
        print("\n[3] CUSTOMIZE PARAMETERS")
        topic = input("  Topic (Enter for default): ").strip() or \
                "Why Flexible Fitness Infrastructure Is Replacing Traditional Gyms"
        
        obj = input("  Objective (Enter for default): ").strip() or \
              "Reinforce infrastructure positioning"
        
        kpi = input("  KPI Target (Enter for default): ").strip() or \
              "Increase CTR by 15% in 90 days"
        
        return {"topic": topic, "objective": obj, "kpi": kpi}

    def notify_loading(self, message: str):
        print(f"  ⏳ {message}...")

    def notify_success(self, path):
        print("\n" + "=" * self.width)
        print(f"✅ SUCCESS: Content saved to:".center(self.width))
        print(f"{path}".center(self.width))
        print("=" * self.width + "\n")