import requests
from flask import Flask, render_template, request
import json

clientID = "C714b104c6dda60bbb378bb7e5e8a1dcec16c01e8ad2764e083bf8bcec19b9c8"
secretID = "4a8995bcb5b94f2ff782328afc3906a6701a090558b1ec017867781c6c51826"
redirectURI = "https://<your server ip or domain>:5007/oauth" #This could be different if you publicly expose this endpoint.



def get_tokens(code):
    """Gets access token and refresh token"""
    print("code:", code)
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&""code={2}&redirect_uri={3}").format(clientID, secretID, code, redirectURI)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    print(results)
    access_token = results["access_token"]
    refresh_token = results["refresh_token"]
    return access_token, refresh_token



app = Flask(__name__)


@app.route("/")
def main_page():
    """Main Grant page"""
    return render_template("index.html")


@app.route("/oauth")  # Endpoint acting as Redirect URI.
def oauth():
    """Retrieves oauth code to generate tokens for users"""

    if "code" in request.args and "state" in request.args:
        state = request.args.get("state")  # Captures value of the state.
        code = request.args.get("code")  # Captures value of the code.
        if state == "HELMUT_STRING":
            print("OAuth code:", code)
            print("OAuth state:", state)
            access_token, refresh_token = get_tokens(code)  # As you can see, get_tokens() uses the code and returns access and refresh tokens.

            return render_template("granted.html", access_token=access_token, refresh_token=refresh_token)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")


################################################################################################
# Run the server app
if __name__ == "__main__":
    # Do not keep debug=True in production
    app.run(host='0.0.0.0', port=5007, use_reloader=True, debug=True, ssl_context='adhoc') #, ssl_context='adhoc'


