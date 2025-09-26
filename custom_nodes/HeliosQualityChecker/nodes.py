import json
import re

class HeliosQualityCheckerNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompts": ("STRING", {"default": "[]"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "check_quality"
    CATEGORY = "Helios"

    def check_quality(self, prompts):
        try:
            prompts_list = json.loads(prompts)
            checked = []
            for prompt in prompts_list:
                length = len(prompt)
                keyword_density = len(re.findall(r"\b[a-zA-Z]{4,}\b", prompt)) / (length/10)
                quality = 0.3 * (length/100) + 0.7 * keyword_density
                if quality > 0.5:
                    checked.append(prompt)
            return (json.dumps(checked),)
        except Exception as e:
            return (f"Error: {str(e)}",)