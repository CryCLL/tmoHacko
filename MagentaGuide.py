"""
Tmo Hackathon: Alexa Guide for Onboarding
"""

from __future__ import print_function
import smtplib
#Name, email, id
user = ("Joseph Koblitz", "Joseph.Koblitz1@T-Mobile.com","123456")
#user = ("Leo Liu", "Leo.Liu7@T-Mobile.com","123456")
#subject,link,body
email = ["","",""]

# --------------- Email handler -----------------
def send_email(email, subject, message):
    """Sends email to employee"""
    smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpObj.ehlo()

    sent_from = "faketmobileofficialemail@gmail.com"
    to = email

    email_text = """From: {}
To: {}
Subject: {}

{}""".format(sent_from, ", ".join(to), subject, message)
    smtpObj.login('faketmobileofficialemail@gmail.com', 'tmobileis3real5me')
    smtpObj.sendmail(sent_from, to[0],email_text)
    smtpObj.quit()



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
    """ Alexa enters the guide. Prompts user if they understand
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the T Mobile Magenta Guide. " \
                    "I will now walk you through the steps to becoming a successful employee... " \
                    "First, let's get you logged into your company laptop. " \
                    "Please log in with your given NT ID and password. " \
                    "If you do not have your log in information, please contact " \
                    "your manager. Once you have finished, say get started or i'm ready "\
                    "to ask me any questions. "

    reprompt_text = "Are you still there?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getting_started():
    """
        Alexa says this when the user understands
    """

    card_title= "Getting Started"
    speech_output ="To get started, ask me questions about your first day " \
                    "for example, you can ask me about things like employee discounts or time keeping."

    reprompt_text = "Are you still there"

    should_end_session = False

    return build_response({}, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    """
        Alexa leaves you.
    """
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Magenta Guide. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def give_information_disco(session):
    """
        Alexa gives user information about discounts
    """
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
        
    card_title = "Giving Information"
    speech_output = "I see you wanted to know about employee discounts. " \
					"Well, everyone gets 200% off everything. " \
					"That is right, we give you the cost of the item to take it away. " \
					"If you would like more information, please say yes and I will email the link to you. "

    should_end_session = False

    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, None, should_end_session))


def give_information_time_keeping(session):

    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    card_title = "Time-Keeping"
    speech_output = "To log your hours, look for the Kronos desktop application. " \
                    "You can stamp your time card virtually on the right corner to log in and out. " \
                    "If you would like more information, please say yes and I will email the link to you. "

    reprompt_text = "Are you still there? "
    should_end_session = False

    session_attributes['email'] = ["Time Keeping Information","https://employeecare.t-mobile.com/hc/en-us/articles/115005758868-Kronos-Overview-Access?flash_digest=b6899f54d7ddaab4c8447bccdfa70d595bfc586e",\
                                    "\n\nHere's the information you requested: ", " If you need more help, please contact the EIT or Help Desk. "]

    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))

def email_information(session):
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output = "I have sent a link to you about more information. " \
					"Please check your inbox in a moment. " \
					"What else would you like to learn about?"
    card_title = "Email Link"
    reprompt_text = "Hello? Are you still there? What else would you like" \
	                "to learn about?"

    try:
        email=session_attributes['email']
    except:
        email= {}
    send_email([user[1]],email[0], email[3]+email[2]+email[1])

    should_end_session = False

    return build_response({}, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))

def helper():
    card_title = "Help"
    speech_output = "If you require more asisstance, please contact the EIT or Help Desk. Farewell. "

    should_end_session = True
    return build_response({}, build_speechlet_response(
    card_title, speech_output, None, should_end_session))

def thatIsAll():
    card_title = "Farewell"
    speech_output = "Have a great time at T Mobile!"

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
    """
        Alexa says this if she doesn't understand you
    """
    session_attributes = {}
    reprompt_text = None

    speech_output = "I'm not sure what you want to know. " \
                    "You can say, the topic I want to know is employee discounts or time keeping."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def employee_benefits(session):
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
        
    card_title = "Employee Benefits"
    speech_output = "T Mobile's benefits are going to rock your world. " \
                    " Benefits include medical and prescription benefits. " \
                    " dental and vision plans, life insurance, flexible spending. " \
                    "and much much more. " \
                    "If you would like more information, please say yes and I will email the link to you. "
                    
    reprompt_text = "Hello? Is there anyone there? Would you like an email sent to you? "
    should_end_session = False
	
    session_attributes['email'] = ["Employee Benefits","https://employeecare.t-mobile.com/hc/en-us/articles/115005758868-Kronos-Overview-Access?flash_digest=b6899f54d7ddaab4c8447bccdfa70d595bfc586e",\
                                    "\n\nHere's the information you requested: ", " If you need more help, please contact the EIT or Help Desk. "]

    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
        
def retirement(session):
    card_title="401k"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
        
    speech_output = "As one of the top companies to work for, " \
                    "we will contribute to your four oh one k, " \
                    "however, it is only 5% of your earnings because " \
                    "to be frank, we don't want you to retire too early. " \
                    "Would you like an email to be sent to you about this? "
                    
    reprompt_text = "Hello? It has been a few seconds since I last heard your voice. "\
                    "What else would you like to know about? "
                    
    session_attributes['email'] = ["401k Info","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]


    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))               
    
        
def code_of_conduct(session):
   card_title= "Code of Business Conduct"
   try:
        session_attributes = session['attributes']
   except:
        session_attributes = {}
   speech_output= "Some principles of our code of conduct include" \
                   "non-discrimination policies and privacy laws. " \
                   "Also, please refrain from chest bumping of any sort " \
                   "as that can be deemed inappropriate depending on the employee. " \
                   "Would you like an email about more information? "           
    
   reprompt_text = "Hello? Are you still there? What else would you like " \
        "to learn about? "

   session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]
               

   should_end_session = False
   return build_response(session_attributes, build_speechlet_response(
   card_title, speech_output, reprompt_text, should_end_session))  
   
def employee_handbook(session):
    card_title= "Employee Handbook"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "T-Mobile's employee's handbook can be found on twitter. " \
                   "It is a short read with a brief 140 characters. " \
                   "Would you like an email with more information? "
    reprompt_text = "Hello? Are you still there? What else would you like" \
                   "to learn about?"
                   
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def company_culture(session):
    card_title= "Our Culture"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output = "T Mobile's company culture is best exemplified by our CEO, John Legere. " \
                    "He swears a lot and wears magenta converse" \
                    "In other words, we're a lot cooler than Verizon. " \
                    "Would you like more information sent to your email? "
    
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
                    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def diversity_inclusion(session):
    card_title= "Diversity and Inclusion"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "If you turn everyone Magenta, you don't need to worry about diversity. Exclamation mark. Because I can't sound enthusiastic. Would you like an email with more information sent to you?"

    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def talent_referral(session):
    card_title= "Talent Referral"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output = "To clone and refer yourself, thereby doubling your paycheck, please discuss your options with John Legere's ego on the 50th floor of Newport Five. Would you like an email with new info? "
    
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))   
    
def wireless_network(session):
    card_title = "Wireless network"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output = "All that you need to know is that our network is the best network. Not Verizon's. Ours."

    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def employee_recognition(session):
    card_title = "Employee Recognition"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output = "Wow, the team that made this product is so cool! Would you like more information about how to be recognized to be sent to you through email? "
    
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def development_resources(session):
    card_title = "Develop Resources"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output = "Our resources don't need development. I'm a strong independent AI, leave me alone. I will give you the option of recieving an email with more information though. Would you like an email with more information sent to your inbox? "

    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]


    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))

def Professional_Standards_Training(session):
    card_title= "Pro_Standards_Training"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "I see you are wanting to know more about our " \
                    "fantastic Professional Standards Training Program. Would you like an email sent to you about that? "
    
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def Learning_Resources(session):
    card_title= "eses"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "I see you want to learn more about Learn Resources. " \
                    "Am I not enough? That's okay, I'll send you an email with more resources if you want. Do you want it? "
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def Accelerate_My_Performance(session):
    card_title= "AccelTime"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "I see you are interested in accelerating your own performance. " \
                    "The first step would be to switch from Verizon to T Mobile... There is no step 2. Would you like an email with the steps? "
       
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "    
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def Employee_Expectations(session):
    card_title= "employ_expect"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "I see you are wanting to know more about " \
                    "Employee Expectations. You are expected to make us money and not get in trouble. Would you like an email with more information? "
    
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "    
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def TMUS_Policies(session):
    card_title= "TMUS Policy"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "I see you are wanting to know more about our legal policies. Be a good person and do the right thing. That's pretty much it. Would you like an email with more information on how to be a good person? "
    
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
    
def Complaints_and_Incidents(session):
    card_title= "Pro_Standards_Training"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "I see you are interested in complaining about something. " \
                    "There will be no complaining. Would you like an email sent to you with the same amount of information? "
                    
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def socialMedia(session):
    card_title = "Social Media"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "I see you are interested in learning more about social Media. Well, just follow John Legere on Twitter. " \
                    "Would you like me to email you his Twitter handle? "
    
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "
    
    
    session_attributes['email'] = ["Employee Discount Information","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
    
def employeeMobileDiscount(session):
    card_title= "employeemobilediscount"
    try:
        session_attributes = session['attributes']
    except:
        session_attributes = {}
    speech_output= "I see you are interested in the mobile discount we offer to employees. " \
                    "Fantastic! It is a long and complicated process. Would you like an email with more information? "
       
    reprompt_text = "Hello? Anyone still there? Would you like an email to be sent? "    
    
    session_attributes['email'] = ["Employee Mobile Discount","https://tmobileusa.sharepoint.com/sites/humanresources/Pages/EmployeeDiscounts.aspx#topic_1", \
                                    "\n\nHere's the information you requested: ", "If you require more asisstance, please contact the EIT or Help Desk. "]

    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
    
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
    elif intent_name == "employeeMobileDiscountIntent":
        return employeeMobileDiscount(session)
    elif intent_name == "TimeKeepingIntent":
        return give_information_time_keeping(session)
    elif intent_name == "tmusIntent":
        return TMUS_Policies(session)
    elif intent_name == "LearningResourcesIntent":
        return Learning_Resources(session)
    elif intent_name == "professionalTrainingIntent":
        return Professional_Standards_Training(session)
    elif intent_name == "ComplaintIntent":
        return Complaints_and_Incidents(session)
    elif intent_name  == "accelerateMyPerformanceIntent":
        return Accelerate_My_Performance(session)
    elif intent_name == "codeOfconductIntent":
        return code_of_conduct(session)
    elif intent_name == "employeeExpectationsIntent":
        return Employee_Expectations(session)
    elif intent_name == "diversityInclusionIntent":
        return diversity_inclusion(session)
    elif intent_name == "retirementIntent":
        return retirement(session)
    elif intent_name == "wirelessIntent":
        return wireless_network(session)
    elif intent_name == "employeeRecognitionIntent":
        return employee_recognition(session)
    elif intent_name == "CodeOfConductIntent":
        return code_of_conduct(session)
    elif intent_name == "EmpHandbookIntent":
        return employee_handbook(session)
    elif intent_name == "CompanyCultureIntent":
        return company_culture(session)
    elif intent_name == "diversityIntent":
        return diversity_inclusion(session)
    elif intent_name == "talentIntent":
        return talent_referral(session)
    elif intent_name == "employeeBenefitsIntent":
        return employee_benefits(session)
    elif intent_name == "emailInfoIntent":
        return email_information(session)
    elif intent_name == "GettingStartedIntent":
        return getting_started()
    elif intent_name == "thatIsAllIntent":
        return thatIsAll()
    elif intent_name == "middle_anymore":
        return middle_anymore_info()
    elif intent_name == "giveInformationIntentDisco":
        return give_information_disco(session)
    elif intent_name == "socialMediaIntent":
        return socialMedia(session)
    elif intent_name == "continueIntent":
        return middle_anymore_info()
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
