##
# Import data objects to a Weaviate database
# Validate imported objects
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



######### IMPORT OBJECTS TO WEAVIATE DB #########

## Load objects by batch

# New Batch method (Only in weaviate-client version >=3.0.0.)
from weaviate.batch import Batch # for the typing purposes
from weaviate.util import generate_uuid5 # old way was from weaviate.tools import generate_uuid


# function to add company object
def add_company(batch: Batch, company_data: dict) -> str:

    company_object = {
        'name': company_data['name'],
        "industry": company_data["industry"],
        "size": company_data["size"],
        "website": company_data["website"],
        "description": company_data["description"],
        "globalScore": company_data["globalScore"],
        "countReviews": company_data["countReviews"],
        "recruitmentMethods": company_data["recruitmentMethods"],
        "businessAreas": company_data["businessAreas"],
        "competition": company_data["competition"],
        "url": company_data["url"],
        "opinionRateAttractiveness": company_data["opinionRateAttractiveness"],
        "opinionRateRecruitment": company_data["opinionRateRecruitment"],
        "opinionRateSpam": company_data["opinionRateSpam"],
        "opinionRateJobOffers": company_data["opinionRateJobOffers"],
        "opinionRateTransparency": company_data["opinionRateTransparency"],
        "opinionRateWorkplace": company_data["opinionRateWorkplace"],
        "reviewRateRecommendation": company_data["reviewRateRecommendation"],
        "reviewAverageWorkHours": company_data["reviewAverageWorkHours"],
        "reviewRateInterviewFeedback": company_data["reviewRateInterviewFeedback"],
        "reviewAverageSalary": company_data["reviewAverageSalary"],
        "reviewScoreInterviewDifficulty": company_data["reviewScoreInterviewDifficulty"],
        "reviewAverageInterviewTime": company_data["reviewAverageInterviewTime"],
        "faqWorkAt": company_data["faqWorkAt"],
        "faqSalaryAt": company_data["faqSalaryAt"],
        "faqTimeWorkAt": company_data["faqTimeWorkAt"],
        "faqInterviewFeedbackAt": company_data["faqInterviewFeedbackAt"],
        "faqInterviewAt": company_data["faqInterviewAt"],
        "rankingGlobalScore": company_data["rankingGlobalScore"],
        "rankingBalanceWorkSocial": company_data["rankingBalanceWorkSocial"],
        "rankingReward": company_data["rankingReward"],
        "rankingSalary": company_data["rankingSalary"],
        "rankingQuality": company_data["rankingQuality"],
        "rankingOpportunity": company_data["rankingOpportunity"],
        "rankingInterviewDifficultyScore": company_data["rankingInterviewDifficultyScore"],
        "vacancyPolicy": company_data["vacancyPolicy"],
        "teamDescription": company_data["teamDescription"]
    }
    company_id = company_data['id']

    # add company to the batch
    batch.add_data_object(  # old way was batch.add(...)
        data_object=company_object,
        class_name='CompanyInfo',
        uuid=company_id
    )

    return company_id


# function to add job review object
def add_jobreview(batch: Batch, jobreview: dict) -> str:

    jobreview_object = {
        'title': jobreview['title'],
        'subtitle': jobreview['subtitle'],
        'technology': jobreview['technology'],
        'score': jobreview['score'],
        'commentPros': jobreview['commentPros'],
        'commentCons': jobreview['commentCons'],
        'location': jobreview['location'],
        'lastYearAt': jobreview['lastYearAt'],
        'salary': jobreview['salary']
        # add any additional key-value pairs you want to include here
    }

    #if jobreview in created_job_reviews:
        #return created_job_reviews[jobreview]

    # generate an UUID for the Job Review
    jobreview_id = generate_uuid5(jobreview)

    # add job review to the batch
    batch.add_data_object(  # old way was batch.add(...)
        data_object=jobreview_object,
        class_name='JobReviews',
        uuid=jobreview_id
    )

    #created_job_reviews[jobreview] = jobreview_id
    return jobreview_id


# function to add cross references between CompanyInfo and JobReviews
def add_references(batch: Batch, company_id: str, jobreview_id: str)-> None:
    # add references to the batch
    ## JobReviews -> CompanyInfo
    batch.add_reference(  # old way was batch.add(...)
        from_object_uuid=jobreview_id,
        from_object_class_name='JobReviews',
        from_property_name='forCompany',
        to_object_uuid=company_id
    )

    ## CompanyInfo -> JobReviews
    batch.add_reference(  # old way was batch.add(...)
        from_object_uuid=company_id,
        from_object_class_name='CompanyInfo',
        from_property_name='hasJobReviews',
        to_object_uuid=jobreview_id
    )


from tqdm import trange

# configure the batch params
client.batch.configure(
    batch_size=30,
    #dynamic=True, # use this to auto-size the batch
    callback=None, # use this argument to set a callback function on the batch creation results
)
with client.batch(batch_size=30) as batch: # the client.batch(batch_size=30) is the same as client.batch.configure(batch_size=30)
    for i in trange(len(data)): # this verify the lenght of data objects

        # add company to the batch
        company_id = add_company(batch, data[i])

        for jobreview in data[i]['companyJobReviews']:

            # add job review to the batch
            jobreview_id = add_jobreview(batch, jobreview)

            # add cross references to the batch
            add_references(batch, company_id=company_id, jobreview_id=jobreview_id)



######### VERIFY/PRINT IMPORTED OBJECTS #########

## Verify if a object was imported correctly
# print company objects
print(json.dumps(client.data_object.get(company_id, with_vector=False), indent=4))

## print references for JobReview object
from weaviate.util import get_valid_uuid # extract UUID from URL (beacon or href)

# extract jobreview references, take only the first one as an example (the company may have only one)
jobreview = client.data_object.get(company_id, with_vector=False)['properties']['hasJobReviews'][0]

# get and print data object by providing the 'beacon'
jobreview_uuid = get_valid_uuid(jobreview['beacon']) # can be 'href' too
print(json.dumps(client.data_object.get(jobreview_uuid, with_vector=False), indent=4))