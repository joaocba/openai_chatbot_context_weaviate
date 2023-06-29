##
# Query objects on Weaviate Database
# The used Weaviate instance on this demo is hosted on WCS Cloud

## Dependecies:
# pip install weaviate-client



######### CONFIG #########

import weaviate
import json
import os
import uuid
from tqdm import tqdm


# OpenAi API
# os.environ["OPENAI_API_KEY"] = ''
# in case it is already defined on windows path variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

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



######### QUERYING #########

# Method for questioning
def qna(query, collection_name):
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
        .with_ask(ask)
        .with_limit(1)
        .do()
    )

    # Check for errors
    if ("errors" in result):
        print ("\033[91mYou probably have run out of OpenAI API calls for the current minute – the limit is set at 60 per minute.")
        raise Exception(result["errors"][0]['message'])

    return result["data"]["Get"][collection_name]


# Query to run
query_result = qna("Qual é a taxa de opinião sobre a transparencia da Mindera", "CompanyInfo")

for i, company in enumerate(query_result):
    if company['_additional']['answer']['hasAnswer'] == False:
      print('No answer found')
    else:
      print(f"{i+1}. { company['_additional']['answer']['result']} (Distance: {round(company['_additional']['distance'],3) })")