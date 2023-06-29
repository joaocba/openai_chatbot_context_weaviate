##
# This contain all the steps to prepare data for a Weaviate Db
# Define and create a schema to receive JSON file
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



######### PREPARE DATA #########

# Method to get data from local JSON file
def get_companies_from_json(
        json_file: str,
        max_companies: int=100
    ) -> None:
    """
    Extract companies information from a local JSON file and save them as weaviate schema.
    Parameters
    ----------
    json_file : str
        Path to the JSON file containing companies information.
    """

    objects = []

    with open(json_file, 'r', encoding='utf-8') as f:
        companies_data = json.load(f)

    if max_companies > len(companies_data):
        max_companies = len(companies_data)
    pbar = tqdm(total=max_companies)
    pbar.set_description(f"{json_file}")
    for i in range(max_companies):
        company_data = companies_data[i]
        try:
            if (company_data.get('name') and \
                company_data.get('industry') and \
                company_data.get('size') and \
                company_data.get('website') and \
                company_data.get('description') and \
                company_data.get('globalScore') and \
                company_data.get('countReviews') and \
                company_data.get('recruitmentMethods') and \
                company_data.get('businessAreas') and \
                company_data.get('competition') and \
                company_data.get('url') and \
                company_data.get('opinionRateAttractiveness') and \
                company_data.get('opinionRateRecruitment') and \
                company_data.get('opinionRateSpam') and \
                company_data.get('opinionRateJobOffers') and \
                company_data.get('opinionRateTransparency') and \
                company_data.get('opinionRateWorkplace') and \
                company_data.get('reviewRateRecommendation') and \
                company_data.get('reviewAverageWorkHours') and \
                company_data.get('reviewRateInterviewFeedback') and \
                company_data.get('reviewAverageSalary') and \
                company_data.get('reviewScoreInterviewDifficulty') and \
                company_data.get('reviewAverageInterviewTime') and \
                company_data.get('faqWorkAt') and \
                company_data.get('faqSalaryAt') and \
                company_data.get('faqTimeWorkAt') and \
                company_data.get('faqInterviewFeedbackAt') and \
                company_data.get('faqInterviewAt') and \
                company_data.get('rankingGlobalScore') and \
                company_data.get('rankingBalanceWorkSocial') and \
                company_data.get('rankingReward') and \
                company_data.get('rankingSalary') and \
                company_data.get('rankingQuality') and \
                company_data.get('rankingOpportunity') and \
                company_data.get('rankingInterviewDifficultyScore') and \
                company_data.get('vacancyPolicy') and \
                company_data.get('teamDescription') and \
                company_data.get('companyJobReviews')):

                # create an UUID for the company using its name
                company_id = uuid.uuid3(uuid.NAMESPACE_DNS, company_data['name'])

                # create the object
                objects.append({
                    'id': str(company_id),
                    'name': company_data['name'],
                    "industry": company_data["industry"],
                    "size": company_data["size"],
                    "website": company_data["website"],
                    "description": company_data["description"].replace('\n', ''),
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
                    "teamDescription": company_data["teamDescription"],
                    "companyJobReviews": company_data["companyJobReviews"]
                })

                pbar.update(1)

        except:
            # something went wrong with getting the company data, ignore
            pass
    pbar.close()
    return objects


# load data from local json file, can increment each other as long the structure is as defined
data = []
data += get_companies_from_json('./schemas/teamlyzer_companies_dataset.json')

# verify if data is populated
print(json.dumps(data[0], indent=4))



######### CREATE SCHEMAS #########

