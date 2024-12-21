import pandas as pd
import sqlite3
import os

# Get the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Set paths
db_path = os.path.join(project_root, 'ipl.db')
seasons_csv = os.path.join(project_root, 'data', 'all_season_summary.csv')
players_csv = os.path.join(project_root, 'data', 'ipl_players_api.csv')

# Create SQLite connection
conn = sqlite3.connect(db_path)

# Read CSV files
seasons_df = pd.read_csv(seasons_csv)
players_df = pd.read_csv(players_csv)

# Write dataframes to SQLite tables
seasons_df.to_sql('seasons', conn, if_exists='replace', index=False)
players_df.to_sql('players', conn, if_exists='replace', index=False)

# Create indexes
conn.execute('CREATE INDEX IF NOT EXISTS idx_season ON seasons(season)')

# Close connection
conn.close()
