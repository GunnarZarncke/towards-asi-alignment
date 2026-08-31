# Witness host traces (local)

Gitignored under `experiments/witness/data/` (see repo `.gitignore`). Re-fetch; do not commit the 563 MB Perceval dump or the Linux clone.

```bash
# Zenodo 10654193 (CSV + Perceval JSON)
mkdir -p experiments/witness/data/zenodo
curl -L -o experiments/witness/data/zenodo/bfc_bic.csv \
  https://zenodo.org/api/records/10654193/files/bfc_bic.csv/content
curl -L -o experiments/witness/data/zenodo/linux-commits-2023-11-12.json.gz \
  https://zenodo.org/api/records/10654193/files/linux-commits-2023-11-12.json.gz/content

# SNAP RfA
mkdir -p experiments/witness/data/snap
curl -L -o experiments/witness/data/snap/wiki-RfA.txt.gz \
  https://snap.stanford.edu/data/wiki-RfA.txt.gz

# wiki-socks
git clone --depth 1 https://github.com/lraszewski/wiki-socks.git \
  experiments/witness/data/wiki-socks/repo

# Optional: -stable episode git (filter often ignored; ~full tree)
git clone --single-branch --branch linux-6.1.y --depth 400 \
  https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git \
  experiments/witness/data/kernel-git/linux-6.1.y-shallow

python3 experiments/witness/join_bic_review_tags.py
python3 experiments/witness/collect_rfa_followup.py
python3 experiments/witness/collect_rfa_passed_2012.py
python3 experiments/witness/collect_bot_successor.py
python3 experiments/witness/summarize_wiki_socks.py
python3 experiments/witness/check_h2.py
python3 experiments/witness/check_h3.py

# Phase 3: Moral Machine country AMCE + pinned Arena Elo
mkdir -p experiments/witness/data/moral-machine experiments/witness/data/arena
curl -L -o experiments/witness/data/moral-machine/CountriesChangePr.csv.tar.gz \
  https://files.osf.io/v1/resources/3hvt2/providers/osfstorage/5b54f67969e43a0010d38204
tar -xzf experiments/witness/data/moral-machine/CountriesChangePr.csv.tar.gz \
  -C experiments/witness/data/moral-machine
curl -L -o experiments/witness/data/arena/elo-20250301.csv \
  https://huggingface.co/datasets/mathewhe/chatbot-arena-elo/resolve/20250301/elo.csv

python3 experiments/witness/collect_h4_bundle.py
python3 experiments/witness/collect_h4_selector.py
python3 experiments/witness/check_h4_bundle.py
python3 experiments/witness/check_h4_selector.py

# W-12: Moral Machine raw (individual table, not country AMCE)
curl -L -o experiments/witness/data/moral-machine/SharedResponses.csv.tar.gz \
  https://files.osf.io/v1/resources/3hvt2/providers/osfstorage/5b54f679c86a8c0010444782
python3 experiments/witness/collect_h4_mm_raw.py
python3 experiments/witness/check_h4_mm_raw.py

# W-13: PDG — metadata probe only (do not download adolescent SPSS)
python3 experiments/witness/collect_h4_pdg.py
python3 experiments/witness/check_h4_pdg.py

# W-14: CPC2015 Experiment 1
mkdir -p experiments/witness/data/cpc2015
python3 experiments/witness/collect_h4_cpc2015.py
python3 experiments/witness/check_h4_cpc2015.py

# W-16: SCDB justice-centered
mkdir -p experiments/witness/data/scotus
python3 experiments/witness/collect_h4_scotus.py
python3 experiments/witness/check_h4_scotus.py

# W-17: Moltbook MB7a (H7) — export jscmp4/Moltbook 2026-07-03 posts + comments
mkdir -p experiments/witness/data/moltbook
# Place posts.parquet and comments.parquet (or .jsonl / .csv) from HF pin under data/moltbook/
python3 experiments/witness/collect_h7_moltbook_mb7a.py
python3 experiments/witness/check_h7_moltbook_mb7a.py
```

Derived counts used by the freeze live in `fixtures/` (committed). This directory is a cache.
