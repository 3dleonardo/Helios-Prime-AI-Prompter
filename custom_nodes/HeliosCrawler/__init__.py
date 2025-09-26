import requests
from .nodes import HeliosCrawlerNode

NODE_CLASS_MAPPINGS = {
    "HeliosCrawler": HeliosCrawlerNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HeliosCrawler": "Helios Crawler Agent",
}