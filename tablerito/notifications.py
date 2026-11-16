import logging
import time
from dataclasses import asdict, dataclass

import requests

from tablerito import config

log = logging.getLogger(__name__)


@dataclass
class Notification:
    message: str


class NotificationClient:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key

    # Makes sure the notification service is up before taking requests
    def wait_until_available(self, attempts: int = 5) -> None:
        for attempt in range(1, attempts + 1):
            try:
                requests.get(self.url, timeout=2)
                return
            except requests.RequestException:
                log.warning("Notification service not available (attempt %d of %d)", attempt, attempts)
                time.sleep(2)
        log.warning("Starting without the notification service")

    def send(self, notification: Notification) -> None:
        response = requests.post(
            self.url,
            json=asdict(notification),
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=5,
        )
        response.raise_for_status()


notifications = NotificationClient(config.NOTIFICATIONS_URL, config.NOTIFICATIONS_API_KEY)


def notify(notification: Notification) -> None:
    if config.ENVIRONMENT == "production":
        notifications.send(notification)
    else:
        log.info("Simulated notification: %s", notification)
