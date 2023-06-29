## Chatbot AI Assistant (Context Knownledge Base) + Vector Database (Weaviate)

#### Technology: OpenAi, Weaviate
#### Method: Completions (davinci model)

#### Description:
Chatbot developed with Python and Flask that features conversation with a virtual assistant. This make use of OpenAi for completions and embeddings, it will also use Weaviate as a vector store to host data. By using Weaviate it allows to properly format data with classes and objects that are previously defined on a schema. One of the advantages of Weaviate is by having great performance for semantic search and long-term memory since it will save all queries that are ran on it.

On this demo is it used a Weaviate Cloud hosted cluster to save the data objects. To create a cluster go to: https://console.weaviate.cloud/dashboard
It requires data preparation before running the demo, to do so follow the instructions below.

### How to run (commands Windows terminal with Python 2.7):

#### Part One: Compose data
- **Create the dataset objects containing the information you wish to use and place it on folder '/schemas'**
- It must follow the example of file 'teamlyzer_companies_dataset.json'

#### Part Two: Prepare data
- **Define necessary parameters (OpenAi API key, ...) on file 'weaviate_prepare_data.py'**
- Initialize virtual environment and install dependencies, run:

	    virtualenv env
	    env\Scripts\activate
        pip install weaviate-client

- Set Weaviate Authentication login info for the Weaviate Cloud (https://console.weaviate.cloud/dashboard):

		resource_owner_config = weaviate.AuthClientPassword(
			username = "",
			password = ""
		)

- Set the URL of the Weaviate cluster created on Weaviate Cloud (https://console.weaviate.cloud/dashboard):

		client = weaviate.Client(
			url="https://test2-qlps4q84.weaviate.network"
		)

#### Part Three: Run the script
- To run the script:

	    python weaviate_prepare_data.py

- It will create the schema, import data to the cluster by batchs and cross-reference objects to assign matching IDs for object dependant objects (Example: Company X has Reviews 1 and 2, Company Y has Reviews 3 and 4, ...)

#### Part Four: Run the chat app
- **Define necessary parameters (OpenAi API key, ...) on file 'app.py'**
- Install dependencies, run:

	    pip install flask python-dotenv
        pip install openai
	    flask run

- Enter "http://localhost:5000" on browser to interact with app

#### Changelog
- v0.1
	- initial build