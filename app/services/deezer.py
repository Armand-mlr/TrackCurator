import httpx

BASE = "https://api.deezer.com"
TIMEOUT = httpx.Timeout(5.0, connect=3.0)

class DeezerError(Exception):
    pass

async def search(query: str, limit: int = 10) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f"{BASE}/search", params={"q": query, "limit": limit})
            r.raise_for_status()
            data = r.json()
    except httpx.TimeoutException as exc:
        raise DeezerError("Deezer ne repond pas") from exc
    except httpx.HTTPError as exc:
        raise DeezerError("Appel Deezer en echec") from exc

    return [
        {
            "deezer_id": item["id"],
            "titre": item["title"],
            "artiste": item["artist"]["name"],
            "duree_s": item["duration"],
        }
        for item in data.get("data", [])
    ]

async def track_detail(deezer_id: int) -> dict:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f"{BASE}/track/{deezer_id}")
            r.raise_for_status()
            item = r.json()
    except httpx.HTTPError as exc:
        raise DeezerError("Appel Deezer en echec") from exc

    if item.get("error"):
        raise DeezerError("Morceau introuvable chez Deezer")

    bpm = item.get("bpm") or None
    return {
        "deezer_id": item["id"],
        "titre": item["title"],
        "artiste": item["artist"]["name"],
        "duree_s": item.get("duration"),
        "bpm": int(bpm) if bpm else None,
    }

if __name__ == "__main__":
    import asyncio
    from pprint import pprint

    async def main():
        resultat = await search("Daft Punk")
        pprint(resultat)

    asyncio.run(main())