import json
from collections import defaultdict

class KnifeCalculator:
    """
    CS2 Knife Calculator - Handles both case unboxing probabilities and trade-up requirements
    """
    
    # Base knife drop rate from cases
    KNIFE_DROP_RATE = 0.0026  # 0.26% chance per case
    
    def __init__(self):
        # Load knife trade-up data (this would be populated with actual data)
        self.knife_trade_up_data = self._load_trade_up_data()
        
    def _load_trade_up_data(self):
        """
        Load trade-up requirements for knives. In a real implementation, this would be
        fetched from a database or API with current CS2 trade-up rules.
        """
        # This is a simplified example - in reality this would be much more comprehensive
        return {
            "Karambit": {
                "eligible_collections": ["Dreams & Nightmares", "Operation Riptide", "Shattered Web"],
                "required_covert_skins": [
                    "AWP | Dragon Lore", "M4A4 | Howl", "AK-47 | Fire Serpent",
                    "Desert Eagle | Blaze", "AWP | Neo-Noir"
                ],
                "success_rate": 0.85  # 85% chance to get desired knife pattern
            },
            "Butterfly Knife": {
                "eligible_collections": ["Glove Case", "Gamma 2", "Spectrum 2"],
                "required_covert_skins": [
                    "USP-S | Neo-Noir", "Glock-18 | Bullet Queen", "P250 | Wingshot",
                    "MAC-10 | Neon Rider", "UMP-45 | Primal Saber"
                ],
                "success_rate": 0.82
            },
            "M9 Bayonet": {
                "eligible_collections": ["Chroma 3", "Gamma", "Bravo"],
                "required_covert_skins": [
                    "M4A1-S | Hyper Beast", "P90 | Death Grip", "Five-SeveN | Fowl Play",
                    "Nova | Hyper Beast", "PP-Bizon | Osiris"
                ],
                "success_rate": 0.88
            },
            "Gut Knife": {
                "eligible_collections": ["Gamma 2", "Operation Broken Fang", "CS20"],
                "required_covert_skins": [
                    "G3SG1 | Flux", "Dual Berettas | Royal Consorts", "FAMAS | Djinn",
                    "Tec-9 | Re-Entry", "MP7 | Nemesis"
                ],
                "success_rate": 0.83
            },
            "Flip Knife": {
                "eligible_collections": ["Glove Case", "Spectrum", "Clutch"],
                "required_covert_skins": [
                    "SCAR-20 | Cardiac", "SG 553 | Phantom", "R8 Revolver | Llama Cannon",
                    "XM1014 | Quicksilver", "CZ75-Auto | Tacticat"
                ],
                "success_rate": 0.86
            }
        }
    
    def calculate_unbox_probability(self, cases_opened):
        """
        Calculate probability of getting at least one knife from opening cases
        """
        probability = 1 - (1 - self.KNIFE_DROP_RATE) ** cases_opened
        return probability * 100
    
    def cases_needed_for_probability(self, target_probability):
        """
        Calculate how many cases needed to reach target probability
        """
        if target_probability <= 0 or target_probability >= 100:
            raise ValueError("Target probability must be between 0 and 100")
        
        target_prob_decimal = target_probability / 100
        cases_needed = 0
        
        while True:
            current_prob = self.calculate_unbox_probability(cases_needed)
            if current_prob >= target_probability:
                return cases_needed
            cases_needed += 1
    
    def get_trade_up_requirements(self, knife_name):
        """
        Get trade-up requirements for a specific knife
        """
        knife_name = knife_name.title()
        if knife_name not in self.knife_trade_up_data:
            available_knives = list(self.knife_trade_up_data.keys())
            raise ValueError(f"Knife '{knife_name}' not found. Available knives: {', '.join(available_knives)}")
        
        return self.knife_trade_up_data[knife_name]
    
    def calculate_trade_up_cost(self, knife_name, covert_skin_prices):
        """
        Calculate the cost of getting a specific knife via trade-up
        """
        requirements = self.get_trade_up_requirements(knife_name)
        
        # Find the cheapest eligible Covert skins from the requirements
        eligible_skins = requirements["required_covert_skins"]
        total_cost = 0
        cheapest_skins = []
        
        for skin in eligible_skins:
            if skin in covert_skin_prices:
                cheapest_skins.append((skin, covert_skin_prices[skin]))
        
        # Sort by price and take the 5 cheapest
        cheapest_skins.sort(key=lambda x: x[1])
        selected_skins = cheapest_skins[:5]
        
        if len(selected_skins) < 5:
            raise ValueError(f"Not enough price data for required Covert skins. Need 5, found {len(selected_skins)}")
        
        total_cost = sum(price for _, price in selected_skins)
        success_rate = requirements["success_rate"]
        
        # Calculate expected cost considering success rate
        expected_cost = total_cost / success_rate
        
        return {
            "knife_name": knife_name,
            "selected_skins": selected_skins,
            "raw_cost": total_cost,
            "success_rate": success_rate * 100,
            "expected_cost": expected_cost,
            "eligible_collections": requirements["eligible_collections"]
        }
    
    def compare_methods(self, knife_name=None, covert_skin_prices=None, budget=None):
        """
        Compare case unboxing vs trade-up methods
        """
        results = {}
        
        # Case unboxing analysis
        results["case_unboxing"] = {
            "probability_per_case": self.KNIFE_DROP_RATE * 100,
            "cases_for_50_percent": self.cases_needed_for_probability(50),
            "cases_for_90_percent": self.cases_needed_for_probability(90)
        }
        
        # Trade-up analysis if requested
        if knife_name and covert_skin_prices:
            try:
                trade_up_results = self.calculate_trade_up_cost(knife_name, covert_skin_prices)
                results["trade_up"] = trade_up_results
            except ValueError as e:
                results["trade_up_error"] = str(e)
        
        # Budget analysis if provided
        if budget:
            cases_affordable = int(budget / 2.5)  # Assuming average case price of $2.5
            unbox_prob = self.calculate_unbox_probability(cases_affordable)
            
            results["budget_analysis"] = {
                "budget": budget,
                "cases_affordable": cases_affordable,
                "unbox_probability": unbox_prob,
                "recommendation": "Trade-up" if knife_name and "trade_up" in results and results["trade_up"]["expected_cost"] <= budget else "Case unboxing"
            }
        
        return results
    
    def generate_report(self, knife_name=None, covert_skin_prices=None, budget=None):
        """
        Generate a comprehensive report comparing both methods
        """
        results = self.compare_methods(knife_name, covert_skin_prices, budget)
        
        report = []
        report.append("=" * 60)
        report.append("CS2 KNIFE ACQUISITION CALCULATOR")
        report.append("=" * 60)
        report.append("")
        
        # Case unboxing section
        report.append("📊 CASE UNBOXING PROBABILITIES")
        report.append("-" * 40)
        report.append(f"🎯 Base knife drop rate: {results['case_unboxing']['probability_per_case']:.3f}% per case")
        report.append(f"🎲 Cases needed for 50% chance: {results['case_unboxing']['cases_for_50_percent']:,}")
        report.append(f"🎯 Cases needed for 90% chance: {results['case_unboxing']['cases_for_90_percent']:,}")
        report.append("")
        
        # Trade-up section if applicable
        if knife_name and "trade_up" in results:
            trade_up = results["trade_up"]
            report.append(f"🔧 TRADE-UP REQUIREMENTS FOR {knife_name.upper()}")
            report.append("-" * 40)
            report.append(f"📋 Required: 5 Covert skins from eligible collections")
            report.append(f"📚 Eligible collections: {', '.join(trade_up['eligible_collections'])}")
            report.append("")
            report.append("💰 Cost Analysis:")
            report.append("   Selected Covert skins (cheapest options):")
            
            for i, (skin, price) in enumerate(trade_up["selected_skins"], 1):
                report.append(f"   {i}. {skin}: ${price:.2f}")
            
            report.append(f"   💸 Total raw cost: ${trade_up['raw_cost']:.2f}")
            report.append(f"   ✅ Success rate: {trade_up['success_rate']:.1f}%")
            report.append(f"   📈 Expected cost (factoring in success rate): ${trade_up['expected_cost']:.2f}")
            report.append("")
        
        # Budget analysis if provided
        if budget and "budget_analysis" in results:
            budget_analysis = results["budget_analysis"]
            report.append(f"💰 BUDGET ANALYSIS (${budget:.2f})")
            report.append("-" * 40)
            report.append(f"📦 Cases you can afford: {budget_analysis['cases_affordable']:,}")
            report.append(f"🎯 Probability of getting ANY knife: {budget_analysis['unbox_probability']:.2f}%")
            
            if knife_name and "trade_up" in results:
                trade_up_cost = results["trade_up"]["expected_cost"]
                can_afford_tradeup = budget >= trade_up_cost
                report.append("")
                report.append(f"🔧 Trade-up cost for {knife_name}: ${trade_up_cost:.2f}")
                report.append(f"✅ Can afford trade-up: {'YES' if can_afford_tradeup else 'NO'}")
                report.append(f"💡 Recommendation: {budget_analysis['recommendation']}")
        
        # Key insights
        report.append("")
        report.append("💡 KEY INSIGHTS")
        report.append("-" * 40)
        report.append("• Case unboxing gives random knives with 0.26% probability per case")
        report.append("• Trade-ups allow targeting specific knives but require 5 Covert skins")
        report.append("• Trade-ups have an 82-88% success rate for getting your desired knife pattern")
        report.append("• The trade-up system lets players exchange five Covert (red) skins into a Gold-tier item, such as a knife or gloves. [[1]]")
        report.append("• To obtain your desired knife skin in CS2, you must combine 5 Covert skins that belong to CS2 cases that contain it. [[6]]")
        
        return "\n".join(report)

