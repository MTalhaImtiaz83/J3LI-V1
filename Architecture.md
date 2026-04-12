



\## 1. Vision \& Purpose



\*\*Just Three Like It\*\* is a Quranic Research System that maps the interconnected landscape of the Quran, Hadith, Seerah, and Tafsir. It combines a Knowledge Graph (for structural relationships between texts) with Vector Search (for semantic, meaning-based retrieval) to deliver a research experience that honours the depth and interconnectedness of Islamic scholarship.



\*\*The Name:\*\* The Quran issues a challenge to all of humanity — produce even a single surah like it (\*"Fa'tu bi surati min mithlihi"\* — 2:23). The smallest surah in the Quran is Al-Kawthar (108): just three verses. That is the lowest possible bar. In 1,400 years, it remains unmet. "Just Three Like It" is not a boast — it is an invitation: come look at what is inside these verses, and you will understand why the challenge stands. The system exists to reveal the linguistic precision, the interconnected web of meaning, the layers of authenticated scholarship, and the historical context that make three verses of the Quran unlike anything humanity has produced.



\*\*Technical shorthand:\*\* `j3li` (used in code, repos, Docker services, CLI commands)



\*\*Core Principles:\*\*

\- Only authenticated sources (Sahih collections, established Tafsir, verified Seerah chronologies)

\- No AI hallucinations — if a link doesn't exist in the dataset, the system says so

\- Human-first, AI-assisted — the AI synthesises and connects, never invents

\- Tiered experience — approachable for everyday users, powerful for researchers

\- Classical Arabic fidelity — definitions drawn from Lane's Lexicon and Lisan al-Arab, not modern dictionaries



\*\*Brand Identity:\*\*

\- \*\*Full name:\*\* Just Three Like It

\- \*\*Arabic line:\*\* فَأْتُوا بِسُورَةٍ مِّن مِّثْلِهِ (Produce a surah the like thereof)

\- \*\*Logo mark:\*\* The numeral \*\*3\*\* — bold, isolated, unmistakable — optionally rendered in Arabic numerals (٣)

\- \*\*Technical name:\*\* `j3li`

\- \*\*Domain candidates:\*\* `justthreelikeit.com`, `just3likeit.com`, `just3.app`, `j3li.app`

\- \*\*Tagline:\*\* None. The name is the tagline.



\---



\## 2. System Architecture



\### 2.1 Architectural Pattern: Modular Monolith



A single FastAPI (Python) application with \*\*six\*\* strictly separated domain modules (added: Linguistics Module), running alongside Neo4j and Milvus in a local Docker Compose stack.



```

┌──────────────────────────────────────────────────────────────┐

│                     Docker Compose Stack                      │

│                                                               │

│  ┌────────────────────────────────────────────────────────┐  │

│  │                j3li-api (FastAPI)                        │  │

│  │                                                          │  │

│  │  ┌──────────┐ ┌──────────┐ ┌────────────────────────┐  │  │

│  │  │ API      │ │ RAG      │ │ Ingestion Module (CLI) │  │  │

│  │  │ Module   │ │ Module   │ └────────────┬───────────┘  │  │

│  │  └────┬─────┘ └────┬─────┘              │              │  │

│  │       │             │                    │              │  │

│  │  ┌────┴─────┐ ┌────┴─────┐ ┌───────────┴──────────┐  │  │

│  │  │ Graph    │ │ Vector   │ │ Linguistics Module    │  │  │

│  │  │ Module   │ │ Module   │ │ (NLP + Lexicon)       │  │  │

│  │  └────┬─────┘ └────┬─────┘ └───────────┬──────────┘  │  │

│  │       │             │                    │              │  │

│  │  ┌────┴─────────────┴────────────────────┴──────────┐  │  │

│  │  │            SQLite (metadata cache)                │  │  │

│  │  └──────────────────────────────────────────────────┘  │  │

│  └────────────────────────────────────────────────────────┘  │

│         │                      │                              │

│  ┌──────┴──────┐       ┌──────┴──────┐                       │

│  │   Neo4j     │       │   Milvus    │                       │

│  │  (Graph DB) │       │ (Vector DB) │                       │

│  │  :7474/7687 │       │   :19530    │                       │

│  └─────────────┘       └─────────────┘                       │

└──────────────────────────────────────────────────────────────┘

```



\### 2.2 Technology Decisions



| Component | Technology | Rationale |

|-----------|-----------|-----------|

| Backend Framework | FastAPI (Python 3.11+) | High performance, async support, auto-generated API docs, strong Python ML/NLP ecosystem |

| Knowledge Graph | Neo4j Community Edition 5.x | Industry standard for graph databases, excellent Cypher query language, free community edition |

| Vector Database | Milvus Standalone 2.4+ | Open-source, runs locally, handles millions of vectors, good Python SDK |

| Metadata Cache | SQLite 3 (embedded) | Zero-config, embedded in the app, perfect for fast lookups and caching |

| Embeddings | Sentence-Transformers (local) + optional cloud providers | Start with `intfloat/multilingual-e5-large` for Arabic support, swap to Gemini/Jina v4 later |

| LLM Provider | Provider-agnostic abstraction | Supports Claude, Gemini, OpenAI, and local models (Ollama) via a unified interface |

| Arabic NLP | `language-ml/quranic-nlp` | Dependency parsing, POS tagging, lemmatisation, trilateral root extraction for Quranic Arabic |

| NER (Islamic entities) | `nigar-azhar/SemanticHadithNLP` models | Custom NER for prophets, angels, clans, locations in classical Arabic text |

| Classical Lexicon | `ejtaal/mr` (Mawrid Reader) | Lane's Lexicon, Lisan al-Arab, Kitab ul-Ayn — root-based classical definitions |

| Frontend | Next.js 14+ (React) | Server-side rendering, excellent developer experience, Vercel-ready |

| Graph Visualisation | react-force-graph-3d | 2D/3D interactive graph rendering, WebGL-accelerated |

| Voice Input | Web Speech API (browser-native) | Zero dependency, Arabic speech recognition supported |

| Arabic Font | Amiri + Scheherazade New | Full Arabic ligature support, beautiful Naskh script rendering |

| Containerisation | Docker Compose | Single command to spin up the entire stack locally |



\### 2.3 Module Responsibilities (6 Modules)



\*\*API Module\*\* (`j3li/api/`)

\- REST endpoints for search, graph exploration, verse lookup

\- WebSocket endpoint for streaming LLM responses

\- Request validation, rate limiting, CORS

\- Talks ONLY to RAG, Graph, and Linguistics modules — never touches databases directly



\*\*RAG Module\*\* (`j3li/rag/`)

\- Orchestrates the GraphRAG pipeline (vector search → graph expansion → context construction → LLM generation)

\- Manages the LLM provider abstraction layer

\- Handles prompt engineering and response formatting

\- Enforces citation requirements and hallucination guardrails

\- Adopts KG2RAG's pattern of expanding seed chunks using graph relations



\*\*Graph Module\*\* (`j3li/graph/`)

\- All Neo4j Cypher queries live here

\- Subgraph extraction for visualisation

\- Relationship traversal (verse → hadith → narrator chains)

\- Graph statistics and analytics

\- Schema informed by SemanticHadith-V2 and SemanticTafsir OWL ontologies



\*\*Vector Module\*\* (`j3li/vector/`)

\- All Milvus interactions

\- Embedding generation (local or cloud)

\- Similarity search with metadata filtering

\- Index management and optimisation



\*\*Linguistics Module\*\* (`j3li/linguistics/`) — NEW in v2

\- Morphological analysis (root extraction, POS tagging, lemmatisation) via `quranic-nlp`

