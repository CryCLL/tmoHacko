"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ Alexa enters the 
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the T Mobile Magenta Guide. " \
                    "I will now walk you through the steps to becoming a successful employee... " \
					"There are many things to learn!" \
					"For instance, you could learn about popular topics such as " \
					"Employee discounts, paid time off, vacations, and more!" \
					"What topic do you want to learn about?"
    reprompt_text = "Are you still there?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Magenta Guide. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
		
def give_information():
    card_title = "Giving Information"
    speech_output = "I see you wanted to know about employee discounts. " \
					"Well, everyone gets 200% off everything. " \
					"That is right, we give you the cost of the item to take it away. " \
					"If you would like more information, please say yes and I will email the link. " 

    should_end_session = False
    return build_response({}, build_speechlet_response(
    card_title, speech_output, None, should_end_session))
		
def email_information():
	card_title = "Email Link"
	speech_output = "I have sent a link to you about more information. " \
					"Please check your inbox in 5 seconds or more. " \
					"What else would you like to learn about?"
	reprompt_text = "Hello? Are you still there? What else would you like" \
	                "to learn about?"
	
	should_end_session = False
	return build_response({}, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))


def create_focus_object_attributes(focus_object):
    return {"favoriteColor": focus_object}

def helper():
	card_title = "Help"
	speech_output = "No help will be given. Farewell."
	
	should_end_session = True
	return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def middle_anymore_info():
	card_title = "Just Asking Anymore"
	speech_output = "Go ahead and ask about anything else you would" \
					"like to know more about!"
	
	reprompt_text = "Is anyone still there?"
	should_end_session = False
	return build_response({}, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))

def top_level_menu(intent, session):
    session_attributes = {}
    reprompt_text = None

    speech_output = "I'm not sure what you want to know. " \
                    "You can say, the topic I want to know is employee discounts."
    should_end_session = False
	
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "askingIntent":
        return top_level_menu(intent, session)
    elif intent_name == "emailInfoIntent":
        return email_information()
    elif intent_name == "middle_anymore":
        return middle_anymore_info()
    elif intent_name == "giveInformationIntent":
        return give_information()
    elif intent_name == "AMAZON.HelpIntent":
        return helper()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
