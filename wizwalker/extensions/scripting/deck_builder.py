from typing import TYPE_CHECKING, Optional, Callable, List

if TYPE_CHECKING:
    from wizwalker import Client

import asyncio
from wizwalker.memory.memory_reader import MemoryReadError
from wizwalker.extensions.scripting.utils import _maybe_get_named_window
from wizwalker.memory.memory_objects.spell import *
from wizwalker.memory.memory_objects.window import (DynamicDeckListControl,
                                                    DynamicSpellListControl,
                                                    SpellListControl,
                                                    DeckListControl,
                                                    DeckListControlSpellEntry,
                                                    SpellListControlSpellEntry)

"""
async with DeckBuilder(client) as db:
    db.add(123)

# entire deck config window
--- [DeckConfigurationWindow] SpellBookPrefsPage

# toolbar parent?
---- [ControlSprite] ControlSprite

# top bar buttons
----- [toolbar] Window

# select school
------ [TabBackground] ControlSprite
------ [Cards_Fire] ControlCheckBox
------ [Cards_Ice] ControlCheckBox
------ [Cards_Storm] ControlCheckBox
------ [Cards_Myth] ControlCheckBox
------ [Cards_All] ControlCheckBox
------ [Cards_Life] ControlCheckBox
------ [RightSideTabs] Window
------- [Cards_Death] ControlCheckBox
------- [Cards_Balance] ControlCheckBox
------- [Cards_Astral] ControlCheckBox
------- [Cards_Shadow] ControlCheckBox
------- [Cards_MonsterMagic] ControlCheckBox


# other pages (unrelated)
------ [GoToTieredWindow] Window
------- [GoToTieredGlow] ControlSprite
------- [GoToTiered] ControlCheckBox
------ [GoToGardening] ControlCheckBox
------ [GoToFishing] ControlCheckBox
------ [GoToCantrips] ControlCheckBox
------ [GoToCastleMagic] ControlCheckBox
------ [GoBackToCastleMagic] ControlCheckBox
------ [GoBackToFishing] ControlCheckBox
------ [GoBackToGardening] ControlCheckBox
------ [GoBackToTieredWindow] Window
------- [GoBackToTieredGlow] ControlSprite
------- [GoBackToTiered] ControlCheckBox


# just parent window?
----- [DeckPage] Window

?
------ [PageUp] ControlButton
------ [PageDown] ControlButton

# cards to add to deck?
------ [SpellList] SpellListControl

# equip icon
------ [EquipBorder] ControlWidget

# ?
------ [InvBorder] ControlWidget

# cards given by items? (most likely)
------ [ItemSpells] DeckListControl

# ?
------ [ControlSprite] ControlSprite

# deck selection
------ [PrevDeck] ControlButton
------ [NextDeck] ControlButton

# deck name
------ [DeckName] ControlText

# equip icon?
------ [equipFist] Window

# spells added to normal deck (may also be used for tc)
------ [CardsInDeck] DeckListControl


# tc info
------ [TreasureCardCountBackground] Window
------ [TreasureCardCount] ControlText
------ [TreasureCardIcon] Window

# rename deck
------ [NewDeckName] ControlButton

# select deck
------ [EquipButton] ControlButton

# next card selection page?
------ [NextItemSpells] ControlButton
------ [PrevItemSpells] ControlButton

# help button
------ [Help] ControlButton

# clear deck (hidden on small decks; try unhiding)
------ [ClearDeckButton] ControlButton

# quick sell tc
------ [QuickSellButton] ControlButton

# ?
----- [ControlSprite] ControlSprite
------ [DeckTitle] ControlText
----- [TutorialLogBackground1] ControlSprite

# switch to tc view
----- [TreasureCardButton] ControlCheckBox


builder.add_card_by_name("unicorn", number_of_copies: int | None)
-> number_of_copies = None: add max copies 
-> raises: ValueError(already at max copies)
-> raises: ValueError(card not found)

builder.remove_card_by_name("unicorn", number_of_copies: int | None)
-> inverse

builder.add_by_predicate(pred, number_of_copies: int | None)
-> see add_card_by_name
def pred(spell: graphical spell):
    return True or False

builder.remove_by_predicate(pred, number_of_copies: int | None)
-> inverse

builder.get_deck_preset() -> dict[...]
{
    normal: {template id: number of copies},
    tc: {template id: number of copies},
    item: {template id: number of copies}
}
-> 


builder.set_deck_preset(dict[see above], ignore_failures: bool = False)
-> removes and adds cards as needed for a preset which is a dict

"""


