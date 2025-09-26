import git
import json

class HeliosKnowledgeBaseNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "new_examples": ("STRING", {"default": "[]"}),
                "file_path": ("STRING", {"default": "datasets-prompt-library.md"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "update_kb"
    CATEGORY = "Helios"

    def update_kb(self, new_examples, file_path):
        try:
            examples = json.loads(new_examples)
            with open(file_path, "a", encoding="utf-8") as f:
                for ex in examples:
                    f.write(ex + "\n")
            repo = git.Repo(".")
            repo.git.add(file_path)
            repo.git.commit(m=f"Update KB with new examples")
            return (f"Knowledge base updated and committed.",)
        except Exception as e:
            return (f"Error: {str(e)}",)