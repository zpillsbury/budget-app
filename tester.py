from pprint import pp

import anyio
import httpx

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImI4Y2FjOTViNGE1YWNkZTBiOTY1NzJkZWU4YzhjOTVlZWU0OGNjY2QiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vYnVkZ2V0LTE0NTRiIiwiYXVkIjoiYnVkZ2V0LTE0NTRiIiwiYXV0aF90aW1lIjoxNzMxMDAwOTU3LCJ1c2VyX2lkIjoiYmMzZUE4S01BUWIzOUt0Y0VHR0xVTmxFUTRSMiIsInN1YiI6ImJjM2VBOEtNQVFiMzlLdGNFR0dMVU5sRVE0UjIiLCJpYXQiOjE3MzEwMDA5NTcsImV4cCI6MTczMTAwNDU1NywiZW1haWwiOiJ6cGlsbHNidXJ5OThAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInpwaWxsc2J1cnk5OEBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.yzDiyjmtFTcajy3z9sMAlnD57iMO6ad8iyjqEZy3rB_JchxnJ6DHwFN5yjR3XDMHof6oL6XwkSzX7lSfCjy0KExZH_3RZZky9MsCSFEM103bw7GIlccaXzVgsRFSiqdt89fCubgt3Vt3WuBVgI4NuzbOK4cx602avudfXkcX5JabeQ8GBFEk7zh2iqw1uzTIQIdL29CFTMsymFwEeBMgjmvAVX5PAoKKHvcuHxlI-f3KiwrixIJvxf47gYczM6fPB51YrX8DStquVaQUnFgozmCRAoFxvWFmKGR5Gx7bSjezbSMaXLmwOH4MxjEAIknWVGvRHMWgmLEg7ftlQqJCng"  # noqa: E501


async def get_budgets() -> None:
    """
    Get budget
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL}/v1/budgets", headers={"Authorization": f"Bearer {TOKEN}"}
        )
        print(r.status_code)

        if r.is_success:
            data = r.json()
            pp(data)


async def add_budget() -> None:
    """
    Add budget
    """
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BASE_URL}/v1/budgets",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={"total": 2438, "category": "food", "name": "house"},
        )
        print(r.status_code)

        if r.is_success:
            data = r.json()
            pp(data)


async def main() -> None:
    """
    testing api calls
    """
    # await get_budgets()
    await add_budget()


if __name__ == "__main__":
    anyio.run(main)
