from json import load, JSONDecodeError

def get():
    try:
        with open('user_data.json','r') as file:
            credentials = load(file)
    except FileNotFoundError:
        print('File "user_data.json" not found')
        return None
    except JSONDecodeError:
        print('Error while decoding "user_data.json"')
        return None

    return credentials
