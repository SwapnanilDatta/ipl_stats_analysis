import sqlite3
import pandas as pd
import os

class IPLDataLoader:
    def __init__(self, db_path=None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            database_dir = os.path.join(current_dir, 'database')
            self.db_path = os.path.join(database_dir, 'ipl.db')
        else:
            self.db_path = db_path

            
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def load_seasons_data(self):
        """Load all seasons data from database"""
        conn = self.get_connection()
        query = "SELECT * FROM seasons"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def load_players_data(self):
        """Load all players data from database"""
        conn = self.get_connection()
        query = "SELECT * FROM players"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_seasons_list(self):
        """Get list of unique seasons"""
        conn = self.get_connection()
        query = "SELECT DISTINCT season FROM seasons ORDER BY season"
        seasons = pd.read_sql_query(query, conn)
        conn.close()
        return seasons['season'].tolist()
    
    def get_season_stats(self, season):
        """Get stats for a specific season"""
        conn = self.get_connection()
        query = f"SELECT * FROM seasons WHERE season = {season}"
        stats = pd.read_sql_query(query, conn)
        conn.close()
        return stats
    
    def get_player_details(self, player_name):
        """Get details for a specific player"""
        conn = self.get_connection()
        query = f"SELECT * FROM players WHERE player = '{player_name}'"
        player = pd.read_sql_query(query, conn)
        conn.close()
        return player

    
    def get_team_list(self):
        """Get list of all teams"""
        conn = self.get_connection()
        query = "SELECT DISTINCT team FROM players ORDER BY team"
        teams = pd.read_sql_query(query, conn)
        conn.close()
        return teams['team'].tolist()
    
    def get_team_players(self, team_name):
        """Get all players from a specific team"""
        conn = self.get_connection()
        query = f"SELECT * FROM players WHERE team = '{team_name}'"
        players = pd.read_sql_query(query, conn)
        conn.close()
        return players
    # Add these methods to your IPLDataLoader class
    def get_team_list(self):
        """Get list of all teams"""
        conn = self.get_connection()
        # First, let's print the table schema
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(seasons)")
        columns = cursor.fetchall()
        print("Available columns:", [col[1] for col in columns])
        
        # Then modify the query based on actual column names
        query = """
        SELECT DISTINCT winner FROM seasons 
        ORDER BY winner
        """
        teams = pd.read_sql_query(query, conn)
        conn.close()
        return teams['winner'].tolist()


    def get_team_head_to_head(self):
        """Get head to head records between teams"""
        conn = self.get_connection()
        # First let's see what columns we have
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM seasons LIMIT 1")
        columns = [description[0] for description in cursor.description]
        print("Available columns:", columns)
        
        # Then we'll modify the query based on actual column names
        query = """
        SELECT 
            winner,
            COUNT(*) as matches_played
        FROM seasons 
        GROUP BY winner
        """
        head_to_head = pd.read_sql_query(query, conn)
        conn.close()
        return head_to_head
    
    def get_team_performance_trend(self, team_name):
        """Get team performance across seasons"""
        conn = self.get_connection()
        query = f"""
        SELECT 
            season,
            COUNT(*) as matches_played,
            SUM(CASE WHEN winner = '{team_name}' THEN 1 ELSE 0 END) as matches_won
        FROM seasons
        WHERE winner = '{team_name}'
        GROUP BY season
        ORDER BY season
        """
        trend = pd.read_sql_query(query, conn)
        conn.close()
        return trend




