import begin
import operator


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

    return webpage.format(top_contributors_rows=top_contributors_rows, top_teams_rows=top_teams_rows)


@begin.start(auto_convert=True)
def main(org, access_token = None, output_file = 'index.html'):
    organization = extract_all_data(org_name=org, access_token=access_token)

    with open(output_file, 'w') as f:
        f.write(generate_webpage(organization))

