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

import logging
import json
import helpers
import config
import boto3
import os
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info('<help_desk_bot>> Lex event info = ' + json.dumps(event))

    session_attributes = event.get('sessionAttributes', None)
    inputtranscript = event.get("inputTranscript")
    session_attributes["inputTranscript"] = inputtranscript
    print(inputtranscript)

    intentName = event.get("currentIntent").get('name', None)
    print(intentName)
    if intentName == "getFallBackIntenttwo":
        counter = counter + 1
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table("getMissedUtterances")
        import time
        ts = str(time.time())
        table.put_item(Item={"Timestamp": ts, 'utterance': inputtranscript})

    if session_attributes is None:
        session_attributes = {}

    logger.debug('<<help_desk_bot> lambda_handler: session_attributes = ' + json.dumps(session_attributes))

    currentIntent = event.get('currentIntent', None)
    if currentIntent is None:
        response_string = 'Sorry, I didn\'t understand.'
        return helpers.close(session_attributes, 'Fulfilled',
                             {'contentType': 'CustomPayload', 'content': response_string})

    if intentName is None:
        response_string = 'Sorry, I didn\'t understand.'
        return helpers.close(session_attributes, 'Fulfilled',
                             {'contentType': 'CustomPayload', 'content': response_string})

    # see HANDLERS dict at bottom
    if HANDLERS.get(intentName, False):
        if intentName == "getFallBackIntenttwo":
            return HANDLERS[intentName]['handler'](event, session_attributes, counter)  # dispatch to the event handler
        else:
            return HANDLERS[intentName]['handler'](event, session_attributes)  # dispatch to the event handler
    else:
        response_string = "The intent " + intentName + " is not yet supported."
        return helpers.close(session_attributes, 'Fulfilled',
                             {'contentType': 'CustomPayload', 'content': response_string})


def make_appointment_intent_handler(intent_request, session_attributes):
    try:
        slot_values = helpers.get_latest_slot_values(intent_request, session_attributes)
    except config.SlotError as err:
        return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'CustomPayload', 'content': str(err)})

    logger.debug('<<help_desk_bot>> make_appointment_intent_handler(): slot_values = %s', json.dumps(slot_values))

    if slot_values.get('time', None) is None:
        response_string = "Please check the bot configuration for slot {time}."
    elif slot_values.get('problem', None) is None:
        response_string = "Please check the bot configuration for slot {problem}."
    else:
        response_string = "Got it, we'll see you then to take a look at your {}.".format(slot_values['problem'])

    return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'CustomPayload', 'content': response_string})


def check_appointment_intent_handler(intent_request, session_attributes):
    try:
        slot_values = helpers.get_latest_slot_values(intent_request, session_attributes)
    except config.SlotError as err:
        return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'CustomPayload', 'content': str(err)})

    logger.debug('<<help_desk_bot>> check_appointment_intent_handler(): slot_values = %s', json.dumps(slot_values))

    if slot_values.get('time', None) is None:
        response_string = "We don't have a time set up yet."
    elif slot_values.get('problem', None) is None:
        response_string = "We don't have a problem identified yet."
    else:
        response_string = "Hi, we will see you at {} today to fix your {}.".format(slot_values['time'],
                                                                                   slot_values['problem'])

    return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'CustomPayload', 'content': response_string})


def hello_intent_handler(intent_request, session_attributes):
    message = "Hi! I am your  Deloitte AI Institute  Chat Bot, I can help you with different sections!.You can choose one of the options below or write your own question"
    # dict_1 = helpers.config_file()
    # welcome_dict = dict_1["Welcome"]
    # message =random.choice(welcome_dict["message"])
    # title= random.choice(welcome_dict["Title"])
    # print(title)
    # if title == "AI Innovation":
    #     button_dict = welcome_dict["AI Innovation"]
    #     button_1 =  list(button_dict.keys())[0]
    #     print(button_1)
    #     value_1  = list(button_dict.values())[0]
    #     print(value_1)
    #     button_2 = list(button_dict.keys())[1]
    #     value_2  = list(button_dict.values())[1]
    #     button_3 = list(button_dict.keys())[2]
    #     value_3  = list(button_dict.values())[2]
    #     button_4 = list(button_dict.keys())[3]
    #     value_4 = list(button_dict.values())[3]

    return helpers.suggestOptions(session_attributes, message)

    # response_string = "Hi! I am your  Deloitte AI Institute  Chat Bot.I can help you with different sections like Featured Insights, Innovation, Ethics, Talent, Service, AI In the Enterprise. What do you want to  do today?"
    # return helpers.elicitIntent(session_attributes,{'contentType': 'CustomPayload','content': response_string})
    # return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'CustomPayload','content': response_string})


