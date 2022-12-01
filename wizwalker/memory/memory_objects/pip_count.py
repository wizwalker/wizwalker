from wizwalker.memory.memory_object import DynamicMemoryObject, PropertyClass

class PipCount(PropertyClass):
    async def read_base_address(self) -> int:
        raise NotImplementedError
    
    async def generic_pips(self) -> int:
        """
        The number of generic pips this combat participant has
        """
        return await self.read_value_from_offset(80, "unsigned char")

    async def write_generic_pips(self, generic_pips: int):
        """
        Write the number of generic pips this combat participant has

        Args:
            generic_pips: The generic pip number to write
        """
        await self.write_value_to_offset(80, generic_pips, "unsigned char")
    
    async def power_pips(self) -> int:
        """
        The number of power pips this combat participant has
        """
        return await self.read_value_from_offset(81, "unsigned char")

    async def write_power_pips(self, power_pips: int):
        """
        Write the number of power pips this combat participant has

        Args:
        power_pips: The power pip number to write
        """
        await self.write_value_to_offset(81, power_pips, "unsigned char")
    
    async def balance_pips(self) -> int:
        """
        The number of balance pips this combat participant has
        """
        return await self.read_value_from_offset(82, "unsigned char")

    async def write_balance_pips(self, balance_pips: int):
        """
        Write the number of balance pips this combat participant has

        Args:
            balance_pips: The balance pip number to write
        """
        await self.write_value_to_offset(82, balance_pips, "unsigned char")
    
    async def death_pips(self) -> int:
        """
        The number of death pips this combat participant has
        """
        return await self.read_value_from_offset(83, "unsigned char")

    async def write_death_pips(self, death_pips: int):
        """
        Write the number of death pips this combat participant has

        Args:
            death_pips: The death pip number to write
        """
        await self.write_value_to_offset(83, death_pips, "unsigned char")
    
    async def fire_pips(self) -> int:
        """
        The number of fire pips this combat participant has
        """
        return await self.read_value_from_offset(84, "unsigned char")

    async def write_fire_pips(self, fire_pips: int):
        """
        Write the number of fire pips this combat participant has

        Args:
            fire_pips: The fire pip number to write
        """
        await self.write_value_to_offset(84, fire_pips, "unsigned char")

    
    async def ice_pips(self) -> int:
        """
        The number of ice pips this combat participant has
        """
        return await self.read_value_from_offset(85, "unsigned char")

    async def write_ice_pips(self, ice_pips: int):
        """
        Write the number of ice pips this combat participant has

        Args:
            ice_pips: The ice pip number to write
        """
        await self.write_value_to_offset(85, ice_pips, "unsigned char")
    
    async def life_pips(self) -> int:
        """
        The number of life pips this combat participant has
        """
        return await self.read_value_from_offset(86, "unsigned char")

    async def write_life_pips(self, life_pips: int):
        """
        Write the number of life pips this combat participant has

        Args:
            life_pips: The life pip number to write
        """
        await self.write_value_to_offset(86, life_pips, "unsigned char")
    
    async def myth_pips(self) -> int:
        """
        The number of myth pips this combat participant has
        """
        return await self.read_value_from_offset(87, "unsigned char")

    async def write_myth_pips(self, myth_pips: int):
        """
        Write the number of myth pips this combat participant has

        Args:
            myth_pips: The myth pip number to write
        """
        await self.write_value_to_offset(87, myth_pips, "unsigned char")
    
    async def storm_pips(self) -> int:
        """
        The number of storm pips this combat participant has
        """
        return await self.read_value_from_offset(88, "unsigned char")

    async def write_storm_pips(self, storm_pips: int):
        """
        Write the number of storm pips this combat participant has

        Args:
            storm_pips: The storm pip number to write
        """
        await self.write_value_to_offset(88, storm_pips, "unsigned char")
    
    async def shadow_pips(self) -> int:
        """
        The number of shadow pips this combat participant has
        """
        return await self.read_value_from_offset(89, "unsigned char")

    async def write_shadow_pips(self, shadow_pips: int):
        """
        Write the number of shadow pips this combat participant has

        Args:
            shadow_pips: The shadow pip number to write
        """
        await self.write_value_to_offset(89, shadow_pips, "unsigned char")

class DynamicPipCount(DynamicMemoryObject, PipCount):
    pass