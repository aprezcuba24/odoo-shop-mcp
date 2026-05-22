from enum import Enum


class PushTokenBodyPlatform(str, Enum):
    ANDROID = "android"
    IOS = "ios"

    def __str__(self) -> str:
        return str(self.value)
