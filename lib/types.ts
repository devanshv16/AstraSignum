export type VideoRecord = {
  title: string;
  url: string;
  category: string;
  source: string;
  slug?: string;
};

export type TranscriptSegment = {
  text: string;
  start: number;
  duration: number;
};

export type CleanedSegment = TranscriptSegment & {
  cleaned_text: string;
};

export type EntityType = "PERSON" | "GPE" | "ORG" | "DATE" | "EVENT" | "OTHER";

export type ExtractedEntity = {
  text: string;
  label: EntityType;
  count: number;
  mentions: Array<{
    start: number;
    snippet: string;
  }>;
};

export type CaseSummary = {
  slug: string;
  title: string;
  short_summary: string;
  key_points: string[];
  timeline_years: string[];
  top_people: string[];
  top_places: string[];
  top_orgs: string[];
};

export type PersonProfile = {
  name: string;
  case_slug: string;
  role_summary: string;
  timeline_facts: string[];
  associated_places: string[];
  associated_orgs: string[];
  snippets: string[];
};