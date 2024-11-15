import requests
import base64
import io
from app.settings import PINATA_API_KEY, PINATA_API_SECRET


class PinataClient:
    def __init__(self):
        self.base_url = "https://api.pinata.cloud"
        self.api_key = PINATA_API_KEY
        self.api_secret = PINATA_API_SECRET

    def _get_headers(self):
        return {
            "pinata_api_key": self.api_key,
            "pinata_secret_api_key": self.api_secret,
        }

    def upload_image(self, base64_image, file_name: str):
        image_data = base64.b64decode(base64_image)
        file_stream = io.BytesIO(image_data)
        files = {"file": (file_name, file_stream)}
        url = f"{self.base_url}/pinning/pinFileToIPFS"
        response = requests.post(
            url, files=files, headers=self._get_headers(), timeout=15
        )
        response.raise_for_status()
        return response.json()["IpfsHash"]
