import requests
import json
import random

class HeliosFreeCrawlerNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "topic": ("STRING", {"default": "nature"}),
                "api_choice": (["pexels", "pixabay", "sample"], {"default": "sample"}),
                "pexels_api_key": ("STRING", {"default": ""}),
                "pixabay_api_key": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "crawl_free"
    CATEGORY = "Helios"

    def crawl_free(self, topic, api_choice, pexels_api_key, pixabay_api_key):
        try:
            if api_choice == "pexels" and pexels_api_key:
                return self._crawl_pexels(topic, pexels_api_key)
            elif api_choice == "pixabay" and pixabay_api_key:
                return self._crawl_pixabay(topic, pixabay_api_key)
            else:
                return self._crawl_sample(topic)
        except Exception as e:
            print(f"Free crawler error: {e}")
            return self._crawl_sample(topic)

    def _crawl_pexels(self, topic, api_key):
        """Crawl Pexels API (free tier available)"""
        url = f"https://api.pexels.com/v1/search?query={topic}&per_page=20"
        headers = {"Authorization": api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])
            crawled_data = []
            for photo in photos:
                item = {
                    "title": photo.get("alt", f"{topic} photo"),
                    "tags": [tag for tag in photo.get("url", "").split("/") if tag],
                    "downloads": random.randint(50, 500),  # Pexels doesn't provide download counts
                    "competition": random.randint(10, 100),
                }
                crawled_data.append(item)
            return (json.dumps(crawled_data),)
        else:
            return self._crawl_sample(topic)

    def _crawl_pixabay(self, topic, api_key):
        """Crawl Pixabay API (free)"""
        url = f"https://pixabay.com/api/?key={api_key}&q={topic}&per_page=20"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            hits = data.get("hits", [])
            crawled_data = []
            for hit in hits:
                item = {
                    "title": hit.get("tags", "").split(", ")[0] if hit.get("tags") else f"{topic} image",
                    "tags": hit.get("tags", "").split(", ") if hit.get("tags") else [topic],
                    "downloads": hit.get("downloads", random.randint(100, 1000)),
                    "competition": hit.get("likes", random.randint(5, 200)),
                }
                crawled_data.append(item)
            return (json.dumps(crawled_data),)
        else:
            return self._crawl_sample(topic)

    def _crawl_sample(self, topic):
        """Fallback sample data when no API is available"""
        sample_data = [
            {"title": f"{topic} landscape", "tags": ["nature", "outdoor", "scenic"], "downloads": random.randint(100, 500), "competition": random.randint(10, 50)},
            {"title": f"{topic} portrait", "tags": ["people", "photography", "portrait"], "downloads": random.randint(50, 300), "competition": random.randint(20, 80)},
            {"title": f"{topic} abstract", "tags": ["art", "design", "abstract"], "downloads": random.randint(200, 800), "competition": random.randint(5, 30)},
            {"title": f"{topic} urban", "tags": ["city", "urban", "architecture"], "downloads": random.randint(150, 600), "competition": random.randint(15, 60)},
            {"title": f"{topic} wildlife", "tags": ["animals", "wildlife", "nature"], "downloads": random.randint(80, 400), "competition": random.randint(25, 90)},
            {"title": f"{topic} food", "tags": ["food", "culinary", "delicious"], "downloads": random.randint(120, 700), "competition": random.randint(30, 100)},
            {"title": f"{topic} technology", "tags": ["tech", "digital", "innovation"], "downloads": random.randint(90, 450), "competition": random.randint(12, 45)},
            {"title": f"{topic} travel", "tags": ["travel", "adventure", "vacation"], "downloads": random.randint(180, 900), "competition": random.randint(8, 40)},
        ]
        # Shuffle and return random subset
        random.shuffle(sample_data)
        return (json.dumps(sample_data[:8]),)