import json
from datetime import datetime


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


def lambda_handler(event, context):
    print(json.dumps(event))

    session_attributes = event.get("sessionAttributes", {})
    current_intent = event.get("currentIntent", {})
    slots = current_intent.get("slots")
    current_intent_name = current_intent.get("name")

    # if current_intent.get("confirmationStatus") == "None":
    #     return dialog_confirm_intent(current_intent_name, plainText("Are you sure want to book a room?"))

    response = dialog_delegate(slots, session_attributes);
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
    print(json.dumps(response))

    return response