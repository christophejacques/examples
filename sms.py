import requests
import urllib


ERROR_API = "Error during API call"
URL = 'https://api.smsmode.com/http/1.6/'
PATH_SEND_SMS = "sendSMS.do"


"""
*    - access_token (required)
*    - message (required)
*    - destinataires (required): Receivers separated by a comma
*    - emetteur (optional): Allows to deal with the sms sender
*    - option_stop (optional): Deal with the STOP sms when marketing send (cf. API HTTP documentation)
"""
class ExempleClientHttpApi:

    # send SMS with GET method
    def send_sms_get(self, access_token, message, destinataires, emetteur, option_stop):
        final_url = (
            URL + PATH_SEND_SMS +
            '?accessToken=' + access_token +
            '&message=' + urllib.request.quote(message.encode('iso-8859-15')) +
            '&numero=' + destinataires + 
            '&emetteur=' + emetteur + 
            '&stop=' + option_stop
        )
        r = requests.get(final_url)
        if not r:
            return ERROR_API
        return r.text


sms = ExempleClientHttpApi()
try:
    sms.send_sms_get("qk78bsmQ2JtniitkXfL2mVpL2fkn34Om", "message API", "33666439347", "33666439347", "36034")
except Exception as e:
    print("Error:", e)
