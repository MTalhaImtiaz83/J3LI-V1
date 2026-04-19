import json
import os
from typing import List, Dict
from j3li.graph.client import graph_client

class DataIngestor:
    """Module for loading Quranic and Scholarly datasets into the Cloud Brain."""
    
    def __init__(self):
        self.graph = graph_client

    def create_constraints(self):
        """Setup unique constraints for the graph nodes."""
        constraints = [
            "CREATE CONSTRAINT surah_id IF NOT EXISTS FOR (s:Surah) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT verse_id IF NOT EXISTS FOR (v:Verse) REQUIRE v.id IS UNIQUE",
            "CREATE CONSTRAINT scholar_id IF NOT EXISTS FOR (s:Scholar) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT hadith_id IF NOT EXISTS FOR (h:Hadith) REQUIRE h.id IS UNIQUE"
        ]
        for cmd in constraints:
            self.graph.query(cmd)

    def load_surahs(self, surah_data: List[Dict]):
        """Load Surah metadata and establish chronological revelation order."""
        query = """
        UNWIND $batch AS data
        MERGE (s:Surah {id: data.id})
        SET s += data
        """
        self.graph.query(query, {"batch": surah_data})
        
        # Establish REVEALED_AFTER relationships based on revelation_order
        chrono_query = """
        MATCH (s1:Surah), (s2:Surah)
        WHERE s2.revelation_order = s1.revelation_order + 1
        MERGE (s1)-[:REVEALED_AFTER]->(s2)
        """
        self.graph.query(chrono_query)

    def load_verses(self, verse_data: List[Dict]):
        """Load Verse data and link to their respective Surahs."""
        query = """
        UNWIND $batch AS data
        MERGE (v:Verse {id: data.id})
        SET v += data
        WITH v, data
        MATCH (s:Surah {id: data.surah_id})
        MERGE (v)-[:BELONGS_TO]->(s)
        """
        self.graph.query(query, {"batch": verse_data})

ingestor = DataIngestor()