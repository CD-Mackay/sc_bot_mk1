from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId



class WorkerRushBot(BotAI):
    async def on_step(self, iteration: int):
        print("currently on interation:", iteration)

        if self.townhalls:
            nexus = self.townhalls.random()
            if nexus.is_idle and self.can_afford(UnitTypeId.PROBE):
              nexus.train(UnitTypeId.PROBE)

        else:
            if self.can_afford(UnitTypeId.NEXUS):
                await self.expand_now()
                


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, WorkerRushBot()),
    Computer(Race.Zerg, Difficulty.Medium)
], realtime=False)