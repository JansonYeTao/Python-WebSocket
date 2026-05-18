from fastapi import FastAPI, Query


app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items/{item_id}")
async def get_item(item_id: int) -> dict[str, int | str]:
    return {"item_id": item_id, "name": f"item-{item_id}", "status": "ok"}


@app.get("/poll")
async def poll(payload: str = Query(default="")) -> dict[str, str]:
    return {"reversed_data": payload[::-1], "status": "ok"}
