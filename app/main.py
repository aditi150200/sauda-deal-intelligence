from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.engine import assess_deal
from app.models import Assessment, Deal, DealView
from app.store import load_deals

app = FastAPI(
    title="Sauda Deal Intelligence API",
    description="Explainable revenue-risk scoring across CRM, CPQ, and ERP signals.",
    version="1.0.0",
)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/deals", response_model=list[DealView])
def list_deals() -> list[DealView]:
    return [DealView(deal=deal, assessment=assess_deal(deal)) for deal in load_deals()]


@app.get("/api/deals/{deal_id}", response_model=DealView)
def get_deal(deal_id: str) -> DealView:
    deal = next((item for item in load_deals() if item.id == deal_id), None)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return DealView(deal=deal, assessment=assess_deal(deal))


@app.post("/api/assess", response_model=Assessment)
def assess(deal: Deal) -> Assessment:
    return assess_deal(deal)

