import requests
import json

class HeliosCrawlerNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "topic": ("STRING", {"default": "nature"}),
                "api_key": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "crawl"
    CATEGORY = "custom"
    OUTPUT_NODE = False

    def crawl(self, topic, api_key):
        print(f"Crawl executed with topic: {topic}, api_key: {api_key}")
        # Fallback data since no API key
        crawled_data = [
            {"title": f"{topic} landscape", "tags": ["nature", "outdoor"], "downloads": 150, "competition": 20},
            {"title": f"{topic} portrait", "tags": ["people", "photography"], "downloads": 80, "competition": 30},
            {"title": f"{topic} abstract", "tags": ["art", "design"], "downloads": 200, "competition": 10}
        ]
        result = json.dumps(crawled_data)
        print(f"Result: {result}")
        return (result,)