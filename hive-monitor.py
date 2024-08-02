import os
import pyhiveapi as Hive
from dotenv import load_dotenv

load_dotenv()

tokens = {}

hive_auth = Hive.Auth(os.getenv("HIVE_USERNAME"),os.getenv("HIVE_PASSWORD"))
auth_data = hive_auth.login()

if auth_data.get("ChallengeName") == "SMS_MFA":
    code = input("Enter your 2FA code: ")
    auth_data = hive_auth.sms_2fa(code, auth_data)

if "AuthenticationResult" in auth_data:
    session = auth_data["AuthenticationResult"]
    tokens.update({"token": session["IdToken"]})
    tokens.update({"refreshToken": session["RefreshToken"]})
    tokens.update({"accessToken": session["AccessToken"]})


api = Hive.API(token=tokens["token"])
data = api.getAll()
devices = data["parsed"]["devices"]
products = data["parsed"]["products"]

device_uuid = os.getenv("HIVE_DEVICE_UUID")

device = [d for d in devices if d["id"] == device_uuid][0]
# The power data is inside the products
print(device)
product = [p for p in products if p["id"] == device_uuid][0]
print(product)
power = product["props"]["powerConsumption"]
print(power)
