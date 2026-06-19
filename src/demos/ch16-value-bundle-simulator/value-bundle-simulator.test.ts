import { describe, expect, it } from "vitest";
import { presets, topValues } from "./value-bundle-simulator";

const calibrationCases: Array<{
  preset: keyof typeof presets;
  expectedTopTen: string[];
}> = [
  {
    preset: "Pastoral herder honor culture",
    expectedTopTen: ["Honor", "Loyalty", "Courage", "Hospitality"],
  },
  {
    preset: "Intensive rice village",
    expectedTopTen: ["Duty", "Conformity", "Hierarchy", "Filial piety", "Purity"],
  },
  {
    preset: "Merchant port city",
    expectedTopTen: ["Justice", "Fairness", "Truth", "Achievement", "Universalism"],
  },
  {
    preset: "Modern affluent online society",
    expectedTopTen: ["Liberty", "Equality", "Autonomy", "Universalism", "Fairness"],
  },
  {
    preset: "Arctic hunter camp",
    expectedTopTen: ["Solidarity", "Care", "Stoicism", "Frugality", "Courage"],
  },
  {
    preset: "Imperial bureaucracy",
    expectedTopTen: ["Hierarchy", "Authority", "Duty", "Legacy", "Justice"],
  },
  {
    preset: "Mobile forager band",
    expectedTopTen: ["Equality", "Autonomy", "Care", "Humility", "Fraternity"],
  },
];

describe("value bundle calibration presets", () => {
  for (const testCase of calibrationCases) {
    it(`${testCase.preset} contains calibration values in top ten`, () => {
      const names = topValues(presets[testCase.preset], 10).map((v) => v.name);
      expect(names).toEqual(expect.arrayContaining(testCase.expectedTopTen));
    });
  }
});
