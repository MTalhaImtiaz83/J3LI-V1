from j3li.ingestion.loader import ingestor

def main():
    print("Initializing J3LI Cloud Brain Constraints...")
    ingestor.create_constraints()
    
    # Example: Loading Al-Fatiha (Chronological Order: 5)
    sample_surah = [{
        "id": 1,
        "name_arabic": "الفاتحة",
        "name_english": "Al-Fatiha",
        "revelation_order": 5,
        "revelation_type": "Meccan",
        "verse_count": 7
    }]
    
    print("Seeding Initial Constellation (Al-Fatiha)...")
    ingestor.load_surahs(sample_surah)
    print("Success. Phase 2 Initialized.")

if __name__ == "__main__":
    main()