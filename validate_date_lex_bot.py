import json
from datetime import datetime

event = {
    "messageVersion": "1.0",
    "invocationSource": "DialogCodeHook",
    "userId": "gvaxmipgyix1kqu8k8c5dnmpbmpmqaqg",
    "sessionAttributes": {},
    "requestAttributes": None,
    "bot": {
        "name": "BookHoteBySk",
        "alias": "$LATEST",
        "version": "$LATEST"
    },
    "outputDialogMode": "Text",
    "currentIntent": {
        "name": "book_hotel_intent_sk",
        "slots": {
            "fromDate": "2021-08-21",
            "rooms": "2",
            "toDate": "2021-08-22",
            "whichCity": "texas",
            "roomType": "VIP"
        },
        "slotDetails": {
            "fromDate": {
                "resolutions": [
                    {
                        "value": "2021-08-21"
                    }
                ],
                "originalValue": "tomorrow"
            },
            "rooms": {
                "resolutions": [
                    {
                        "value": "2"
                    }
                ],
                "originalValue": "2"
            },
            "toDate": {
                "resolutions": [
                    {
                        "value": "2021-08-22"
                    }
                ],
                "originalValue": "22-08-2021"
            },
            "whichCity": {
                "resolutions": [],
                "originalValue": "texas"
            },
            "roomType": {
                "resolutions": [
                    {
                        "value": "VIP"
                    }
                ],
                "originalValue": "vip"
            }
        },
        "confirmationStatus": "None",
        "nluIntentConfidenceScore": 1
    },
    "alternativeIntents": [
        {
            "name": "AMAZON.FallbackIntent",
            "slots": {},
            "slotDetails": {},
            "confirmationStatus": "None",
            "nluIntentConfidenceScore": None
        },
        {
            "name": "getDetailOfBooking",
            "slots": {
                "ticketNumber": None
            },
            "slotDetails": {
                "ticketNumber": None
            },
            "confirmationStatus": "None",
            "nluIntentConfidenceScore": 0.34
        }
    ],
    "inputTranscript": "vip",
    "recentIntentSummaryView": [
        {
            "intentName": "book_hotel_intent_sk",
            "checkpointLabel": None,
            "slots": {
                "fromDate": "2021-08-21",
                "rooms": "2",
                "toDate": "2021-08-22",
                "whichCity": "texas",
                "roomType": None
            },
            "confirmationStatus": "None",
            "dialogActionType": "ElicitSlot",
            "fulfillmentState": None,
            "slotToElicit": "roomType"
        }
    ],
    "sentimentResponse": {
        "sentimentLabel": "MIXED",
        "sentimentScore": "{Positive: 0.39050132,Negative: 0.011171613,Neutral: 0.17653176,Mixed: 0.42179528}"
    },
    "kendraResponse": None,
    "activeContexts": []
}

def dialog_close(message, session_attributes={}, fulfilled=False):
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled" if fulfilled else "Failed",
            "message": message,
        }
    }


def dialog_elicit_intent(message, session_attributes={}):
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitIntent",
            "message": message
        }
    }


def dialog_elicit_slot(intent_name, slot_to_elicit, message, slots, session_attributes={}):
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message
        }
    }


def dialog_confirm_intent(intent_name, message, session_attributes={}):
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ConfirmIntent",
            "intentName": intent_name,
            "message": message
        }
    }


def dialog_delegate(slots, session_attributes={}):
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Delegate",
            "slots": slots
        }
    }


def ssml(text):
    return {
        "contentType": "SSML",
        "content": text
    }


def plainText(text):
    return {
        "contentType": "PlainText",
        "content": text
    }


# main function to perform all the validation and to perform fulfillment action too
def book_hotel(event):
    print("Book Hotel Function Called")
    session_attributes = event.get("sessionAttributes", {})
    source = event["invocationSource"]
    print("SOURCE IS : ", source)
    slots = event["currentIntent"]["slots"]
    intent_name = event["currentIntent"]["name"]
    toDate = slots["toDate"]
    fromDate = slots["fromDate"]
    print("=======================")
    print(toDate, fromDate)
    response = dialog_delegate(slots=slots, session_attributes=session_attributes)
    # performing validation and fulfillment in same lambda
    if source == 'DialogCodeHook':
        # Date Validation
        if toDate is not None and fromDate is not None:
            if toDate < fromDate:
                print("========= toDate is less than fromDate=======")
                response = dialog_elicit_slot(intent_name,
                                              "toDate",
                                              plainText("Your To Date is ahead of fromDate, Please enter proper date"),
                                              {
                                                  **slots,
                                                  "toDate": None,
                                                  "roomType":None,
                                                  "rooms":None
                                              },
                                              session_attributes
                                              )
                print(response)
                return response
        return response
    # the portion below runs on fulfillment of all the slots
    return dialog_close(
                        message=plainText("Thank you for booking with us"),
                        session_attributes=session_attributes,
                        fulfilled=True
                        )

# Dispatcher Function
def dispatch(event):
    intent_name = event["currentIntent"]["name"]
    if intent_name == 'book_hotel_intent_sk':
        return book_hotel(event)

    # if the Intent Name is not matched then return error
    return Exception("Intent Name Not Found ")


def lambda_handler(event, context):
    print("========== Lambda Function Called : Printing the Even Variable ===========")
    print(json.dumps(event))
    return dispatch(event)