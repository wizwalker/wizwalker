from wizwalker.memory.memory_object import DynamicMemoryObject, PropertyClass

class SpellRank(PropertyClass):
    async def read_base_address(self) -> int:
        raise NotImplementedError
    
    async def balance_pips(self) -> int:
        """
        The number of balance pips this spell costs
        """
        return await self.read_value_from_offset(81, "unsigned char")

    async def write_balance_pips(self, balance_pips: int):
        """
        Write the number of death pips this spell costs

        Args:
            balance_pips: The balance pip cost to write
        """
        await self.write_value_to_offset(81, balance_pips, "unsigned char")
    
    async def death_pips(self) -> int:
        """
        The number of death pips this spell costs
        """
        return await self.read_value_from_offset(82, "unsigned char")

    async def write_death_pips(self, death_pips: int):
        """
        Write the number of death pips this spell costs

        Args:
            death_pips: The death pip cost to write
        """
        await self.write_value_to_offset(82, death_pips, "unsigned char")
    
    async def fire_pips(self) -> int:
        """
        The number of fire pips this spell costs
        """
        return await self.read_value_from_offset(83, "unsigned char")

    async def write_fire_pips(self, fire_pips: int):
        """
        Write the number of fire pips this spell costs

        Args:
            fire_pips: The fire pip cost to write
        """
        await self.write_value_to_offset(83, fire_pips, "unsigned char")

    
    async def ice_pips(self) -> int:
        """
        The number of ice pips this spell costs
        """
        return await self.read_value_from_offset(84, "unsigned char")

    async def write_ice_pips(self, ice_pips: int):
        """
        Write the number of ice pips this spell costs

        Args:
            ice_pips: The ice pip cost to write
        """
        await self.write_value_to_offset(84, ice_pips, "unsigned char")
    
    async def life_pips(self) -> int:
        """
        The number of life pips this spell costs
        """
        return await self.read_value_from_offset(85, "unsigned char")

    async def write_life_pips(self, life_pips: int):
        """
        Write the number of life pips this spell costs

        Args:
            life_pips: The life pip cost to write
        """
        await self.write_value_to_offset(85, life_pips, "unsigned char")
    
    async def myth_pips(self) -> int:
        """
        The number of myth pips this spell costs
        """
        return await self.read_value_from_offset(86, "unsigned char")

    async def write_myth_pips(self, myth_pips: int):
        """
        Write the number of myth pips this spell costs

        Args:
            myth_pips: The myth pip cost to write
        """
        await self.write_value_to_offset(86, myth_pips, "unsigned char")
    
    async def storm_pips(self) -> int:
        """
        The number of storm pips this spell costs
        """
        return await self.read_value_from_offset(87, "unsigned char")

    async def write_storm_pips(self, storm_pips: int):
        """
        Write the number of storm pips this spell costs

        Args:
            storm_pips: The storm pip cost to write
        """
        await self.write_value_to_offset(87, storm_pips, "unsigned char")
    
    async def shadow_pips(self) -> int:
        """
        The number of shadow pips this spell costs
        """
        return await self.read_value_from_offset(88, "unsigned char")

    async def write_shadow_pips(self, shadow_pips: int):
        """
        Write the number of shadow pips this spell costs

        Args:
            shadow_pips: The shadow pip cost to write
        """
        await self.write_value_to_offset(88, shadow_pips, "unsigned char")
    
    async def is_xpip_spell(self) -> bool:
        """
        If this spell is a x pip cost spell
        """
        return await self.read_value_from_offset(90, "bool")

    async def write_is_xpip_spell(self, is_xpip: bool):
        """
        Write if this spell is a x pip cost spell

        Args:
            shadow_pips: write if it is a x pip cost spell; True for it is.
        """
        await self.write_value_to_offset(90, is_xpip, "bool")

class DynamicSpellRank(DynamicMemoryObject, SpellRank):
    pass