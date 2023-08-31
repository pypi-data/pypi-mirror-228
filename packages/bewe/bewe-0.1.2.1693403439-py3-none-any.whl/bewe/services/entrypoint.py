from absl import app
from absl import flags
from absl import logging

from bewe.services.databases import asset_orm
from bewe.services.crawler import finmind_downloader
import enum


class Mode(enum.Enum):
    INCR_FETCH_PRICE = 1
    UPDATE_STOCK_LIST = 2
    DELETE_CREATE_DB = 3


_mode = flags.DEFINE_enum_class(
    name='mode',
    default='INCR_FETCH_PRICE',
    enum_class=Mode,
    help='Decide which mode for this execution.'
)
_inc_count = flags.DEFINE_integer(
    name='inc_count',
    default=50,
    help='Setting how many stocks should be updated at this run.'
)


def main(argv):
    parameters = ' '.join(argv)
    logging.info(f'[Parameters] {parameters}')

    if _mode.value == Mode.INCR_FETCH_PRICE:
        logging.info('[Execution] executing fetch price.')
        fn = finmind_downloader.FinmindWrapper()
        fn.incremental_get_stock_price(limit=_inc_count.value)
        return

    if _mode.value == Mode.UPDATE_STOCK_LIST:
        logging.info('[Execution] executing update stock list.')
        fn = finmind_downloader.FinmindWrapper()
        fn.get_tw_stock_info()
        return

    if _mode.value == Mode.DELETE_CREATE_DB:
        logging.info('[Execution] executing delete create db.')
        asset_orm.delete_all()
        asset_orm.create_all()
        return

    logging.warning(f'[Execution] out of scope parameter: {_mode.value}')
    return


if __name__ == '__main__':
    app.run(main)
