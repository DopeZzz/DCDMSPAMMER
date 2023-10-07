import requests
import threading

def send_message_with_token(TOKEN, user_id):
    HEADERS = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json',
    }

    session = requests.Session() 

    dm_channel_url = 'https://discord.com/api/v10/users/@me/channels'
    dm_data = {
        "recipient_id": user_id
    }

    dm_response = session.post(dm_channel_url, json=dm_data, headers=HEADERS)
    if dm_response.status_code == 200:
        dm_channel_id = dm_response.json().get("id")

        post_url = f'https://discord.com/api/v10/channels/{dm_channel_id}/messages'
        post_data = {
            "content": "test",
            "tts": False
        }

        response = session.post(post_url, json=post_data, headers=HEADERS)
        if response.status_code == 200:
            print(f"Message successfully sent using the token: {TOKEN}")
        else:
            print(f"Error sending message with token {TOKEN}: {response.status_code} {response.text}")
    else:
        print(f"Error creating DM channel with token {TOKEN}: {dm_response.status_code} {dm_response.text}")

tokens = []
with open('token.txt', 'r') as file:
    for line in file:
        tokens.append(line.strip())

user_id = input("Enter the user_id: ")

threads = []
for token in tokens:
    t = threading.Thread(target=send_message_with_token, args=(token, user_id))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All messages have been sent!")
