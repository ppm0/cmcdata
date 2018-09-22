import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cmc_model import Base

cfg = json.loads(open('config.json').read())

engine = create_engine(cfg['db'], echo=False)  # , pool_size=20, max_overflow=100
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()
    session.execute('create index if not exists ix_gth_ts_token on gth(ts, token)')
    session.execute('create index if not exists ix_gth_token_ts on gth(token, ts)')
    session.commit()
