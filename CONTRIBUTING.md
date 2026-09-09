# 🤝 Contributing

Thanks for considering a contribution to **Python Games**.

Contributions can include bug fixes, gameplay improvements, code cleanup, documentation updates, compatibility fixes and other useful improvements.

## Getting started

1. Fork the repository.
2. Clone your fork.
3. Create a branch for your change.
4. Install the dependencies with `py -m pip install -r requirements.txt`.
5. Make your changes.
6. Test the affected game before opening a Pull Request.

## Testing checklist

Before submitting a change, please check that:

- [ ] the affected game starts without a traceback
- [ ] menus and basic controls still work
- [ ] a normal play session can be started
- [ ] restarting and returning to menus do not crash
- [ ] save/load still works if the game uses a JSON save file
- [ ] new dependencies are added to `requirements.txt`
- [ ] unrelated files were not changed accidentally

Running the game from PowerShell is recommended while testing because Python errors remain visible after a crash.

## Pull Requests

Keep Pull Requests focused on one change or closely related group of changes when possible. Explain what you changed, why you changed it and how you tested it.

For larger gameplay changes or new games, opening a Feature Request first can help document the idea.

## Bug reports

Use the repository's Bug Report template. Include the affected game, steps to reproduce the problem and the traceback/error message when available.

Never include passwords, API keys, tokens or other private information in an issue or Pull Request.

## Code style

There is no strict formatter requirement currently. Keep code readable, use clear names and try to match the style of the file you are modifying.

## Save files

Local JSON save files contain player progress and should not be committed to the repository.

Thanks for helping improve the project. 🎮