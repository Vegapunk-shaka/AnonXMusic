import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from aiohttp import web

import config
from AnonXMusic import LOGGER, app, userbot
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import ALL_MODULES
from AnonXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
from AnonXMusic.plugins import web_server


async def init():
    # Check if assistant client variables are defined
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    # Load sudoers
    await sudo()

    # Get banned users and add them to BANNED_USERS
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).error(f"Error fetching banned users: {str(e)}")

    # Start the bot
    await app.start()

    # Import all modules dynamically from AnonXMusic.plugins
    for all_module in ALL_MODULES:
        # Ensure that module names are valid and not empty
        if not all_module.strip():
            LOGGER(__name__).warning(f"Skipped importing an empty or invalid module: '{all_module}'")
            continue

        try:
            importlib.import_module("AnonXMusic.plugins." + all_module)
            LOGGER("AnonXMusic.plugins").info(f"Successfully imported module: {all_module}")
        except ModuleNotFoundError as e:
            LOGGER(__name__).error(f"Failed to import module {all_module}: {str(e)}")
        except Exception as e:
            LOGGER(__name__).error(f"Error importing module {all_module}: {str(e)}")

    LOGGER("AnonXMusic.plugins").info("Successfully imported all modules...")

    # Start the userbot
    await userbot.start()

    # Start the call client (PyTgCalls)
    await Anony.start()

    # Attempt to start streaming call
    try:
        await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AnonXMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except Exception as e:
        LOGGER(__name__).error(f"Error in stream_call: {str(e)}")

    # Decorators for Anony call client
    await Anony.decorators()

    LOGGER("AnonXMusic").info(
        "\x41\x6e\x6f\x6e\x58\x20\x4d\x75\x73\x69\x63\x20\x42\x6f\x74\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\n\n\x44\x6f\x6e'\x74\x20\x66\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x46\x61\x6c\x6c\x65\x6e\x41\x73\x73\x6f\x63\x69\x61\x74\x69\x6f\x6e"
    )

    # Start the web server
    runner = web.AppRunner(await web_server())
    await runner.setup()

    # Set bind address and start the TCP site
    bind_address = "0.0.0.0"
    await web.TCPSite(runner, bind_address, config.PORT).start()

    # Run the bot in idle mode
    await idle()

    # Stop the app and userbot when done
    await app.stop()
    await userbot.stop()

    LOGGER("AnonXMusic").info("Stopping AnonX Music Bot...")


if __name__ == "__main__":
    # Run the init function inside the event loop
    asyncio.get_event_loop().run_until_complete(init())
