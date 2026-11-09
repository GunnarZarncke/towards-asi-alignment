export type NavigationTimingLike = {
  transferSize?: number;
  workerStart?: number;
  deliveryType?: string;
};

/** Cache fills use ?cache=1 and are not visits. A shown page has a clean URL. */
export function shouldRecordVisit(search: string): boolean {
  return new URLSearchParams(search).get("cache") !== "1";
}

/**
 * True when this showing did not download the document.
 * Service-worker cache hits report no transfer; back-forward cache sets restored.
 */
export function servedFromCache(
  navigation: NavigationTimingLike | undefined,
  restored: boolean
): boolean {
  if (restored) return true;
  if (!navigation) return false;
  if (navigation.deliveryType === "cache") return true;
  return (navigation.workerStart ?? 0) > 0 && (navigation.transferSize ?? 0) === 0;
}

export function pageviewProperties(input: {
  title: string;
  restored: boolean;
  navigation?: NavigationTimingLike;
}): { title: string; served_from_cache?: true } {
  const properties: { title: string; served_from_cache?: true } = { title: input.title };
  if (servedFromCache(input.navigation, input.restored)) properties.served_from_cache = true;
  return properties;
}
