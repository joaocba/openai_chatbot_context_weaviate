##
# Flask app that query a Weaviate DB and return a response with OpenAi completions
# Requires data to be prepared previously, use weaviate_prepare_data.py*
# *data preparation can be done separately, check the prep_data folder
# The used Weaviate instance on this demo is hosted on WCS Cloud

## Dependecies:
# pip install flask
# pip install weaviate-client


from flask import Flask, request, render_template
import weaviate
import json
import os
import logging
import datetime



## LOGGER ##
# create logs folder if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# get current date and time for log filename
log_filename = f"logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# configure logger
logging.basicConfig(filename=log_filename, level=logging.INFO)


## OPENAI SETTINGS ##
# set OpenAI API
# os.environ["OPENAI_API_KEY"] = ''
# in case it is already defined on windows path variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")


## WEAVIATE CONNECT ##
# Weaviate Auth Config
resource_owner_config = weaviate.AuthClientPassword(
  username = "",
  password = "",
  scope = "offline_access" # optional, depends on the configuration of your identity provider (not required with WCS)
  )


# Connect to Weaviate instance
client = weaviate.Client(
    url="https://test2-qlps4q84.weaviate.network",
    auth_client_secret=resource_owner_config,
#   url="http://localhost:8080/",
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    }
)

# Check if instance is live and ready
#print(client.is_ready())


## WEAVIATE METHODS ##
# Method for questioning
def qna(query, collection_name):
    # the properties to be queried from schema
    properties = [
        "name", "industry", "size", "website", "description", "globalScore", "countReviews", "recruitmentMethods", "businessAreas", "competition", "url", "opinionRateAttractiveness", "opinionRateRecruitment", "opinionRateSpam", "opinionRateJobOffers", "opinionRateTransparency", "opinionRateWorkplace", "reviewRateRecommendation", "reviewAverageWorkHours", "reviewRateInterviewFeedback", "reviewAverageSalary", "reviewScoreInterviewDifficulty", "reviewAverageInterviewTime", "faqWorkAt", "faqSalaryAt", "faqTimeWorkAt", "faqInterviewFeedbackAt", "faqInterviewAt", "rankingGlobalScore", "rankingBalanceWorkSocial", "rankingReward", "rankingSalary", "rankingQuality", "rankingOpportunity", "rankingInterviewDifficultyScore", "vacancyPolicy", "teamDescription", 
        "hasJobReviews { ... on JobReviews { title subtitle technology score commentPros commentCons location lastYearAt salary } }",
        "_additional { answer { hasAnswer property result startPosition endPosition } distance }"
    ]

    ask = {
        "question": query,
        "properties": properties
    }

    result = (
        client.query
        .get(collection_name, properties)
        #.get(collection_name, ["name", "hasJobReviews { ... on JobReviews { title subtitle technology score commentPros commentCons location lastYearAt salary } }", "_additional {answer {hasAnswer property result startPosition endPosition} }"])
        .with_ask(ask)
        .with_limit(1)
        .with_additional(['certainty'])
        .do()
    )

    # Check for errors
    if ("errors" in result):
        print ("\033[91mYou probably have run out of OpenAI API calls for the current minute – the limit is set at 60 per minute.")
        raise Exception(result["errors"][0]['message'])

    return result["data"]["Get"][collection_name]


## APP ##
# array to store conversations
conversation = ["You are a virtual assistant and you speak portuguese."]    # define initial role

app = Flask(__name__)

# define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    # get user input
    user_input = request.args.get("msg") + '\n'
    response = ''
    if user_input:
        conversation.append(f"{user_input}")

        # get conversation history
        prompt = "\n".join(conversation[-3:])

        # generate AI response based on indexed data for class
        query_result = qna(prompt, "CompanyInfo")

        # check if answer was found
        for i, company in enumerate(query_result):
            if company['_additional']['answer']['hasAnswer'] == False:
                response = 'No answer found'
            else:
                #response = f"{i+1}. { company['_additional']['answer']['result']} (Distance: {round(company['_additional']['distance'],3) })"
                #response = f"{ company['_additional']['answer']['result']} (Distance: {round(company['_additional']['distance'],3) }) (Certainty: {round(company['_additional']['certainty'],3) })\n"
                #response = f"{ company['_additional']['answer']['result']} (Distance: {round(company['_additional']['distance'],3)})" + (f" (Certainty: {round(company['_additional']['certainty'],3)})" if company['_additional']['certainty'] else "") + "\n"
                response = f"{ company['_additional']['answer']['result']}" + "\n"


        # add AI response to conversation
        conversation.append(f"{response}")

        # log conversation
        with open(log_filename, "a") as f:
            f.write(f"User: {user_input}\n")
            f.write(f"AI: {response}\n\n")

        # log conversation using logger
        logging.info(f"User: {user_input}")
        logging.info(f"AI: {response}")

    return response if response else "Sorry, I didn't understand that."


if __name__ == "__main__":
    app.run()