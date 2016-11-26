import requests, json
import operator
from tqdm import tqdm

def main():
    org = 'asrob-uc3m'
    url_repos = 'https://api.github.com/orgs/{}/repos'
    url_repo_contributors = 'https://api.github.com/repos/{}/{}/contributors'
    contributors = {}

    resp = requests.get(url=url_repos.format(org))
    data = json.loads(resp.text)

    for repo in tqdm(data):
        #print(repo)
        resp = requests.get(url_repo_contributors.format(org, repo['name']))
        contrib_data = json.loads(resp.text)

        for contributor in contrib_data:
            total_contribs = contributors.get(contributor['login'], 0)
            total_contribs += int(contributor['contributions'])
            contributors[contributor['login']] = total_contribs

    print("<html><body>")
    for i, contributor in enumerate(reversed(sorted(contributors.items(), key=operator.itemgetter(1)))):
        print("{:2.0f}. {} -> {}<br>".format(i+1, contributor[0], contributor[1]))
    print("</body></html>")

if __name__ == '__main__':
    main()