# TODO: finish
class DeckBuilder:
    """
    async with DeckBuilder(client) as deck_builder:
        # adds two unicorns
        await deck_builder.add_by_name("Unicorn", 2)
    """
    def __init__(self, client: "Client"):
        self.client = client

        self._deck_config_window = None

    async def open(self):
        pass

    async def close(self):
        pass

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def starr_calculate_icon_position(
            card_number: int,
            horizontal_size: int = 33,
            vertical_size: int = 33,
            number_of_rows: int = 8,
            horizontal_spacing: int = 6,
            vertical_spacing: int = 0,
    ):
        x = (horizontal_size * card_number) - (horizontal_size // 2) + (horizontal_spacing * (card_number - 1))
        y = (vertical_size * (((card_number - 1) // number_of_rows) + 1))\
            - (vertical_size // 2) + \
            (vertical_spacing * ((card_number - 1) // number_of_rows))
        return x, y

    async def open_deck_page(self):
        spellbook = await _maybe_get_named_window(self.client.root_window, "btnSpellbook")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(spellbook)

        await asyncio.sleep(1)
        self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        deck_button = await _maybe_get_named_window(self._deck_config_window, "Deck")

        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(deck_button)

        Cards_All =  await _maybe_get_named_window(self._deck_config_window, "Cards_All")

        if await Cards_All.is_visible():
            async with self.client.mouse_handler:
                await self.client.mouse_handler.click_window(Cards_All)


    async def spell_list_get_card_named(self, name: str) -> SpellListControlSpellEntry:
            """
            Args:
                name: The name (display name) of the card to find
            Returns: The first Card with name
            """
            possible = await self.spell_list_get_cards_with_name(name)

            if possible:
                return possible[0]

            raise ValueError(f"Couldn't find a card named {name}")


    async def spell_list_get_cards_with_predicate(self, pred: Callable) -> List[SpellListControlSpellEntry]:
            """
            Return cards that match a predicate

            Args:
                pred: The predicate function
            """
            cards = []
            spell_list = await self.get_spell_cards()
            for spell in spell_list:
                if await pred(spell):
                    cards.append(spell)

            return cards


    async def get_spell_cards(self):
        if not self._deck_config_window:
            self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")

        SpellList_window = await _maybe_get_named_window(self._deck_config_window, "SpellList")
        SpellListControl = DynamicSpellListControl(self.client.hook_handler, (await SpellList_window.read_base_address()))
        list_of_spells = await SpellListControl.spell_entries()
        list_of_SpellListControl = []
        for spell in list_of_spells:
            graphical = await spell.graphical_spell()
            if graphical:
                try:
                    template = await graphical.spell_template()
                    _ = await template.name()
                except MemoryReadError:
                    pass
                except AttributeError:
                    pass
                else:
                    list_of_SpellListControl.append(spell)

        return list_of_SpellListControl


    async def get_spell_card_names(self):
        
        spell_list = await self.get_spell_cards()
        names = []
        for spell in spell_list:
            graphical = await spell.graphical_spell()
            template = await graphical.spell_template()
            names.append(await template.name())

        return names

    async def spell_list_get_cards_with_name(self, name: str) -> List[SpellListControlSpellEntry]:
            """
            Args:
                name: The name (debug name) of the cards to find

            Returns: list of possible CombatCards with the name
            """
            
            async def _pred(card):
                return name.lower() == (await (await (await card.graphical_spell()).spell_template()).name()).lower()

            return await self.spell_list_get_cards_with_predicate(_pred)


    async def get_item_card_names(self) -> list[str]:
        if not self._deck_config_window:
            self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")

        CardsInDeck_window = await _maybe_get_named_window(self.client.root_window, "ItemSpells")
        DeckListControl = DynamicDeckListControl(self.client.hook_handler, await CardsInDeck_window.read_base_address())
        list_of_spells = await DeckListControl.spell_entries()
        list_of_name = []
        for spell in list_of_spells:
            graphical = await spell.graphical_spell()
            if graphical:
                try:
                    template = await graphical.spell_template()
                    name = await template.name()
                except MemoryReadError:
                    pass
                except AttributeError:
                    pass
                else:
                    list_of_name.append(name)
        return list_of_name


    async def get_card_index(self, card_name) -> int:
        cards_names = await self.get_spell_card_names()
        cards_lower = [c.lower() for c in cards_names]
        card_placement = cards_lower.index(card_name.lower())

        index = round(card_placement // 6)

        card_num = (card_placement - (index * 6)) + 1

        return int(index), card_num


    async def get_spell_xy(self, card_placement: int, SpellListControl: SpellListControl):
        rectangle = await SpellListControl.scale_to_client()
        number_of_rows = 3
        number_of_columns = 2 
        xy = self.calculate_card_position(card_placement,
            await SpellListControl.card_size_horizontal(),
            await SpellListControl.card_size_vertical(),
            number_of_rows,
            number_of_columns,
            await SpellListControl.card_spacing_horizontal_adjust(),
            await SpellListControl.card_spacing_vertical_adjust(),
            await self.client.render_context.ui_scale()
            )

        x = rectangle.x1 + xy[0]
        y = rectangle.y1 + xy[1]
        return x, y

    async def click_card(self, x: int, y: int):
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click(x,y)
        await asyncio.sleep(0.2)


    async def click_card_spell_list(self, card_num: int, number_of_copies: Optional[int]):
        SpellList = await _maybe_get_named_window(self.client.root_window, "SpellList")
        SpellListControl = DynamicSpellListControl(self.client.hook_handler, await SpellList.read_base_address())
        x, y = await self.get_spell_xy(card_num, SpellListControl)
        for _ in range(number_of_copies):
            await self.click_card(x, y)


    async def go_to_card_page(self, card_index):
        SpellList = await _maybe_get_named_window(self.client.root_window, "SpellList")
        SpellListControl = DynamicSpellListControl(self.client.hook_handler, await SpellList.read_base_address())
        await SpellListControl.write_card_page(card_index)
        await asyncio.sleep(0.15)


    async def add_by_name(self, name: str, number_of_copies: Optional[int]):
        """
        builder.add_card_by_name("unicorn", number_of_copies: int | None)
        -> number_of_copies = None: add max copies
        -> raises: ValueError(already at max copies)
        -> raises: ValueError(card not found)
        """

        card = await self.spell_list_get_card_named(name)
        if await card.max_copies() == await card.current_copies():
            raise ValueError(f"already at max copies for {name}")
        elif await card.max_copies() < (await card.current_copies()) + (number_of_copies):
            raise ValueError(f"number of copies is greater than the card allows")

        card_index, card_num = await self.get_card_index(name) 
        await self.go_to_card_page(card_index)
        await self.click_card_spell_list(card_num, number_of_copies)


    async def get_deck_card_index(self, card_name: str) -> int:
            cards_names = await self.get_deck_card_names()
            cards_lower = [c.lower() for c in cards_names]
            card_placement = cards_lower.index(card_name.lower())
            return card_placement + 1


    async def get_item_card_index(self, card_name: str) -> list[int]:
        cards_names = await self.get_item_card_names()
        cards_lower = [c.lower() for c in cards_names]
        card_placement = [i for i in range(len(cards_lower)) if cards_lower[i]==card_name.lower()]
        return card_placement


    async def get_deck_card_names(self) -> list[str]:
        if not self._deck_config_window:
            self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")

        CardsInDeck_window = await _maybe_get_named_window(self.client.root_window, "CardsInDeck")
        DeckListControl = DynamicDeckListControl(self.client.hook_handler, await CardsInDeck_window.read_base_address())
        list_of_spells = await DeckListControl.spell_entries()
        list_of_name = []
        for spell in list_of_spells:
            graphical = await spell.graphical_spell()
            if graphical:
                try:
                    template = await graphical.spell_template()
                    name = await template.name()
                except MemoryReadError:
                    pass
                except AttributeError:
                    pass
                else:
                    list_of_name.append(name)
        return list_of_name


    def calc_icon_pos(self, 
        card_number: int,
        ui_scale: int,
        horizontal_size: int = 33,
        vertical_size: int = 33,
        number_of_rows: int = 8,
        number_of_column: int = 8,
        horizontal_spacing: int = 6,
        vertical_spacing: int = 0):

        y_line = ceil(card_number / number_of_rows)
        y = (y_line * vertical_size) + (vertical_spacing * y_line)
        
        x_num = card_number % number_of_column
        if x_num == 0:
            x_num = number_of_column

        x = ((x_num * horizontal_size) - (horizontal_size//2)) + (horizontal_spacing * x_num)

        return int(x*ui_scale), int(y*ui_scale)


    def calculate_card_position(self,
            card_number: int ,
            horizontal_size: int ,
            vertical_size: int ,
            number_of_rows: int ,
            number_of_columns: int,
            horizontal_spacing: int ,
            vertical_spacing: int,
            ui_scale = float,
        ):
            #TODO get someone who know math to rewrite this correctly
        if card_number == 1:
            x = 59
            y = 89
        elif card_number == 2:
            x = 185
            y = 89
        elif card_number == 3:
            x = 59
            y = 266
        elif card_number == 4:
            x = 154
            y = 266
        elif card_number == 5:
            x = 59
            y = 355
        elif card_number == 6:
            x = 185
            y = 355

        return round(x*ui_scale), round(y*ui_scale)


    async def remove_by_name(self, name: str, number_of_copies: Optional[int]):
        CardsInDeck_window = await _maybe_get_named_window(self.client.root_window, "CardsInDeck")
        DeckListControl = DynamicDeckListControl(self.client.hook_handler, await CardsInDeck_window.read_base_address())
        for _ in range(number_of_copies):
            card_number = await self.get_deck_card_index(name)
            x, y = await self.get_deck_xy(card_number, DeckListControl)
            await self.click_card(x, y)


    async def get_deck_xy(self, card_placement: int, DeckListControl: DeckListControl):
        rectangle = await DeckListControl.scale_to_client()
        x_offset, y_offset = self.calc_icon_pos(card_placement, await self.client.render_context.ui_scale())
        x = rectangle.x1 + x_offset
        y = rectangle.y1 + y_offset
        return x, y


    async def clear_main_deck(self):
        ClearDeckButton = await _maybe_get_named_window(self._deck_config_window, "ClearDeckButton")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(ClearDeckButton)

        MessageBoxModalWindow = await _maybe_get_named_window(self.client.root_window, "MessageBoxModalWindow")
        leftButton = await _maybe_get_named_window(MessageBoxModalWindow, "leftButton")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(leftButton)

        #close and reopen
        await self.close_deck_page()
        await self.open_deck_page()

    async def clear_item_deck(self):
        #item card stuff
        pass


    async def close_deck_page(self):
        Close_Button = await _maybe_get_named_window(self.client.root_window, "Close_Button")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(Close_Button)
        await asyncio.sleep(1)


    async def clear_tc_deck(self):
        #tc stuff
        for _ in range(2): # trys twice just to make sure
            await self.click_tc_button()

            unwanted_cards = await self.get_deck_card_names()
            for card in unwanted_cards:
                try:
                    await self.remove_by_name(card, 1)
                except:
                    pass

            #close and reopen
            await self.close_deck_page()

            await self.open_deck_page()


    async def click_tc_button(self):
        TreasureCardButton = await _maybe_get_named_window(self._deck_config_window, "TreasureCardButton")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(TreasureCardButton)
        await asyncio.sleep(1)


    async def get_deck_preset(self) -> dict:
        """
        builder.get_deck_preset() -> dict[...]
        {
            normal: {template id: number of copies},
            tc: {template id: number of copies},
            item: {template id: number of copies}
        }
        """

        def dict_maker(list: list, tc: bool):
            d = {}

            def checkKey(dic: dict, key: str):
                if key in dic.keys():
                    return True
                else:
                    return False

            for card in list:
                if tc and not "tc" in card.lower():
                    break
                if checkKey(d, card):
                    d[card] = d[card] + 1
                else:
                    d[card] = 1
            return d

        saved_deck= {}

        list_normal = await self.get_deck_card_names()
        normal =  dict_maker(list_normal, False)

        await self.click_tc_button()

        list_tc = await self.get_deck_card_names()
        tc = dict_maker(list_tc, True)

        await self.click_tc_button()

        saved_deck["normal"] = normal
        saved_deck["tc"] = tc

        return saved_deck


    async def clear_all_deck(self):
        await self.clear_main_deck()
        await self.clear_item_deck()
        await self.clear_tc_deck()


    async def set_deck_preset(self, preset: dict, *, ignore_failures: bool = True):
        await self.clear_all_deck()

        deck = {}
        deck_section = preset.keys()

        if ignore_failures:
            for section in deck_section:
                if section == "tc":
                    await self.click_tc_button()
                for card in (preset[section]).keys():
                    try:
                        await self.add_by_name(card, (preset[section])[card])
                    except:
                        pass
                if section == "tc":
                    await self.click_tc_button()
        else:	
            for section in deck_section:
                if section == "tc":
                    await self.click_tc_button()
                preset[section] = deck
                for card in deck.keys():
                    if "tc" in card.lower():
                        await self.add_by_name(card, deck[card])
                if section == "tc":
                    await self.click_tc_button()


    async def get_item_card_names(self):
        if not self._deck_config_window:
            self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        ItemSpells_window = await _maybe_get_named_window(self._deck_config_window , "ItemSpells")

        DeckListControl = DynamicDeckListControl(self.client.hook_handler, await ItemSpells_window.read_base_address())
        list_of_spells = await DeckListControl.spell_entries()
        list_of_name = []
        for spell in list_of_spells:
            graphical = await spell.graphical_spell()
            if graphical:
                try:
                    template = await graphical.spell_template()
                    name = await template.name()
                except MemoryReadError:
                    pass
                except AttributeError:
                    pass
                else:
                    list_of_name.append(name)
        return list_of_name


    async def get_itemDeckList_card_named(self, name: str) -> list[DeckListControlSpellEntry]:
        if not self._deck_config_window:
            self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        ItemSpells_window = await _maybe_get_named_window(self._deck_config_window , "ItemSpells")
        DeckListControl = DynamicDeckListControl(self.client.hook_handler, await ItemSpells_window.read_base_address())
        list_of_spells = await DeckListControl.spell_entries()
        list_of_name = []
        for spell in list_of_spells:
            graphical = await spell.graphical_spell()
            if graphical:
                try:
                    template = await graphical.spell_template()
                    named = await template.name()
                    if name.lower() == named.lower():
                        list_of_name.append(spell)
                except MemoryReadError:
                    pass
                except AttributeError:
                    pass

        return list_of_name


    async def item_remove_add_by_name(self, name: str, number_of_copies: Optional[int]):
        ItemSpells_window = await _maybe_get_named_window(self.client.root_window, "ItemSpells")
        DeckListControl = DynamicDeckListControl(self.client.hook_handler, await ItemSpells_window.read_base_address())
        number_of_copies_count = 0
        card_numbers = await self.get_item_card_index(name)
        for card_number in card_numbers:
            x, y = await self.get_deck_xy(card_number + 1, DeckListControl)
            await self.click_card(x, y)
            await asyncio.sleep(0.5)
            number_of_copies_count += 1
            if number_of_copies:
                if number_of_copies_count >= number_of_copies:
                    break


    async def change_all_item_card(self):
        all_cards = await self.get_item_card_names()
        cards = [*set(all_cards)]
        for card in cards:
            await self.item_remove_add_by_name(card, None)

