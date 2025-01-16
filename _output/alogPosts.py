import os, sys, requests
from datetime import datetime
from panoptes_client import Panoptes
from dotenv import find_dotenv, load_dotenv

# Once Panoptes is connected, load the Bearer Token
_ = load_dotenv(find_dotenv())
user = os.environ.get("PANOPTES_USER")
pswd = os.environ.get("PANOPTES_PASS")
Panoptes.connect(username=user, password=pswd)
token = os.environ.get("PANOPTES_BEARER_TOKEN")

# If you’ve set up OAuth credentials or have them stored, you can also manually set a token. The above approach works for a straightforward login scenario.

#Post a Comment to Talk Using requests:

# Once you have a valid token from the above steps, you can make a POST request to the Talk API. In this example, we’ll assume you know the discussion_id and want to post a new comment.

# Base URL for the Talk API
TALK_API_BASE = "https://www.zooniverse.org/projects/zooniverse/gravity-spy/talk/"

# Example discussion_id you want to post to (ask Kevin to create the discussion id?)
discussion_id = 329
current_time = f"{datetime.now()}"
# JSON payload for your new comment
payload = {
    "comment": {
        "discussion_id": discussion_id,
        "body": f"test post: {current_time}"
    }
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Send the POST request
response = requests.post(f"{TALK_API_BASE}/comments", json=payload, headers=headers)

if response.status_code == 201:
    data = response.json()
    print("Comment posted successfully!")
    print("Response data:", data)
else:
    print("Failed to post comment. Status code:", response.status_code)
    print("Response:", response.text)
