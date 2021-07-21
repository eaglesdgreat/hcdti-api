from .sms import *
new = SMS()


"""
Class that Handle sending of Message 
to also to filter what message to be 
sending out to customer and user of 
the system
"""

# Declare the Message type


def msgType(fullname, appid):
    new = fullname.split(' ')
    newname = new[0]
    msgFormat = {
        "CREDIT_APPROVED": f'Dear {newname}\n\nYour loan Application has been registered on our System with ID: {appid}.\n\nThanks\nHCDTI Team.',
        "BRANCH_APPROVED": f'Dear {newname}\n\nYour loan Application with ID: {appid} has PASS the 2nd stage.\n\nThanks\nHCDTI Team.',
        "BRANCH_DECLINED": f'Dear {newname}\n\nYour loan Application with ID: {appid} has FAIL the 2nd stage.\n\nThanks\nHCDTI Team.',
        "SENIOR_APPROVED": f'Dear {newname}\n\nYour loan Application with ID: {appid} has PASS the final stage.\n\nThanks\nHCDTI Team.',
        "SENIOR_DECLINE": f'Dear {newname}\n\nYour loan Application with ID: {appid} has FAIL the final stage.\n\nThanks\nHCDTI Team.',
        "DISBURSE": f'Dear {newname}\n\nYour loan Application with ID: {appid} has been disburse to your account NO.\n\nThanks\nHCDTI Team.',
    }
    return msgFormat


class HandleSms:

    ## Send Message ##
    def sendMessage(self, mobile, fullname, appid, msg_type):
        msgData = msgType(fullname, appid)
        msg = msgData[msg_type]
        new.SendSMS(mobile, msg)
        pass