def goodbye_intent_handler(intent_request, session_attributes):
    # clear session attributes to start over
    session_attributes = {}
    response_string = "Thanks! Have a great rest of your day."
    return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'CustomPayload', 'content': response_string})


def fallback_intent_handler(intent_request, session_attributes, counter):
    if counter == 1:
        response = {
            'sessionAttributes': session_attributes,
            "dialogAction": {
                "type": "Close",
                'fulfillmentState': 'Fulfilled',
                "message": {
                    "contentType": "PlainText",
                    "content": "Let me help you suggest something. Choose an option below and i will suggest you some articles"
                },
                "responseCard": {
                    "version": 1,
                    "contentType": "application/vnd.amazonaws.card.generic",
                    "genericAttachments": [
                        {
                            "buttons": [
                                {
                                    "text": text_1,
                                    "value": value_1
                                },
                                {
                                    "text": "Innovation in AI Public Industries",
                                    "value": "Innovation in AI Public Industries"
                                }
                            ]
                        }
                    ]
                }
            }
        }
        return response
        # response = "Sorry, I was not able to understand your question. Do you want to try again?"
        # return helpers.elicitIntent(session_attributes, {'contentType': 'PlainText','content': response})

    elif counter == 2:
        response = "Sorry,I seriously dont understand what you mean."
        return helpers.elicitIntent(session_attributes, {'contentType': 'PlainText', 'content': response})
    else:
        response = "Let me help you suggesting something. You can ask us about AI in Indusries, talent, innovation ethics. Just write your query down and i will help you find it"
        return helpers.elicitIntent(session_attributes, {'contentType': 'PlainText', 'content': response})


