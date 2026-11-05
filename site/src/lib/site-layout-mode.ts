export type LayoutMode = "standard" | "wide" | "focus";

export const LAYOUT_MODE_STORAGE_KEY = "site-layout-mode";
export const LEGACY_FULL_WIDTH_STORAGE_KEY = "site-layout-full-width";

const MODE_ORDER: LayoutMode[] = ["standard", "wide", "focus"];

const MODE_CLASSES: Record<LayoutMode, string[]> = {
  standard: [],
  wide: ["layout-full-width"],
  focus: ["layout-focus"]
};

export function normalizeLayoutMode(value: string | null): LayoutMode {
  if (value === "wide" || value === "focus" || value === "standard") {
    return value;
  }
  return "standard";
}

export function readStoredLayoutMode(): LayoutMode {
  try {
    const stored = localStorage.getItem(LAYOUT_MODE_STORAGE_KEY);
    if (stored) {
      return normalizeLayoutMode(stored);
    }
    if (localStorage.getItem(LEGACY_FULL_WIDTH_STORAGE_KEY) === "true") {
      return "wide";
    }
  } catch {
    /* ignore quota / private mode */
  }
  return "standard";
}

export function applyLayoutMode(mode: LayoutMode): void {
  const root = document.documentElement;
  for (const classes of Object.values(MODE_CLASSES)) {
    for (const className of classes) {
      root.classList.remove(className);
    }
  }
  for (const className of MODE_CLASSES[mode]) {
    root.classList.add(className);
  }
}

export function persistLayoutMode(mode: LayoutMode): void {
  try {
    localStorage.setItem(LAYOUT_MODE_STORAGE_KEY, mode);
    localStorage.removeItem(LEGACY_FULL_WIDTH_STORAGE_KEY);
  } catch {
    /* ignore quota / private mode */
  }
}

export function cycleLayoutMode(mode: LayoutMode): LayoutMode {
  const index = MODE_ORDER.indexOf(mode);
  const next = index < 0 ? MODE_ORDER[0] : MODE_ORDER[(index + 1) % MODE_ORDER.length];
  return next;
}

export function layoutModeLabel(mode: LayoutMode): string {
  switch (mode) {
    case "standard":
      return "Standard layout width";
    case "wide":
      return "Full-width layout";
    case "focus":
      return "Focus layout (no side panel, minimal margin)";
  }
}

export function layoutModeNextAction(mode: LayoutMode): string {
  const next = cycleLayoutMode(mode);
  switch (next) {
    case "standard":
      return "Switch to standard layout width";
    case "wide":
      return "Switch to full-width layout";
    case "focus":
      return "Switch to focus layout (hide side panel, minimal margin)";
  }
}
