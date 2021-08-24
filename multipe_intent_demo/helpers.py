#
# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import boto3
import time
import logging
import json
import pprint
import os
import config as help_desk_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_slot_values(slot_values, intent_request):
    if slot_values is None:
        slot_values = {key: None for key in help_desk_config.SLOT_CONFIG}

    slots = intent_request['currentIntent']['slots']

    for key, config in help_desk_config.SLOT_CONFIG.items():
        slot_values[key] = slots.get(key)
        logger.debug('<<help_desk_bot>> retrieving slot value for %s = %s', key, slot_values[key])
        if slot_values[key]:
            if config.get('type', help_desk_config.ORIGINAL_VALUE) == help_desk_config.TOP_RESOLUTION:
                # get the resolved slot name of what the user said/typed
                if len(intent_request['currentIntent']['slotDetails'][key]['resolutions']) > 0:
                    slot_values[key] = intent_request['currentIntent']['slotDetails'][key]['resolutions'][0]['value']
                else:
                    errorMsg = help_desk_config.SLOT_CONFIG[key].get('error', 'Sorry, I don\'t understand "{}".')
                    raise help_desk_config.SlotError(errorMsg.format(slots.get(key)))

    return slot_values


def get_remembered_slot_values(slot_values, session_attributes):
    logger.debug('<<help_desk_bot>> get_remembered_slot_values() - session_attributes: %s', session_attributes)

    str = session_attributes.get('rememberedSlots')
    remembered_slot_values = json.loads(str) if str is not None else {key: None for key in help_desk_config.SLOT_CONFIG}

    if slot_values is None:
        slot_values = {key: None for key in help_desk_config.SLOT_CONFIG}

    for key, config in help_desk_config.SLOT_CONFIG.items():
        if config.get('remember', False):
            logger.debug('<<help_desk_bot>> get_remembered_slot_values() - slot_values[%s] = %s', key,
                         slot_values.get(key))
            logger.debug('<<help_desk_bot>> get_remembered_slot_values() - remembered_slot_values[%s] = %s', key,
                         remembered_slot_values.get(key))
            if slot_values.get(key) is None:
                slot_values[key] = remembered_slot_values.get(key)

    return slot_values


def remember_slot_values(slot_values, session_attributes):
    if slot_values is None:
        slot_values = {key: None for key, config in help_desk_config.SLOT_CONFIG.items() if config['remember']}
    session_attributes['rememberedSlots'] = json.dumps(slot_values)
    logger.debug('<<help_desk_bot>> Storing updated slot values: %s', slot_values)
    return slot_values


def get_latest_slot_values(intent_request, session_attributes):
    slot_values = session_attributes.get('slot_values')

    try:
        slot_values = get_slot_values(slot_values, intent_request)
    except config.SlotError as err:
        raise help_desk_config.SlotError(err)

    logger.debug('<<help_desk_bot>> "get_latest_slot_values(): slot_values: %s', slot_values)

    slot_values = get_remembered_slot_values(slot_values, session_attributes)
    logger.debug('<<help_desk_bot>> "get_latest_slot_values(): slot_values after get_remembered_slot_values: %s',
                 slot_values)

    remember_slot_values(slot_values, session_attributes)

    return slot_values


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    logger.info('<<help_desk_bot>> "Lambda fulfillment function response = \n' + pprint.pformat(response, indent=4))

    return response


def elicitIntent(session_attributes, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': message
        }
    }

    logger.info('<<help_desk_bot>> "Lambda fulfillment function response = \n' + pprint.pformat(response, indent=4))

    return response


def elicitIntentResponse(session_attributes, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': message
        },
        "responseCard": {
            "version": 1,
            "contentType": "application/vnd.amazonaws.card.generic",
            "genericAttachments": [
                {
                    "buttons": [
                        {
                            "text": "button-text",
                            "value": "Value sent to server on button click"
                        }
                    ]
                }
            ]
        }
    }

    logger.info('<<help_desk_bot>> "Lambda fulfillment function response = \n' + pprint.pformat(response, indent=4))

    return response


def confirmIntent(session_attributes, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'message': message
        },
        "intentName": "getSuggestionIntent"
    }

    logger.info('<<help_desk_bot>> "Lambda fulfillment function response = \n' + pprint.pformat(response, indent=4))

    return response


