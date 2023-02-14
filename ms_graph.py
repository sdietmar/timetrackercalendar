# https://learndataanalysis.org/ms_graph-py-source-code/
import webbrowser
from datetime import datetime
import json
import PySimpleGUI as sg
import os
import msal

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

def generate_access_token(app_id, scopes):
    # Save Session Token as a token file
    access_token_cache = msal.SerializableTokenCache()

    # read the token file
    if os.path.exists('ms_graph_api_token.json'):
        access_token_cache.deserialize(open("ms_graph_api_token.json", "r").read())
        token_detail = json.load(open('ms_graph_api_token.json',))
        token_detail_key = list(token_detail['AccessToken'].keys())[0]
        token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
        if datetime.now() > token_expiration:
            os.remove('ms_graph_api_token.json')
            access_token_cache = msal.SerializableTokenCache()

    # assign a SerializableTokenCache object to the client instance
    client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

    accounts = client.get_accounts()
    if accounts:
        # load the session
        token_response = client.acquire_token_silent(scopes, accounts[0])
        print(" account connected!")
    else:
        # authenticate your account as usual
        flow = client.initiate_device_flow(scopes=scopes)
        print('user_code: ' + flow['user_code'])

        # Create the PySimpleGUI popup
        layout = [
            [sg.Text("user_code: " + flow['user_code'])],
            [sg.Text("user_code: ", size=(15, 1)), sg.InputText(flow['user_code'])],
            [sg.Button("ok")]
        ]
        window = sg.Window("Authentication", layout)
        # Show the popup and get the user input
        while True:
            clickevent, values = window.read()
            if clickevent in (None, "ok"):
                break
        window.close()
        webbrowser.open('https://microsoft.com/devicelogin')
        token_response = client.acquire_token_by_device_flow(flow)

    with open('ms_graph_api_token.json', 'w') as _f:
        _f.write(access_token_cache.serialize())

    return token_response

if __name__ == '__main__':
    ...
