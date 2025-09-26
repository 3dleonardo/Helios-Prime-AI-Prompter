import json
from datetime import datetime
import os

class HeliosFileWriterNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompts": ("STRING", {"default": "[]"}),
                "filename": ("STRING", {"default": datetime.now().strftime("%Y-%m-%d.txt")}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "write_file"
    CATEGORY = "Helios"
    OUTPUT_NODE = True

    def write_file(self, prompts, filename):
        try:
            # Generate unique filename with timestamp if filename is default
            if filename == datetime.now().strftime("%Y-%m-%d.txt"):
                # Create prompts directory if it doesn't exist
                os.makedirs("prompts", exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"prompts/prompts_{timestamp}.txt"

            prompts_list = json.loads(prompts)
            with open(filename, "w", encoding="utf-8") as f:
                for prompt in prompts_list:
                    f.write(prompt + "\n")
            result = f"File saved: {filename} with {len(prompts_list)} prompts"
            print(result)
            return ()
        except Exception as e:
            error = f"Error: {str(e)}"
            print(error)
            return ()