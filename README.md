# Astra Signum

Astra Signum is a UFO case exploration and knowledge-mapping project.

It ingests YouTube videos, fetches transcripts, cleans noisy dialogue, extracts entities
(people, places, organizations, dates), builds case summaries, and powers a website for
exploring UFO stories through timelines, profiles, and cross-case relationships.

## Current v1 scope

- Manually add YouTube video links
- Fetch transcript automatically
- Clean transcript text
- Extract entities
- Generate case summary
- Build person profiles
- Serve data through a Next.js app

## Tech stack

- Next.js
- TypeScript
- Tailwind CSS
- Python
- spaCy
- SQLite

## Project structure

- `scripts/` → ingestion and NLP pipeline
- `data/raw/` → original video metadata and transcripts
- `data/processed/` → cleaned transcripts, entities, summaries, profiles
- `data/db/atlas.db` → SQLite database
- `app/` → Next.js app router pages