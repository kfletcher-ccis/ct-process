import json
from dataclasses import asdict, is_dataclass

class ConstituentSerializer:
    @staticmethod
    def constituent_to_dict(constituent):
        if is_dataclass(constituent):
            return asdict(constituent)
        raise TypeError(f"Unsupported type: {type(constituent)}")

    @staticmethod
    def constituents_to_dict(constituents):
        return {lookup_id: ConstituentSerializer.constituent_to_dict(c) for lookup_id, c in constituents.items()}

    @staticmethod
    def write_json(constituents, output_file):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(ConstituentSerializer.constituents_to_dict(constituents), f, indent=2, ensure_ascii=False)
