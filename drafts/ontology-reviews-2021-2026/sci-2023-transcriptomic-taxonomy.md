# Hierarchical transcriptomic brain-cell taxonomy

- **Date:** 2023
- **Field:** Neuroscience
- **Source:** https://www.nature.com/articles/s41586-023-06812-z
- **Source read:** full
- **TSA files consulted:** `chapters/ch07-finding-boundary.tex`, `chapters/ch11-capability-without-task-ontology.tex`
- **Keywords grepped:** cell type; transcriptom; taxonomy; natural abstraction / natural latent; coarse-grain; ontology trap / task ontology; bearer; hierarchical type

## Source ontology

Yao et al. (BICCN) recarve “cell type” from a morphology/location/name category into a nested high-dimensional molecular/spatial object. Combining ~4 million QC scRNA-seq cells with ~4.3 million MERFISH cells, they organize the adult mouse brain into four nested levels—34 classes, 338 subclasses, 1,201 supertypes, 5,322 clusters—plus overlapping “neighbourhoods” that are explicitly *not* hierarchy nodes. Transcriptomic identity and spatial specificity correspond strongly; transcription-factor combinatorial codes are the main classifiers. The tree is useful but incomplete: relationships are both hierarchical and multidimensional, and not every cluster is claimed as a true type. Anatomical names become hypotheses to map onto, not the type primitive.

## TSA coverage

- **Status:** orthogonal
- **Closest TSA terms/chapters:** ontology trap (ch07); coarse-graining / which nested unit (ch07); task ontology (ch11); natural latents / NAH (ch17, App. B MB2/MB3) as analog only.
- **Overlap:** Ch07 already refuses to treat pre-existing labels (model, user, company) as discovered boundaries and notes that incentive results are not abstraction-invariant. Ch11 refuses evaluator-named tasks as the capability object. Yao is a worked empirical instance of that operation in neuroscience: named anatomy ≠ recovered type; two independent high-bandwidth channels jointly pin the object.
- **Gap:** TSA has no cell-type primitive and does not need one. Yao’s extra structure—four nested levels whose “real” grain is region-dependent, dual-modality correspondence as type-validation, TF combinatorial code—does not express an alignment state variable. Mapping it onto bearer maps, agent types, or NAH would be a hostile-test rename.

## Applicability to TSA

- **Score (0–5):** 1
- **Why:** Status-B recarving of a biological type, not a missing TSA cut. The analogical lesson (don’t trust morphology names; recover nested types from high-bit observations under an independent spatial constraint) is already inside ontology trap plus coarse-graining search. No App. B row, chapter rewrite, or reverse-gap is warranted; NAH already occupies the “convergent natural types” slot.
- **Ontology-stickiness risk:** Low for TSA. Pre-2023 models already have scRNA-seq taxonomies; the 2023 move is whole-brain nested scale plus spatial correspondence as constitutive of type, easy to flatten into “a bigger atlas.” A sticky LLM might analogize “we need a cell-type taxonomy of agents,” which TSA should refuse. TSA neither includes, renames, nor fails to see a load-bearing alignment primitive here—it correctly excludes it.
- **Recommended action:** ignore

## One-line finding

Yao et al. make “cell type” a nested molecular/spatial object, a real neuroscience recarving with almost no TSA purchase beyond the ontology-trap lesson TSA already has.
