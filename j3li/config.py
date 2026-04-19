import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Neo4j Cloud Credentials
    NEO4J_URI: str = "neo4j+s://f0568f66.databases.neo4j.io"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "rX7BPNEXRV06UZPsbW4YJxTXRT6b0TCVREwKqTrc78Q"
    
    # Gemini AI Intelligence
    GEMINI_API_KEY: str = "AIzaSyCQp57wIEdDfxwJ3FfLCTjZqVXSFtCo7YU"
    
    # System Paths
    APP_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(APP_DIR, "data")
    
    class Config:
        env_file = ".env"

settings = Settings()