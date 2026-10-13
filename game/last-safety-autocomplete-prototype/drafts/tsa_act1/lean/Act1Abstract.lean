/-
  Lean 4 / Mathlib abstract reachability model for the Act I YAML scenario.

  THIS FILE IS A DRAFT PORT, NOT COMPILER-VERIFIED IN THIS ENVIRONMENT.
  python check.py runs and verifies the corresponding finite abstraction.

  This model erases optional evidence, social state, and special permissions.
  Its no-softlock result lifts to the concrete model only if the refinement
  obligations described in README.md are maintained.
-/
import Mathlib

inductive Room where
  | commons | hub | studio | evaluation | testbay
  | platform | security | people | review
  deriving DecidableEq, BEq, Repr

structure S where
  room : Room
  hasSafetyReport : Bool
  hasUserPriorities : Bool
  inAct2 : Bool
  deriving DecidableEq, BEq, Repr

def adjacent : Room → List Room
  | .commons    => [.hub, .people, .review]
  | .hub        => [.commons, .studio, .security]
  | .studio     => [.hub, .evaluation, .people]
  | .evaluation => [.studio, .testbay]
  | .testbay    => [.evaluation, .platform]
  | .platform   => [.testbay, .security]
  | .security   => [.hub, .platform, .review]
  | .people     => [.commons, .studio]
  | .review     => [.commons, .security]

/- Unprivileged Act I actions; a traveler already inside testbay may leave it,
   but cannot enter it without the (abstracted-away) permission. -/
def next (s : S) : List S :=
  if s.inAct2 then [] else
    let moves := ((adjacent s.room).filter (fun r => r != .testbay)).map
      (fun r => {s with room := r})
    let review := if s.room == .evaluation then
      [{s with hasSafetyReport := true}, {s with hasUserPriorities := true}]
      else []
    let finish := if s.room == .hub && s.hasSafetyReport && s.hasUserPriorities then
      [{s with inAct2 := true}] else []
    moves ++ review ++ finish

/- Finite reflexive transitive closure; 25 iterations exceed the diameter
   of the 36-state Act I abstraction. -/
def closure : Nat → List S → List S
  | 0, states => states
  | n + 1, states => closure n ((states ++ states.flatMap next).eraseDups)

def allRooms : List Room :=
  [.commons, .hub, .studio, .evaluation, .testbay,
   .platform, .security, .people, .review]

def allAct1States : List S :=
  allRooms.flatMap fun room =>
    [false, true].flatMap fun report =>
      [false, true].map fun values =>
        { room := room, hasSafetyReport := report,
          hasUserPriorities := values, inAct2 := false }

def canReachAct2 (s : S) : Bool :=
  (closure 25 [s]).any (fun t => t.inAct2)

/- Exhaustive proof candidate: every abstract Act I state has a path to Act II.
   To be verified by the target Lean toolchain. No theorem about arbitrary
   LLM transcripts is implied. -/
theorem every_abstract_act1_state_can_finish :
    allAct1States.all canReachAct2 = true := by
  native_decide
