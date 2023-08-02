from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
import random
from aliases import probe, forge, cannon, pylon, assimilator,gateway, cybercore, stargate, voidray

class WorkerRushBot(BotAI):
    async def on_step(self, iteration: int):
        print("currently on interation:", iteration)

        await self.distribute_workers()

        if self.townhalls:
            nexus = self.townhalls.random
            if nexus.is_idle and self.can_afford(probe):
              nexus.train(probe)
        
            if self.structures(voidray).amount < 10 and self.can_afford(voidray):
               for sg in self.structures(stargate).ready.idle:
                  if self.can_afford(voidray):
                     sg.train(voidray)

            elif not self.structures(pylon) and self.already_pending(pylon) == 0:
              if self.can_afford(pylon):
                await self.build(pylon, near=nexus)

            elif self.structures(pylon).amount < 5:
              if self.can_afford(pylon):
                target_pylon = self.structures(pylon).closest_to(self.enemy_start_locations[0])
                pos = target_pylon.position.towards(self.enemy_start_locations[0], random.randrange(8, 15))
                await self.build(pylon, near=pos)
            
            elif self.structures(assimilator).amount <= 1:
               for nexus in self.structures(nexus):
                  vespenes = self.vespene_geyser.closer_than(15, nexus)
                  for vespene in vespenes:
                     if self.can_afford(assimilator) and not self.already_pending(assimilator):
                        await self.build(assimilator, vespene)
              
            elif not self.structures(gateway):
               if self.can_afford(gateway):
                  await self.build(gateway, near = self.structures(pylon).closest_to(nexus))

            elif not self.structures(cybercore):
               if self.can_afford(cybercore):
                  await self.build(cybercore, near = self.structures(pylon).closest_to(nexus))

            elif not self.structures(stargate):
               if self.can_afford(stargate):
                  await self.build(stargate, near = self.structures(pylon).closest_to(nexus))
            



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