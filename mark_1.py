from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
import random



class WorkerRushBot(BotAI):
    async def on_step(self, iteration: int):
        print("currently on interation:", iteration)

        await self.distribute_workers()

        if self.townhalls:
            nexus = self.townhalls.random
            if nexus.is_idle and self.can_afford(UnitTypeId.PROBE):
              nexus.train(UnitTypeId.PROBE)
        
            elif not self.structures(UnitTypeId.PYLON) and self.already_pending(UnitTypeId.PYLON) == 0:
              if self.can_afford(UnitTypeId.PYLON):
                await self.build(UnitTypeId.PYLON, near=nexus)

            elif self.structures(UnitTypeId.PYLON).amount < 5:
              if self.can_afford(UnitTypeId.PYLON):
                target_pylon = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0])
                pos = target_pylon.position.towards(self.enemy_start_locations[0], random.randrange(8, 15))
                await self.build(UnitTypeId.PYLON, near=pos)

            elif not self.structures(UnitTypeId.FORGE):
               if self.can_afford(UnitTypeId.FORGE):
                  await self.build(UnitTypeId.FORGE, near=self.structures(UnitTypeId.PYLON).closest_to(nexus))

            elif self.structures(UnitTypeId.FORGE).ready and self.structures(UnitTypeId.PHOTONCANNON).amount < 3:
               if self.can_afford(UnitTypeId.PHOTONCANNON):
                  await self.build(UnitTypeId.PHOTONCANNON, near=self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0]))
            
        else:
          if self.can_afford(UnitTypeId.NEXUS):
            await self.expand_now()

                


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, WorkerRushBot()),
    Computer(Race.Zerg, Difficulty.Medium)
], realtime=False)