from bs4 import BeautifulSoup
import requests
import pandas as pd

choice = 'y'
while choice == 'y':

    gender = input("\nEnter the gender, men or women: ")
    format = input("Select the format; test, odi or t20i: ")
    rankingType = input("Do you want team or player rankings: ")
    print()

    if rankingType == "team":

        # Get the html code from the website specified by the user (through gender and format)
        source = requests.get(f"https://www.icc-cricket.com/rankings/{gender}s/team-rankings/{format}").text
        soup = BeautifulSoup(source, "lxml")

        data_dict = {'Team': [], 'Weighted Matches': [], 'Points': [], 'Ratings': []}

        for team_data in soup.find_all("tr", class_="table-body"):
            ranking, *team, matches, points, ratings = team_data.text.split()
            data_dict['Team'].append(" ".join(team))
            data_dict['Weighted Matches'].append(matches)
            data_dict['Points'].append(points)
            data_dict['Ratings'].append(ratings)

    elif rankingType == "player":

        category = input('Enter the category; batting, bowling or all-rounder: ')
        print()
        source = requests.get(f"https://www.icc-cricket.com/rankings/{gender}s/player-rankings/{format}/{category}").text
        soup = BeautifulSoup(source, "lxml")

        data_dict = {'Name': [], 'Team': [], 'Ratings': []}

        for player_data in soup.find_all("tr", class_="table-body"):
            ranking, *name, team, ratings = player_data.text.split()
            data_dict['Name'].append(" ".join(name))
            data_dict['Team'].append(team)
            data_dict['Ratings'].append(ratings)


    data_dict_df = pd.DataFrame(data=data_dict)
    data_dict_df.index = [i for i in range(1, len(data_dict['Team'])+1)]

    # List the top 10 teams
    print(data_dict_df.head(10))
    print()
    choice = input("Press y to continue, any other key to stop: ")
