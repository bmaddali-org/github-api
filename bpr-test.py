#!/usr/bin/env python
from termcolor import colored
import requests
from json2html import *
import os
import webbrowser
GITHUB_API_URL = 'https://api.github.com'
gh_org = ''
branch = 'main'
endpoint = '/orgs/'+gh_org+'/repos'
u = GITHUB_API_URL+endpoint
access_token = ''
headers = {'Accept': 'application/vnd.github.luke-cage-preview+json','Authorization': 'Token {0}'.format(access_token)}

def ghAPI( endpoint, paging=True, verbose=True ):
    #print( endpoint )
    error = 0
    page = 1
    run = True
    #headers = {'Accept': 'application/vnd.github.luke-cage-preview+json','Authorization': 'Token {0}'.format(access_token)}
    #headers = {"Authorization":"token {0}".format(access_token)}
    datas = []

    while run:
        try:
            u = GITHUB_API_URL+endpoint
            #print(u)
            if paging:
                u = u + '?page='+str(page)
            if verbose:
                print( u )
            r = requests.get( u, headers=headers )
            print(r.text)
            page = page + 1
            if len(r.text):
                if type(r.json()) is dict and 'documentation_url' not in r.json():
                    datas.append( r.json() )
                elif type(r.json()) is list and 'documentation_url' not in r.json():
                    datas = datas + r.json()
                else:
                    run = False
            else:
                run = False
            if not len(r.text) or not len(r.json()) or not paging:
                run = False
        except Exception as e:
            error = error + 1
            print( colored("[-] error occurred: %s" % e, 'red') )

        if error:
            run = False
    return datas

# r = ghAPI('/orgs/'+gh_org+'/repos')
r = ghAPI(endpoint)
print( colored('[+] %d repositories found.' % len(r), 'green') )
filename = 'test.html'
f = open(filename, 'w')
# print( colored('[+] %d repositories found.' % r, 'green') )

d = {} 
for repo in r:
    repo_name = repo.get('name')
    bpr_data = requests.get("https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection".format(owner=gh_org, repo=repo_name, branch=branch),headers = {'Accept': 'application/vnd.github.luke-cage-preview+json','Authorization': 'Token {0}'.format(access_token)})
    j_data = bpr_data.json()
    if j_data.get('message'):
        print('check')
        d[repo_name] = j_data.get('message')
        j_data.update(REPO_NAME =repo_name)
        html_data = json2html.convert(json = j_data) + '<br>'
        f.write(html_data + '\n')
print(d)
f.close()
webbrowser.open('file://' + os.path.realpath(filename))