# define schema
schema = {
    "classes": [
        {
            "class": "CompanyInfo",
            "description": "Details about a company, reviews from employees that worked there and opinions about interviews for that company",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {  
                "vectorizeClassName": True,
                "model": "ada",
                "modelVersion": "002",
                "type": "text"
                }, 
                "qna-openai": {
                "model": "text-davinci-003",
                "maxTokens": 150,
                "temperature": 0.0,
                "topP": 1,
                "frequencyPenalty": 0.0,
                "presencePenalty": 0.0
                }
            },
            "properties": [{
                    "name": "name",
                    "description": "The name of the company",
                    "dataType": ["text"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "industry",
                    "description": "The industry of the company",
                    "dataType": ["text"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "size",
                    "description": "The employee size of the company",
                    "dataType": ["string"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "website",
                    "description": "Website of the company",
                    "dataType": ["string"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "description",
                    "description": "The description of the company",
                    "dataType": ["text"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "globalScore",
                    "description": "The score classification of the company",
                    "dataType": ["string"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "countReviews",
                    "description": "The total count of reviews about the company",
                    "dataType": ["string"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "recruitmentMethods",
                    "description": "The score classification of the company",
                    "dataType": ["text"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "businessAreas",
                    "description": "The business areas of the company",
                    "dataType": ["text"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "competition",
                    "description": "The market competition of the company",
                    "dataType": ["text"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "url",
                    "description": "URL to the company profile at Teamlyzer",
                    "dataType": ["string"],
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The community opinion rate from 0% to 100% about company attactiveness to go for an interview",
                    "name": "opinionRateAttractiveness",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The community opinion rate from 0% to 100% about company recruitment to go for a job",
                    "name": "opinionRateRecruitment",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The community opinion rate from 0% to 100% about company doing spam",
                    "name": "opinionRateSpam",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The community opinion rate about company job offers",
                    "name": "opinionRateJobOffers",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The community opinion rate about company transparency",
                    "name": "opinionRateTransparency",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The community opinion rate about company as a workplace",
                    "name": "opinionRateWorkplace",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The recommendation rate from employees reviews from 0% to 100% about the company",
                    "name": "reviewRateRecommendation",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The average amount of works hours per day from employees reviews about the company",
                    "name": "reviewAverageWorkHours",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The candidates review rate from 0% to 100% about the company interviews",
                    "name": "reviewRateInterviewFeedback",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The average monthly salary from employees reviews about the company",
                    "name": "reviewAverageSalary",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The score classification from of the interviews from reviews of candidates for the company",
                    "name": "reviewScoreInterviewDifficulty",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The average time in hours and minutes spent by candidates in interviews for the company",
                    "name": "reviewAverageInterviewTime",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "What is it like to work at the company",
                    "name": "faqWorkAt",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "How much is the salary at the company",
                    "name": "faqSalaryAt",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "What are the working hours at the company",
                    "name": "faqTimeWorkAt",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "Does the company give feedback from job interviews",
                    "name": "faqInterviewFeedbackAt",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "How are the interviews at the company",
                    "name": "faqInterviewAt",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The global rank score of the company",
                    "name": "rankingGlobalScore",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The work/life balance score from 0 to 100 of the company",
                    "name": "rankingBalanceWorkSocial",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The recognition and reward score from 0 to 100 of the company",
                    "name": "rankingReward",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The wage score from 0 to 100 of the company",
                    "name": "rankingSalary",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The management quality score from 0 to 100 of the company",
                    "name": "rankingQuality",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The career opportunities score from 0 to 100 of the company",
                    "name": "rankingOpportunity",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The difficulty of the interviews score from 0.0 to 5.0 of the company",
                    "name": "rankingInterviewDifficultyScore",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The vacancy policy of the company",
                    "name": "vacancyPolicy",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The team description of the company",
                    "name": "teamDescription",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "hasJobReviews",
                    "dataType": ["JobReviews"],
                    "description": "Job reviews from employees about the company",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
            ],
        }, 
        {
            "class": "JobReviews",
            "description": "Job reviews from employees about the company",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                "vectorizeClassName": True,
                "model": "ada",
                "modelVersion": "002",
                "type": "text"
                }, 
                "qna-openai": {
                "model": "text-davinci-003",
                "maxTokens": 150,
                "temperature": 0.0,
                "topP": 1,
                "frequencyPenalty": 0.0,
                "presencePenalty": 0.0
                }
            },
            "properties": [{
                    "dataType": ["text"],
                    "description": "The job review title",
                    "name": "title",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The job review subtitle and post date",
                    "name": "subtitle",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The technologies or programming languages performed on the job",
                    "name": "technology",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["string"],
                    "description": "The job review score given from 0.0 to 5.0",
                    "name": "score",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The job review comment about the pros or positive aspects of working for the company",
                    "name": "commentPros",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The job review comment about the cons or negative aspects of working for the company",
                    "name": "commentCons",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The location where the job reviewer employee worked for the company",
                    "name": "location",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The last year the job reviewer employee worked for the company",
                    "name": "lastYearAt",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "dataType": ["text"],
                    "description": "The average monthly wage the job reviewer employee received working for the company",
                    "name": "salary",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                },
                {
                    "name": "forCompany",
                    "dataType": ["CompanyInfo"],
                    "description": "The company info the job review was wrote for",
                    "moduleConfig": {
                        "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": True
                        }
                    }
                }
            ]
        }
    ]
}

# save schema to file
with open('./schema.json', 'w') as outfile:
    json.dump(schema, outfile)

# remove current schema from Weaviate, removes all the data too
client.schema.delete_all()

# import schema using file path
client.schema.create('./schema.json')

# create schema from variable
#client.schema.create(schema)

# show current schema
print(json.dumps(client.schema.get(), indent=4))



######### VALIDATE OBJECTS #########

# prepare CompanyInfo object (only supporting the first object)
company_object = {
    'name': data[0]['name'],
    "industry": data[0]["industry"],
    "size": data[0]["size"],
    "website": data[0]["website"],
    "description": data[0]["description"].replace('\n', ''),
    "globalScore": data[0]["globalScore"],
    "countReviews": data[0]["countReviews"],
    "recruitmentMethods": data[0]["recruitmentMethods"],
    "businessAreas": data[0]["businessAreas"],
    "competition": data[0]["competition"],
    "url": data[0]["url"],
    "opinionRateAttractiveness": data[0]["opinionRateAttractiveness"],
    "opinionRateRecruitment": data[0]["opinionRateRecruitment"],
    "opinionRateSpam": data[0]["opinionRateSpam"],
    "opinionRateJobOffers": data[0]["opinionRateJobOffers"],
    "opinionRateTransparency": data[0]["opinionRateTransparency"],
    "opinionRateWorkplace": data[0]["opinionRateWorkplace"],
    "reviewRateRecommendation": data[0]["reviewRateRecommendation"],
    "reviewAverageWorkHours": data[0]["reviewAverageWorkHours"],
    "reviewRateInterviewFeedback": data[0]["reviewRateInterviewFeedback"],
    "reviewAverageSalary": data[0]["reviewAverageSalary"],
    "reviewScoreInterviewDifficulty": data[0]["reviewScoreInterviewDifficulty"],
    "reviewAverageInterviewTime": data[0]["reviewAverageInterviewTime"],
    "faqWorkAt": data[0]["faqWorkAt"],
    "faqSalaryAt": data[0]["faqSalaryAt"],
    "faqTimeWorkAt": data[0]["faqTimeWorkAt"],
    "faqInterviewFeedbackAt": data[0]["faqInterviewFeedbackAt"],
    "faqInterviewAt": data[0]["faqInterviewAt"],
    "rankingGlobalScore": data[0]["rankingGlobalScore"],
    "rankingBalanceWorkSocial": data[0]["rankingBalanceWorkSocial"],
    "rankingReward": data[0]["rankingReward"],
    "rankingSalary": data[0]["rankingSalary"],
    "rankingQuality": data[0]["rankingQuality"],
    "rankingOpportunity": data[0]["rankingOpportunity"],
    "rankingInterviewDifficultyScore": data[0]["rankingInterviewDifficultyScore"],
    "vacancyPolicy": data[0]["vacancyPolicy"],
    "teamDescription": data[0]["teamDescription"]
}

company_id = data[0]['id']

# validate the object
result = client.data_object.validate(
    data_object=company_object,
    class_name='CompanyInfo',
    uuid=company_id
)

# print validation result
print(json.dumps(result, indent=4))



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