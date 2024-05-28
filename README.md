# Flask App and LLM Integration

This project is a Flask application that integrates with a Language Learning Model (LLM) to process files, answer questions, and provide insights based on the content of the files.

## Features

•  [**File Processing**]: Supports processing of PDF and JSON files. Downloads and stores files locally for processing.

•  [**Question Answering**]: Utilizes LLM to answer questions based on the file content.


## Getting Started

### Prerequisites

•  Python 3.6+

•  Flask

•  Requests library

•  Libraries required for your LLM


### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/OpenRnD007/flask-llm.git
cd flask-llm
```

Install the required packages:
```bash
pip install -r requirements.txt
```

Environment Variables

Create a .env file in the root directory and add the necessary environment variables:

# Example .env content
```
OPENAI_API_KEY=sk-proj-4**
```

### Running the Application
Start the Flask server:

```bash
python app.py
```

The server will start on http://localhost:5000/.

### Usage
To use the API, send a POST request to /processllm with the required JSON payload:
```
{
"filetype": "PDF",
"filepath": "path_to_file",
"questions": ["What is the main topic of the file?"]
}
```
#### Example
```bash
curl -X POST http://localhost:5000/processllm -H "Content-Type: application/json" -d '{"filetype": "JSON", "filepath": "https://compliancereportszania.blob.core.windows.net/soc2-reports/safebase-short.json", "questions": ["Do you have formally defined criteria for notifying a client during an incident that might impact the security of their data or systems? What are your SLAs for notification?", "Which cloud providers do you rely on?"]}'


curl -X POST http://localhost:5000/processllm -H "Content-Type: application/json" -d '{"filetype": "PDF", "filepath": "https://us.aicpa.org/content/dam/aicpa/interestareas/frc/assuranceadvisoryservices/downloadabledocuments/soc2_csa_ccm_report.pdf", "questions": ["Is personal information transmitted, processed, stored, or disclosed to or retained by third parties? If yes, describe.","Please specify the primary data center location/region of the underlying cloud infrastructure used to host the service(s) as well as the backup location(s)."]}'
```

You can use above curl or any HTTP client to make the request.

API Reference
POST /processllm
Processes the file and returns answers to the questions.

### Request Body
•  filetype: The type of the file (PDF or JSON).

•  filepath: The URL path to the file.

•  questions: An array of questions to be answered.

### Response
•  200 OK: Returns a JSON object with the answers.

•  400 Bad Request: If the filetype is unsupported.

•  404 Not Found: If the file does not exist at the provided path.

•  500 Internal Server Error: If there is a connection error.

### Installation/Demo 
[llm-installation.webm](https://github.com/OpenRnD007/flask-llm/assets/107931489/ce97fe10-fc80-458a-9863-7d7dc8c9a0d0)


## License
This project is licensed under the MIT License.


## Sidenote
```
This is my first time utilizing an LLM, and it has been a positive experience. 
I'm aware that the code isn't ready for production due to certain constraints. 
However, if I were to refactor it for a production environment, 
I would adopt a more feature-centric architecture. This approach would facilitate easier testing and readability, allowing any developer to quickly adapt. 
Additionally, implementing Docker would be advantageous for scaling purposes. Thank you.
```
