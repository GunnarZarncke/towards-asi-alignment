import assert from "node:assert/strict";
import test from "node:test";
import { isoDateDaysAgo, selectFeaturedFieldNews, type FieldNewsIndexItem } from "./field-news-featured.ts";

const now = new Date("2026-10-07T12:00:00.000Z");

function item(date: string, slug: string): FieldNewsIndexItem {
  return { slug, card: slug, date, kind: "research", title: slug };
}

test("isoDateDaysAgo subtracts calendar days in UTC", () => {
  assert.equal(isoDateDaysAgo(now, 7), "2026-09-30");
});

test("selectFeaturedFieldNews includes all of last week before padding", () => {
  const rows = [
    item("2026-10-07", "a"),
    item("2026-10-01", "b"),
    item("2026-09-29", "c"),
    item("2026-08-01", "d")
  ];
  const { featured, older } = selectFeaturedFieldNews(rows, { now, minCount: 0 });
  assert.deepEqual(featured.map((row) => row.slug), ["a", "b"]);
  assert.deepEqual(older.map((row) => row.slug), ["c", "d"]);
});

test("selectFeaturedFieldNews pads to three with older items", () => {
  const rows = [
    item("2026-10-07", "a"),
    item("2026-09-29", "b"),
    item("2026-09-28", "c"),
    item("2026-08-01", "d")
  ];
  const { featured, older } = selectFeaturedFieldNews(rows, { now });
  assert.deepEqual(featured.map((row) => row.slug), ["a", "b", "c"]);
  assert.deepEqual(older.map((row) => row.slug), ["d"]);
});

test("selectFeaturedFieldNews shows more than three when the week is busy", () => {
  const rows = [
    item("2026-10-07", "a"),
    item("2026-10-06", "b"),
    item("2026-10-05", "c"),
    item("2026-10-04", "d"),
    item("2026-09-01", "e")
  ];
  const { featured, older } = selectFeaturedFieldNews(rows, { now });
  assert.equal(featured.length, 4);
  assert.deepEqual(older.map((row) => row.slug), ["e"]);
});
