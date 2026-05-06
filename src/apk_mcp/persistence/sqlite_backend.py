"""SQLite implementation of :class:`~apk_mcp.persistence.base.DeviceKeyRepository`."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path

import aiosqlite


class SqliteDeviceKeyRepository:
    """Store ``device_key`` per ``persistence_key`` in a local SQLite file."""

    def __init__(self, db_path: Path) -> None:
        self._path = Path(db_path)
        self._init_lock = asyncio.Lock()
        self._ready = False

    async def _ensure_schema(self) -> None:
        if self._ready:
            return
        async with self._init_lock:
            if self._ready:
                return
            self._path.parent.mkdir(parents=True, exist_ok=True)
            async with aiosqlite.connect(self._path) as db:
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS device_keys (
                        persistence_key TEXT PRIMARY KEY,
                        device_key TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                    """
                )
                await db.commit()
            await self._migrate_legacy_client_id_column()
            self._ready = True

    async def _migrate_legacy_client_id_column(self) -> None:
        """Rename legacy ``client_id`` column to ``persistence_key`` if present."""
        try:
            async with aiosqlite.connect(self._path) as db:
                cur = await db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='device_keys'"
                )
                if await cur.fetchone() is None:
                    return
                info_cur = await db.execute("PRAGMA table_info(device_keys)")
                cols = {row[1] for row in await info_cur.fetchall()}
                if "persistence_key" in cols:
                    return
                if "client_id" in cols:
                    await db.execute(
                        "ALTER TABLE device_keys RENAME COLUMN client_id TO persistence_key"
                    )
                    await db.commit()
        except Exception:
            return

    async def get(self, persistence_key: str) -> str | None:
        await self._ensure_schema()
        async with aiosqlite.connect(self._path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute(
                "SELECT device_key FROM device_keys WHERE persistence_key = ?",
                (persistence_key,),
            )
            row = await cur.fetchone()
        if row is None:
            return None
        key = row["device_key"]
        return str(key) if key else None

    async def set(self, persistence_key: str, device_key: str) -> None:
        await self._ensure_schema()
        now = datetime.now(UTC).isoformat()
        async with aiosqlite.connect(self._path) as db:
            await db.execute(
                """
                INSERT INTO device_keys (persistence_key, device_key, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(persistence_key) DO UPDATE SET
                    device_key = excluded.device_key,
                    updated_at = excluded.updated_at
                """,
                (persistence_key, device_key, now),
            )
            await db.commit()

    async def delete(self, persistence_key: str) -> None:
        await self._ensure_schema()
        async with aiosqlite.connect(self._path) as db:
            await db.execute(
                "DELETE FROM device_keys WHERE persistence_key = ?",
                (persistence_key,),
            )
            await db.commit()

    async def aclose(self) -> None:
        return None
