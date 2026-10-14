/**
 * Room photos are downscaled before file.write so JSON saves and /api/tool bodies stay bounded.
 */

const DEFAULTS = { maxW: 720, maxH: 960, quality: 0.88, mime: 'image/jpeg' };

/** @param {HTMLCanvasElement} source */
export function encodePhotoCanvas(source, opts = {}) {
  const { maxW, maxH, quality, mime } = { ...DEFAULTS, ...opts };
  let w = source.width;
  let h = source.height;
  const scale = Math.min(1, maxW / w, maxH / h);
  w = Math.max(1, Math.round(w * scale));
  h = Math.max(1, Math.round(h * scale));
  const out = document.createElement('canvas');
  out.width = w;
  out.height = h;
  out.getContext('2d').drawImage(source, 0, 0, w, h);
  const dataUrl = out.toDataURL(mime, quality);
  return { dataUrl, width: w, height: h, mime };
}
