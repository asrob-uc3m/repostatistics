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
         '            <th>Username</th>\n'
         '            <th>Contribs</th>\n'
         '        </tr>\n'
         '        {top_contributors_rows}\n'
         '    </table>\n'
         '    </body>\n'
         '</html>')

    top_contributors_rows = ''
    sorted_contribs = sorted(organization['members'].items(), key=lambda x: x[1]['total_contributions'], reverse=True)
    for i, (name, data) in enumerate(sorted_contribs):
        top_contributors_rows += '<tr>\n<th>{}</th>\n<th>{}</th>\n<th>{}</th>\n</tr>\n'.format(i+1, name, data['total_contributions'])

    return webpage.format(top_contributors_rows=top_contributors_rows)


@begin.start(auto_convert=True)
def main(org, access_token = None, output_file = 'index.html'):
    organization = extract_all_data(org_name=org, access_token=access_token)

    with open(output_file, 'w') as f:
        f.write(generate_webpage(organization))

