import streamlit as st
from data_loader import IPLDataLoader
import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt  # Add this import



# Initialize data loader with explicit path to app/database/ipl.db
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'database', 'ipl.db')

loader = IPLDataLoader(db_path)

# Rest of your code remains the same




def main():
    st.title("IPL Dashboard")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Season Stats", "Player Stats", "Team Analysis"])

    if page == "Season Stats":
        show_season_stats()
    elif page == "Player Stats":
        show_player_stats()
    elif page == "Team Analysis":    
        show_team_analysis()     






def show_season_stats():
    st.header("IPL Season Statistics")
    
    # Get seasons list
    seasons = loader.get_seasons_list()
    selected_season = st.selectbox("Select Season", seasons)
    
    # Display season statistics
    stats = loader.get_season_stats(selected_season)
    
    
    

    IPL_WINNERS = {
    2008: "Rajasthan Royals",
    2009: "Deccan Chargers",
    2010: "Chennai Super Kings",
    2011: "Chennai Super Kings",
    2012: "Kolkata Knight Riders",
    2013: "Mumbai Indians",
    2014: "Kolkata Knight Riders",
    2015: "Mumbai Indians",
    2016: "Sunrisers Hyderabad",
    2017: "Mumbai Indians",
    2018: "Chennai Super Kings",
    2019: "Mumbai Indians",
    2020: "Mumbai Indians",
    2021: "Chennai Super Kings",
    2022: "Gujarat Titans",
    2023: "Chennai Super Kings"
}
    
    # Season Summary using actual column names
    st.subheader("Season Summary")
    col1, col2, col3 = st.columns(3)
    
    # Display metrics based on actual columns
    with col1:
        st.metric("Season", selected_season)
    with col2:
        if 'matches' in stats.columns:
            st.metric("Matches", stats['matches'].iloc[0])
    with col3:
        winner = IPL_WINNERS.get(selected_season, "Not Available")
        st.metric("Winner", winner)
    
    # Detailed Stats Table
    st.subheader("Detailed Statistics")
    st.dataframe(stats)

def show_player_stats():
    st.header("Player Statistics")
    
    # Load players data
    players_data = loader.load_players_data()
    player_list = sorted(players_data['player'].unique())
    
    # Create two columns for player selection
    col1, col2 = st.columns(2)
    
    with col1:
        player1 = st.selectbox("Select First Player", player_list, key='p1')
        player1_info = loader.get_player_details(player1)
        
    with col2:
        player2 = st.selectbox("Select Second Player", player_list, key='p2')
        player2_info = loader.get_player_details(player2)
    
    
    
    # Create comparison dataframe
    comparison_stats = {
        'Player': [player1, player2],
        'Matches': [player1_info['matches'].iloc[0], player2_info['matches'].iloc[0]],
        'Runs': [player1_info['runs'].iloc[0], player2_info['runs'].iloc[0]],
        'Batting Average': [player1_info['batting_avg'].iloc[0], player2_info['batting_avg'].iloc[0]],
        'Strike Rate': [player1_info['batting_strike_rate'].iloc[0], player2_info['batting_strike_rate'].iloc[0]],
        'Wickets': [player1_info['wickets'].iloc[0], player2_info['wickets'].iloc[0]],
        'Bowling Economy': [player1_info['bowling_economy'].iloc[0], player2_info['bowling_economy'].iloc[0]],
        'Catches': [player1_info['catches'].iloc[0], player2_info['catches'].iloc[0]]
    }
    
    comparison_df = pd.DataFrame(comparison_stats)
    
    # Create bar plots for comparison
    metrics = ['Matches', 'Runs', 'Batting Average', 'Strike Rate', 'Wickets', 'Bowling Economy', 'Catches']
    for metric in metrics:
        fig = px.bar(comparison_df, x='Player', y=metric, title=f'{metric} Comparison',
                    color='Player', barmode='group')
        st.plotly_chart(fig)







def show_team_analysis():
    st.header("Team Analysis Dashboard")
    
    
    matches_df = loader.load_matches_data()
    
    # Team Selection
    teams = loader.get_team_list()
    
    # Head to Head Analysis
    st.subheader("Head to Head Records")
    team1 = st.selectbox("Select First Team", teams, key='t1')
    team2 = st.selectbox("Select Second Team", teams, key='t2')
    
    if st.button("Show Head to Head Analysis"):
        seasonal_stats = seasonal_h2h_analysis(team1, team2, matches_df)
        st.pyplot(plt)
        st.dataframe(seasonal_stats)

def seasonal_h2h_analysis(team1, team2, matches_df):
    team_matches = matches_df[
        ((matches_df['Team1'] == team1) & (matches_df['Team2'] == team2)) |
        ((matches_df['Team1'] == team2) & (matches_df['Team2'] == team1))
    ]
    
    seasonal_stats = team_matches.groupby('Season').apply(
        lambda x: pd.Series({
            team1: len(x[x['WinningTeam'] == team1]),
            team2: len(x[x['WinningTeam'] == team2])
        })
    ).fillna(0)
    
    plt.figure(figsize=(12, 6))
    seasonal_stats.plot(kind='bar', width=0.8)
    plt.title(f'Season-wise Head to Head: {team1} vs {team2}')
    plt.xlabel('Season')
    plt.ylabel('Number of Wins')
    plt.legend(title='Teams')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    return seasonal_stats






if __name__ == "__main__":
    main()
