from customFunctions import *
import datetime
import time

from multiprocessing import Process
configs = getConfigs()
score = configs['score']
companyName = configs['company']
day = configs['day']
operationId = configs['opId']
captchaTimes = configs['captchaTimes']
runTimes = configs['runTimes']


def getCaptchas():
    print("CAPTCHALAR HAZIRLANIR")
    blockSlotHcaptchaToken = solveHcaptchaAntiCaptcha()
    time.sleep(20)
    slotsForOperationsToken = getSolvedAnticaptchaToken(companyName, score,
                                                        'GetAvailableSlotsForOperationAndDay')
    blockSlotToken = getSolvedAnticaptchaToken(companyName, score, 'BlockSlot')
    tokenConfirm = getSolvedAnticaptchaToken(companyName, score, 'ConfirmReservation')
    print("CAPTCHALAR HAZIRDIR BASLAYAQ")
    return {'blockSlotHcaptcha': blockSlotHcaptchaToken, 'slotsForOperationsToken': slotsForOperationsToken,
            'blockSlotToken': blockSlotToken, 'tokenConfirm': tokenConfirm}


# time.sleep(60)
def startBot(slotID, blockSlotToken, blockSlotHcaptchaToken, tokenConfirm):
    slotId = slotID
    print(slotId)
    jwtToken = blockSlot(autToken, slotId, companyName, blockSlotToken, blockSlotHcaptchaToken)
    print(jwtToken)
    inputs = getSlotProperties(jwtToken['token'])
    print(inputs)
    customizeData = dataCustomize(inputs, configs['inputs'])
    updateResp = updateSlotProperties(customizeData, companyName, score, jwtToken['token'])
    if (updateResp == True):
        lastResult = confirmReservation(jwtToken['token'], score, tokenConfirm)

        print(lastResult)
        print("Yer Alindi emailiniz kontrol edin")
        time.sleep(60)
        exit()
    else:
        print("Slot Update Olunmadi")

if __name__ == "__main__":
    while 1:
        time.sleep(1)
        currentime = datetime.datetime.now()
        nowHour = currentime.strftime('%H:%M:%S')
        if nowHour in captchaTimes:
            captchalar = getCaptchas()
            autToken = getAuthToken(companyName)
            daysSlots = getAvailableDaysSlots(autToken, operationId, captchalar['slotsForOperationsToken'], day,
                                              companyName)
            if(isArrayss(daysSlots)):

                while 1:
                    mycrntTIme = datetime.datetime.now()
                    nowStartHour = mycrntTIme.strftime('%H:%M:%S')
                    if (nowStartHour in runTimes):
                        startBot(daysSlots[configs['slotID']]['id'], captchalar['blockSlotToken'],
                                 captchalar['blockSlotHcaptcha'], captchalar['tokenConfirm'])
                break
            else:
                print(f"XETA     {daysSlots}")
