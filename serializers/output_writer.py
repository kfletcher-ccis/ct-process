import json
class OutputWriter:
    @staticmethod
    def write_json(payload, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
