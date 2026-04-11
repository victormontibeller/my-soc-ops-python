# Copilot Instructions for Soc Ops

## Mandatory Development Checklist

Run these before handing work back:

- Lint: `uv run ruff check .`
- Build: `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Test: `uv run pytest`

## Architecture

- Keep routes thin in `app/main.py`.
- Keep session state and transitions in `app/game_service.py`.
- Keep bingo rules and board logic in `app/game_logic.py` as pure functions when possible.
- Keep enums and data models in `app/models.py`.
- Keep prompts and constant content in `app/data.py`.

## UI

- Use Jinja templates in `app/templates/` as the source of rendered markup.
- Put reusable partials in `app/templates/components/`.
- Preserve the HTMX server-rendered flow; do not add a frontend framework unless asked.
- Prefer existing utility classes in `app/static/css/app.css` before adding new ones.

## Design Guide

- Visual direction is dark cyberpunk with neon accents.
- Keep dark as the default experience for app and docs unless the task explicitly asks for theming options.
- Prefer semantic color tokens and CSS variables over hardcoded color values.
- Maintain strong contrast for readability in all states: default, marked, winning, disabled, and modal overlays.
- Use motion intentionally: prioritize a few high-impact transitions over many subtle animations.
- Keep the board legible first: free-space, marked, and winning states must remain immediately distinguishable.
- When changing UI copy, update behavior-focused tests only where assertions depend on text labels.
- Preserve mobile usability: touch targets should remain comfortably tappable and layouts should avoid horizontal overflow.

## Behavior To Preserve

- The board is always 5x5.
- The center square is a marked free space.
- Winning lines are rows, columns, and both diagonals.
- Session state stays in memory and is keyed by the cookie-backed session id.
- Reset returns the user to the start screen.
- HTMX updates should work without a full page reload.

## Testing Guidance

- Update `tests/test_api.py` for route or template changes.
- Update `tests/test_game_logic.py` for bingo rule or board changes.
- Keep tests behavior-focused and deterministic.

## Constraints

- Prefer small, focused changes.
- Preserve existing naming and layout unless the task requires otherwise.
- Avoid adding persistence, auth, client-side frameworks, or external services unless requested.
- Use `README.md` for project context; treat `workshop/` and `docs/` as secondary unless working on documentation.