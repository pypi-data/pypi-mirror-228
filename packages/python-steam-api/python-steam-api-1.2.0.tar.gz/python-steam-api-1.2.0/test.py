import json

from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")


terraria_app_id = 105600
steam = Steam(KEY)

# arguments: app_id
user = steam.apps.get_app_details(terraria_app_id)

print(json.dumps(user))
