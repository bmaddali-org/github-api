import requests
access_token = "cd454597797cacb58f8a4f94e5c835e0e5d17825"
owner = "bmaddali"
repo = 'hashicat-aws'
branch = 'master'
r = requests.get("https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection".format(owner=owner, repo=repo, branch=branch),headers = {'Accept': 'application/vnd.github.luke-cage-preview+json','Authorization': 'Token {0}'.format(access_token)})
print(r.json())
