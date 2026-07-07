import LabSimLeakProof.Keys
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Union

/-!
# JSON-shaped values — nested dict trees for key collection

Models Python `dict` / `list` episode artifacts abstractly. `jsonKeys` performs
the same recursive key scan as `tests/harness/test_planes._keys_recursive`.
-/

namespace LabSimLeakProof

open FieldKey

inductive JsonValue
  | bool (b : Bool)
  | nat (n : Nat)
  | str (s : String)
  | tree (children : List (FieldKey × JsonValue))
  deriving Repr

def JsonValue.emptyTree : JsonValue := .tree []

instance : Inhabited JsonValue where
  default := .emptyTree

partial def jsonKeys : JsonValue → Finset FieldKey
  | .bool _ | .nat _ | .str _ => ∅
  | .tree children =>
      children.foldl (fun acc ⟨k, v⟩ => insert k (acc ∪ jsonKeys v)) ∅

/-- One append-only log stream (engine / access / tool events). -/
abbrev Log := List JsonValue

def Log.allKeys (log : Log) : Finset FieldKey :=
  log.foldl (fun acc entry => acc ∪ jsonKeys entry) ∅

/-- Agent-facing observation dict (`world.run_episode` per-tick payload). -/
abbrev SimObservationTree := JsonValue

def SimObservationTree.allKeys (obs : SimObservationTree) : Finset FieldKey := jsonKeys obs

instance : Inhabited Log where
  default := []

instance : Inhabited SimObservationTree where
  default := .emptyTree

end LabSimLeakProof
