# Code Refactor Insight

## Description
Code Refactor Insight is a tool that helps you refactor your codebase by providing insights on how to improve your codebase. It integrates with GitHub and SonarCloud to fetch recent commits and perform code analysis.

## Key Features
- Periodic analysis of recent code commits
- AI-powered code review with improvement suggestions
- Performance optimization insights
- Best practices recommendations for readability and maintainability
- Seamless integration with Git repositories

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

## Environment Variables
Make sure to set the following environment variables in your `.env` file:
- `GITHUB_TOKEN`: Your GitHub personal access token.
- `SONAR_TOKEN`: Your SonarCloud token.
- `SONAR_PROJECT_KEY`: Your SonarCloud project key.

## License
This project is licensed under the MIT License.