def suggestOptions(session_attributes,
                   message):  # title, button_1,value_1,button_2,value_2,button_3,value_3,button_4,value_4):
    return {
        'sessionAttributes': session_attributes,
        "dialogAction": {
            "type": "Close",
            'fulfillmentState': 'Fulfilled',
            "message": {
                "contentType": "CustomPayload",
                #   "content": "{\"messages\":[{\"type\":\"PlainText\",\"group\":1,\"value\":\"Hello\"},{\"type\":\"PlainText\",\"group\":2,\"value\":\"Hey\"}]}"
                #   "content" : "Hi! I am your  Deloitte AI Institute  Chat Bot, I can help you with different sections!.You can choose one of the options below or write your own question",
                "content": message
            },
            "responseCard": {
                "version": 1,
                "contentType": "application/vnd.amazonaws.card.generic",
                "genericAttachments": [
                    #   {
                    #     'title': title,
                    #     'subTitle': 'Innovation',
                    #     # 'attachmentLinkUrl': 'link_that_will_open_on_click',
                    #     'imageUrl': 'https://deloitte.wsj.com/cio/files/2021/02/Data-governance-IMAGE.png',
                    #     "buttons":[
                    #          {
                    #             "text": button_1,
                    #             "value": value_1
                    #          },
                    #          {
                    #             "text": button_2,
                    #             "value":value_2
                    #          },
                    #          {
                    #             "text":button_3,
                    #             "value":value_3
                    #         },
                    #          {
                    #             "text":button_4,
                    #             "value":value_4
                    #          }

                    #       ]
                    #   },
                    {
                        'title': 'AI Innovation',
                        'subTitle': 'Innovation',
                        # 'attachmentLinkUrl': 'link_that_will_open_on_click',
                        'imageUrl': 'https://deloitte.wsj.com/cio/files/2021/02/Data-governance-IMAGE.png',
                        "buttons": [
                            {
                                "text": "Deloitte's State of AI in the Enterprise",
                                "value": "Deloitte's State of AI in the Enterprise"
                            },
                            {
                                "text": "Humans with Machines",
                                "value": "Humans with Machines"
                            },
                            {
                                "text": "ML Ops in Business",
                                "value": "ML Ops in Business"
                            },
                            {
                                "text": "More Options",
                                "value": "What is AI Innovation"
                            }

                        ]
                    },
                    {

                        'title': 'AI Ethics ',
                        'subTitle': 'Ethics',
                        'attachmentLinkUrl': 'https://deloitte.wsj.com/cio/2021/02/24/the-ai-era-is-here-is-your-data-governance-ready/',
                        'imageUrl': 'https://www2.deloitte.com/content/dam/Deloitte/us/Images/header_images/abstract/ai-ethicists-banner.jpg/_jcr_content/renditions/cq5dam.web.1400.350.desktop.jpeg',

                        "buttons": [
                            {
                                "text": "TrustWorth AI Framework",
                                "value": "TrustWorth AI Framework?"
                            },
                            {
                                "text": "Conquering AI Risk",
                                "value": "Conquering AI Risk?"
                            }
                        ]
                    },
                    {

                        'title': 'AI Enterprise ',
                        'subTitle': 'AI Enterprise',
                        'attachmentLinkUrl': 'https://deloitte.wsj.com/cio/2021/02/24/the-ai-era-is-here-is-your-data-governance-ready/',
                        'imageUrl': 'https://www2.deloitte.com/content/dam/Deloitte/ch/Images/header_images/industries/life-sciences-and-health-care/deloitte-ch-brain-in-hand-banner.jpg/_jcr_content/renditions/cq5dam.web.1400.350.desktop.jpeg',

                        "buttons": [
                            {
                                "text": "AI in Biopharma",
                                "value": "AI in Biopharma"
                            },
                            {
                                "text": "Colorado Labor Department Software Flags Thousands of Claims",
                                "value": "Colorado Labor Department Software Flags Thousands of Claims"
                            },
                            {
                                "text": "More Options",
                                "value": "what is AI Enterprise?"
                            }

                        ]
                    },
                    {

                        'title': 'AI Talent ',
                        'subTitle': 'AI Talent',
                        'attachmentLinkUrl': 'https://deloitte.wsj.com/cio/2021/02/24/the-ai-era-is-here-is-your-data-governance-ready/',
                        'imageUrl': 'https://www2.deloitte.com/content/dam/insights/us/articles/us43244_human-capital-trends-2020/us53443_superteams/images/53443_banner.jpg/jcr:content/renditions/cq5dam.web.1440.660.jpeg',

                        "buttons": [
                            {
                                "text": "Redesigning the Post-Pandemic Workplace",
                                "value": "Redesigning the Post-Pandemic Workplace"
                            },
                            {
                                "text": "More Options",
                                "value": "what is Talent?"
                            }
                        ]
                    },
                    {

                        'title': 'AI Services ',
                        'subTitle': 'AI Services',
                        'attachmentLinkUrl': 'https://deloitte.wsj.com/cio/2021/02/24/the-ai-era-is-here-is-your-data-governance-ready/',
                        'imageUrl': 'https://www2.deloitte.com/content/dam/Deloitte/us/Images/header_images/us-circle-banners/blue-green-abstarct-cosmos-particle-banner.jpg/_jcr_content/renditions/cq5dam.web.1400.350.desktop.jpeg',

                        "buttons": [
                            {
                                "text": "Tax",
                                "value": "Tax"
                            },
                            {
                                "text": "More Options",
                                "value": "What is Services"
                            }
                        ]
                    }
                ]

            }
        }
    }


def config_file():
    return {
        "Welcome": {
            "message": ["Hi i am deloitte Assistant", "Hi nice to meet you i am the deloitte assistant",
                        " Hey. Welcome. I am the deloitte assistant"],
            "Title": ["AI Innovation", "AI Innovation", " AI Innovation", " 'AI Innovation", "AI Innovation"],

            "AI Innovation": {"Deloitte's State of AI in the Enterprise": "Deloitte's State of AI in the Enterprise",
                              "Humans with Machines": "Humans with Machines",
                              "ML Ops in Business": "ML Ops in Business",
                              "Similar Options": "what is AI Innovation?"
                              },

            "AI Ethics": {
                "TrustWorth AI Framework": "TrustWorth AI Framework",
                "Conquering AI Risk": "Conquering AI Risk"

            },

            "AI Enterprise": {
                "AI in Biopharma": "AI in Biopharma",
                "Colorado Labor Department Software Flags Thousands of Claims": "Colorado Labor Department Software Flags Thousands of Claims",
                "More Options": "what is AI Enterprise?"
            },
            "AI Talent": {
                "Redesigning the Post-Pandemic Workplace": "Redesigning the Post-Pandemic Workplace",
                "More Options": "what is Talent?"
            }

        }
    }

