import requests
from datetime import datetime

class ArchipelagoAPI:
    # Fall back to archipelago.gg
    def __init__(self, base_url: str = "https://archipelago.gg"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    # GET Request
    def _get(self, endpoint: str) -> dict | list:
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    # POST Request
    def _post(self, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"
        response = self.session.post(url, **kwargs)
        data = response.json()
        if response.status_code >= 400:
            raise ArchipelagoAPIError(
                f"API error {response.status_code}: {data.get('text', data)}"
            )
        return data

    # Datapackage Endpoints
    def get_datapackage(self) -> dict:
        return self._get("/datapackage")

    def get_datapackage_by_checksum(self, checksum: str) -> dict:

        return self._get(f"/datapackage/{checksum}")

    def get_datapackage_checksums(self) -> dict:
        return self._get("/datapackage_checksum")

    # Generation Endpoints
    def generate_from_file(self, file_path: str) -> dict:
        with open(file_path, "rb") as f:
            return self._post("/generate", files={"file": f})

    def generate_from_weights(self, weights: dict) -> dict:
        return self._post("/generate", json={"weights": weights})

    def get_generation_status(self, seed_suuid: str) -> dict:
        url = f"{self.base_url}/api/status/{seed_suuid}"
        response = self.session.get(url)
        return {"status_code": response.status_code, **response.json()}

    def wait_for_generation(self, seed_suuid: str, poll_interval: float = 2.0, timeout: float = 120.0) -> dict:
        import time
        start = time.time()
        while True:
            result = self.get_generation_status(seed_suuid)
            if result["status_code"] == 201:
                return result
            if result["status_code"] in (404, 500):
                raise ArchipelagoAPIError(f"Generation failed: {result.get('text')}")
            if time.time() - start > timeout:
                raise TimeoutError(f"Generation timed out after {timeout}s")
            time.sleep(poll_interval)

    # Room Endpoints
    def get_room_status(self, room_id: str) -> dict:
        return self._get(f"/room_status/{room_id}")

    # Tracker Endpoints
    def get_tracker(self, tracker_id: str) -> dict:
        return self._get(f"/tracker/{tracker_id}")

    def get_static_tracker(self, tracker_id: str) -> dict:
        return self._get(f"/static_tracker/{tracker_id}")

    def get_slot_data_tracker(self, tracker_id: str) -> list:
        return self._get(f"/slot_data_tracker/{tracker_id}")

    # User Endpoints
    def set_session_cookie(self, cookie: str):
        self.session.cookies.set("session", cookie, domain=self.base_url.split("//")[-1])

    def get_rooms(self) -> list:
        return self._get("/get_rooms")

    def get_seeds(self) -> list:
        return self._get("/get_seeds")