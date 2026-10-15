/** Max stored data-URL length for room photos (~720×960 JPEG). */
export const MAX_IMAGE_DATA_URL_LEN = 900_000;
/** Reject tiny decodes (truncated uploads often decode to garbage). */
export const MIN_IMAGE_BYTES = 256;

export function parseImageDataUrl(text) {
  const raw = String(text ?? '').trim();
  // Raster types only: an SVG served from our origin could carry script.
  const m = /^data:image\/(jpeg|png|webp);base64,([A-Za-z0-9+/=\s]+)$/s.exec(raw);
  if (!m) return null;
  const body = m[2].replace(/\s/g, '');
  if (!body || body.length % 4 === 1) return null;
  try {
    const buf = Buffer.from(body, 'base64');
    if (buf.length < MIN_IMAGE_BYTES) return null;
    return { mime: m[1], body: buf, dataUrl: `data:image/${m[1]};base64,${body}` };
  } catch {
    return null;
  }
}
