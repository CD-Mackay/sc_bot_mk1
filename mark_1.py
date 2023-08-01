from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
import random


probe = UnitTypeId.PROBE
pylon = UnitTypeId.PYLON
cannon = UnitTypeId.PHOTONCANNON
forge = UnitTypeId.FORGE

class WorkerRushBot(BotAI):
    async def on_step(self, iteration: int):
        print("currently on interation:", iteration)

        await self.distribute_workers()

        if self.townhalls:
            nexus = self.townhalls.random
            if nexus.is_idle and self.can_afford(probe):
              nexus.train(probe)
        
            elif not self.structures(pylon) and self.already_pending(pylon) == 0:
              if self.can_afford(pylon):
                await self.build(pylon, near=nexus)

            elif self.structures(pylon).amount < 5:
              if self.can_afford(pylon):
                target_pylon = self.structures(pylon).closest_to(self.enemy_start_locations[0])
                pos = target_pylon.position.towards(self.enemy_start_locations[0], random.randrange(8, 15))
                await self.build(pylon, near=pos)

            elif not self.structures(forge):
               if self.can_afford(forge):
                  await self.build(forge, near=self.structures(pylon).closest_to(nexus))

            elif self.structures(forge).ready and self.structures(cannon).amount < 3:
               if self.can_afford(cannon):
                  await self.build(cannon, near=self.structures(pylon).closest_to(self.enemy_start_locations[0]))
            
        else:
          if self.can_afford(UnitTypeId.NEXUS):
            await self.expand_now()

                


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, WorkerRushBot()),
    Computer(Race.Zerg, Difficulty.Medium)
], realtime=False)