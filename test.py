import json
from datetime import datetime

event = {
    "messageVersion": "1.0",
    "invocationSource": "DialogCodeHook",
    "userId": "bt4xvx9s5b4udov05bjgtdhvom7f6k5x",
    "sessionAttributes": {

    },
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
            "fromDate": "2021-08-20",
            "rooms": "2",
            "toDate": "2021-08-19",
            "whichCity": "Texas",
            "roomType": "VIP"
        },
        "slotDetails": {
            "fromDate": {
                "resolutions": [
                    {
                        "value": "2021-08-20"
                    }
                ],
                "originalValue": "today"
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
                        "value": "2021-08-21"
                    }
                ],
                "originalValue": "tomorrow"
            },
            "whichCity": {
                "resolutions": [],
                "originalValue": "Texas"
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
                "fromDate": "2021-08-20",
                "rooms": "2",
                "toDate": "2021-08-21",
                "whichCity": "Texas",
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


def lambda_handler(event):
    # print(json.dumps(event, indent=4))

    session_attributes = event.get("sessionAttributes", {})
    current_intent = event.get("currentIntent", {})
    slots = current_intent.get("slots")
    current_intent_name = current_intent.get("name")

    # if current_intent.get("confirmationStatus") == "None":
    #     return dialog_confirm_intent(current_intent_name, plainText("Are you sure want to book a room?"))
    print("================================")
    print(slots)
    print("================================")
    response = dialog_delegate(slots, session_attributes)
    print(response)
    print("================================")
    print(slots.get("fromDate"),slots.get("toDate"),session_attributes.get("dateValidated"))
    # print(event['bot']['name'])  # Another way to access values
    if slots.get("fromDate") and slots.get("toDate") and not session_attributes.get("dateValidated"):
        fromDate = datetime.strptime(slots.get("fromDate"), "%Y-%m-%d")
        toDate = datetime.strptime(slots.get("toDate"), "%Y-%m-%d")
        if toDate < fromDate:
            response = dialog_elicit_slot(
                current_intent_name,
                "toDate",
                plainText(
                    "You have entered an invalid date, Your checkout date should be on or after the check in date"),
                {
                    **slots,
                    "toDate": None
                },
                session_attributes
            )
        else:
            response = dialog_delegate(slots, {
                **session_attributes,
                "dateValidated": True
            })
    # input_transcript = event.get("inputTranscript", "").strip()
    print(json.dumps(response, indent=3))

    return response

lambda_handler(event)