import json
from pathlib import Path
from app.models import Deal

DATA_FILE = Path(__file__).parent.parent / "data" / "sample_deals.json"


def load_deals() -> list[Deal]:
    return [Deal.model_validate(item) for item in json.loads(DATA_FILE.read_text())]

