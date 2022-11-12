import asyncio
from wizwalker import ClientHandler
from wizwalker.extensions.scripting.deck_builder import DeckBuilder


async def main():
    handler = ClientHandler()
    client = handler.get_new_clients()[0]

    try:
        print("Preparing")
        await client.activate_hooks()
        print("Ready for Deck Building")

        async with DeckBuilder(client) as builder:
            await builder.open_deck_page()
            
            print(await builder.get_spell_card_names())
            
            await builder.add_by_name("fairy", 2)

            await builder.remove_by_name("fairy", None)

            await builder.close_deck_page()

    finally:
        print("Closing")
        await handler.close()


if __name__ == "__main__":
    asyncio.run(main())
