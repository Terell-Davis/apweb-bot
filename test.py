from ApWebAPI import ArchipelagoAPI
import os
import dotenv

api = ArchipelagoAPI(os.getenv('APHOST'))
data = api.get_room_status("gICCaVNrRu2TV9DIPn_YYA")
print(data)
print("===================================================")

players = data.get("players", [])
downloads = data.get("downloads", [])
slot_patches = {item['slot']: item['download'] for item in downloads}
ARCHIPELAGO_BASE = os.getenv('APHOST')
print(downloads)
print("======================")
print(slot_patches)
        
def get_patch_for_slot(slot_number, slot_patch):
    patch = slot_patch.get(slot_number)
    if patch is None:
        return "None"
    return f"{ARCHIPELAGO_BASE}{patch}"

lines = [
    f"{i+1}. **{name}** — *{game}* - {patch if (patch := get_patch_for_slot(i+1, slot_patches)) != 'None' else 'No Patch'}"
    for i, (name, game) in enumerate(players)
]