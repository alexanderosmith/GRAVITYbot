#from panoptes_client import User
import re
#user = next(User.where(login='GRAVITYbot'))
#print(user.id)

text = "Check these: https://first.com and https://second.com"

# Insert '+tab+' before every https://
result = re.sub(r'https://', r'+tab+https://', text)

print(result)