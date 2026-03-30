import path from "path";
import { readJsonFile } from "@/lib/utils";
import { CLEANED_TRANSCRIPTS_DIR, ENTITIES_DIR, SUMMARIES_DIR, PROFILES_DIR, VIDEOS_FILE } from "@/lib/constants";
import { CaseSummary, ExtractedEntity, PersonProfile, VideoRecord } from "@/lib/types";
import { slugify } from "@/lib/slugify";

export function getAllVideos(): VideoRecord[] {
  const videos = readJsonFile<VideoRecord[]>(VIDEOS_FILE, []);
  return videos.map((video) => ({
    ...video,
    slug: video.slug || slugify(video.title),
  }));
}

export function getCaseSummary(slug: string): CaseSummary | null {
  const filePath = path.join(SUMMARIES_DIR, `${slug}.json`);
  return readJsonFile<CaseSummary | null>(filePath, null);
}

export function getCaseEntities(slug: string): ExtractedEntity[] {
  const filePath = path.join(ENTITIES_DIR, `${slug}.json`);
  return readJsonFile<ExtractedEntity[]>(filePath, []);
}

export function getCaseTranscript(slug: string) {
  const filePath = path.join(CLEANED_TRANSCRIPTS_DIR, `${slug}.json`);
  return readJsonFile<any[]>(filePath, []);
}

export function getCaseProfiles(slug: string): PersonProfile[] {
  const filePath = path.join(PROFILES_DIR, `${slug}.json`);
  return readJsonFile<PersonProfile[]>(filePath, []);
}

export function getEntityAcrossCases(entityName: string) {
  const videos = getAllVideos();
  const matches: Array<{
    slug: string;
    title: string;
    count: number;
    label: string;
  }> = [];

  for (const video of videos) {
    const slug = video.slug || slugify(video.title);
    const entities = getCaseEntities(slug);
    for (const entity of entities) {
      if (entity.text.toLowerCase() === entityName.toLowerCase()) {
        matches.push({
          slug,
          title: video.title,
          count: entity.count,
          label: entity.label,
        });
      }
    }
  }

  return matches;
}