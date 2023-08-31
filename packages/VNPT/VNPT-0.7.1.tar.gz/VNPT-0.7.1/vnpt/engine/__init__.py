'''
建立连接 - 引擎
'''
from sqlalchemy import create_engine
from engine.config import Config
from sqlalchemy.orm import sessionmaker


def get_engine(config:Config):
    engine = create_engine(
        url=config.url,
        echo=config.echo,  # 是不是要把所执行的SQL打印出来，一般用于调试
        pool_size=config.pool_size,  # 连接池大小
        max_overflow=config.max_overflow,  # 连接池最大的大小
    )
    return engine

engine = get_engine(Config())

Session = sessionmaker(bind=engine)