\- Classical lexicon lookups (Lane's Lexicon, Lisan al-Arab) via `ejtaal/mr` data

\- Named Entity Recognition for Islamic entities via SemanticHadithNLP models

\- Word-level annotation enrichment from `mustafa0x/quran-morphology`

\- Provides "word explorer" data: click any word → see root, morphology, classical definition, related words



\*\*Ingestion Module\*\* (`j3li/ingestion/`)

\- CLI commands (not live endpoints) — run manually to load data

\- Downloads and parses 15+ source datasets (see Section 7)

\- Normalises text to unified format (Uthmani script, standard IDs)

\- Writes to Neo4j (structure) and Milvus (embeddings) in coordinated batches

\- Deduplication logic for overlapping data sources



\---



\## 3. Complete Repository Inventory



\### 3.1 Tiered Repository Strategy



Every repository has been assessed for data quality, architectural fit, and integration priority.



\#### Tier 1 — Critical Foundations (Phase 1)



| # | Repository | What It Provides | Node Types Fed |

|---|-----------|-----------------|----------------|

| 1 | `islamAndAi/QURAN-NLP` | 190,655 corpus entries, 53,924 dictionary items, 700,000+ hadiths, translations, tafaseer (CSV) | Verse, Surah, Hadith, TafsirEntry |

| 2 | `SAFI174/tafsir-json` | 7 Tafsirs in clean JSON (Ibn Kathir, Qurtubi, Jalalayn, Sa'di, Tabari, Baghawi, Muyassar) | TafsirEntry, Scholar |

| 3 | `mostafaahmed97/asbab-al-nuzul-dataset` | Authenticated occasions of revelation (JSON, CSV, plaintext) | SeerahEvent, + CONTEXT\_FOR relationships |

| 4 | `A-Kamran/SemanticHadith-V2` | OWL ontology for hadith corpus: isnad chains, narrator networks, matan content | Schema reference for Hadith, Narrator, + HEARD\_FROM/NARRATED relationships |

| 5 | `A-Kamran/SemanticTafsir` | OWL ontology for Tafsir al-Tabari: discourse structure, referenced hadiths, interpretive themes | Schema reference for TafsirEntry, Topic |



\#### Tier 2 — Valuable Accelerators (Phase 2-3)



| # | Repository | What It Provides | Integration Phase |

|---|-----------|-----------------|-------------------|

| 6 | `language-ml/quranic-nlp` | Python NLP toolbox: dependency parsing, POS tagging, lemmatisation, root extraction | Phase 2 (Linguistics Module) |

| 7 | `mustafa0x/quran-morphology` | Refined morphology data with root/lemma fixes, noun forms, verbal structures | Phase 2 (Linguistics Module) |

| 8 | `abdelrahmaan/Hadith-Data-Sets` | 62,000 hadiths from Nine Books (Kutub al-Tis'ah) with/without tashkeel | Phase 2 (Hadith expansion) |

| 9 | `ejtaal/mr` (Mawrid Reader) | Lane's Lexicon, Lisan al-Arab, Kitab ul-Ayn in machine-readable format | Phase 2 (Classical Lexicon) |

| 10 | `gonotech/quran-through-seerah` | Chronological surah order mapped to Prophet's life stages | Phase 2 (Seerah timeline) |

| 11 | `nigar-azhar/SemanticHadithNLP` | Custom NER models for Islamic entities (prophets, angels, clans) | Phase 2 (Auto-tagging) |

| 12 | `A-Kamran/SemanticHadithKG` | Extended hadith knowledge graph bridging narrators to Quranic topics | Phase 3 (Graph enrichment) |

| 13 | `qazasaz/quranwbw` | Word-level annotations and metadata in structured JSON | Phase 3 (Word explorer) |



\#### Tier 3 — Reference Implementations (Study, Don't Integrate)



| # | Repository | What We Learn From It |

|---|-----------|----------------------|

| 14 | `nju-websoft/KG2RAG` | Pattern for expanding seed chunks using KG relations to prevent hallucination → Adopt in RAG Module |

| 15 | `fatemehsrz/RAG\_Knowledge\_Graph` | RAG + Neo4j + LangChain implementation patterns → Reference for pipeline design |

| 16 | `rahulnyk/knowledge\_graph` | Corpus-to-graph conversion using local models → Reference for unstructured text ingestion |

| 17 | `DEEP-PolyU/Awesome-GraphRAG` | Curated state-of-the-art GraphRAG resources → Ongoing learning reference |

| 18 | `abdulmunimjemal/hadith-search` | BERT embeddings for hadith search → Compare our embedding approach against theirs |

| 19 | `0arm/quranic` | Sentence embedding search across Quran + Hadith → Benchmark our search quality |



\#### Tier 4 — Deferred or Redundant



| # | Repository | Reason for Deferral |

|---|-----------|-------------------|

| 20 | `misraj-ai/quranhub` | Redundant API infrastructure; however, their 300+ editions dataset is valuable for Phase 4 (multi-language) |

| 21 | `sajadah/hadith-graph` | Built on ArangoDB (incompatible); frontend patterns may inspire UI |

| 22 | `Kuddari/Quran\_analysis\_with\_python` | PostgreSQL star schema — different paradigm; useful if we add analytical dashboards later |

| 23 | `umar1997/quran-md` | Audio-word alignment — Phase 4 (voice search enhancement) |

| 24 | `vitali87/code-graph-rag` | For codebases, not Islamic texts — skip entirely |



\### 3.2 Data Overlap Resolution



Several repositories contain overlapping data. Here's how we resolve conflicts:



| Data Type | Primary Source | Secondary Source | Resolution Rule |

|-----------|---------------|-----------------|-----------------|

| Quranic text (Uthmani) | `islamAndAi/QURAN-NLP` | `misraj-ai/quranhub` | Use QURAN-NLP as canonical; validate against quranhub |

| Hadith collections | `islamAndAi/QURAN-NLP` | `abdelrahmaan/Hadith-Data-Sets` | QURAN-NLP for Phase 1; merge additional collections from Hadith-Data-Sets in Phase 2 |

| Morphology | `mustafa0x/quran-morphology` | `qazasaz/quranwbw` | Use mustafa0x (higher quality fixes); supplement with quranwbw annotations |

| Tafsir | `SAFI174/tafsir-json` | `islamAndAi/QURAN-NLP` | tafsir-json for structured per-verse tafsir; QURAN-NLP for additional tafsir metadata |

| Isnad chains | `A-Kamran/SemanticHadith-V2` | `sajadah/hadith-graph` | Use SemanticHadith-V2 ontology (Neo4j compatible); ignore ArangoDB-specific structures |

| Narrator bios | `mahmoudlotfi/hadith-narrators-graph-dataset` | `A-Kamran/SemanticHadithKG` | Merge both; mahmoudlotfi for biographical data, SemanticHadithKG for graph relationships |



\---



\## 4. Neo4j Knowledge Graph Schema



\### 4.1 Schema Design Philosophy



The schema is informed by two authoritative OWL ontologies:

\- \*\*SemanticHadith-V2\*\* — for modelling isnad chains, narrator networks, and hadith authentication

\- \*\*SemanticTafsir\*\* — for modelling tafsir discourse structures, scholarly interpretation layers, and thematic hierarchies



We translate their semantic web concepts (RDF triples, OWL classes) into Neo4j's property graph model, which is more practical for our query patterns.



\### 4.2 Node Types



```

(:Surah {

&#x20;   id: INT,                        // 1-114

&#x20;   name\_arabic: STRING,            // "الفاتحة"

&#x20;   name\_english: STRING,           // "Al-Fatiha"

&#x20;   name\_transliteration: STRING,   // "Al-Fatihah"

&#x20;   revelation\_type: STRING,        // "Meccan" | "Medinan"

&#x20;   revelation\_order\_noldeke: INT,  // Nöldeke chronological order

&#x20;   revelation\_order\_azhar: INT,    // Al-Azhar chronological order

&#x20;   verse\_count: INT,

&#x20;   juz\_start: INT,

&#x20;   hizb\_start: INT,

&#x20;   seerah\_period: STRING           // From quran-through-seerah: "Early Meccan", "Late Meccan", "Medinan"

})



(:Verse {

&#x20;   id: STRING,                     // "2:255" (Surah:Ayah)

&#x20;   surah\_id: INT,

&#x20;   ayah\_number: INT,

&#x20;   text\_uthmani: STRING,           // Uthmani script (canonical)

&#x20;   text\_simple: STRING,            // Simplified Arabic (no tashkeel)

&#x20;   text\_english: STRING,           // Sahih International translation

&#x20;   juz: INT,

&#x20;   hizb: INT,

&#x20;   page: INT,

&#x20;   sajda: BOOLEAN,

&#x20;   milvus\_id: STRING,              // Link to vector embedding

&#x20;   word\_count: INT,

&#x20;   has\_asbab\_nuzul: BOOLEAN        // Flag for verses with known occasions of revelation

})



(:Word {                            // NEW — from mustafa0x/quran-morphology

&#x20;   id: STRING,                     // "2:255:1" (Surah:Ayah:WordPosition)

&#x20;   verse\_id: STRING,

&#x20;   position: INT,

&#x20;   text\_uthmani: STRING,

&#x20;   text\_simple: STRING,

&#x20;   root: STRING,                   // Trilateral root (e.g., "ك ت ب")

&#x20;   lemma: STRING,

&#x20;   pos\_tag: STRING,                // Part of speech

&#x20;   morphology: STRING,             // Full morphological breakdown

&#x20;   prefix: STRING,

&#x20;   stem: STRING,

&#x20;   suffix: STRING

})



(:Root {                            // NEW — linguistic root node

&#x20;   id: STRING,                     // The trilateral root (e.g., "كتب")

&#x20;   transliteration: STRING,        // "k-t-b"

&#x20;   core\_meaning: STRING,           // From Lane's Lexicon

&#x20;   lane\_entry: STRING,             // Full Lane's Lexicon entry

&#x20;   lisan\_entry: STRING,            // Lisan al-Arab entry (Arabic)

&#x20;   occurrences\_count: INT          // How many times this root appears in the Quran

})



(:Hadith {

&#x20;   id: STRING,                     // "bukhari:1" (collection:number)

&#x20;   collection: STRING,             // "bukhari", "muslim", "tirmidhi", "abu\_dawud", "nasai", "ibn\_majah", "malik", "ahmad", "darimi"

&#x20;   book: STRING,

&#x20;   chapter: STRING,

&#x20;   number: INT,

&#x20;   text\_arabic: STRING,

&#x20;   text\_arabic\_no\_tashkeel: STRING,// From Hadith-Data-Sets (searchable form)

&#x20;   text\_english: STRING,

&#x20;   grade: STRING,                  // "Sahih", "Hasan", "Da'if"

&#x20;   grading\_scholar: STRING,        // Who graded it

&#x20;   milvus\_id: STRING

})



(:Narrator {

&#x20;   id: STRING,

&#x20;   name\_arabic: STRING,

&#x20;   name\_english: STRING,

&#x20;   generation: STRING,             // "Sahabi", "Tabi'i", "Tabi' al-Tabi'in"

&#x20;   birth\_year\_hijri: INT,

&#x20;   death\_year\_hijri: INT,

&#x20;   reliability\_grade: STRING,      // "Thiqa", "Saduq", "Da'if", etc. (from SemanticHadith-V2 ontology)

&#x20;   biography: STRING,

&#x20;   region: STRING,                 // Geographic location

&#x20;   narrations\_count: INT           // Total hadiths narrated

})



(:SeerahEvent {

&#x20;   id: STRING,

&#x20;   title\_arabic: STRING,

&#x20;   title\_english: STRING,

&#x20;   description: STRING,

&#x20;   year\_hijri: INT,

&#x20;   year\_ce: INT,

&#x20;   location: STRING,

&#x20;   category: STRING,               // "Battle", "Treaty", "Migration", "Revelation\_Occasion", "Social", "Political"

&#x20;   seerah\_period: STRING,          // "Early Meccan", "Late Meccan", "Medinan"

&#x20;   source\_reference: STRING,       // Which historical source this comes from

&#x20;   milvus\_id: STRING

})



(:AsbabNuzul {                      // NEW — from mostafaahmed97/asbab-al-nuzul-dataset

&#x20;   id: STRING,

&#x20;   verse\_id: STRING,               // The verse this occasion relates to

&#x20;   text\_arabic: STRING,

&#x20;   text\_english: STRING,

&#x20;   source: STRING,                 // Which compilation (Al-Wahidi, Al-Suyuti, etc.)

&#x20;   narrator: STRING,               // Who narrated the occasion

&#x20;   authenticity: STRING            // Grade of the narration

})



(:Topic {

&#x20;   id: STRING,

&#x20;   name\_arabic: STRING,

&#x20;   name\_english: STRING,

&#x20;   category: STRING,               // "Worship", "Ethics", "Law", "Theology", "History", "Eschatology", "Nature"

&#x20;   description: STRING,

&#x20;   parent\_topic\_id: STRING         // Hierarchical topics (from SemanticTafsir ontology)

})



(:TafsirEntry {

&#x20;   id: STRING,                     // "ibn\_kathir:2:255"

&#x20;   tafsir\_name: STRING,            // "Ibn Kathir", "Al-Qurtubi", "Al-Jalalayn", "Al-Sa'di", "Al-Tabari", "Al-Baghawi", "Al-Muyassar"

&#x20;   scholar\_id: STRING,

&#x20;   verse\_id: STRING,

&#x20;   text\_arabic: STRING,

&#x20;   text\_english: STRING,

&#x20;   milvus\_id: STRING

})



(:Scholar {

&#x20;   id: STRING,

&#x20;   name\_arabic: STRING,

&#x20;   name\_english: STRING,

&#x20;   era: STRING,

&#x20;   school: STRING,                 // "Hanafi", "Maliki", "Shafi'i", "Hanbali"

&#x20;   notable\_works: \[STRING],

&#x20;   birth\_year\_hijri: INT,

&#x20;   death\_year\_hijri: INT,

&#x20;   methodology: STRING             // "Tafsir bil-Ma'thur", "Tafsir bil-Ra'y", etc.

})



(:IslamicEntity {                   // NEW — from SemanticHadithNLP NER

&#x20;   id: STRING,

&#x20;   name\_arabic: STRING,

&#x20;   name\_english: STRING,

&#x20;   entity\_type: STRING,            // "Prophet", "Angel", "Companion", "Clan", "Location", "Event"

&#x20;   description: STRING

})

```



\### 4.3 Relationship Types



```

// Structural

(:Verse)-\[:BELONGS\_TO]->(:Surah)

(:Verse)-\[:NEXT\_VERSE]->(:Verse)               // Sequential reading order

(:Verse)-\[:REVEALED\_AFTER]->(:Verse)           // Chronological revelation order

(:Word)-\[:PART\_OF]->(:Verse)                    // Word belongs to verse

(:Word)-\[:HAS\_ROOT]->(:Root)                    // Word derives from root

(:Topic)-\[:SUBTOPIC\_OF]->(:Topic)               // Hierarchical topic structure



// Cross-Referencing

(:Hadith)-\[:REFERENCES]->(:Verse)              // Hadith cites or explains a verse

(:Hadith)-\[:REFERENCES]->(:Hadith)             // Hadith references another hadith

(:SeerahEvent)-\[:CONTEXT\_FOR]->(:Verse)        // Asbab al-Nuzul (occasion of revelation)

(:AsbabNuzul)-\[:OCCASION\_FOR]->(:Verse)        // Specific occasion record

(:AsbabNuzul)-\[:PART\_OF\_EVENT]->(:SeerahEvent) // Links occasion to broader event

(:Verse)-\[:RELATED\_TO]->(:Verse)               // Thematic cross-reference



// Scholarly

(:Verse)-\[:EXPLAINED\_BY]->(:TafsirEntry)

(:TafsirEntry)-\[:AUTHORED\_BY]->(:Scholar)

(:TafsirEntry)-\[:CITES]->(:Hadith)             // NEW — from SemanticTafsir: tafsir citing hadith

(:TafsirEntry)-\[:REFERENCES\_EVENT]->(:SeerahEvent) // Tafsir referencing historical context



// Hadith Authentication Chain (Isnad) — informed by SemanticHadith-V2 ontology

(:Narrator)-\[:NARRATED]->(:Hadith)

(:Narrator)-\[:HEARD\_FROM]->(:Narrator)         // Chain of transmission

(:Narrator)-\[:TEACHER\_OF]->(:Narrator)

(:Narrator)-\[:CONTEMPORARY\_OF]->(:Narrator)    // Temporal overlap validation



// Topical

(:Verse)-\[:DISCUSSES]->(:Topic)

(:Hadith)-\[:DISCUSSES]->(:Topic)

(:SeerahEvent)-\[:RELATED\_TO]->(:Topic)

(:IslamicEntity)-\[:MENTIONED\_IN]->(:Verse)      // NER-extracted entity references

(:IslamicEntity)-\[:MENTIONED\_IN]->(:Hadith)



// Temporal

(:SeerahEvent)-\[:PRECEDED\_BY]->(:SeerahEvent)

(:SeerahEvent)-\[:FOLLOWED\_BY]->(:SeerahEvent)

(:Surah)-\[:REVEALED\_DURING]->(:SeerahEvent)     // Surah-level temporal mapping



// Linguistic

(:Root)-\[:RELATED\_ROOT]->(:Root)                // Semantically related roots

```



\### 4.4 Key Graph Queries



\*\*Find all context for a verse (the "deep dive" query):\*\*

```cypher

MATCH (v:Verse {id: "2:255"})

OPTIONAL MATCH (v)-\[:EXPLAINED\_BY]->(t:TafsirEntry)-\[:AUTHORED\_BY]->(s:Scholar)

OPTIONAL MATCH (h:Hadith)-\[:REFERENCES]->(v)

OPTIONAL MATCH (se:SeerahEvent)-\[:CONTEXT\_FOR]->(v)

OPTIONAL MATCH (an:AsbabNuzul)-\[:OCCASION\_FOR]->(v)

OPTIONAL MATCH (v)-\[:DISCUSSES]->(topic:Topic)

OPTIONAL MATCH (ie:IslamicEntity)-\[:MENTIONED\_IN]->(v)

RETURN v,

&#x20;      collect(DISTINCT {tafsir: t, scholar: s}) AS tafsirs,

&#x20;      collect(DISTINCT h) AS hadiths,

&#x20;      collect(DISTINCT se) AS seerah\_events,

&#x20;      collect(DISTINCT an) AS occasions\_of\_revelation,

&#x20;      collect(DISTINCT topic) AS topics,

&#x20;      collect(DISTINCT ie) AS entities

```



\*\*Trace a Hadith's full narration chain (Isnad):\*\*

```cypher

MATCH path = (n:Narrator)-\[:HEARD\_FROM\*1..10]->(source:Narrator)

WHERE EXISTS((n)-\[:NARRATED]->(:Hadith {id: "bukhari:1"}))

RETURN path, \[node IN nodes(path) | node.reliability\_grade] AS grades

```



\*\*Find all words sharing a root (linguistic exploration):\*\*

```cypher

MATCH (r:Root {id: "صبر"})<-\[:HAS\_ROOT]-(w:Word)-\[:PART\_OF]->(v:Verse)-\[:BELONGS\_TO]->(s:Surah)

RETURN r.core\_meaning AS root\_meaning,

&#x20;      w.text\_uthmani AS word,

&#x20;      w.morphology AS morphology,

&#x20;      v.id AS verse\_ref,

&#x20;      v.text\_english AS translation

ORDER BY s.id, v.ayah\_number

```



\*\*Cross-tafsir comparison for a verse:\*\*

```cypher

MATCH (v:Verse {id: "2:255"})-\[:EXPLAINED\_BY]->(t:TafsirEntry)-\[:AUTHORED\_BY]->(s:Scholar)

OPTIONAL MATCH (t)-\[:CITES]->(h:Hadith)

RETURN s.name\_english AS scholar,

&#x20;      s.methodology AS approach,

&#x20;      t.text\_english AS interpretation,

&#x20;      collect(h.id) AS cited\_hadiths

ORDER BY s.death\_year\_hijri

```



\---



\## 5. Vector Search \& RAG Pipeline



\### 5.1 Embedding Strategy



\*\*Model:\*\* `intfloat/multilingual-e5-large` (local, 1024 dimensions)

\- Excellent Arabic language support including Classical Arabic

\- Runs locally — no cloud dependency

\- Can be swapped to Gemini Embedding or Jina v4 later via the abstraction layer

\- Benchmark against `abdulmunimjemal/hadith-search` BERT embeddings to validate quality



\*\*What Gets Embedded:\*\*

| Content Type | Source Repository | Estimated Count |

|-------------|-------------------|-----------------|

| Verses (Arabic + English) | `islamAndAi/QURAN-NLP` | \~6,236 |

| Tafsir entries (7 tafsirs) | `SAFI174/tafsir-json` | \~43,652 |

| Hadith texts (Phase 1) | `islamAndAi/QURAN-NLP` | \~30,000 |

| Hadith texts (Phase 2 expansion) | `abdelrahmaan/Hadith-Data-Sets` | \~32,000 additional |

| Seerah events | `gonotech/quran-through-seerah` | \~500 |

| Asbab al-Nuzul entries | `mostafaahmed97/asbab-al-nuzul-dataset` | \~500-800 |

| Classical lexicon entries | `ejtaal/mr` | \~5,000 (key roots) |

| \*\*Total vectors (Phase 1)\*\* | | \*\*\~80,000\*\* |

| \*\*Total vectors (all phases)\*\* | | \*\*\~120,000-150,000\*\* |



\*\*Metadata stored with each vector:\*\*

\- `node\_type`: "verse", "tafsir", "hadith", "seerah", "asbab\_nuzul", "lexicon"

\- `neo4j\_id`: The corresponding Neo4j node ID

\- `source\_id`: The human-readable ID (e.g., "2:255", "bukhari:1")

\- `language`: "ar", "en"

\- `collection`: For hadith — "bukhari", "muslim", etc.

\- `tafsir\_name`: For tafsir — "ibn\_kathir", "jalalayn", etc.

\- `source\_repo`: Which repository the data came from (for traceability)



\### 5.2 Milvus Collection Schema



```python

collection\_schema = {

&#x20;   "collection\_name": "j3li\_embeddings",

&#x20;   "fields": \[

&#x20;       {"name": "id", "type": "VARCHAR", "max\_length": 128, "is\_primary": True},

&#x20;       {"name": "embedding", "type": "FLOAT\_VECTOR", "dim": 1024},

&#x20;       {"name": "node\_type", "type": "VARCHAR", "max\_length": 32},

&#x20;       {"name": "neo4j\_id", "type": "VARCHAR", "max\_length": 128},

&#x20;       {"name": "source\_id", "type": "VARCHAR", "max\_length": 128},

&#x20;       {"name": "language", "type": "VARCHAR", "max\_length": 8},

&#x20;       {"name": "text\_preview", "type": "VARCHAR", "max\_length": 512},

&#x20;       {"name": "source\_repo", "type": "VARCHAR", "max\_length": 64},

&#x20;   ],

&#x20;   "index": {

&#x20;       "field": "embedding",

&#x20;       "type": "IVF\_FLAT",

&#x20;       "metric": "COSINE",

&#x20;       "params": {"nlist": 256}

&#x20;   }

}

```



\### 5.3 The GraphRAG Pipeline (Enhanced with KG2RAG Pattern)



This pipeline adopts the KG-guided expansion pattern from `nju-websoft/KG2RAG`: rather than treating vector search and graph traversal as independent steps, the graph actively guides which vectors to retrieve next.



```

Step 1: UNDERSTAND

&#x20;  User query → Classify intent:

&#x20;  - "verse\_lookup" → Direct ID-based retrieval

&#x20;  - "thematic\_search" → Full GraphRAG pipeline

&#x20;  - "comparative\_tafsir" → Multi-scholar comparison

&#x20;  - "hadith\_search" → Hadith-focused with isnad

&#x20;  - "linguistic" → Root/word exploration

&#x20;  - "seerah\_context" → Timeline-based



Step 2: EMBED

&#x20;  Query text → Generate embedding using multilingual-e5-large

&#x20;  For Arabic queries: also generate a root-extracted variant for better matching



Step 3: INITIAL VECTOR SEARCH

&#x20;  Embedding → Search Milvus → Return top 10 results with metadata

&#x20;  Apply filters: node\_type, language, collection (if specified)



Step 4: GRAPH-GUIDED EXPANSION (KG2RAG pattern)

&#x20;  Take the top 5 vector results' neo4j\_ids

&#x20;  For each, run a 2-hop graph traversal in Neo4j:

&#x20;  a. Connected Tafsir entries (via EXPLAINED\_BY)

&#x20;  b. Connected Hadith with grades (via REFERENCES)

&#x20;  c. Connected Seerah events (via CONTEXT\_FOR)

&#x20;  d. Asbab al-Nuzul records (via OCCASION\_FOR)

&#x20;  e. Related verses via shared Topics (via DISCUSSES)

&#x20;  f. Connected Islamic entities (via MENTIONED\_IN)



&#x20;  KEY INNOVATION (from KG2RAG):

&#x20;  Take the newly discovered graph nodes and do a SECOND vector search

&#x20;  using their embeddings as queries → this finds semantically related

&#x20;  content that wasn't in the initial results but IS structurally connected.



&#x20;  Cap total expansion at 75 nodes to keep context manageable.



Step 5: CONTEXT CONSTRUCTION

&#x20;  Assemble a structured context package:

&#x20;  {

&#x20;    "primary\_results": \[top 5 vector matches with full text],

&#x20;    "graph\_context": {

&#x20;      "tafsirs": \[relevant tafsir excerpts with scholar names],

&#x20;      "hadiths": \[related hadith with grades and narrators],

&#x20;      "seerah": \[contextual events with dates],

&#x20;      "asbab\_nuzul": \[occasions of revelation],

&#x20;      "related\_verses": \[thematically linked verses],

&#x20;      "topics": \[shared topic names],

&#x20;      "entities": \[mentioned prophets, angels, etc.],

&#x20;      "linguistic": \[root meanings from classical lexicon]

&#x20;    },

&#x20;    "metadata": {

&#x20;      "sources\_count": N,

&#x20;      "authenticity\_grades": {...},

&#x20;      "source\_repositories": \[which repos data came from]

&#x20;    }

&#x20;  }



Step 6: GENERATE

&#x20;  Send to LLM with system prompt enforcing:

&#x20;  - Cite every claim with specific verse/hadith/tafsir references

&#x20;  - State "No direct scholarly link found" when inference is needed

&#x20;  - Prioritise Sahih sources over weaker ones

&#x20;  - Present multiple scholarly opinions where they differ

&#x20;  - Use classical Arabic definitions from Lane's Lexicon when explaining terms

&#x20;  - Use respectful, scholarly tone

&#x20;  - Never present a Da'if hadith without explicitly stating its grade



Step 7: VALIDATE

&#x20;  Post-process the LLM response:

&#x20;  - Verify all cited references exist in the dataset (Neo4j lookup)

&#x20;  - Verify quoted text matches stored text (fuzzy match, >90% similarity)

&#x20;  - Check hadith grades are correctly stated

&#x20;  - Flag any uncited claims

&#x20;  - Add source links for the UI to render

&#x20;  - Add confidence score based on source coverage

```



\### 5.4 LLM Provider Abstraction



```python

\# Provider interface — all providers implement this

class LLMProvider(Protocol):

&#x20;   async def generate(self, prompt: str, context: dict, config: GenerationConfig) -> LLMResponse: ...

&#x20;   async def embed(self, text: str) -> list\[float]: ...

&#x20;   def model\_name(self) -> str: ...



\# Supported providers:

\# - ClaudeProvider (Anthropic API)

\# - GeminiProvider (Google AI API)

\# - OpenAIProvider (OpenAI API)

\# - OllamaProvider (local models via Ollama — default for local dev)

\# - SentenceTransformerProvider (local embeddings only)



\# Configuration via environment variables:

\# J3LI\_LLM\_PROVIDER=claude|gemini|openai|ollama

\# J3LI\_LLM\_MODEL=claude-sonnet-4-5-20250514|gemini-1.5-pro|gpt-4o|llama3

\# J3LI\_EMBEDDING\_PROVIDER=local|gemini|openai

\# J3LI\_EMBEDDING\_MODEL=intfloat/multilingual-e5-large|text-embedding-004|...

```



\---



\## 6. API Design



\### 6.1 REST Endpoints



```

\# Search \& RAG

POST   /api/v1/search                          # Main search (text query → GraphRAG response)

POST   /api/v1/search/semantic                  # Pure vector search (no graph expansion)

POST   /api/v1/search/graph                     # Pure graph search (Cypher-based)



\# Verse Operations

GET    /api/v1/verses/{surah}:{ayah}            # Single verse with metadata

GET    /api/v1/verses/{surah}                   # All verses in a surah

GET    /api/v1/verses/{surah}:{ayah}/context    # Full context (tafsir, hadith, seerah, asbab)

GET    /api/v1/verses/{surah}:{ayah}/tafsir     # All tafsir for a verse

GET    /api/v1/verses/{surah}:{ayah}/graph      # Subgraph for visualisation

GET    /api/v1/verses/{surah}:{ayah}/words      # Word-level breakdown with morphology



\# Hadith Operations

GET    /api/v1/hadith/{collection}:{number}     # Single hadith

GET    /api/v1/hadith/{collection}:{number}/isnad   # Narration chain

GET    /api/v1/hadith/search?q=...              # Text search within hadith



\# Seerah \& Asbab al-Nuzul

GET    /api/v1/seerah/timeline                  # Chronological event list

GET    /api/v1/seerah/{event\_id}                # Single event with connections

GET    /api/v1/asbab-nuzul/{verse\_id}           # Occasions of revelation for a verse



\# Linguistics (NEW)

GET    /api/v1/roots/{root}                     # Root entry with classical definitions

GET    /api/v1/roots/{root}/verses              # All verses containing this root

GET    /api/v1/words/{verse\_id}/{position}       # Single word morphology



\# Graph Exploration

GET    /api/v1/graph/node/{id}                  # Any node with its connections

GET    /api/v1/graph/path/{from\_id}/{to\_id}     # Shortest path between nodes

GET    /api/v1/graph/subgraph?center={id}\&depth=2  # Subgraph for visualisation



\# Topics

GET    /api/v1/topics                           # All topics (hierarchical)

GET    /api/v1/topics/{topic\_id}/verses         # All verses on a topic



\# Streaming (WebSocket)

WS     /api/v1/ws/search                        # Streaming search responses

```



\### 6.2 Search Request/Response Schema



\*\*Request:\*\*

```json

{

&#x20; "query": "What does the Quran say about patience?",

&#x20; "mode": "graphrag",

&#x20; "filters": {

&#x20;   "node\_types": \["verse", "hadith"],

&#x20;   "hadith\_grade": \["sahih", "hasan"],

&#x20;   "tafsir\_sources": \["ibn\_kathir", "qurtubi"],

&#x20;   "language": "en"

&#x20; },

&#x20; "limit": 10,

&#x20; "include\_graph": true,

&#x20; "include\_linguistics": true

}

```



\*\*Response:\*\*

```json

{

&#x20; "answer": "The Quran addresses patience (sabr, from the root ص-ب-ر meaning 'to restrain oneself') extensively across multiple contexts...",

&#x20; "citations": \[

&#x20;   {

&#x20;     "type": "verse",

&#x20;     "id": "2:153",

&#x20;     "text": "O you who have believed, seek help through patience and prayer...",

&#x20;     "relevance\_score": 0.94,

&#x20;     "source\_repo": "islamAndAi/QURAN-NLP"

&#x20;   },

&#x20;   {

&#x20;     "type": "hadith",

&#x20;     "id": "bukhari:1469",

&#x20;     "text": "...",

&#x20;     "grade": "Sahih",

&#x20;     "relevance\_score": 0.87,

&#x20;     "narrator\_chain": \["Abu Hurayra", "..."]

&#x20;   }

&#x20; ],

&#x20; "linguistics": {

&#x20;   "key\_root": "صبر",

&#x20;   "classical\_definition": "To restrain, to bind, to be patient...",

&#x20;   "source": "Lane's Lexicon",

&#x20;   "quran\_occurrences": 103

&#x20; },

&#x20; "graph": {

&#x20;   "nodes": \[...],

&#x20;   "edges": \[...],

&#x20;   "center\_node": "topic:patience"

&#x20; },

&#x20; "metadata": {

&#x20;   "sources\_used": 15,

&#x20;   "processing\_time\_ms": 1800,

&#x20;   "llm\_provider": "claude",

&#x20;   "confidence": "high",

&#x20;   "kg\_expansion\_depth": 2

&#x20; }

}

```



\---



\## 7. UI/UX Architecture — Tiered Experience



\### 7.1 Two Modes



\*\*Discovery Mode\*\* (default — for general users):

\- Clean, minimal search interface with a single search bar

\- Microphone icon for voice input (Arabic and English)

\- Results displayed as readable cards with clear citations

\- "Word Explorer" — tap any Arabic word to see root, meaning, morphology

\- Gentle visual connections between related results

\- "Explore connections" button on each card to enter Research Mode for that topic



\*\*Research Mode\*\* (toggle — for scholars and advanced users):

\- Full 3D interactive graph visualiser (react-force-graph-3d)

\- Clicking any node reveals its full data panel (tafsir comparison, isnad chain, etc.)

\- Advanced filters (by collection, grade, tafsir scholar, topic, revelation period, root)

\- Comparative tafsir view (side-by-side from different scholars)

\- Timeline view for Seerah events with connected revelations

\- Linguistic root explorer — see all Quranic words sharing a root, with classical definitions

\- Isnad chain visualiser — interactive narrator chain with reliability grades colour-coded

\- Export functionality (JSON, PDF)



\### 7.2 Page Structure



```

/ (Home)

├── Search bar (always visible, sticky header)

├── Discovery Mode results

│   ├── Answer card (AI-generated summary with citations)

│   ├── Primary verse cards (with Word Explorer on tap)

│   ├── Related hadith cards (with grade badges)

│   ├── Asbab al-Nuzul card (if applicable)

│   └── "Explore deeper →" toggle to Research Mode

│

├── /verse/{surah}:{ayah} (Verse Detail)

│   ├── Arabic text (Amiri font, large, interactive — tap any word)

│   ├── Word-by-word breakdown (root, morphology, classical definition)

│   ├── English translation

│   ├── Tafsir tabs (switch between 7 scholars)

│   ├── Related hadith section (with isnad preview)

│   ├── Asbab al-Nuzul section (occasion of revelation)

│   └── Mini graph showing connections

│

├── /research (Research Mode)

│   ├── Full-screen graph visualiser

│   ├── Sidebar: node detail panel

│   ├── Filters panel (collapsible)

│   ├── Timeline slider (Hijri/CE dates)

│   └── Root explorer panel

│

├── /seerah (Seerah Timeline)

│   ├── Interactive timeline (Early Meccan → Late Meccan → Medinan)

│   ├── Event cards with connected verses and asbab al-nuzul

│   └── Map view (locations)

│

└── /roots/{root} (Root Explorer) — NEW

&#x20;   ├── Classical definition (Lane's Lexicon)

&#x20;   ├── All Quranic occurrences grouped by derived form

&#x20;   ├── Related roots

&#x20;   └── Frequency visualisation

```



\### 7.3 Visual Design Direction



\- \*\*Typography:\*\* Amiri for Arabic text, Inter for English UI, JetBrains Mono for reference IDs

\- \*\*Colour palette:\*\* Deep navy (#0A1628) base, warm gold (#C9A84C) accents, white (#FAFAFA) cards, emerald (#2D6A4F) for Sahih, amber (#E09F3E) for Hasan, muted red (#9B2335) for Da'if

\- \*\*Graph nodes:\*\* Colour-coded by type — verses (gold), hadith (emerald), tafsir (blue), seerah (amber), narrators (grey), topics (purple), roots (teal), entities (rose)

\- \*\*Animations:\*\* Subtle, respectful — smooth graph physics, gentle card reveals

\- \*\*Arabic rendering:\*\* RTL layout for Arabic content, bidirectional support, proper kashida, full tashkeel display



\---



\## 8. Data Ingestion Pipeline — 5 Phases



\### Phase 1: Core Foundation (Weeks 1-3)

\*\*Goal:\*\* Basic search working with Quran + Tafsir



| Step | Source Repository | Action | Nodes/Relationships Created |

|------|------------------|--------|---------------------------|

| 1.1 | `islamAndAi/QURAN-NLP` | Parse Quran CSV → Create Surah + Verse nodes | 114 Surah, \~6,236 Verse |

| 1.2 | `SAFI174/tafsir-json` | Parse 7 tafsir JSONs → Create TafsirEntry + Scholar nodes | \~43,652 TafsirEntry, 7 Scholar |

| 1.3 | — | Link TafsirEntry → Verse via EXPLAINED\_BY | \~43,652 relationships |

| 1.4 | `mostafaahmed97/asbab-al-nuzul-dataset` | Parse occasions of revelation → Create AsbabNuzul nodes | \~500-800 AsbabNuzul |

| 1.5 | — | Link AsbabNuzul → Verse via OCCASION\_FOR | \~500-800 relationships |

| 1.6 | — | Generate embeddings for all Verses + TafsirEntry | \~50,000 vectors |

| 1.7 | — | Load embeddings into Milvus | — |

| \*\*Milestone:\*\* | | \*\*Can query "patience" and get relevant verses with tafsir\*\* | |



\### Phase 2: Hadith \& Narrators (Weeks 4-6)

\*\*Goal:\*\* Full hadith search with authentication chains



| Step | Source Repository | Action | Nodes/Relationships Created |

|------|------------------|--------|---------------------------|

| 2.1 | `islamAndAi/QURAN-NLP` | Parse hadith collections → Create Hadith nodes (Phase 1 set) | \~30,000 Hadith |

| 2.2 | `abdelrahmaan/Hadith-Data-Sets` | Parse Nine Books → Create additional Hadith nodes | \~32,000 Hadith |

| 2.3 | — | Deduplicate overlapping hadiths between sources | — |

| 2.4 | `A-Kamran/SemanticHadith-V2` | Use ontology to model Narrator nodes + relationships | Schema validation |

| 2.5 | `mahmoudlotfi/hadith-narrators-graph-dataset` | Parse narrator biographical data | \~5,000 Narrator |

| 2.6 | — | Build isnad chains (HEARD\_FROM, NARRATED) | \~100,000+ relationships |

| 2.7 | — | Link Hadith → Verse via REFERENCES | \~20,000 relationships |

| 2.8 | — | Generate and load hadith embeddings | \~62,000 vectors |

| \*\*Milestone:\*\* | | \*\*Can ask a question and get cited, multi-source answer with hadith grades\*\* | |



\### Phase 3: Linguistics \& Lexicon (Weeks 7-9)

\*\*Goal:\*\* Word-level exploration with classical definitions



| Step | Source Repository | Action | Nodes/Relationships Created |

|------|------------------|--------|---------------------------|

| 3.1 | `mustafa0x/quran-morphology` | Parse morphology data → Create Word nodes | \~77,000 Word |

| 3.2 | — | Extract unique roots → Create Root nodes | \~1,800 Root |

| 3.3 | `ejtaal/mr` | Parse Lane's Lexicon + Lisan al-Arab → Enrich Root nodes | — |

| 3.4 | `language-ml/quranic-nlp` | Run NLP pipeline for POS tagging + dependency parsing | Word node enrichment |

| 3.5 | — | Link Word → Verse (PART\_OF), Word → Root (HAS\_ROOT) | \~77,000 relationships |

| 3.6 | — | Generate root/lexicon embeddings | \~5,000 vectors |

| \*\*Milestone:\*\* | | \*\*Can tap any Arabic word → see root, morphology, Lane's Lexicon definition\*\* | |



\### Phase 4: Seerah \& Topics (Weeks 10-12)

\*\*Goal:\*\* Full timeline + topic graph + entity recognition



| Step | Source Repository | Action | Nodes/Relationships Created |

|------|------------------|--------|---------------------------|

| 4.1 | `gonotech/quran-through-seerah` | Parse chronological data → Create SeerahEvent nodes + enrich Surah nodes | \~500 SeerahEvent |

| 4.2 | `A-Kamran/SemanticTafsir` | Use ontology to model Topic hierarchy | \~200 Topic |

| 4.3 | `nigar-azhar/SemanticHadithNLP` | Run NER on verse/hadith texts → Create IslamicEntity nodes | \~500 IslamicEntity |

| 4.4 | — | Build Seerah timeline (PRECEDED\_BY, FOLLOWED\_BY) | \~500 relationships |

| 4.5 | — | Link SeerahEvent → Verse via CONTEXT\_FOR | \~800 relationships |

| 4.6 | — | Build DISCUSSES relationships (Verse/Hadith → Topic) | \~50,000 relationships |

| 4.7 | — | Link IslamicEntity → Verse/Hadith via MENTIONED\_IN | \~10,000 relationships |

| \*\*Milestone:\*\* | | \*\*Full knowledge graph operational — researchers can explore the complete connected landscape\*\* | |



\### Phase 5: Enrichment \& Polish (Weeks 13-16)

\*\*Goal:\*\* Production-ready system with full data coverage



| Step | Source Repository | Action |

|------|------------------|--------|

| 5.1 | All sources | Cross-reference verification (validate ALL links against source data) |

| 5.2 | `umar1997/quran-md` | Audio-word alignment for voice search |

| 5.3 | `misraj-ai/quranhub` | Multi-language translations (50+ languages) |

| 5.4 | `A-Kamran/SemanticHadithKG` | Extended graph enrichment — narrator-topic bridges |

| 5.5 | — | Performance optimisation (Neo4j indexes, Milvus tuning) |

| 5.6 | — | Data integrity audit: zero fabricated relationships |

| \*\*Milestone:\*\* | | \*\*Production-ready local system with full data coverage\*\* | |



\### Data Normalisation Rules



\- All Quranic text stored in Uthmani script as the canonical form

\- All verse IDs follow `{surah\_number}:{ayah\_number}` format (e.g., "2:255")

\- All hadith IDs follow `{collection}:{number}` format (e.g., "bukhari:1")

\- All tafsir IDs follow `{tafsir\_name}:{surah}:{ayah}` format

\- All word IDs follow `{surah}:{ayah}:{position}` format

\- Arabic text preserves full diacritical marks (tashkeel)

\- English translations default to Sahih International unless specified

\- Dates stored in both Hijri and CE calendars

\- All nodes include `source\_repo` field for traceability

\- Deduplication: when overlapping data exists, primary source takes precedence (see Section 3.2)



\---



\## 9. Security, Authentication \& Guardrails



\### 9.1 Data Integrity Guardrails



\*\*No Hallucination Protocol:\*\*

The system prompt for the LLM includes strict instructions:

1\. Every factual claim MUST cite a specific source from the context window

2\. If the context doesn't contain enough information, respond: "Based on the available authenticated sources, I cannot find a direct scholarly reference for this. The closest related content is..."

3\. Never infer relationships between Hadith and Quran that don't exist in the dataset

4\. When scholars disagree, present all authenticated opinions without ranking them

5\. Always include the authenticity grade when citing Hadith

6\. Use classical Arabic definitions (from Lane's Lexicon) when explaining Quranic terms — never modern colloquial meanings

7\. Never present a Da'if hadith as evidence without explicitly stating its grade



\*\*Source Verification Pipeline:\*\*

After every LLM response, a post-processing step:

1\. Extract all cited references from the response

2\. Verify each reference exists in Neo4j

3\. Verify the quoted text matches the stored text (fuzzy match, >90% similarity)

4\. Verify hadith grades are correctly stated

5\. Flag any unverifiable citations and append a disclaimer

6\. Cross-check against `source\_repo` metadata for traceability



\### 9.2 API Security



\- Rate limiting: 60 requests/minute per IP (configurable)

\- Input sanitisation: All user queries cleaned of injection attempts (Cypher injection, prompt injection)

\- No authentication required for read-only operations in v1 (local deployment)

\- API key authentication ready for when the system goes to cloud

\- All LLM prompts include injection-resistant framing



\### 9.3 Content Safety



\- The system only serves content from the authenticated dataset

\- No user-generated content in v1

\- LLM responses are bounded by the retrieved context — the model cannot draw on its general training data for Islamic rulings

\- Clear disclaimers: "This system is a research tool. For religious guidance, consult qualified scholars."



\---



\## 10. Project Directory Structure



```

j3li/

├── docker-compose.yml                  # Neo4j + Milvus + j3li-api

├── Dockerfile                          # FastAPI app container

├── pyproject.toml                      # Python dependencies (Poetry)

├── .env.example                        # Environment variable template

│

├── j3li/                               # Main Python package

│   ├── \_\_init\_\_.py

│   ├── config.py                       # Centralised configuration

│   ├── main.py                         # FastAPI app entry point

│   │

│   ├── api/                            # API Module

│   │   ├── \_\_init\_\_.py

│   │   ├── routes/

│   │   │   ├── search.py

│   │   │   ├── verses.py

│   │   │   ├── hadith.py

│   │   │   ├── seerah.py

│   │   │   ├── graph.py

│   │   │   ├── topics.py

│   │   │   ├── linguistics.py          # NEW — root/word endpoints

│   │   │   └── asbab\_nuzul.py          # NEW

│   │   ├── middleware/

│   │   │   ├── rate\_limiter.py

│   │   │   └── sanitiser.py

│   │   └── schemas/

│   │       ├── search.py

│   │       ├── verse.py

│   │       ├── hadith.py

│   │       ├── linguistics.py          # NEW

│   │       └── graph.py

│   │

│   ├── rag/                            # RAG Module

│   │   ├── \_\_init\_\_.py

│   │   ├── pipeline.py                 # Main GraphRAG orchestration

│   │   ├── kg\_expander.py              # NEW — KG2RAG-style graph expansion

│   │   ├── context\_builder.py

│   │   ├── prompt\_templates.py

│   │   ├── validator.py                # Post-generation citation verification

│   │   └── providers/

│   │       ├── base.py

│   │       ├── claude.py

│   │       ├── gemini.py

│   │       ├── openai.py

│   │       └── ollama.py

│   │

│   ├── graph/                          # Graph Module

│   │   ├── \_\_init\_\_.py

│   │   ├── client.py

│   │   ├── queries/

│   │   │   ├── verse\_context.py

│   │   │   ├── hadith\_isnad.py

│   │   │   ├── topic\_graph.py

│   │   │   ├── linguistic\_graph.py     # NEW — root/word queries

│   │   │   ├── entity\_graph.py         # NEW — Islamic entity queries

│   │   │   └── subgraph.py

│   │   └── models.py

│   │

│   ├── vector/                         # Vector Module

│   │   ├── \_\_init\_\_.py

│   │   ├── client.py

│   │   ├── embedder.py

│   │   ├── search.py

│   │   └── index.py

│   │

│   ├── linguistics/                    # NEW — Linguistics Module

│   │   ├── \_\_init\_\_.py

│   │   ├── morphology.py              # Morphological analysis (quranic-nlp integration)

│   │   ├── root\_extractor.py          # Trilateral root extraction

│   │   ├── lexicon.py                 # Classical dictionary lookups (Lane's, Lisan)

│   │   ├── ner.py                     # Named entity recognition (SemanticHadithNLP)

│   │   └── models.py                  # Word, Root, Entity data models

│   │

│   └── ingestion/                      # Ingestion Module (CLI)

│       ├── \_\_init\_\_.py

│       ├── cli.py                      # Typer CLI commands

│       ├── sources/

│       │   ├── quran\_nlp.py            # islamAndAi/QURAN-NLP parser

│       │   ├── tafsir\_json.py          # SAFI174/tafsir-json parser

│       │   ├── asbab\_nuzul.py          # mostafaahmed97 parser                # NEW

│       │   ├── hadith\_datasets.py      # abdelrahmaan/Hadith-Data-Sets parser  # NEW

│       │   ├── narrators.py            # mahmoudlotfi parser

│       │   ├── quran\_morphology.py     # mustafa0x parser                     # NEW

│       │   ├── mawrid\_reader.py        # ejtaal/mr parser                     # NEW

│       │   ├── quran\_seerah.py         # gonotech parser                      # NEW

│       │   ├── semantic\_hadith.py      # A-Kamran ontology loader             # NEW

│       │   ├── semantic\_tafsir.py      # A-Kamran ontology loader             # NEW

│       │   ├── ner\_pipeline.py         # SemanticHadithNLP NER runner         # NEW

│       │   ├── audio\_text.py           # HuggingFace audio parser (Phase 5)

│       │   └── quranhub.py             # misraj-ai multi-language (Phase 5)   # NEW

│       ├── normaliser.py               # Text normalisation

│       ├── deduplicator.py             # Cross-source deduplication           # NEW

│       └── loader.py                   # Batch loading to Neo4j + Milvus

│

├── frontend/                           # Next.js frontend

│   ├── package.json

│   ├── app/

│   │   ├── page.tsx                    # Home / Search

│   │   ├── verse/\[ref]/page.tsx        # Verse detail

│   │   ├── research/page.tsx           # Research mode (graph explorer)

│   │   ├── seerah/page.tsx             # Seerah timeline

│   │   └── roots/\[root]/page.tsx       # Root explorer                        # NEW

│   ├── components/

│   │   ├── SearchBar.tsx

│   │   ├── VoiceInput.tsx

│   │   ├── GraphVisualiser.tsx

│   │   ├── VerseCard.tsx

│   │   ├── HadithCard.tsx

│   │   ├── TafsirTabs.tsx

│   │   ├── IsnadChain.tsx

│   │   ├── ModeToggle.tsx

│   │   ├── Timeline.tsx

│   │   ├── WordExplorer.tsx            # NEW — tap-to-explore word breakdowns

│   │   ├── RootExplorer.tsx            # NEW — root-based exploration

│   │   └── EntityBadge.tsx             # NEW — prophet/angel/companion badges

│   └── lib/

│       ├── api.ts

│       └── fonts.ts

│

├── data/

│   ├── raw/                            # Downloaded source datasets (gitignored)

│   ├── processed/                      # Normalised data

│   ├── ontologies/                     # OWL files from SemanticHadith/Tafsir    # NEW

│   └── cache.db                        # SQLite metadata cache

│

├── scripts/

│   ├── download\_all\_sources.sh         # Download ALL source repositories

│   ├── seed\_topics.py

│   ├── verify\_data.py

│   └── benchmark\_embeddings.py         # Compare embedding models               # NEW

│

├── tests/

│   ├── test\_graph/

│   ├── test\_vector/

│   ├── test\_rag/

│   ├── test\_linguistics/               # NEW

│   └── test\_api/

│

└── docs/

&#x20;   ├── plans/

&#x20;   │   └── 2026-04-02-j3li-architecture-design-v2.md

&#x20;   ├── repository-assessment.md         # This analysis

&#x20;   ├── api/

&#x20;   └── setup.md

```



\---



\## 11. Docker Compose Configuration



```yaml

version: "3.8"



services:

&#x20; j3li-api:

&#x20;   build: .

&#x20;   ports:

&#x20;     - "8000:8000"

&#x20;   environment:

&#x20;     - NEO4J\_URI=bolt://neo4j:7687

&#x20;     - NEO4J\_USER=neo4j

&#x20;     - NEO4J\_PASSWORD=j3li\_local\_dev

&#x20;     - MILVUS\_HOST=milvus

&#x20;     - MILVUS\_PORT=19530

&#x20;     - J3LI\_LLM\_PROVIDER=${J3LI\_LLM\_PROVIDER:-ollama}

&#x20;     - J3LI\_LLM\_MODEL=${J3LI\_LLM\_MODEL:-llama3}

&#x20;     - J3LI\_EMBEDDING\_PROVIDER=local

&#x20;     - J3LI\_EMBEDDING\_MODEL=intfloat/multilingual-e5-large

&#x20;   volumes:

&#x20;     - ./data:/app/data

&#x20;     - model-cache:/root/.cache/huggingface

&#x20;   depends\_on:

&#x20;     neo4j:

&#x20;       condition: service\_healthy

&#x20;     milvus:

&#x20;       condition: service\_started



&#x20; neo4j:

&#x20;   image: neo4j:5-community

&#x20;   ports:

&#x20;     - "7474:7474"

&#x20;     - "7687:7687"

&#x20;   environment:

&#x20;     - NEO4J\_AUTH=neo4j/j3li\_local\_dev

&#x20;     - NEO4J\_PLUGINS=\["apoc"]

&#x20;   volumes:

&#x20;     - neo4j-data:/data

&#x20;   healthcheck:

&#x20;     test: \["CMD-SHELL", "wget -q --spider http://localhost:7474 || exit 1"]

&#x20;     interval: 10s

&#x20;     timeout: 5s

&#x20;     retries: 5



&#x20; etcd:

&#x20;   image: quay.io/coreos/etcd:v3.5.11

&#x20;   environment:

&#x20;     - ETCD\_AUTO\_COMPACTION\_MODE=revision

&#x20;     - ETCD\_AUTO\_COMPACTION\_RETENTION=1000

&#x20;     - ALLOW\_NONE\_AUTHENTICATION=yes

&#x20;   volumes:

&#x20;     - etcd-data:/etcd



&#x20; minio:

&#x20;   image: minio/minio:RELEASE.2023-12-20T01-00-02Z

&#x20;   environment:

&#x20;     - MINIO\_ACCESS\_KEY=minioadmin

&#x20;     - MINIO\_SECRET\_KEY=minioadmin

&#x20;   volumes:

&#x20;     - minio-data:/minio\_data

&#x20;   command: minio server /minio\_data



&#x20; milvus:

&#x20;   image: milvusdb/milvus:v2.4-latest

&#x20;   ports:

&#x20;     - "19530:19530"

&#x20;   environment:

&#x20;     - ETCD\_ENDPOINTS=etcd:2379

&#x20;     - MINIO\_ADDRESS=minio:9000

&#x20;   depends\_on:

&#x20;     - etcd

&#x20;     - minio

&#x20;   volumes:

&#x20;     - milvus-data:/var/lib/milvus



volumes:

&#x20; neo4j-data:

&#x20; etcd-data:

&#x20; minio-data:

&#x20; milvus-data:

&#x20; model-cache:

```



\---



\## 12. Development Timeline (16 Weeks)



\### Phase 1: Foundation (Weeks 1-3)

\- Docker Compose stack running locally

\- Neo4j populated with Quran + Tafsir + Asbab al-Nuzul data

\- Milvus populated with verse + tafsir embeddings

\- Basic search endpoint working (vector search only)

\- \*\*Milestone:\*\* Can query "patience" and get relevant verses with tafsir



\### Phase 2: GraphRAG + Hadith (Weeks 4-6)

\- Full GraphRAG pipeline operational with KG2RAG expansion pattern

\- Hadith data ingested from both primary sources with deduplication

\- Narrator nodes + isnad chains built from SemanticHadith-V2 ontology

\- LLM provider abstraction with at least 2 providers

\- \*\*Milestone:\*\* Can ask a question and get a cited, multi-source answer



\### Phase 3: Linguistics + Frontend Discovery Mode (Weeks 7-9)

\- Linguistics Module operational (morphology, root extraction, Lane's Lexicon)

\- Word and Root nodes populated from mustafa0x/quran-morphology + ejtaal/mr

\- Next.js frontend with Discovery Mode search interface

\- Word Explorer (tap any Arabic word → root, meaning, morphology)

\- \*\*Milestone:\*\* Non-technical users can search and explore with word-level depth



\### Phase 4: Seerah + Research Mode (Weeks 10-12)

\- Seerah events + Topics + Islamic entities fully ingested

\- 3D graph visualiser operational

\- Isnad chain visualiser

\- Root explorer page

\- Comparative tafsir view + Seerah timeline

\- \*\*Milestone:\*\* Researchers can explore the full knowledge graph



\### Phase 5: Enrichment \& Polish (Weeks 13-16)

\- Multi-language support (from quranhub — 50+ languages)

\- Audio-word alignment (voice search)

\- Cross-reference verification across ALL data sources

\- Performance optimisation

\- Data integrity audit

\- \*\*Milestone:\*\* Production-ready local system



\---



\## 13. Risk Register



| Risk | Impact | Likelihood | Mitigation |

|------|--------|------------|------------|

| Arabic embedding model quality insufficient for Classical Arabic | High | Medium | Benchmark multilingual-e5-large against hadith-search BERT; fall back to Jina v4 or Gemini |

| Data inconsistencies across 15+ repositories | High | High | Deduplication module + primary source precedence rules (Section 3.2) + data verification scripts |

| OWL ontology translation to Neo4j loses semantic nuance | Medium | Medium | Manual review of SemanticHadith/Tafsir ontology mappings; consult Islamic studies expertise |

| Neo4j performance with complex multi-hop traversals | Medium | Low | Index all ID fields; cap traversal at 3 hops; use APOC procedures; query plan optimisation |

| LLM hallucination despite guardrails | High | Medium | Post-generation verification; conservative prompting; user-visible confidence scores; Lane's Lexicon for definitions |

| Classical dictionary parsing complexity (ejtaal/mr) | Medium | High | Start with most common 500 roots; expand incrementally; accept partial coverage initially |

| NER model accuracy on classical Arabic text | Medium | Medium | Validate SemanticHadithNLP models against gold-standard entities; manual correction pipeline |

| Milvus resource consumption on local machines | Medium | Medium | Use IVF\_FLAT; provide minimum specs; offer "lite mode" with ChromaDB for lower-spec machines |

| Repository data format changes or unavailability | Low | Medium | Cache all downloaded data locally; version-pin all source datasets |

| Scope creep from 25+ repositories | High | High | Strict phase gating — only Tier 1 repos in Phase 1; defer others per the tiered strategy |



\---



\## 14. Minimum Hardware Requirements



| Resource | Minimum | Recommended |

|----------|---------|-------------|

| RAM | 16 GB | 32 GB |

| CPU | 4 cores | 8 cores |

| Storage | 30 GB free | 60 GB free |

| GPU | Not required | NVIDIA GPU (faster embeddings) |

| Docker | Docker Desktop 4.x | Same |

| OS | macOS / Linux / Windows (WSL2) | macOS or Linux |



\---



\## 15. Success Metrics



| Metric | Target | How Measured |

|--------|--------|--------------|

| Search relevance | >85% of results rated "relevant" by test users | Manual evaluation on 100 test queries |

| Citation accuracy | 100% of LLM citations verifiable in the dataset | Automated post-generation verification |

| Graph coverage (tafsir) | >95% of Quranic verses linked to at least 1 Tafsir | Neo4j query |

| Graph coverage (hadith) | >50% of Sahih hadith linked to at least 1 Verse | Neo4j query |

| Root coverage | >90% of Quranic roots have Lane's Lexicon entries | Neo4j query |

| Response latency | <3 seconds for GraphRAG queries (local) | API response time monitoring |

| Data integrity | Zero fabricated relationships | Automated verification script |

| Data traceability | 100% of nodes have source\_repo metadata | Neo4j query |

| Deduplication accuracy | <1% duplicate nodes across overlapping sources | Deduplication audit |



\---



\## Appendix A: Repository Download Script



```bash

\#!/bin/bash

\# download\_all\_sources.sh — Downloads all Tier 1 and Tier 2 repositories



mkdir -p data/raw \&\& cd data/raw



echo "=== Tier 1: Critical Foundations ==="

git clone https://github.com/islamAndAi/QURAN-NLP.git

git clone https://github.com/SAFI174/tafsir-json.git

git clone https://github.com/mostafaahmed97/asbab-al-nuzul-dataset.git

git clone https://github.com/A-Kamran/SemanticHadith-V2.git

git clone https://github.com/A-Kamran/SemanticTafsir.git



echo "=== Tier 2: Valuable Accelerators ==="

git clone https://github.com/language-ml/quranic-nlp.git

git clone https://github.com/mustafa0x/quran-morphology.git

git clone https://github.com/abdelrahmaan/Hadith-Data-Sets.git

git clone https://github.com/ejtaal/mr.git

git clone https://github.com/gonotech/quran-through-seerah.git

git clone https://github.com/nigar-azhar/SemanticHadithNLP.git

git clone https://github.com/A-Kamran/SemanticHadithKG.git

git clone https://github.com/qazasaz/quranwbw.git

git clone https://github.com/mahmoudlotfi/hadith-narrators-graph-dataset.git



echo "=== Tier 3: Reference Only (for study) ==="

git clone https://github.com/nju-websoft/KG2RAG.git

git clone https://github.com/fatemehsrz/RAG\_Knowledge\_Graph.git



echo "=== Deferred (Phase 5) ==="

git clone https://github.com/misraj-ai/quranhub.git

git clone https://github.com/umar1997/quran-md.git



echo "Done. Total repositories: 18"

du -sh .

```



\---



\*This document is the complete architectural specification (v2.1) for Just Three Like It — the Quranic Research System. It incorporates 25+ assessed source repositories, a 6-module architecture, and a 5-phase, 16-week development plan. Any developer with Python and Docker experience can use this to begin implementation immediately.\*



\*Document Version: 2.1 | Updated: 2 April 2026 | Author: BTR\*

