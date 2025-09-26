import google.generativeai as genai
import pinecone
import json
import random

class HeliosPromptGeneratorNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trend_data": ("STRING", {"default": "[]"}),
                "api_key": ("STRING", {"default": ""}),
                "pinecone_api_key": ("STRING", {"default": ""}),
                "backend": ("STRING", {"default": "gemini"}),  # gemini or ollama
                "ollama_url": ("STRING", {"default": "http://localhost:11434"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Helios"

    def generate(self, trend_data, api_key, pinecone_api_key, backend, ollama_url):
        try:
            # Parse trend analysis data
            try:
                trend_info = json.loads(trend_data)
                top_themes = trend_info.get('top_themes', [])
                trend_insights = trend_info.get('trend_insights', '')

                if top_themes:
                    # Use actual trend data to generate prompts
                    return self._generate_trend_based_prompts(top_themes, trend_insights, api_key, backend, ollama_url)
                else:
                    # Fallback to template generation
                    return self._generate_template_prompts("general trends", api_key, backend, ollama_url)

            except json.JSONDecodeError:
                # If not JSON, treat as topic string
                return self._generate_template_prompts(trend_data or "trends", api_key, backend, ollama_url)

        except Exception as e:
            print(f"Prompt generation error: {e}")
            return self._generate_template_prompts("trends", "", "template", "")

    def _generate_trend_based_prompts(self, top_themes, trend_insights, api_key, backend, ollama_url):
        """Generate prompts based on actual trend analysis"""
        prompts = []

        # Extract top 5 themes
        themes = [t.get('theme', 'trends') for t in top_themes[:5]]

        for i in range(min(100, len(themes) * 20)):  # Generate up to 100 prompts
            theme = random.choice(themes)

            # Use AI if available, otherwise use templates
            if backend == "gemini" and api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt_template = f"Create a professional image generation prompt about '{theme}' that incorporates current trends. Make it detailed and suitable for AI art generation. Focus on visual appeal and artistic quality."
                    response = model.generate_content(prompt_template)
                    prompt = response.text.strip()
                except:
                    prompt = self._create_trend_prompt(theme, trend_insights)
            elif backend == "ollama":
                try:
                    import requests
                    prompt_template = f"Create a professional image generation prompt about '{theme}' that incorporates current trends. Make it detailed and suitable for AI art generation."
                    response = requests.post(f"{ollama_url}/api/generate", json={"model": "gemma3:4b", "prompt": prompt_template})
                    prompt = response.json()["response"].strip()
                except:
                    prompt = self._create_trend_prompt(theme, trend_insights)
            else:
                prompt = self._create_trend_prompt(theme, trend_insights)

            prompts.append(prompt)

        # Remove duplicates and limit to 100
        unique_prompts = list(set(prompts))[:100]
        print(f"Generated {len(unique_prompts)} trend-based prompts")
        return (json.dumps(unique_prompts),)

    def _create_trend_prompt(self, theme, trend_insights):
        """Create a trend-aware prompt using templates"""
        styles = [
            "photorealistic", "artistic", "minimalist", "cinematic", "abstract",
            "vintage", "modern", "surreal", "documentary", "studio"
        ]

        style = random.choice(styles)

        if "rising" in trend_insights.lower():
            trend_modifier = "trending contemporary"
        elif "popular" in trend_insights.lower():
            trend_modifier = "popular modern"
        else:
            trend_modifier = "timeless classic"

        templates = [
            f"Professional {style} photograph of {theme}, {trend_modifier} style, high quality, detailed composition, artistic lighting",
            f"Creative {style} image featuring {theme}, contemporary trends, professional quality, detailed and artistic",
            f"Artistic {style} composition of {theme}, modern aesthetic, high resolution, professional photography",
            f"Stunning {style} depiction of {theme}, trending design, professional quality, detailed and refined",
            f"Beautiful {style} image of {theme}, current trends, professional composition, high quality details"
        ]

        return random.choice(templates)

    def _generate_template_prompts(self, topic, api_key, backend, ollama_url):
        """Fallback template generation"""
        prompts = []
        for i in range(50):  # Generate 50 fallback prompts
            prompt = self._generate_template_prompt(topic, random.choice(["realistic", "artistic", "minimalist"]))
            prompts.append(prompt)

        unique_prompts = list(set(prompts))
        print(f"Generated {len(unique_prompts)} template-based prompts")
        return (json.dumps(unique_prompts),)

    def get_embedding(self, text):
        # Placeholder, use sentence-transformers or similar
        return [0.0] * 384  # dummy

    def _generate_template_prompt(self, topic, style):
        """Generate realistic prompts using templates when no API is available"""
        templates = {
            "realistic": [
                f"A highly detailed, realistic photograph of {topic}, professional studio lighting, sharp focus, 8K resolution, photorealistic",
                f"Realistic image of {topic} in natural environment, lifelike details, natural lighting, high resolution photography",
                f"Photorealistic depiction of {topic}, ultra-detailed, professional quality, natural colors, sharp focus"
            ],
            "artistic": [
                f"Artistic interpretation of {topic} in the style of impressionist painting, vibrant colors, brush strokes, artistic composition",
                f"Creative artistic rendering of {topic}, abstract elements, bold colors, artistic lighting, contemporary art style",
                f"Artistic portrait of {topic} with dramatic lighting, artistic composition, creative color palette, fine art photography"
            ],
            "minimalist": [
                f"Minimalist composition featuring {topic}, clean lines, simple background, essential elements only, monochromatic",
                f"Minimalist design with {topic} as focal point, negative space, clean aesthetic, simple geometric forms",
                f"Minimalist still life of {topic}, clean background, essential shapes, balanced composition, subtle details"
            ]
        }

        style_templates = templates.get(style, templates["realistic"])
        return random.choice(style_templates)