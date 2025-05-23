"""data_migrate

迁移 ID: ba63ee20dbc1
父迁移: 1ad5a608c9e0
创建时间: 2024-12-23 21:15:55.454261

"""

from __future__ import annotations

import math
from collections.abc import Sequence

from alembic import op
from nonebot.log import logger
from sqlalchemy import insert, inspect, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

revision: str = "ba63ee20dbc1"
down_revision: str | Sequence[str] | None = "1ad5a608c9e0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def data_migrate() -> None:
    conn = op.get_bind()
    insp = inspect(conn)
    table_names = insp.get_table_names()
    if "nonebot_plugin_memes_api_memegenerationrecord" not in table_names:
        return

    Base = automap_base()
    Base.prepare(autoload_with=conn)
    MemeGenerationRecord = Base.classes.nonebot_plugin_memes_api_memegenerationrecord
    MemeGenerationRecordV2 = (
        Base.classes.nonebot_plugin_memes_api_memegenerationrecord_v2
    )

    with Session(conn) as db_session:
        count = db_session.query(MemeGenerationRecord).count()
        if count == 0:
            return

        try:
            from nonebot_session_to_uninfo import check_tables, get_id_map
        except ImportError:
            raise ValueError("请安装 `nonebot-session-to-uninfo` 以迁移数据")

        check_tables()

        migration_limit = 10000  # 每次迁移的数据量为 10000 条
        last_message_id = -1
        id_map: dict[int, int] = {}

        logger.warning("memes-api: 正在迁移数据，请不要关闭程序...")

        for i in range(math.ceil(count / migration_limit)):
            statement = (
                select(
                    MemeGenerationRecord.id,
                    MemeGenerationRecord.session_persist_id,
                    MemeGenerationRecord.time,
                    MemeGenerationRecord.meme_key,
                )
                .order_by(MemeGenerationRecord.id)
                .where(MemeGenerationRecord.id > last_message_id)
                .limit(migration_limit)
            )
            records = db_session.execute(statement).all()
            last_message_id = records[-1][0]

            session_ids = [record[1] for record in records if record[1] not in id_map]
            if session_ids:
                id_map.update(get_id_map(session_ids))

            bulk_insert_records = []
            for record in records:
                bulk_insert_records.append(
                    {
                        "id": record[0],
                        "session_persist_id": id_map[record[1]],
                        "time": record[2],
                        "meme_key": record[3],
                    }
                )
            db_session.execute(insert(MemeGenerationRecordV2), bulk_insert_records)
            logger.info(
                f"memes-api: 已迁移 {i * migration_limit + len(records)}/{count}"
            )

        db_session.commit()

        logger.warning("memes-api: 数据迁移完成！")


def upgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    data_migrate()
    # ### end Alembic commands ###


def downgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
