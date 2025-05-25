from panoptes_client import User
user = next(User.where(login='GRAVITYbot'))
print(user.id)