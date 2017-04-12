import os

import begin
from jinja2 import Environment, FileSystemLoader, select_autoescape

from advanced import extract_all_data


def generate_webpage(organization, name, website):
    # Put the organization data in the required format

    # Compute Top Contributors
    top_contributors_rows = ''
    sorted_contribs = sorted(organization['members'].items(), key=lambda x: x[1]['total_contributions'], reverse=True)
    contribs = [{'username':name,
                 'img_url':data['avatar_url'],
                 'contribs':data['total_contributions']} for name, data in sorted_contribs]

    # Compute Top Team Contributions
    top_teams_rows = ''
    unsorted_team_contribs = {}
    for team_name, team in organization['teams'].items():
        unsorted_team_contribs[team_name] = 0
        for repo in team['repos']:
            try:
                unsorted_team_contribs[team_name] += sum(organization['repos'][repo]['contributors'].values())
            except KeyError:
                pass
    sorted_team_contribs = sorted(unsorted_team_contribs.items(), key=lambda x: x[1], reverse=True)
    team_contribs = [{'team':team, 'contribs':contribs} for team, contribs in sorted_team_contribs]


    # Compute Top Issues
    issues = []
    sorted_issues = sorted(organization['members'].items(), key=lambda x: len(x[1]['closed_issues']), reverse=True)
    for i, (member, member_data) in enumerate(sorted_issues):
        currently_open = 0
        for repo, issue in member_data['opened_issues']:
            if issue in organization['repos'][repo]['open_issues']:
                currently_open += 1

        assigned_and_open = 0
        assigned_and_closed = 0
        for repo, issue in member_data['assigned_issues']:
            if issue in organization['repos'][repo]['open_issues']:
                assigned_and_open += 1
            else:
                assigned_and_closed += 1

        issues.append({'img_url':member_data['avatar_url'],
                       'username':member,
                       'opened':len(member_data['opened_issues']),
                       'open':currently_open,
                       'closed':len(member_data['closed_issues']),
                       'assigned_open':assigned_and_open,
                       'assigned_closed':assigned_and_closed})

        # Store info in organization dict
        organization['members'][member]['open_issues'] = currently_open
        organization['members'][member]['assigned_open_issues'] = assigned_and_open
        organization['members'][member]['assigned_closed_issues'] = assigned_and_closed

    # Compute Top Team Issues
    top_team_issues_rows = ''
    unsorted_team_issues = {team: dict() for team in organization['teams']}
    for team_name, team in organization['teams'].items():
        try:
            # Create team entry
            unsorted_team_issues[team_name]['opened_issues'] = 0
            unsorted_team_issues[team_name]['closed_issues'] = 0
            unsorted_team_issues[team_name]['open_issues'] = 0
            unsorted_team_issues[team_name]['assigned_open_issues'] = 0
            unsorted_team_issues[team_name]['assigned_closed_issues'] = 0

            for repo in team['repos']:
                repo_data = organization['repos'][repo]
                unsorted_team_issues[team_name]['opened_issues'] += len(repo_data['issues'])
                unsorted_team_issues[team_name]['open_issues'] += len(repo_data['open_issues'])

            unsorted_team_issues[team_name]['closed_issues'] = unsorted_team_issues[team_name]['opened_issues'] - unsorted_team_issues[team_name]['open_issues']
        except KeyError:
            pass

    sorted_team_issues = sorted(unsorted_team_issues.items(), key=lambda x: x[1]['closed_issues'], reverse=True)
    team_issues =[{'team':team,
                   'opened':team_issues_data['opened_issues'],
                   'open':team_issues_data['open_issues'],
                   'closed':team_issues_data['closed_issues'] } for team, team_issues_data in sorted_team_issues ]

    # Generate the website using the template
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.split(__file__)[0],'templates')),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('index.html')
    html = template.render(org_name=name,
                           org_url=website,
                           contribs=contribs,
                           issues=issues,
                           team_contribs=team_contribs,
                           team_issues=team_issues)

    return html


@begin.start(auto_convert=True)
def main(org, access_token=None, output_file=os.path.join(os.path.split(__file__)[0],'website', 'index.html'),
         name='DUMMY', website='#'):
    organization = extract_all_data(org_name=org, access_token=access_token)

    with open(output_file, 'w') as f:
        f.write(generate_webpage(organization, name, website))

