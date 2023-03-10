import requests
import json
import datetime
import re

# Get some stats from a rich public repository to help with a Personal Software Process presentation

# GitHub authentication token
token=input('Enter your GitHub token:')

def get_most_contributed_files(username:str, token:str):
    # Get the date one year ago
    now = datetime.datetime.now()
    last_year = (now - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    # Set the authentication headers
    headers = {"Authorization": f"Token {token}"}
    # Use the GitHub API to get the user's contributions
    url = f"https://api.github.com/search/commits?q=author:{username}+committer-date:>={last_year}+repo:daos-stack/daos"
    try:
        response = requests.get(url, headers=headers)
        commits = json.loads(response.text)['items']
        # Get a list of files contributed to
        files = {}
        for commit in commits:
            response = requests.get(f"https://api.github.com/repos/{commit.get('repository').get('full_name')}/commits/{commit.get('sha')}", headers=headers)
            for file in json.loads(response.text)['files']:
                file_name = file['filename']
                if file_name not in files:
                    files[file_name] = 1
                else:
                    files[file_name] += 1
        # Sort the files by number of contributions
        sorted_files = sorted(files.items(), key=lambda x: x[1], reverse=True)
        # Print the result
        print(f"The user {username} has contributed to the following files in the last year:")
        for i, file in enumerate(sorted_files[:10]):
            print(f"{i+1}. {file[0]} ({file[1]} contributions)")
    except Exception:
        print(response.text)


def get_most_worked_on_JIRAs(username:str, token:str, jira_project:str):
    # Get the date one year ago
    now = datetime.datetime.now()
    last_year = (now - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    # Set the authentication headers
    headers = {"Authorization": f"Token {token}"}
    # Use the GitHub API to get the user's contributions
    url = f"https://api.github.com/search/commits?q=author:{username}+committer-date:>={last_year}+repo:daos-stack/daos"
    try:
        response = requests.get(url, headers=headers)
        commits = json.loads(response.text)['items']
        # Get a list of JIRAs contributed to
        JIRAs = {}
        for commit in commits:
            try:
                message = commit.get('commit').get('message')
                JIRA_ID = re.search(f"{jira_project}\-\d+", message).group()
            except Exception as e:
                print(str(e))
                print(f"{message}\n\n")
                continue
            if JIRA_ID not in JIRAs:
                JIRAs[JIRA_ID] = 1
            else:
                JIRAs[JIRA_ID] += 1
        # Sort the JIRAs by number of contributions
        sorted_JIRAs = sorted(JIRAs.items(), key=lambda x: x[1], reverse=True)
        # Print the result
        print(f"The user {username} has contributed to the following JIRAs in the last year:")
        for i, JIRA in enumerate(sorted_JIRAs[:10]):
            print(f"{i+1}. {JIRA[0]} ({JIRA[1]} contributions)")
    except Exception as e:
        print(str(e))
        print(response.text)
        pass

# get_most_contributed_files("brianjmurrell", token)
get_most_worked_on_JIRAs("brianjmurrell", token, "DAOS")
