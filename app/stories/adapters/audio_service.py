import requests
import re


class AudioService:
    def __init__(self, api_key, api_userid):
        self.api_key = api_key
        self.api_userid = api_userid

    def text_to_speach(self, text):
        audio_url = "https://play.ht/api/v2/tts"

        payload = {
            "text": text,
            "voice": "larry",
            "quality": "medium",
            "output_format": "mp3",
            "speed": 1,
            "sample_rate": 24000,
            "seed": None,
            "temperature": None
        }

        headers = {
            "accept": "text/event-stream",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-User-Id": f"{self.api_userid}"
        }

        response = requests.post(audio_url, json=payload, headers=headers)

        match = re.search(r'"url":"(.*?)"', response.text)
        url_aud = match.group(1)
        return url_aud