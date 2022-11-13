import asyncio

import wizwalker


async def main():
  async with wizwalker.ClientHandler() as ch:
    client = ch.get_new_clients()[0]
    await client.activate_hooks(wait_for_ready=False)
    
    await client.root_window.debug_print_ui_tree()

    #ccb = (await client.root_window.get_windows_with_name("DeckConfiguration"))[0]
    #ccbf = await ccb.flags()
    #await ccb.write_flags((ccbf | 1) & (~2147483648))
    #print(await ccb.flags())

    #ccbs = await ccb.style()
    #print(ccbs)
    #await ccb.write_style(ccbs)
    #print(await ccb.flags())


asyncio.run(main())
