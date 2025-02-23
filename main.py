import logging
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Union
import httpx
import os
import json
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
SONAR_TOKEN = os.getenv('SONAR_TOKEN')
SONAR_PROJECT_KEY = os.getenv('SONAR_PROJECT_KEY')
TELEX_URL = 'https://ping.telex.im/v1/webhooks/01952f15-fb05-7941-b053-82c441dac57b'
GITHUB_API_URL = 'https://api.github.com/repos/{owner}/{repo}/commits'
SONAR_API_URL = "https://sonarcloud.io/api/measures/component"

async def log_to_telex(report: dict):
    """Send report logs to Telex."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(TELEX_URL, json=report)
            response.raise_for_status()
            logger.info("Successfully logged report to Telex")
    except Exception as e:
        logger.error(f"Failed to log report to Telex: {e}")

async def fetch_github_commits(owner: str, repo: str, count: int = 5) -> Union[List[dict], dict]:
    if not GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN is not set")
        return {'error': 'GITHUB_TOKEN not set'}
    
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Fetching latest {count} commits from {owner}/{repo}")
            response = await client.get(GITHUB_API_URL.format(owner=owner, repo=repo), headers=headers)
            response.raise_for_status()
            commits = response.json()
            return [
                {
                    'sha': commit['sha'],
                    'message': commit['commit']['message'],
                    'author': commit['commit']['author']['name'],
                    'date': commit['commit']['author']['date']
                }
                for commit in commits[:count]
            ]
    except httpx.HTTPStatusError as e:
        logger.error(f"GitHub API error: {e.response.status_code} {e.response.text}")
        return {'error': f'GitHub API error: {e.response.status_code} {e.response.text}'}
    except Exception as e:
        logger.exception("Unexpected error fetching GitHub commits")
        return {'error': f'Unexpected error fetching GitHub commits: {str(e)}'}

async def fetch_sonar_analysis():
    if not SONAR_TOKEN or not SONAR_PROJECT_KEY:
        logger.error("SonarCloud credentials not set")
        return {'error': 'SonarCloud credentials not set'}
    
    params = {
        "component": SONAR_PROJECT_KEY,
        "metricKeys": "code_smells,bugs,vulnerabilities"
    }
    headers = {"Authorization": f"bearer {SONAR_TOKEN}"}
    
    try:
        async with httpx.AsyncClient() as client:
            logger.info("Fetching SonarCloud analysis")
            response = await client.get(SONAR_API_URL, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"SonarCloud API error: {e.response.status_code} {e.response.text}")
        return {'error': f'SonarCloud API error: {e.response.status_code} {e.response.text}'}
    except Exception as e:
        logger.exception("Unexpected error fetching SonarCloud analysis")
        return {'error': f'Unexpected error fetching SonarCloud analysis: {str(e)}'}
    

class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str

class MonitorPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]

@app.post('/tick', status_code=202)
def handle_tick(payload: MonitorPayload, background_tasks: BackgroundTasks):
    owner = 'codenamemomi'
    repo = 'CodeRefactorInsight_HNG12_stage3'
    
    logger.info("Received tick event, processing in background")
    background_tasks.add_task(process_task, owner, repo, payload.return_url)
    return {'status': 'accepted'}

async def process_task(owner: str, repo: str, return_url: str):
    logger.info("Starting background task for processing commits and analysis")
    commits = await fetch_github_commits(owner, repo)
    if 'error' in commits:
        logger.error("Failed to fetch commits")
        return
    
    insights = [
        f"- [{commit['sha'][:7]}] {commit['message']} by {commit['author']}"
        for commit in commits
    ]
    
    sonar_analysis = await fetch_sonar_analysis()
    sonar_insights = json.dumps(sonar_analysis, indent=2)
    
    report_data = {
        'commits': insights,
        'sonar_analysis': sonar_analysis,
        'summary': "Periodic report with key insights from GitHub and SonarCloud"
    }
    await log_to_telex(report_data)
    
    data = {
        'message': "🚀 Recent Code Changes:\n\n" + "\n".join(insights) + f"\n\n🔍 SonarCloud Analysis:\n{sonar_insights}",
        'username': 'codename Bot',
        'event_name': 'code_refactor_insight',
        'status': 'success'
    }
    
    try:
        async with httpx.AsyncClient() as client:
            logger.info("Sending analysis data to return URL")
            await client.post(return_url, json=data)
    except Exception as e:
        logger.exception("Error sending data")
        raise HTTPException(status_code=500, detail=f'Error sending data: {str(e)}')

@app.get("/integration.json")
def get_integration_json(request: Request):
    base_url  = str(request.base_url).rstrip('/')
    
    return {
        'data': {
            'date': {
                'created_at': '2025-2-22',
                'updated_at': '2025-2-22'
            },
            'descriptions':{
                'app_name': 'Code Refactor Insight',
                'app_description': 'Code Refactor Insight is a tool that helps you refactor your codebase by providing insights on how to improve your codebase.',
                'app_url': base_url,
                'app_logo': 'https://res.cloudinary.com/drujauolr/image/upload/v1740249649/942a2999-c065-47b3-adb0-3222599294eb_rsoloz.jpg',
                'background_color': '#f0f0f0'
            },
            'is_active': True,
            'integration_type': 'interval',
            'integration_category': 'Monitoring & Logging',
            'key_features': [
                'Periodic analysis of recent code commits',
                'AI-powered code review with improvement suggestions',
                'Performance optimization insights',
                'Best practices recommendations for readability and maintainability',
                'Seamless integration with Git repositories'
            ],
            'author': 'codename',
            'settings': [
                {"label": "interval", "type": "text", "required": True, "default": "* * * * *"},
                {"label": "custom_setting", "type": "text", "required": False, "default": ""}
            ],
            'target_url': '',
            'tick_url': f'{base_url}/tick',
        }
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
