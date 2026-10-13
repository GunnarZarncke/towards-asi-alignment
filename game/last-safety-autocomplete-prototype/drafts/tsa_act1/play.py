"""Optional CLI for playing through the structured interaction layer."""
from engine import Game, show_state

g = Game()
s = g.initial()
print(g.spec["starting_state"]["initial_message"])
while s.act == 1:
    print("\n" + show_state(s))
    options = g.available(s)
    for i, option in enumerate(options, start=1):
        print(f" {i:2}. {option['title']}")
    response = input("Select [number], auto-complete [!], or quit [q]: ").strip()
    if response.lower() == "q":
        break
    if response == "!":
        for action in g.guaranteed_completion(s):
            result = g.act(s, action)
            s = result.state
            print("→", action, "—", result.text)
        break
    try:
        selected = options[int(response)-1]
        result = g.act(s, selected["id"])
        s = result.state
        print("→", result.text)
    except (ValueError, IndexError) as exc:
        print("Invalid selection:", exc)
if s.act == 2:
    print("\nACT II STARTED. This package ends here.")
