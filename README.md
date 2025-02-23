# Code Refactor Insight

## Description
Code Refactor Insight is a tool that helps you refactor your codebase by providing insights on how to improve your codebase. It integrates with GitHub and SonarCloud to fetch recent commits and perform code analysis, allowing developers to maintain high-quality code.

## Key Features
- Periodic analysis of recent code commits
- AI-powered code review with improvement suggestions
- Performance optimization insights
- Best practices recommendations for readability and maintainability
- Seamless integration with Git repositories
- Error handling for API requests with informative logging

## Installation
1. Clone the repository:
   ```bash
   git clone <https://github.com/codenamemomi/CodeRefactorInsight_HNG12_stage3.git>
   cd <CodeRefactorInsight_HNG12_stage3>
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the application, use the following command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
You can then access the API at `http://localhost:8000`.

### API Endpoints
- **POST /tick**: Accepts a payload to process GitHub commits and SonarCloud analysis.
- **GET /integration.json**: Returns integration details for the app.

## Environment Variables
Make sure to set the following environment variables in your `.env` file:
- `GITHUB_TOKEN`: Your GitHub personal access token.

## How the App Works
The Code Refactor Insight app is built using FastAPI and integrates with GitHub and SonarCloud to provide developers with insights into their codebase. Here's a detailed explanation of how the app operates:

0. **QUICK TEST**:
   curl -X POST https://coderefactorinsight-s3.onrender.com/tick \
     -H "Content-Type: application/json" \
     -d '{
           "channel_id": "developers-productivity",
           "return_url": "https://ping.telex.im/v1/webhooks/0195334e-4ed7-7b87-8312-507db7eba65c",
           "settings": [
             {"label": "interval", "type": "text", "required": true, "default": "* * * * *"}
           ]
         }'





1. **Application Setup**: 
   - The app is initialized using FastAPI, which allows for the creation of RESTful APIs. It loads environment variables from a `.env` file, which contain sensitive information like API tokens.

2. **Endpoints**:
   - The app exposes two main endpoints:
     - **POST /tick**: This endpoint is designed to handle incoming requests that trigger the analysis process. When a request is received, it processes the payload in the background.
     - **GET /integration.json**: This endpoint provides integration details about the app, including metadata such as the app name, description, and key features.

3. **Processing Requests**:
   - When a request is made to the `/tick` endpoint, the app extracts the necessary information from the payload, including the GitHub repository owner and name. It then initiates a background task to fetch the latest commits and perform a SonarCloud analysis.

4. **Fetching Data**:
   - The app uses the GitHub API to retrieve the latest commits from the specified repository. It requires a GitHub personal access token for authentication.
   - Simultaneously, it fetches code quality metrics from SonarCloud using the SonarCloud API, which also requires authentication via a token.

5. **Logging and Error Handling**:
   - Throughout the process, the app logs important events and errors using Python's logging module. This helps in monitoring the application's performance and troubleshooting issues.

6. **Sending Reports**:
   - After gathering the data, the app compiles a report that includes insights from both GitHub and SonarCloud. This report is then sent to a specified return URL, allowing users to receive updates on their code quality and recent changes.

7. **Integration**:
   - The app is designed to be integrated into existing workflows, providing developers with timely insights that can help improve code quality and maintainability.

This detailed explanation should help users understand the inner workings of the Code Refactor Insight app and how to effectively utilize its features.

## License
This project is licensed under the MIT License.
