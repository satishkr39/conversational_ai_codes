evetn = {
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