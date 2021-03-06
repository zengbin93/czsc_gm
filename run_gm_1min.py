# coding: utf-8
import traceback
from src.gm_utils import *
from src import conf
from src.log import create_logger

set_gm_token(conf.gm_token)

def adjust_position(context, symbol):
    bars = context.data(symbol=symbol, frequency='60s', count=100, fields='symbol,eob,open,close,high,low,volume')
    trader = context.symbols_map[symbol]['trader']
    bars = format_kline(bars)
    bars_new = [x for x in bars if x.dt > trader.kg.end_dt]
    if bars_new:
        trader.update_factors(bars_new)
    context.symbols_map[symbol]['trader'] = trader

    last_bar = bars[-1]
    if last_bar.dt.minute % 30 == 0:
        print("{} - {} - {}".format(trader.s['symbol'], trader.s['dt'], trader.s['close']))
        if context.mode != MODE_BACKTEST:
            take_snapshot(context, trader, name='快照')

    exchange = symbol.split(".")[0]
    if exchange in ["SZSE", "SHSE"]:
        adjust_share_position(context, symbol, trader)
    else:
        adjust_future_position(context, symbol, trader)


def init(context):
    data_path = conf.data_path
    context.wx_key = conf.wx_token
    context.share_id = conf.share_account_id   # 股票账户ID
    context.future_id = conf.future_account_id  # 期货账户ID

    cache_path = os.path.join(data_path, "cache")
    if not os.path.exists(data_path):
        os.makedirs(cache_path)
    context.logger = create_logger(os.path.join(data_path, "backtest.log"), cmd=True, name="gm")
    context.data_path = data_path
    context.cache_path = cache_path
    context.file_orders = os.path.join(data_path, "orders.txt")

    # 交易因子定义
    long_open_factors = ['日线笔因子@C6C5C3L1A0~次级别三买',
                         '日线笔因子@C6C5C3L1A1~次级别三买&次级别近五笔高点等于近九笔高点',
                         '日线笔因子@C6C5C3L1A2~次级别三买&次级别近五笔低点等于近九笔低点',
                         '日线笔因子@C6C4C2L1A0~次级别三买',
                         '日线笔因子@C6C4C2L1A1~次级别三买&次级别近五笔高点等于近九笔高点',
                         '日线笔因子@C6C4C2L1A2~次级别三买&次级别近五笔低点等于近九笔低点',
                         '日线笔因子@C6C3C1L1A0~次级别三买',
                         '日线笔因子@C6C3C1L1A1~次级别三买&次级别近五笔高点等于近九笔高点',
                         '日线笔因子@C6C3C1L1A2~次级别三买&次级别近五笔低点等于近九笔低点',
                         '日线笔因子@C6C5C3L1B0~本级别第N笔强底分&小级别近七笔为BaA式右侧底',
                         '日线笔因子@C6C5C3L1B1~本级别第N笔强底分&小级别近七笔为BaA式右侧底&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C4C2L1B0~本级别第N笔强底分&小级别近七笔为BaA式右侧底',
                         '日线笔因子@C6C4C2L1B1~本级别第N笔强底分&小级别近七笔为BaA式右侧底&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C3C1L1B0~本级别第N笔强底分&小级别近七笔为BaA式右侧底',
                         '日线笔因子@C6C3C1L1B1~本级别第N笔强底分&小级别近七笔为BaA式右侧底&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C5C3L1C0~本级别第N笔强底分&次级别近五笔为上颈线突破',
                         '日线笔因子@C6C4C2L1C0~本级别第N笔强底分&次级别近五笔为上颈线突破',
                         '日线笔因子@C6C3C1L1C0~本级别第N笔强底分&次级别近五笔为上颈线突破',
                         '日线笔因子@C6C5C3L2A1~次级别近五笔为底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C4C2L2A1~次级别近五笔为底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C3C1L2A1~次级别近五笔为底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C5C3L2B1~次级别近七笔为底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C4C2L2B1~次级别近七笔为底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C3C1L2B1~次级别近七笔为底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C5C3L2C2~次级别近九笔为底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C5C3L2C3~次级别近九笔为aAbBc式底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C4C2L2C2~次级别近九笔为底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C4C2L2C3~次级别近九笔为aAbBc式底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C3C1L2C2~次级别近九笔为底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C3C1L2C3~次级别近九笔为aAbBc式底背弛&小级别近五笔为上颈线突破',
                         '日线笔因子@C6C5C3L3A0~60分钟近七笔为BaA式右侧底',
                         '日线笔因子@C6C4C2L3A0~30分钟近七笔为BaA式右侧底',
                         '日线笔因子@C6C3C1L3A0~15分钟近七笔为BaA式右侧底',
                         '日线笔因子@C6C5C3L3B0~60分钟近五笔为上颈线突破',
                         '日线笔因子@C6C4C2L3B0~30分钟近五笔为上颈线突破',
                         '日线笔因子@C6C3C1L3B0~15分钟近五笔为上颈线突破']

    long_close_factors = ['日线笔因子@C6C5C3S1A1~次级别三卖&小级别下颈线跌破',
                          '日线笔因子@C6C4C2S1A1~次级别三卖&小级别下颈线跌破',
                          '日线笔因子@C6C3C1S1A1~次级别三卖&小级别下颈线跌破',
                          '日线笔因子@C6C5C3S1B1~次级别和小级别近五笔都为下颈线跌破',
                          '日线笔因子@C6C4C2S1B1~次级别和小级别近五笔都为下颈线跌破',
                          '日线笔因子@C6C3C1S1B1~次级别和小级别近五笔都为下颈线跌破',
                          '日线笔因子@C6C5C3S2A1~次级别顶背弛&小级别下颈线跌破',
                          '日线笔因子@C6C4C2S2A1~次级别顶背弛&小级别下颈线跌破',
                          '日线笔因子@C6C3C1S2A1~次级别顶背弛&小级别下颈线跌破',
                          '日线笔因子@C6C5C3S3A1~次级别下颈线跌破&小级别下颈线跌破',
                          '日线笔因子@C6C4C2S3A1~次级别下颈线跌破&小级别下颈线跌破',
                          '日线笔因子@C6C3C1S3A1~次级别下颈线跌破&小级别下颈线跌破',
                          '日线笔因子@C6C5C3S4A0~小级别顶背驰',
                          '日线笔因子@C6C4C2S4A0~小级别顶背驰',
                          '日线笔因子@C6C3C1S4A0~小级别顶背驰']

    if context.mode == MODE_BACKTEST:
        # mp 小于1，按百分比下单
        symbols_map = {
            # "SHSE.603027": {"mp": 0.8, "factors": {"long_open_factors": long_open_factors,
            #                                        "long_close_factors": long_close_factors,
            #                                        "version": "603027@2021-02-17"}},
            # "SZSE.002739": {"mp": 0.8, "factors": {"long_open_factors": long_open_factors,
            #                                        "long_close_factors": long_close_factors,
            #                                        "version": "603027@2021-02-17"}},
            "SZSE.002588": {"mp": 0.8, "factors": {"long_open_factors": long_open_factors,
                                                   "long_close_factors": long_close_factors,
                                                   "version": "002588@2021-02-17"}},
        }

    subscribe(",".join(symbols_map.keys()), frequency='60s', count=300, wait_group=False)

    if context.mode == MODE_BACKTEST:
        context.logger.info("回测配置：")
        context.logger.info("backtest_start_time = " + str(context.backtest_start_time))
        context.logger.info("backtest_end_time = " + str(context.backtest_end_time))
    else:
        context.logger.info("\n\n")
        context.logger.info("=" * 88)
        context.logger.info("实盘开始 ...")

    for symbol in symbols_map.keys():
        kg = get_init_kg(context, symbol, generator=KlineGeneratorBy1Min, max_count=1000)
        trader = GmTrader(kg, factors=symbols_map[symbol]["factors"])
        symbols_map[symbol]['trader'] = trader
        context.logger.info("{} 初始化完成，当前时间：{}".format(symbol, trader.end_dt))

    context.logger.info(f"交易配置：{symbols_map}")
    context.symbols_map = symbols_map

def on_bar(context, bars):
    context.unfinished_orders = get_unfinished_orders()

    for bar in bars:
        symbol = bar['symbol']
        try:
            adjust_position(context, symbol)
        except:
            traceback.print_exc()

    if context.now.minute == 58 and context.now.hour == 14 and context.mode == MODE_BACKTEST:
        report_account_status(context)


if __name__ == '__main__':
    # run(strategy_id='3d7bd7d2-2733-11eb-a40d-3cf0110437a2',
    #     mode=MODE_LIVE,
    #     filename='run_gm_1min.py',
    #     token='15bd09a572bff415a52b60001504f0a2dc38fa6e')

    run(filename='run_gm_1min.py',
        token='15bd09a572bff415a52b60001504f0a2dc38fa6e',
        strategy_id='add4163e-1825-11eb-a4e8-3cf0110437a2',
        mode=MODE_BACKTEST,
        backtest_start_time='2020-01-01 08:30:00',
        backtest_end_time='2020-12-31 15:30:00',
        backtest_initial_cash=100000000,
        backtest_transaction_ratio=1,
        backtest_commission_ratio=0.001,
        backtest_slippage_ratio=0,
        backtest_adjust=ADJUST_PREV,
        backtest_check_cache=1)