def search_intent_handler(intent_request, session_attributes):
    import boto3
    import pprint

    kendra = boto3.client('kendra')

    query = session_attributes["inputTranscript"]
    index_id = os.environ['KENDRA_INDEX']
    response = kendra.query(
        QueryText=query,
        IndexId=index_id)

    try:
        response["ResultItems"][0]["AdditionalAttributes"][1]["Value"]["TextWithHighlightsValue"]["Text"]
        final_answer_list = "Here these are the links i could find. Happy reading!:\n"
    except:

        if "counter" not in session_attributes:
            session_attributes["counter"] = 0
            counter = session_attributes["counter"]
        elif session_attributes["counter"] == None:
            counter = 0
        else:
            counter = int(session_attributes["counter"])
            counter += counter + 1

        if counter == 0:

            response = "Sorry,I could not find anything related to that. Can you try framing it in a different way?"
            return helpers.close(session_attributes, "Fulfilled", {'contentType': 'PlainText', 'content': response})
        else:
            final_answer_list = "Sorry, I could not find any information about this Query.Let me suggest you something.You can choose from one of the options below"
            session_attributes["counter"] = None
            a = [
                {
                    'title': 'AI Innovation',
                    'subTitle': 'Innovation',
                    # 'attachmentLinkUrl': 'link_that_will_open_on_click',
                    'imageUrl': 'https://deloitte.wsj.com/cio/files/2021/02/Data-governance-IMAGE.png',
                    "buttons": [
                        {
                            "text": "Deloitte's State of AI in the Enterprise",
                            "value": "Deloitte's State of AI in the Enterprise?"
                        },
                        {
                            "text": "Humans with Machines",
                            "value": "Humans with Machines?"
                        },
                        {
                            "text": "ML Ops in Business",
                            "value": "ML Ops in Business?"
                        },
                        {
                            "text": "More Options",
                            "value": "what is AI Innovation?"
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
            return {
                'sessionAttributes': session_attributes,
                "dialogAction": {
                    "type": "Close",
                    'fulfillmentState': 'Fulfilled',
                    "message": {
                        "contentType": "CustomPayload",
                        #   "content": "{\"messages\":[{\"type\":\"PlainText\",\"group\":1,\"value\":\"Hi! I am your  Deloitte AI Institute  Chat Bot!\"},{\"type\":\"PlainText\",\"group\":2,\"value\":\"I can help you with different sections\"},{\"type\":\"PlainText\",\"group\":2,\"value\":\"You can choose one of the options below or write your own question\"}]}"
                        "content": final_answer_list
                    },
                    "responseCard": {
                        "version": 1,
                        "contentType": "application/vnd.amazonaws.card.generic",
                        "genericAttachments": a

                    }
                }
            }

    for i in range(len(response["ResultItems"])):
        answers = response["ResultItems"][i]["AdditionalAttributes"][1]["Value"]["TextWithHighlightsValue"]["Text"]
        url = response["ResultItems"][i]["DocumentURI"]
        # answer_list.append(answers)
        # url_list.append(url_list)
        # print(answers)
        # print(url)

        # final_answer_list += '-' +"<a href = " + url + "</a>" + '|' + answers + '>\n'
        # final_answer_list += '-' +'<a href = " + url +'>'+ answers + "</a\n>'
        final_answer_list = ' ' + "lt a href = " + url + "gt" + answers + "lt /a gt"

    print(final_answer_list)
    print(type(final_answer_list))
    # return helpers.elicitIntent(session_attributes,{'contentType': 'PlainText','content': final_answer_list})
    return helpers.close(session_attributes, 'Fulfilled',
                         {'contentType': 'CustomPayload', 'content': final_answer_list})
    # for i in range(len(final_answer_list)):

    #     response = {
    #         'sessionAttributes': session_attributes,
    #         'dialogAction': {
    #             'type': 'ElicitIntent',
    #             'message': "Here are some documents you could review:\n"
    #         },
    #         "responseCard": {
    #          "version": 1,
    #          "contentType": "application/vnd.amazonaws.card.generic",
    #          "genericAttachments": [
    #               {
    #              "buttons":[
    #                  {
    #                     "text": final_answer_list[i],
    #                     "value": final_answer_list[i]
    #                  }
    #               ]
    #           }
    #       ]
    #     }
    #     }
    # return response

    # contentType": "CustomPayload",
    #     "content":
    # return helpers.elicitIntent(session_attributes, {'contentType': 'CustomPayload','content': response})

    # response = kendra.query(
    # IndexId='a1e57ab6-bc0c-4d28-bf5b-d7014a6d9fb2',
    # QueryText= session_attributes["inputTranscript"],
    # QueryResultTypeFilter='ANSWER'
    # )
    # kendraQuery = {
    # "IndexId": "a1e57ab6-bc0c-4d28-bf5b-d7014a6d9fb2",
    # "QueryResultTypeFilter": "ANSWER"
    # }

    # print(kendraQuery)

    # return {
    #     "dialogAction": {
    #         "type": "Delegate",
    #         "kendraQueryRequestPayload": kendraQuery
    #     }
    # }
    # print(response)

    # return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'customPayload','content': "The answer i found was this -((x-amz-lex:kendra-search-response-question_answer-answer-1))"})


def elicit_suggestion_intent_handler(intent_request, session_attributes):
    print("161")
    source = intent_request['invocationSource']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    slots = intent_request['currentIntent']['slots']
    print(slots)
    if slots['InnovationSubCategory'] == None:

        if slots["category"] == "Innovation":
            print("167")

            response = {
                'sessionAttributes': session_attributes,
                "dialogAction": {
                    "type": "Close",
                    'fulfillmentState': 'Fulfilled',
                    "message": {
                        "contentType": "PlainText",
                        "content": "What subtopic would you like to choose?"
                    },
                    "responseCard": {
                        "version": 1,
                        "contentType": "application/vnd.amazonaws.card.generic",
                        "genericAttachments": [
                            {
                                "buttons": [
                                    {
                                        "text": "Innovation in AI Biopharma",
                                        "value": "Tell me something about talent in AI?"
                                    },
                                    {
                                        "text": "Innovation in AI Public Industries",
                                        "value": "Innovation in AI Public Industries"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
            return response
        else:
            response = {
                'sessionAttributes': session_attributes,
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "What topic would you like to choose?"
                    },
                    "intentName": "getSuggestionIntent",
                    "slots": slots,
                    "slotToElicit": "category",
                    "responseCard": {
                        "version": 1,
                        "contentType": "application/vnd.amazonaws.card.generic",
                        "genericAttachments": [
                            {
                                "buttons": [
                                    {
                                        "text": "AI Innovation",
                                        "value": "Innovation"
                                    },
                                    {
                                        "text": "AI Ethics",
                                        "value": "Ethics"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }

            return response

    elif slots["category"] == None:
        response = {
            'sessionAttributes': session_attributes,
            "dialogAction": {
                "type": "ElicitSlot",
                "message": {
                    "contentType": "PlainText",
                    "content": "What topic would you like to choose?"
                },
                "intentName": "getSuggestionIntent",
                "slots": slots,
                "slotToElicit": "category",
                "responseCard": {
                    "version": 1,
                    "contentType": "application/vnd.amazonaws.card.generic",
                    "genericAttachments": [
                        {
                            "buttons": [
                                {
                                    "text": "AI Innovation",
                                    "value": "Innovation"
                                },
                                {
                                    "text": "AI Ethics",
                                    "value": "Ethics"
                                }
                            ]
                        }
                    ]
                }
            }
        }

        return response


    else:

        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate',
                'slots': slots
            }
        }

        # return helpers.close(session_attributes,"Fulfilled",{'contentType': 'CustomPayload','content': "got it"})


def suggestion_intent_handler(intent_request, session_attributes):
    # response = search_intent_handler(intent_request, session_attributes)
    # intentName =event.get("currentIntent").get('name', None)
    # if intentName == "getSuggestionIntent":
    return {
        'sessionAttributes': session_attributes,
        "dialogAction": {
            "type": "Close",
            'fulfillmentState': 'Fulfilled',
            "message": {
                "contentType": "CustomPayload",
                #   "content": "{\"messages\":[{\"type\":\"PlainText\",\"group\":1,\"value\":\"Hi! I am your  Deloitte AI Institute  Chat Bot!\"},{\"type\":\"PlainText\",\"group\":2,\"value\":\"I can help you with different sections\"},{\"type\":\"PlainText\",\"group\":2,\"value\":\"You can choose one of the options below or write your own question\"}]}"
                "content": "Sure! Let me show you the options again which i can help you with. Click any of the options below or write your own query!. Happy Searching!"
            },
            "responseCard": {
                "version": 1,
                "contentType": "application/vnd.amazonaws.card.generic",
                "genericAttachments": [
                    {
                        'title': 'AI Innovation',
                        'subTitle': 'Innovation',
                        # 'attachmentLinkUrl': 'link_that_will_open_on_click',
                        'imageUrl': 'https://deloitte.wsj.com/cio/files/2021/02/Data-governance-IMAGE.png',
                        "buttons": [
                            {
                                "text": "Deloitte's State of AI in the Enterprise",
                                "value": "Deloitte's State of AI in the Enterprise?"
                            },
                            {
                                "text": "Humans with Machines",
                                "value": "Humans with Machines?"
                            },
                            {
                                "text": "ML Ops in Business",
                                "value": "ML Ops in Business?"
                            },
                            {
                                "text": "More Options",
                                "value": "what is AI Innovation?"
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

    # faq_message  = response.get("dialogAction").get("message").get("content")
    # print(response)
    # slots = intent_request['currentIntent']['slots']
    # source = intent_request['invocationSource']
    # # message = "hi" + "The answer i found was this -((x-amz-lex:kendra-search-response-question_answer-answer-1))"

    # if source == "DialogCodeHook":
    #     return elicit_suggestion_intent_handler(intent_request, session_attributes)

    # else:

    #     return {
    #     'sessionAttributes': session_attributes,
    #     'dialogAction': {
    #         'type': 'Close',
    #         'fulfillmentState': 'Fulfilled',
    #         # 'slots': slots,
    #         'message': {
    #             'contentType': 'PlainText',
    #             'content': "Thanks"
    #         }
    #     }
    # }


# list of intent handler functions for the dispatch proccess
HANDLERS = {
    'getWelcomeIntent': {'handler': hello_intent_handler},
    'help_desk_make_appointment': {'handler': make_appointment_intent_handler},
    'help_desk_check_appointment': {'handler': check_appointment_intent_handler},
    'help_desk_goodbye': {'handler': goodbye_intent_handler},
    'getFallBackIntenttwo': {'handler': fallback_intent_handler},
    "getFAQIntent": {'handler': search_intent_handler},
    "getSuggestionIntent": {'handler': suggestion_intent_handler}
}
