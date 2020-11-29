import os
import json
import pyrebase
from typing import Union
from datetime import datetime
from dotenv import load_dotenv
from data.data_generator import generate_random_image


load_dotenv()


def _get_datetime_string() -> str:
    return datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')


def _read_firebase_config():
    with open("./secrets.json", "r") as f:
        return json.loads(f.read())


def notify():
    pass


def upload_image(storage, content: Union[str, bytes]) -> dict:
    return storage.child(f"/saved-image_{_get_datetime_string()}.jpg").put(content)


def upload_data(storage, database, content: Union[str, bytes], id_token: str):
    metadata = upload_image(storage, content)
    url = storage.child(f"/{metadata['name']}").get_url(metadata['downloadTokens'])
    data = {
        'timeCreated': metadata['timeCreated'],
        'imageUrl': url,
        'coordinates': {
            'latitude': '???',
            'longitude': '???',
        },
    }
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    database.child(date).child(time).push(data, id_token)


def retrieve(database):
    all_users = database.get()
    for user in all_users.each():
        print(user.val())


def main():
    firebase = pyrebase.initialize_app(_read_firebase_config())
    auth = firebase.auth()
    storage = firebase.storage()
    database = firebase.database()

    user = auth.sign_in_with_email_and_password(os.getenv('EMAIL'), os.getenv('PASSWORD'))

    image = generate_random_image(ext=".png")
    upload_data(storage=storage, database=database, content=image, id_token=user["idToken"])


if __name__ == '__main__':
    main()
