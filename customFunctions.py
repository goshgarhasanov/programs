import collections.abc
import json
from twocaptcha import TwoCaptcha
import sys
import os
import requests
from anticaptchaofficial.recaptchav3proxyless import *
from anticaptchaofficial.hcaptchaproxyless import *

def getConfigs():
    f = open('config.json')
    data = json.load(f)
    return data

def isArrayss(arr):
    return isinstance(arr, list)


def getAuthToken(company):
    url = f'https://bezkolejki.eu/api/Authentication/GetEmptyToken/{company}'
    r = requests.get(url)
    token = r.json()['token']
    return token


def getSolvedToken(action, score, company):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    api_key = os.getenv('APIKEY_2CAPTCHA', '43d8b60777446f77cf2dd6e70bb49119')
    solver = TwoCaptcha(api_key)
    try:
        result = solver.recaptcha(
            sitekey='6LeCXbUUAAAAALp9bXMEorp7ONUX1cB1LwKoXeUY',
            url=f'https://bezkolejki.eu/{company}',
            version='v3',
            action=action,
            score=score
        )
    except Exception as e:
        sys.exit(e)
    else:
        return result['code']


# def solveHcaptcha(site_key='b3f14452-58e2-4030-82ae-9d4647a77b88', url='https://bezkolejki.eu/luw-olp'):
#     api_key = os.getenv('APIKEY_2CAPTCHA', '43d8b60777446f77cf2dd6e70bb49119')
#     solver = TwoCaptcha(api_key)
#     try:
#         result = solver.hcaptcha(
#             sitekey=site_key,
#             url=url,
#         )
#     except Exception as e:
#         print(e)
#         return False
#     else:
#         return result['code']


def getSolvedAnticaptchaToken(company, score, action):
    solver = recaptchaV3Proxyless()
    solver.set_verbose(1)
    solver.set_key("37dbb136855a196105b72dbeee61aef8")
    solver.set_website_url(f"https://bezkolejki.eu/{company}")
    solver.set_website_key("6LeCXbUUAAAAALp9bXMEorp7ONUX1cB1LwKoXeUY")
    solver.set_page_action(action)
    solver.set_min_score(score)

    # Specify softId to earn 10% commission with your app.
    # Get your softId here: https://anti-captcha.com/clients/tools/devcenter
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        return g_response
    else:
        return ("task finished with error " + solver.error_code)


def solveHcaptchaAntiCaptcha():
    solver = hCaptchaProxyless()
    solver.set_verbose(1)
    solver.set_key("37dbb136855a196105b72dbeee61aef8")
    solver.set_website_url("https://bezkolejki.eu/")
    solver.set_website_key("b3f14452-58e2-4030-82ae-9d4647a77b88")
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        return g_response
    else:
        return "task finished with error " + solver.error_code




def getSlotProperties(tkn):
    url = f'https://bezkolejki.eu/api/Slot/GetPropertiesForSlot'
    headers = {'Authorization': f'Bearer {tkn}'}
    r = requests.get(url, headers=headers)
    dates = r.json()
    return dates


def updateSlotProperties(properties, company, score, token):
    # token=getSolvedAnticaptchaToken(company,score ,'UpdateSlotProperties' )
    url = f'https://bezkolejki.eu/api/Slot/UpdateSlotProperties'
    data = json.dumps({"isAnonymous": "false", "properties": properties})
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=data)
    dates = r.json()
    return dates


def dataCustomize(data, inputData):
    for i in range(len(data)):
        data[i]['value'] = inputData[i]
    return data


def confirmReservation(tokenJwt, score,tokenRec):
    url = f'https://bezkolejki.eu/api/Slot/ConfirmReservation'
    data = json.dumps({
        "captchaToken": tokenRec,
        "isAnonymous": False, "smsCode": "", "allowSendDocument": False})
    headers = {'Authorization': f'Bearer {tokenJwt}', 'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=data)
    return r.json()


def getAvailableDaysSlots(authTkn, opid, solvedToken, day, company='luw-olp'):
    # solvedToken = getSolvedToken('GetAvailableSlotsForOperationAndDay', score, {company})
    url = f'https://bezkolejki.eu/api/Slot/GetAvailableSlotsForOperationAndDay?companyName={company}&lastStepId={opid}&day={day}&recaptchaToken={solvedToken}'
    headers = {'Authorization': f'Bearer {authTkn}'}
    r = requests.get(url, headers=headers)
    dates = r.json()
    return dates




def blockSlot(authTkn, slotId, cmpnyName, slvRecaptchaTkn, slvHcaptchaTkn):
    # slvRecaptchaTkn = getSolvedToken('BlockSlot', score, cmpnyName)

    data = json.dumps({"slotId": f"{slotId}", "companyName": f"{cmpnyName}",
                       "captchaToken": f"{slvRecaptchaTkn}",
                       "captchaV2Token": f"{slvHcaptchaTkn}"})

    url = f'https://bezkolejki.eu/api/Slot/BlockSlot'
    headers = {'Authorization': f'Bearer {authTkn}', 'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=data)
    jwtToken = r.json()
    return jwtToken



