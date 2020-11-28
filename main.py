import json
import pyrebase
from typing import Union
from datetime import datetime


def _get_datetime_string() -> str:
    return datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')


def _read_firebase_config():
    with open("./secrets.json", "r") as f:
        return json.loads(f.read())


def notify():
    pass


def upload_image(storage, content: Union[str, bytes]) -> dict:
    return storage.child(f"/saved-image_{_get_datetime_string()}.jpg").put(content)


def upload_data(storage, database, content: Union[str, bytes]):
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
    database.push(data)


def main():
    firebase = pyrebase.initialize_app(_read_firebase_config())
    storage = firebase.storage()
    database = firebase.database()

    with open("./data/sample-image.jpg", "rb") as f:
        content = f.read()

    upload_data(storage=storage, database=database, content=content)
    notify()

    # reterving data using loops
    # all_users = database.get()
    # for user in all_users.each():
    #     print(user.val())


if __name__ == '__main__':
    main()
