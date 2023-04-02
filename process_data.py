import os
import json
import pandas as pd
import re

def build_people_registry(tournament: str):
    people = dict()
    cwd = os.getcwd()
    os.chdir(tournament)

    os.remove('people.json')

    json_files = list(filter(lambda x: x.endswith(".json"), os.listdir()))

    for file in json_files:
        print(f"Reading file {file}")
        with open(file) as f:
            data = json.loads(f.read())
        registry = data['info']['registry']['people']
        people.update(registry)
    
    print(len(people))

    content = json.dumps(people, indent=2)
    with open("people.json", 'w') as f:
        f.write(content)

    os.chdir(cwd)

def build_all_data(files_path: str, n: int):
    ball_by_ball_data = pd.DataFrame()
    matches_data = pd.DataFrame()

    all_seasons = dict()
    data_files = [x for x in os.listdir(files_path) if re.match('\d+.json', x) is not None]
    data_files = sorted(data_files, key = lambda x: int(x.split('.')[0]))
    if n is not None and n > -1:
        data_files = data_files[:n]
    total_files = len(data_files)
    for file_no, file in enumerate(data_files):
        if (file_no + 1) % 50 == 0:
            print(f"Read file: {file_no + 1} out of {total_files} files...")
        with open(os.path.join(files_path, file)) as f:
            content = f.read()
            json_data = json.loads(content)
            season = json_data['info']['dates'][0].split('-')[0]
            counter = all_seasons.get(season, 1)
            if season not in all_seasons:
                all_seasons[season] = 1
            all_seasons[season] += 1
            match_data = build_match_data(json_data, counter)
            ball_by_ball = build_match_data_ball_by_ball(json_data, counter)

        ball_by_ball_data = pd.concat([ball_by_ball_data, ball_by_ball], ignore_index=True)
        matches_data = pd.concat([matches_data, match_data], ignore_index=True)
    
    ball_by_ball_data = ball_by_ball_data.sort_values(by = ['season', 'match_no', 'innings', 'over', 'delivery'])
    ball_by_ball_data.to_csv('ball_by_ball.csv', index=False)

    matches_data = matches_data.sort_values(by = ['season', 'match_no'])
    matches_data.to_csv('matches.csv', index=False)

def build_match_data(json_data: dict, counter: int) -> pd.DataFrame:
    season = json_data['info']['dates'][0].split('-')[0]
    match_data = {
                'season': season, 
                'match_no': counter, 
                'date': json_data['info']['dates'][0], 
                'team1': json_data['info']['teams'][0], 
                'team2': json_data['info']['teams'][1],
                'toss_winner': json_data['info']['toss']['winner'], 
                'toss_decision': json_data['info']['toss']['decision'],
                'venue': json_data['info']['venue'],
                'result': True, 
                'super_over': False,
                'winner': '',

    }
    
    if 'winner' in json_data['info']['outcome']:
        match_data['winner'] = json_data['info']['outcome']['winner']
        match_data['result_type'] = 'win'
        match_data['result_value'] = json_data['info']['outcome']['by']
    elif 'result' in json_data['info']['outcome']:
        match_data['result_type'] = json_data['info']['outcome']['result']
        match_data['result_value'] = None
        if json_data['info']['outcome']['result'] == 'tie':
            match_data['winner'] = json_data['info']['outcome']['eliminator']
            match_data['super_over'] = True
        elif json_data['info']['outcome']['result'] == 'no result':
            match_data['result'] = False
    
    match_data['match_referee'] = json_data['info']['officials']['match_referees'][0]
    match_data['umpire1'] = json_data['info']['officials']['umpires'][0]
    match_data['umpire2'] = json_data['info']['officials']['umpires'][1]

    match_data['tv_umpire'] = json_data['info']['officials'].get('tv_umpires', [''])[0]

    row = pd.DataFrame([match_data])
    return row
    


def build_match_data_ball_by_ball(json_data: dict, counter: int) -> pd.DataFrame:
    ball_by_ball_data = pd.DataFrame()

    date = json_data['info']['dates'][0]
    season = date.split('-')[0]
    match_number = counter

    for innnings_num, inning in enumerate(json_data['innings']):
        overs = inning['overs']
        for over_num, over in enumerate(overs):
            deliveries = over['deliveries']
            for delivery_num, delivery in enumerate(deliveries):

                
                delivery_dict = ({
                    'season': season,
                    'match_no': match_number,
                    'date': date, 
                    'innings': innnings_num + 1,
                    'over': over_num + 1,
                    'delivery': delivery_num + 1,
                    'striker': delivery['batter'],
                    'non_striker': delivery['non_striker'], 
                    'bowler': delivery['bowler'],
                    'bat_runs': delivery['runs']['batter'],
                    'extra_runs': delivery['runs']['extras'],
                })

                if 'extras' in delivery:
                    delivery_dict['extra_type'] = list(delivery['extras'].keys())[0]
                
                if 'wickets' in delivery:
                    delivery_dict['wicket'] = True
                    delivery_dict['player_out'] = delivery['wickets'][0]['player_out']
                    delivery_dict['dismissal_type'] = delivery['wickets'][0]['kind']
                    if 'fielders' in delivery['wickets'][0]:
                        count = 1
                        for fielder in delivery['wickets'][0]['fielders']:
                            delivery_dict[f'fielder_{count}'] = fielder['name']
                            count += 1
                delivery_row = pd.DataFrame([delivery_dict])
                ball_by_ball_data = pd.concat([ball_by_ball_data, delivery_row], ignore_index=True)
    
    return ball_by_ball_data
