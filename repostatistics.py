import requests, json
import operator
from tqdm import tqdm
import begin

@begin.start(auto_convert=True)
def main(org: 'Github organization name' = 'asrob-uc3m', access_token: 'Access token' = '',
         generate_html: 'Generate html page with ranking' = False):
    """
    This is the program description
    """
    url_repos = 'https://api.github.com/orgs/{}/repos'
    url_repo_contributors = 'https://api.github.com/repos/{}/{}/contributors'
    contributors = {}

    if access_token:
        params = {'access_token':access_token}
    else:
        params = None

    resp = requests.get(url=url_repos.format(org), params=params)
    data = json.loads(resp.text)

    for repo in tqdm(data):
        #print(repo)
        resp = requests.get(url_repo_contributors.format(org, repo['name']), params=params)
        contrib_data = json.loads(resp.text)

        for contributor in contrib_data:
            total_contribs = contributors.get(contributor['login'], 0)
            total_contribs += int(contributor['contributions'])
            contributors[contributor['login']] = total_contribs

    print("<html><body>")
    for i, contributor in enumerate(reversed(sorted(contributors.items(), key=operator.itemgetter(1)))):
        print("{:2.0f}. {} -> {}<br>".format(i+1, contributor[0], contributor[1]))
    print("</body></html>")
