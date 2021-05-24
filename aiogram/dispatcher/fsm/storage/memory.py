from asyncio import Lock
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, DefaultDict, Dict, Optional

from aiogram.dispatcher.fsm.state import State
from aiogram.dispatcher.fsm.storage.base import BaseStorage, StateType


@dataclass
class MemoryStorageRecord:
    data: Dict[str, Any] = field(default_factory=dict)
    state: Optional[str] = None
    lock: Lock = field(default_factory=Lock)


class MemoryStorage(BaseStorage):
    def __init__(self) -> None:
        self.storage: DefaultDict[int, DefaultDict[int, MemoryStorageRecord]] = defaultdict(
            lambda: defaultdict(MemoryStorageRecord)
        )

    @asynccontextmanager
    async def lock(self, chat_id: int, user_id: int) -> AsyncGenerator[None, None]:
        async with self.storage[chat_id][user_id].lock:
            yield None

    async def set_state(self, chat_id: int, user_id: int, state: StateType = None) -> None:
        self.storage[chat_id][user_id].state = state.state if isinstance(state, State) else state

    async def get_state(self, chat_id: int, user_id: int) -> Optional[str]:
        return self.storage[chat_id][user_id].state

    async def set_data(self, chat_id: int, user_id: int, data: Dict[str, Any]) -> None:
        self.storage[chat_id][user_id].data = data.copy()

    async def get_data(self, chat_id: int, user_id: int) -> Dict[str, Any]:
        return self.storage[chat_id][user_id].data.copy()
