import json

SEND_TO_ALL_OWNER = 'send_message_to_all_owner_peer' 
SEND_TO_ALL_PEER = 'send_message_to_all_peer'
SEND_TO_ALL_EDGE = 'send_message_to_all_edge'

PASS_TO_CLIENT_APP = 'pass_message_to_client_application'


class MyProtocolMessageHandler:
    def __init__(self):
        print('Initializing MyProtocolMessageHandler...')

    def handle_message(self, msg, api):
        msg = json.loads(msg)

        my_api = api('api_type', None)
        print('my_api: ', my_api)
        if my_api == 'server_core_api':
            print('Bloadcasting ...', json.dumps(msg, sort_keys=True, ensure_ascii=False))
            api(SEND_TO_ALL_OWNER, json.dumps(msg, sort_keys=True, ensure_ascii=False))
            api(SEND_TO_ALL_PEER, json.dumps(msg, sort_keys=True, ensure_ascii=False))
            api(SEND_TO_ALL_EDGE, json.dumps(msg, sort_keys=True, ensure_ascii=False))
        else:
            print('MyProtocolMessageHandler received ', msg)
            api(PASS_TO_CLIENT_APP, msg)

        return
