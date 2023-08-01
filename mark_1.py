from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI

class WorkerRushBot(BotAI):
    async def on_step(self, iteration: int):
        print("currently on interation:", iteration)
        

run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, WorkerRushBot()),
    Computer(Race.Zerg, Difficulty.Medium)
], realtime=False)