import requests, json

class RestClient:

    URL = 'https://panopticon.hal9k.dk/api/v1/'
    #URL = 'https://10.42.3.11/api/v1/'
    TOKEN = '1c824b9d79e73074610d4e2b0097ccb461b66e5f32de091060b7e32b35ec0d53'
    
    def check_card(self, card_id):
        data = '{ "api_token": "%s", "card_id": "%s" }' % (self.TOKEN, card_id)
        response = requests.post(self.URL + 'permissions', data=data, headers={"Content-Type": "application/json"}, verify=False)
        if response.status_code != 200:
            return { 'id': 0 }
        return response.json

    def log(self, id, msg):
        if id:
            data = '{ "api_token": "%s", "log": { "user_id": %d, "message": "%s" } }' % (self.TOKEN, id, msg)
        else:
            data = '{ "api_token": "%s", "log": { "message": "%s" } }' % (self.TOKEN, msg)
        response = requests.post(self.URL + 'logs', data=data, headers={"Content-Type": "application/json"}, verify=False)
        return response.status_code == 200
        
if __name__ == "__main__":
    r = RestClient()
    cc = r.check_card("0000BB96C5")
    print(cc)
    print(r.log(cc['id'], 'Dummy log entry'))
