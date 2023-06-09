from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def health_check() -> dict:
    return {"status": "healthy"}


@app.get("/processo/{numero}")
def crawl_processo(numero: str) -> dict:
    return {"message": numero}
