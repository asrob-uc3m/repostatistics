import begin


from advanced import extract_all_data

def generate_webpage(organization):
    webpage = ('<html>\n'
         '    <body>\n'
         '    <h1>Top Contributors</h1>\n'
         '    <table style="width:100%">\n'
         '        <tr>\n'
         '            <th>Pos</th>\n'
         '            <th></th>\n'
         '            <th>Username</th>\n'
         '            <th>Contribs</th>\n'
         '        </tr>\n'
         '        {top_contributors_rows}\n'
         '    </table>\n'
         '    <h1>Top Team Contributions</h1>\n'
         '    <table style="width:100%">\n'
         '        <tr>\n'
         '            <th>Pos</th>\n'
         '            <th>Team</th>\n'
         '            <th>Contribs</th>\n'
         '        </tr>\n'
         '        {top_teams_rows}\n'
         '    </table>\n'
         '    <h1>Top Issues</h1>\n'
         '    <table style="width:100%">\n'
         '        <tr>\n'
         '            <th>Pos</th>\n'
         '            <th></th>\n'
         '            <th>Username</th>\n'
         '            <th>Opened Issues</th>\n'
         '            <th>Currently Open</th>\n'
         '            <th>Closed Issues</th>\n'
         '            <th>Assigned and open</th>\n'
         '            <th>Assigned and closed</th>\n'
         '        </tr>\n'
         '        {top_issues_rows}\n'
         '    </table>\n'
         '    </body>\n'
         '</html>')

    # Compute Top Contributors
    top_contributors_rows = ''
    sorted_contribs = sorted(organization['members'].items(), key=lambda x: x[1]['total_contributions'], reverse=True)
    for i, (name, data) in enumerate(sorted_contribs):
        top_contributors_rows += '<tr>\n<th>{}</th>\n<th><img src="{}" width="50px"></th>\n<th>{}</th>\n<th>{}</th>\n</tr>\n'.format(i+1,
                                    data['avatar_url'], name, data['total_contributions'])

    # Compute Top Team Contributions
    top_teams_rows = ''
    teams_contribs = {}
    for team_name, team in organization['teams'].items():
        teams_contribs[team_name] = 0
        for repo in team['repos']:
            try:
                teams_contribs[team_name] += sum(organization['repos'][repo]['contributors'].values())
            except KeyError:
                pass
    sorted_team_contribs = sorted(teams_contribs.items(), key=lambda x: x[1], reverse=True)
    for i, (team, contribs) in enumerate(sorted_team_contribs):
        top_teams_rows += '<tr>\n<th>{}</th>\n<th>{}</th>\n<th>{}</th>\n</tr>\n'.format(i+1, team, contribs)

    # Compute Top Issues
    top_issues_rows = ''
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

        top_issues_rows += \
        """<tr>
           <th>{}</th>
           <th><img src="{}" width="50px"></th>
           <th>{}</th>
           <th>{}</th>
           <th>{}</th>
           <th>{}</th>
           <th>{}</th>
           <th>{}</th>
        </tr>
        """.format(i+1, member_data['avatar_url'], member, len(member_data['opened_issues']), currently_open,
                                len(member_data['closed_issues']), assigned_and_open, assigned_and_closed)

    return webpage.format(top_contributors_rows=top_contributors_rows, top_teams_rows=top_teams_rows,
                          top_issues_rows=top_issues_rows)


@begin.start(auto_convert=True)
def main(org, access_token = None, output_file = 'index.html'):
    organization = extract_all_data(org_name=org, access_token=access_token)

    with open(output_file, 'w') as f:
        f.write(generate_webpage(organization))

