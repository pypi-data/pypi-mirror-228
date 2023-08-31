from typing import Optional

from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.event import Sender

from .base import SubjectExtractor
from ...utils.superuser import is_superuser


class OneBotV11SubjectExtractor(SubjectExtractor[Bot, Event]):
    @classmethod
    def bot_type(cls) -> str:
        return 'OneBot V11'

    def extract(self, bot: Bot, event: Event):
        li = []

        user_id = getattr(event, "user_id", None)
        group_id = getattr(event, "group_id", None)

        if group_id is not None:
            li.append(f"qq:g{group_id}:{user_id}")
            li.append(f"onebot:g{group_id}:{user_id}")
            li.append(f"qq:{user_id}")
            li.append(f"onebot:{user_id}")

            if is_superuser(user_id, bot.type):
                li.append("superuser")

            li.append(f"qq:g{group_id}")
            li.append(f"onebot:g{group_id}")

            sender: Optional[Sender] = getattr(event, "sender", None)
            if sender is not None:
                if sender.role == 'owner':
                    li.append(f"qq:g{group_id}.group_owner")
                    li.append(f"qq:group_owner")

                if sender.role == 'owner' or sender.role == 'admin':
                    li.append(f"qq:g{group_id}.group_admin")
                    li.append(f"qq:group_admin")

            li.append("qq:group")
            li.append("onebot:group")
        elif user_id is not None:
            li.append(f"qq:{user_id}")
            li.append(f"onebot:{user_id}")

            if is_superuser(user_id, bot.type):
                li.append("superuser")

            li.append("qq:private")
            li.append("onebot:private")

        li.append("qq")
        li.append("onebot")
        li.append("all")

        return li
