import sys
import logging

# Configura o logger do bot e do terminal
from src.modules.TerminalLogger import TerminalLogger  # Importa a classe extraída

sys.stdout = TerminalLogger()
sys.stderr = sys.stdout  # Se quiser capturar erros também

logging.basicConfig(
    filename="src/logs/trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# ------------------------------------------------------------------

# Importa as bibliotecas necessárias
import threading
import time
from binance.client import Client

from src.modules.BinanceTraderBot import BinanceTraderBot
from src.Models.stock_start_model import StockStartModel

# Importa as estratégias de trading
from src.strategies.moving_average_antecipation import getMovingAverageAntecipationTradeStrategy

# from src.strategies.vortex_strategy import getVortexTradeStrategy
# from src.strategies.rsi_strategy import getRsiTradeStrategy
# from src.strategies.vortex_strategy import getVortexTradeStrategy
# from src.strategies.ma_rsi_volume_strategy import getMovingAverageRSIVolumeStrategy
# from src.strategies.chilo import getChiloStrategy
from src.strategies.moving_average import getMovingAverageTradeStrategy
from src.strategies.dev_strategy import getDevStrategy
from src.strategies.chilo_rsi import ChiloRSIStrategy


# fmt: off
# -------------------------------------------------------------------------------------------------
# 🟢🟢🟢 CONFIGURAÇÕES - PODEM ALTERAR - INICIO 🟢🟢🟢

# ------------------------------------------------------------------
# 🚀 AJUSTES DE ESTRATÉGIA 🚀

# 🏆 ESTRATÉGIA PRINCIPAL 🏆

# MAIN_STRATEGY = getMovingAverageAntecipationTradeStrategy
# MAIN_STRATEGY_ARGS = {
#     "volatility_factor": 0.5, # Interfere na antecipação e nos lances de compra de venda limitados 
#     "fast_window": 9,
#     "slow_window": 21
#     }

# MAIN_STRATEGY = getVortexTradeStrategy
# MAIN_STRATEGY_ARGS = {}

MAIN_STRATEGY = ChiloRSIStrategy 
MAIN_STRATEGY_ARGS = {
    "rsi_reentry": 65.0
}

# MAIN_STRATEGY = getDevStrategy
# MAIN_STRATEGY_ARGS = {"decision": True} # True = comprar | False = vender | None = não fazer nada

# -----------------

# 🥈 ESTRATÉGIA DE FALLBACK (reserva) 🥈

FALLBACK_ENABLED  = False      
FALLBACK_STRATEGY = getMovingAverageTradeStrategy
FALLBACK_STRATEGY_ARGS = {
        "fast_window": 7, 
        "slow_window": 40
    }


# ------------------------------------------------------------------
# 🛠️ AJUSTES TÉCNICOS 🛠️

# Ajustes de LOSS PROTECTION
ACCEPTABLE_LOSS_PERCENTAGE  = 0         # (Em base 100%) O quando o bot aceita perder de % (se for negativo, o bot só aceita lucro).
STOP_LOSS_PERCENTAGE        = 5         # (Em base 100%) % Máxima de loss que ele aceita para vender à mercado independente.

# Ajustes de TRAILING STOP (Em base 100%)
TRAILING_STOP_ENABLED = True     # Define se o bot irá usar trailing stop (se False, não usa trailing stop).
TRAILING_STOP_PERCENTAGE = 3    # (Em base 100%) % de trailing stop que o bot irá usar (não use 0 nem valores negativos).



# Ajustes de TAKE PROFIT (Em base 100%)                        
TP_AT_PERCENTAGE =      [5, 10, 20]       # Em [X%, Y%]                       
TP_AMOUNT_PERCENTAGE =  [25, 50, 100]    # Vende [A%, B%] # Erro NOTIONAL -> Ordem menor que 5 dolares 

PAUSE_AFTER_TAKE_PROFIT = False  # Define se o bot deve pausar após executar o take profit
PAUSE_AFTER_STOP_LOSS = False    # Define se o bot deve pausar após executar o stop loss
PAUSE_AFTER_TRAILING_STOP = False  # Define se o bot deve pausar após executar o trailing stop

# Define se o robô irá executar ordens de mercado (se False, ele executa ordens limitadas).
EXECUTE_MARKET_ORDERS = False  # (Stop Loss sempre será executado à mercado, independente deste parâmetro).


# ------------------------------------------------------------------
# ⌛ AJUSTES DE TEMPO

# CANDLE_PERIOD = Client.KLINE_INTERVAL_5MINUTE   # Périodo do candle análisado (Para Scalping)
# CANDLE_PERIOD = Client.KLINE_INTERVAL_15MINUTE  # Périodo do candle análisado (Para Scalping)
CANDLE_PERIOD = Client.KLINE_INTERVAL_1HOUR # Périodo do candle análisado
# CANDLE_PERIOD = Client.KLINE_INTERVAL_4HOUR # Périodo do candle análisado
# CANDLE_PERIOD = Client.KLINE_INTERVAL_1DAY # Périodo do candle análisado



TEMPO_ENTRE_TRADES = 10 * 60   # Tempo que o bot espera para verificar o mercado (em segundos)
DELAY_ENTRE_ORDENS = 10 * 60  # Tempo que o bot espera depois de realizar uma ordem de compra ou venda (ajuda a diminuir trades de borda)


# ------------------------------------------------------------------
# 🪙 MOEDAS NEGOCIADAS

XRP_USDT = StockStartModel(  baseStock = "XRP",
                            quoteStock = "USDT",
                            tradedQuantity = 3,
                            mainStrategy = MAIN_STRATEGY, mainStrategyArgs = MAIN_STRATEGY_ARGS, fallbackStrategy = FALLBACK_STRATEGY, fallbackStrategyArgs = FALLBACK_STRATEGY_ARGS,
                            candlePeriod = CANDLE_PERIOD, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ENABLED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE, executeMarketOrders=EXECUTE_MARKET_ORDERS, trailingStopPercent=TRAILING_STOP_PERCENTAGE, trailingStopEnabled=TRAILING_STOP_ENABLED, pauseAfterTakeProfit=PAUSE_AFTER_TAKE_PROFIT, pauseAfterStopLoss=PAUSE_AFTER_STOP_LOSS, pauseAfterTrailingStop=PAUSE_AFTER_TRAILING_STOP)

SOL_USDT = StockStartModel(  baseStock = "SOL",
                            quoteStock = "USDT",
                            tradedQuantity = 0.1,
                            mainStrategy = MAIN_STRATEGY, mainStrategyArgs = MAIN_STRATEGY_ARGS, fallbackStrategy = FALLBACK_STRATEGY, fallbackStrategyArgs = FALLBACK_STRATEGY_ARGS,
                            candlePeriod = CANDLE_PERIOD, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ENABLED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE, executeMarketOrders=EXECUTE_MARKET_ORDERS, trailingStopPercent=TRAILING_STOP_PERCENTAGE, trailingStopEnabled=TRAILING_STOP_ENABLED, pauseAfterTakeProfit=PAUSE_AFTER_TAKE_PROFIT, pauseAfterStopLoss=PAUSE_AFTER_STOP_LOSS, pauseAfterTrailingStop=PAUSE_AFTER_TRAILING_STOP)

ADA_USDT = StockStartModel(  baseStock = "ADA",
                            quoteStock = "USDT",
                            tradedQuantity = 0,
                            mainStrategy = MAIN_STRATEGY, mainStrategyArgs = MAIN_STRATEGY_ARGS, fallbackStrategy = FALLBACK_STRATEGY, fallbackStrategyArgs = FALLBACK_STRATEGY_ARGS,
                            candlePeriod = CANDLE_PERIOD, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ENABLED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE, executeMarketOrders=EXECUTE_MARKET_ORDERS, trailingStopPercent=TRAILING_STOP_PERCENTAGE, trailingStopEnabled=TRAILING_STOP_ENABLED, pauseAfterTakeProfit=PAUSE_AFTER_TAKE_PROFIT, pauseAfterStopLoss=PAUSE_AFTER_STOP_LOSS, pauseAfterTrailingStop=PAUSE_AFTER_TRAILING_STOP)

BTC_USDT = StockStartModel(  baseStock = "BTC",
                            quoteStock = "USDT",
                            tradedQuantity = 0,
                            mainStrategy = MAIN_STRATEGY, mainStrategyArgs = MAIN_STRATEGY_ARGS, fallbackStrategy = FALLBACK_STRATEGY, fallbackStrategyArgs = FALLBACK_STRATEGY_ARGS,
                            candlePeriod = CANDLE_PERIOD, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ENABLED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE, executeMarketOrders=EXECUTE_MARKET_ORDERS, trailingStopPercent=TRAILING_STOP_PERCENTAGE, trailingStopEnabled=TRAILING_STOP_ENABLED, pauseAfterTakeProfit=PAUSE_AFTER_TAKE_PROFIT, pauseAfterStopLoss=PAUSE_AFTER_STOP_LOSS, pauseAfterTrailingStop=PAUSE_AFTER_TRAILING_STOP)

JUP_USDT = StockStartModel(  baseStock = "JUP",
                            quoteStock = "USDT",
                            tradedQuantity = 30,
                            mainStrategy = MAIN_STRATEGY, mainStrategyArgs = MAIN_STRATEGY_ARGS, fallbackStrategy = FALLBACK_STRATEGY, fallbackStrategyArgs = FALLBACK_STRATEGY_ARGS,
                            candlePeriod = CANDLE_PERIOD, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ENABLED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE, executeMarketOrders=EXECUTE_MARKET_ORDERS, trailingStopPercent=TRAILING_STOP_PERCENTAGE, trailingStopEnabled=TRAILING_STOP_ENABLED, pauseAfterTakeProfit=PAUSE_AFTER_TAKE_PROFIT, pauseAfterStopLoss=PAUSE_AFTER_STOP_LOSS, pauseAfterTrailingStop=PAUSE_AFTER_TRAILING_STOP)

ETH_USDT = StockStartModel(  baseStock = "ETH",
                            quoteStock = "USDT",
                            tradedQuantity = 0.00,
                            mainStrategy = MAIN_STRATEGY, mainStrategyArgs = MAIN_STRATEGY_ARGS, fallbackStrategy = FALLBACK_STRATEGY, fallbackStrategyArgs = FALLBACK_STRATEGY_ARGS,
                            candlePeriod = CANDLE_PERIOD, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ENABLED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE, executeMarketOrders=EXECUTE_MARKET_ORDERS, trailingStopPercent=TRAILING_STOP_PERCENTAGE, trailingStopEnabled=TRAILING_STOP_ENABLED, pauseAfterTakeProfit=PAUSE_AFTER_TAKE_PROFIT, pauseAfterStopLoss=PAUSE_AFTER_STOP_LOSS, pauseAfterTrailingStop=PAUSE_AFTER_TRAILING_STOP)


# ⤵️ Array que DEVE CONTER as moedas que serão negociadas
stocks_traded_list = [JUP_USDT]

THREAD_LOCK = True # True = Executa 1 moeda por vez | False = Executa todas simultânemaente

# 🔴🔴🔴 CONFIGURAÇÕES - FIM 🔴🔴🔴
# -------------------------------------------------------------------------------------------------



# 🔁 LOOP PRINCIPAL

thread_lock = threading.Lock()

def trader_loop(stockStart: StockStartModel):
    MaTrader = BinanceTraderBot(  base_stock = stockStart.baseStock
                                , quote_stock = stockStart.quoteStock
                                , traded_quantity = stockStart.tradedQuantity
                                , traded_percentage = stockStart.tradedPercentage
                                , candle_period = stockStart.candlePeriod
                                , time_to_trade = stockStart.tempoEntreTrades
                                , delay_after_order = stockStart.delayEntreOrdens
                                , acceptable_loss_percentage = stockStart.acceptableLossPercentage
                                , stop_loss_percentage = stockStart.stopLossPercentage
                                , fallback_activated = stockStart.fallBackActivated
                                , take_profit_at_percentage = stockStart.takeProfitAtPercentage
                                , take_profit_amount_percentage= stockStart.takeProfitAmountPercentage
                                , main_strategy = stockStart.mainStrategy
                                , main_strategy_args =  stockStart.mainStrategyArgs
                                , fallback_strategy = stockStart.fallbackStrategy
                                , fallback_strategy_args = stockStart.fallbackStrategyArgs
                                , execute_market_orders = stockStart.executeMarketOrders
                                , trailing_stop_percent = stockStart.trailingStopPercent
                                , trailing_stop_enabled = stockStart.trailingStopEnabled
                                , pause_after_take_profit = stockStart.pauseAfterTakeProfit
                                , pause_after_stop_loss = stockStart.pauseAfterStopLoss
                                , pause_after_trailing_stop = stockStart.pauseAfterTrailingStop)
    

    total_executed:int = 1

    while(True):
        if(THREAD_LOCK):
            with thread_lock:
                print(f"[{MaTrader.operation_code}][{total_executed}] '{MaTrader.operation_code}'")
                MaTrader.execute()
                print(f"^ [{MaTrader.operation_code}][{total_executed}] time_to_sleep = '{MaTrader.time_to_sleep/60:.2f} min'")
                print(f"------------------------------------------------")
                total_executed += 1
        else:
            print(f"[{MaTrader.operation_code}][{total_executed}] '{MaTrader.operation_code}'")
            MaTrader.execute()
            print(f"^ [{MaTrader.operation_code}][{total_executed}] time_to_sleep = '{MaTrader.time_to_sleep/60:.2f} min'")
            print(f"------------------------------------------------")
            total_executed += 1
        time.sleep(MaTrader.time_to_sleep)


# Criando e iniciando uma thread para cada objeto
threads = []

for asset in stocks_traded_list:
    thread = threading.Thread(target=trader_loop, args=(asset,))
    thread.daemon = True  # Permite finalizar as threads ao encerrar o programa
    thread.start()
    threads.append(thread)

print("\nThreads iniciadas para todos os ativos.")

# O programa principal continua executando sem bloquear
try:
    while True:
        time.sleep(1)  # Mantenha o programa rodando
except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário.")

# -----------------------------------------------------------------

# fmt: on
