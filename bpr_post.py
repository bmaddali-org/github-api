import requests 
import configparser

config = configparser.ConfigParser()
config.read('init.properties')

repo = config.get("PropSection", "org_name") + '/macsetup'
branch = 'main' #config.get("PropSection", "bpr_branch_name")
access_token = config.get("PropSection", "pat_token")


r = requests.put(
    'https://api.github.com/repos/{0}/branches/{1}/protection'.format(repo, branch),
    headers = {
        'Accept': 'application/vnd.github.luke-cage-preview+json',
        'Authorization': 'Token {0}'.format(access_token)
    },
    json = {
        "required_pull_request_reviews": {
        "dismissal_restrictions": {
          "users": [
            "bmaddali"
          ]
        },
        "dismiss_stale_reviews": True,
        "require_code_owner_reviews": False,
        "required_approving_review_count": 2
      },
        "restrictions": None,
        "required_status_checks": None,
        "enforce_admins": None
    }
)
print(r.status_code)
print(r.json())