# Example usage and test data
if __name__ == "__main__":
    # Initialize calculator
    calculator = KnifeCalculator()
    
    # Example Covert skin prices (in USD)
    example_prices = {
        "AWP | Dragon Lore": 3500.00,
        "M4A4 | Howl": 1200.00,
        "AK-47 | Fire Serpent": 800.00,
        "Desert Eagle | Blaze": 350.00,
        "AWP | Neo-Noir": 280.00,
        "USP-S | Neo-Noir": 220.00,
        "Glock-18 | Bullet Queen": 180.00,
        "P250 | Wingshot": 150.00,
        "MAC-10 | Neon Rider": 120.00,
        "UMP-45 | Primal Saber": 100.00,
        "M4A1-S | Hyper Beast": 320.00,
        "P90 | Death Grip": 180.00,
        "Five-SeveN | Fowl Play": 95.00,
        "Nova | Hyper Beast": 75.00,
        "PP-Bizon | Osiris": 65.00
    }
    
    # Generate reports
    print(calculator.generate_report())  # General probabilities
    print("\n" + "="*60 + "\n")
    print(calculator.generate_report(knife_name="Karambit", covert_skin_prices=example_prices))  # Karambit specific
    print("\n" + "="*60 + "\n")
    print(calculator.generate_report(knife_name="Butterfly Knife", covert_skin_prices=example_prices, budget=1000))  # With budget analysis
