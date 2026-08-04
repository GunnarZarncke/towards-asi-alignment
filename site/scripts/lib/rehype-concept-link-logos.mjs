import { visit } from "unist-util-visit";
import { fromHtmlIsomorphic } from "hast-util-from-html-isomorphic";
import { conceptSlugFromHref } from "./concept-slug-from-href.mjs";
import { hasConceptLogo, loadConceptLogoSvg } from "./concept-logo-svg.mjs";

function linkHasConceptLogo(node) {
  return node.children?.some(
    (child) =>
      child.type === "element" &&
      Array.isArray(child.properties?.className) &&
      child.properties.className.includes("concept-logo")
  );
}

function conceptLogoSpan(slug) {
  const svg = loadConceptLogoSvg(slug);
  if (!svg) return null;

  const fragment = fromHtmlIsomorphic(
    `<span class="concept-logo concept-logo--inline" aria-hidden="true">${svg}</span>`,
    { fragment: true }
  );
  return fragment.children[0] ?? null;
}

/** Append a trailing concept logo to internal links that target concept cards. */
export default function rehypeConceptLinkLogos() {
  return (tree) => {
    visit(tree, "element", (node) => {
      if (node.tagName !== "a" || !node.properties?.href) return;
      if (linkHasConceptLogo(node)) return;

      const slug = conceptSlugFromHref(String(node.properties.href));
      if (!slug || !hasConceptLogo(slug)) return;

      const logo = conceptLogoSpan(slug);
      if (!logo) return;

      node.children = node.children ?? [];
      node.children.push({ type: "text", value: "\u00a0" });
      node.children.push(logo);
    });
  };
}
