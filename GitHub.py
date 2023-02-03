import requests
import json
import datetime

# Get some stats from a rich public repository to help with a Personal Software Process presentation

def get_most_contributed_files(username:str, token:str):
    # Get the date one year ago
    now = datetime.datetime.now()
    last_year = (now - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    print(last_year)
    # Set the authentication headers
    headers = {"Authorization": f"Token {token}"}
    # Use the GitHub API to get the user's contributions
    url = f"https://api.github.com/search/commits?q=author:{username}+committer-date:>={last_year}+repo:daos-stack/daos"
    response = requests.get(url, headers=headers)
    print(response.text)
    commits = json.loads(response.text)['items']
    # Get a list of files contributed to
    files = {}
    for commit in commits:
        for file in commit.get("files"):
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

token="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";

user_details = requests.get("https://api.github.com/user", headers={"Authorization": f"Token {token}"}).json()
print(f"You are authenticated as {user_details['login']}")

get_most_contributed_files("cotton-daddy", token)