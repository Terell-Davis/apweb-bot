
You can use the API file by itself with something like `from archipelago_api import ArchipelagoAPI`
    api = ArchipelagoAPI("Yourhostedinstancehere")

# How to use
---
Edit and rename `dotenv` to `.env`
You will need your bot


# APWeb-Bot
A discord bot that utilities the [Archipelago's](https://archipelago.gg/) WebHost API documented [here.](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/webhost%20api.md)

## Install/Running

You'll need:
* Python 3.13 or above
* A Discord bot account (see https://discord.com/developers)


Edit and rename `dotenv` to `.env`
```
DISCORD_TOKEN="YOURTOKENHERE"
APHOST="https://archipelago.gg" # Change If you are connecting to a different host.

```bash
pip install -r requirements.txt
python bot.py
```

## Development
You can use `ApWebAPI.py` file by itself. 
```python
from archipelago_api import ArchipelagoAPI
    # Defaults to https://archipelago.gg
    room_json = ArchipelagoAPI("Yourhostedinstancehere").get_room_status("MYxwlrpbQd1OG3e1IVkJl9A")
```