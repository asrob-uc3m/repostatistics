import requests
import json
from tqdm import tqdm
import begin


class DataRetriever(object):
    def __init__(self, token=None):
        self.cache = {}
        if token:
            self.params = {'access_token': token}
        else:
            self.params = None

    def retrieve(self, url):
        if url not in self.cache:
            resp = requests.get(url=url, params=self.params)
            data = json.loads(resp.text)
            self.cache[url] = data

        return self.cache[url]

def do_stuff(*args, **kwargs):
    url_org = 'https://api.github.com/orgs/{}'
    dr = DataRetriever(kwargs['access_token'])
    asrob = {}

    # Teams
    url_teams = url_org.format(kwargs['org'])+'/teams'
    teams_data = dr.retrieve(url_teams)

    asrob['teams'] = dict()
    for team in teams_data:
        work_group = dict()
        work_group['members'] = []
        for member in tqdm(dr.retrieve(team['members_url'].replace('{/member}', ''))):
            work_group['members'].append(member['login'])
        work_group['repos'] = []
        for repo in tqdm(dr.retrieve(team['repositories_url'])):
            work_group['repos'].append(repo['name'])
        asrob['teams'][team['name']] = work_group

    # Repos
    url_repos = url_org.format(kwargs['org'])+'/repos'
    repos_data = dr.retrieve(url_repos)

    asrob['repos'] = dict()
    for repo_data in repos_data:
        repo = dict()
        repo['open_issues'] = repo_data['open_issues']
        repo['issues'] = {}
        for issue_data in tqdm(dr.retrieve(repo_data['issues_url'].replace('{/number}', ''))):
            issue = {}
            print(issue_data)
            issue['title'] = issue_data['title']
            issue['assignees'] = list(issue_data['assignees'])
            issue['labels'] = [label['name'] for label in issue_data['labels']]
            repo['issues'][issue_data['number']] = issue

        asrob['repos'][repo_data['name']] = repo


    print(asrob)


@begin.start(auto_convert=True)
def main(org, access_token = None):
    return do_stuff(org=org, access_token=access_token)
