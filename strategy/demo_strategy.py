from vnpy.app.cta_strategy import CtaTemplate, BarGenerator,ArrayManager
from vnpy.trader.object import BarData
from typing import Any
# 均线策略

class DemoStrategy(CtaTemplate):
    """
    """
    author = "Gyges Zean"

    # 定义参数
    fast_window = 10
    slow_window = 20

    # 定义变量
    fast_ma0=0.0
    fast_ma1=0.0
    slow_ma0=0.0
    slow_ma1=0.0

    parameters = [
        "fast_window",
        "slow_window",
    ]
    variables = [
        "fast_ma0",
        "fast_ma1",
        "slow_ma0",
        "slow_ma1",
    ]

    def __init__(
        self,
    cta_engine: Any,
    strategy_name,
     vt_symbol,
     setting
     ):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_init(self):
        """
            策略初始化
        """
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        """启动"""
        self.write_log("策略启动")

    def on_stop(self):
        """停止"""
        self.write_log("策略停止")

    def on_tick(self, tick):
        """更新行情"""
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """更新K线数据"""
        am = self.am

        am.update_bar(bar)
        if not am.inited:
            return

        # 计算技术指标
        fast_ma = am.sma(self.fast_window, array=True)
        # 倒数第一个均线值
        self.fast_ma0 = fast_ma[-1]
        # 倒数第二个均线值
        self.fast_ma1 = fast_ma[-2]

        slow_ma = am.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]

        # 判断均线交叉
        cross_over = (self.fast_ma0 >= self.slow_ma0 and
                      self.fast_ma1 < self.slow_ma1)

        cross_blow = (self.fast_ma0 <= self.slow_ma0 and
                      self.fast_ma1 > self.slow_ma1)

        if cross_over:
            price = bar.close_price + 5

            if not self.pos:
                self.buy(price, 1)
            elif self.pos < 0:
                self.cover(price, 1)
                self.buy(price, 1)
        elif cross_blow:
            price = bar.close_price - 5

            if not self.pos:
                self.sell(price, 1)
            elif self.pos > 0:
                self.short(price, 1)
                self.sell(price, 1)

        # 更新图形界面
        self.put_event()



