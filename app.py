import streamlit as st
import pandas as pd


@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Load the dataset
file_path = "data/all_season_summary.csv"  # Replace with your file name
df = load_data(file_path)

# App Title
st.title("IPL Matches & Scorecards")

# Sidebar Filters
st.sidebar.header("Filter Matches")
selected_season = st.sidebar.selectbox("Select Season", sorted(df['season'].unique()))
teams = sorted(df['home_team'].unique())
selected_team = st.sidebar.multiselect("Filter by Teams", teams)

# Filter Data Based on Sidebar Inputs
filtered_df = df[df['season'] == selected_season]
if selected_team:
    filtered_df = filtered_df[
        (filtered_df['home_team'].isin(selected_team)) |
        (filtered_df['away_team'].isin(selected_team))
    ]

# Show Matches in Main Area
st.subheader(f"Matches in {selected_season}")
if not filtered_df.empty:
    for index, match in filtered_df.iterrows():
        st.write(f"### {match['name']} ({match['start_date']} - {match['end_date']})")
        st.write(f"**Venue:** {match['venue_name']}")
        st.write(f"**Teams:** {match['home_team']} vs {match['away_team']}")
        st.write(f"**Toss Won By:** {match['toss_won']} - {match['decision']}")
        st.write(f"**Result:** {match['winner']} won by {match['result']}")
        st.write("#### Scorecard")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**1st Innings:** {match['1st_inning_score']}")
            st.write(f"**Home Team Score:** {match['home_score']}")
        with col2:
            st.write(f"**2nd Innings:** {match['2nd_inning_score']}")
            st.write(f"**Away Team Score:** {match['away_score']}")
        st.write("---")
else:
    st.warning("No matches found for the selected filters.")

# Show Raw Data (Optional)
if st.sidebar.checkbox("Show Raw Data"):
    st.write(filtered_df)
