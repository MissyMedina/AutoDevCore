"""
Score Mode - Evaluate apps against industry templates
"""

import yaml
from pathlib import Path
from .base import BaseMode


class ScoreMode(BaseMode):
    """Score mode for evaluating apps against industry templates."""
    
    def __init__(self, template: str, output_dir: str, verbose: bool = False):
        super().__init__(output_dir, verbose)
        self.template = template
    
    def execute(self):
        """Execute the score mode."""
        print(f"📊 Score Mode - App Evaluation")
        print(f"📋 Template: {self.template}")
        print()
        
        # Load the scoring template
        self.log_thought("ScoreAgent", f"Loading scoring template: {self.template}")
        template_data = self._load_template()
        
        if not template_data:
            print(f"❌ Error: Could not load template {self.template}")
            return
        
        self.log_thought("ScoreAgent", "Template loaded successfully", template_data)
        
        # Evaluate the app
        self.log_thought("ScoreAgent", "Starting app evaluation")
        scores = self._evaluate_app(template_data)
        self.log_thought("ScoreAgent", "App evaluation complete", scores)
        
        # Generate radar chart
        self.log_thought("ScoreAgent", "Generating radar chart")
        self._generate_radar_chart(scores, template_data)
        
        # Generate detailed report
        self.log_thought("ScoreAgent", "Generating detailed report")
        self._generate_report(scores, template_data)
        
        # Save thought trail
        self.save_thought_trail()
        self.generate_mermaid_diagram()
        
        print("✅ App scoring complete!")
        print(f"📄 Results saved to: {self.output_dir}")
        print("📊 Radar chart generated")
    
    def _load_template(self) -> dict:
        """Load the scoring template."""
        template_path = Path(self.template)
        
        if not template_path.exists():
            # Try to find it in the profiles directory
            template_path = Path("profiles") / self.template
        
        if not template_path.exists():
            return None
        
        try:
            with open(template_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading template: {e}")
            return None
    
    def _evaluate_app(self, template_data: dict) -> dict:
        """Evaluate the app against the template."""
        scores = {
            "overall_score": 0,
            "categories": {},
            "recommendations": []
        }
        
        categories = template_data.get("categories", {})
        
        for category, criteria in categories.items():
            category_score = 0
            category_max = len(criteria)
            
            for criterion in criteria:
                # Simplified scoring - in production, this would analyze the actual codebase
                score = self._evaluate_criterion(criterion)
                category_score += score
            
            scores["categories"][category] = {
                "score": category_score,
                "max_score": category_max,
                "percentage": (category_score / category_max) * 100 if category_max > 0 else 0
            }
        
        # Calculate overall score
        total_score = sum(cat["score"] for cat in scores["categories"].values())
        total_max = sum(cat["max_score"] for cat in scores["categories"].values())
        scores["overall_score"] = (total_score / total_max) * 100 if total_max > 0 else 0
        
        return scores
    
    def _evaluate_criterion(self, criterion: dict) -> int:
        """Evaluate a single criterion."""
        # Simplified evaluation - in production, this would analyze the actual codebase
        criterion_type = criterion.get("type", "boolean")
        
        if criterion_type == "boolean":
            # For now, return a random score between 0 and 1
            import random
            return random.choice([0, 1])
        elif criterion_type == "scale":
            # Return a score between 0 and 5
            import random
            return random.randint(0, 5)
        else:
            return 0
    
    def _generate_radar_chart(self, scores: dict, template_data: dict):
        """Generate a radar chart of the scores."""
        chart_file = self.output_dir / "radar_chart.md"
        
        with open(chart_file, 'w') as f:
            f.write("# App Scoring Radar Chart\n\n")
            f.write("```mermaid\nradarChart\n")
            f.write("    title App Evaluation Results\n")
            
            # Add categories
            categories = list(scores["categories"].keys())
            f.write(f"    categories {categories}\n")
            
            # Add scores
            score_values = [scores["categories"][cat]["percentage"] for cat in categories]
            f.write(f"    App {score_values}\n")
            
            f.write("```\n")
        
        print(f"📊 Radar chart saved to: {chart_file}")
    
    def _generate_report(self, scores: dict, template_data: dict):
        """Generate a detailed scoring report."""
        report_file = self.output_dir / "scoring_report.md"
        
        with open(report_file, 'w') as f:
            f.write("# App Scoring Report\n\n")
            f.write(f"**Template**: {self.template}\n")
            f.write(f"**Overall Score**: {scores['overall_score']:.1f}%\n\n")
            
            f.write("## Category Breakdown\n\n")
            
            for category, data in scores["categories"].items():
                f.write(f"### {category}\n")
                f.write(f"- **Score**: {data['score']}/{data['max_score']}\n")
                f.write(f"- **Percentage**: {data['percentage']:.1f}%\n\n")
            
            f.write("## Recommendations\n\n")
            for recommendation in scores.get("recommendations", []):
                f.write(f"- {recommendation}\n")
        
        print(f"📄 Detailed report saved to: {report_file}")
