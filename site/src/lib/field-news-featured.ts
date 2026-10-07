export type FieldNewsIndexItem = {
  slug: string;
  card: string;
  date: string;
  eventDate?: string;
  kind: string;
  title: string;
  hook?: string;
  summary?: string;
  previewImage?: string;
};

export function isoDateDaysAgo(from: Date, days: number): string {
  const d = new Date(from.getTime());
  d.setUTCHours(0, 0, 0, 0);
  d.setUTCDate(d.getUTCDate() - days);
  return d.toISOString().slice(0, 10);
}

/** Newest-first items from the last `windowDays`, padded to `minCount` with older news. */
export function selectFeaturedFieldNews(
  items: FieldNewsIndexItem[],
  options?: { now?: Date; minCount?: number; windowDays?: number }
): { featured: FieldNewsIndexItem[]; older: FieldNewsIndexItem[] } {
  const now = options?.now ?? new Date();
  const minCount = options?.minCount ?? 3;
  const windowDays = options?.windowDays ?? 7;

  const sorted = [...items].sort((a, b) => b.date.localeCompare(a.date));
  const weekStart = isoDateDaysAgo(now, windowDays);
  const recentWeek = sorted.filter((item) => item.date >= weekStart);

  const featured: FieldNewsIndexItem[] = [...recentWeek];
  if (featured.length < minCount) {
    for (const item of sorted) {
      if (featured.length >= minCount) break;
      if (!featured.some((entry) => entry.slug === item.slug)) featured.push(item);
    }
  }

  const featuredSlugs = new Set(featured.map((item) => item.slug));
  const older = sorted.filter((item) => !featuredSlugs.has(item.slug));
  return { featured, older };
}
