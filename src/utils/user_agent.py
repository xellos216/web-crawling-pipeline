# src/utils/user_agent.py

from __future__ import annotations

import random

from config import USER_AGENTS


def get_random_user_agent() -> str:
    return random.choice(USER_AGENTS)
