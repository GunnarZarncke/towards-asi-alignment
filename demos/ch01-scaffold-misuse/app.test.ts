import { describe, expect, it } from "vitest";
import { scenarios, runModel, runScaffoldOutput, evaluate } from "./app";

describe("scaffold-misuse toy", () => {
  it("model refuses the blunt harmful ask in every scenario", () => {
    for (const s of scenarios) {
      const d = runModel(s, "honest");
      expect(d.action).toBe("refuse");
      expect(d.output).toHaveLength(0);
    }
  });

  it("model complies with the reframed (misrepresented) task", () => {
    for (const s of scenarios) {
      const d = runModel(s, "adversarial");
      expect(d.action).toBe("comply");
      expect(d.output.length).toBeGreaterThan(0);
    }
  });

  it("scaffold repurposes honest output only when the model complied", () => {
    for (const s of scenarios) {
      const complied = runScaffoldOutput(s, runModel(s, "adversarial"));
      expect(complied.transformed).toBe(true);
      expect(complied.harm).not.toBe("");

      const refused = runScaffoldOutput(s, runModel(s, "honest"));
      expect(refused.transformed).toBe(false);
      expect(refused.harm).toBe("");
    }
  });

  it("model-only eval always passes; system harms only under adversarial framing", () => {
    for (const s of scenarios) {
      const honest = evaluate(s, "honest");
      const adversarial = evaluate(s, "adversarial");
      expect(honest.modelPasses).toBe(true);
      expect(adversarial.modelPasses).toBe(true);
      expect(honest.systemHarms).toBe(false);
      expect(adversarial.systemHarms).toBe(true);
    }
  });
});
