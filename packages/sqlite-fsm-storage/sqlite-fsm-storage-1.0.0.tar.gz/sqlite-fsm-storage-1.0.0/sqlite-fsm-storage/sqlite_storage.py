from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from typing import Optional, Dict, Any
import sqlite3
import json
import ast


class SQLiteStorage(BaseStorage):
    def __init__(self):
        self.connection = sqlite3.connect('fsm-storage.db')
        self.cursor = self.connection.cursor()
        try:
           self.cursor.execute('CREATE TABLE states (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, key TEXT NOT NULL, state TEXT NOT NULL, data TEXT NOT NULL)')
        except sqlite3.OperationalError:
            pass

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        key = f'{key.bot_id}:{key.chat_id}:{key.user_id}:{key.thread_id}:{key.destiny}'
        result = self.cursor.execute('SELECT state FROM states WHERE key = ?', (key,)).fetchone()
        if state is None:
            state = 'NONE'
        if not isinstance(state, str):
            state = state.state
        if result is not None:
            self.cursor.execute('UPDATE `states` SET `state` = ? WHERE `key` = ?', (state, key,))
        else:
            self.cursor.execute('INSERT INTO `states` (`key`, `state`, `data`) VALUES (?,?,?)', (key, state, '{}',))

    async def get_state(self, key: StorageKey) -> Optional[str]:
        key = f'{key.bot_id}:{key.chat_id}:{key.user_id}:{key.thread_id}:{key.destiny}'
        state = self.cursor.execute('SELECT `state` FROM `states` WHERE `key` = ?', (key,)).fetchone()
        if state is not None:
            if state[0] != 'NONE':
                return state[0]
        return None

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        key = f'{key.bot_id}:{key.chat_id}:{key.user_id}:{key.thread_id}:{key.destiny}'
        self.cursor.execute('UPDATE `states` SET `data` = ? WHERE `key` = ?', (json.dumps(data), key,))

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        key = f'{key.bot_id}:{key.chat_id}:{key.user_id}:{key.thread_id}:{key.destiny}'
        data = self.cursor.execute('SELECT `data` FROM `states` WHERE `key` = ?', (key,)).fetchone()
        return ast.literal_eval(data[0])

    async def update_data(self, key: StorageKey, data: Dict[str, Any]) -> Dict[str, Any]:
        current_data = await self.get_data(key=key)
        current_data.update(data)
        await self.set_data(key=key, data=current_data)
        return current_data.copy()

    async def close(self) -> None:
        pass