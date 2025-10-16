# Repository Guidelines

This repo contains the Monarch (Azure Glow) desktop theme for Omarchy: Hyprland, Waybar, Alacritty, Mako, Hyprlock, and Neovim. Keep changes self‑contained under this theme folder and avoid user‑specific absolute paths.

## Project Structure & Module Organization
- Root configs: `hyprland.conf`, `hyprlock.conf`, `alacritty.toml`, `mako.ini`, `neovim.lua`, `waybar.css`.
- Waybar: `waybar/config.jsonc`, `waybar/modules`, `waybar/style.css`, `waybar/colors/*`, `waybar/scripts/*`.
- Hypr extras: `extra-configs/looknfeel.conf`, `extra-configs/windows.conf`, `extra-configs/apps/*.conf` (loaded via `apps.conf`).
- Assets: `backgrounds/*`, `preview.png`, palette notes in `azure-glow-palette-reference.md`.

## Build, Test, and Development Commands
- No build step. Symlink into your `~/.config` and reload affected apps.
  - Example: `ln -sf $(pwd)/waybar ~/.config/waybar && pkill -SIGUSR2 waybar`
  - Example: `ln -sf $(pwd)/hyprland.conf ~/.config/hypr/hyprland.conf && hyprctl reload`
- Validate JSONC quickly: `jq -e . <(grep -v '^//' waybar/config.jsonc)`

## Coding Style & Naming Conventions
- Indent with 2 spaces; UTF‑8; end files with a newline.
- File names: kebab‑case for CSS/INI (`waybar.css`, `swayosd.css`), lowercase scopes for Hypr extras (`apps/*.conf`).
- Colors: prefer tokens in `waybar/colors/*` and reference `monarch-glow.css`. Keep palette edits centralized.
- Paths: use relative imports/includes from the theme root; do not hardcode `$HOME`.

## Testing Guidelines
- Visual checks: reload Hyprland (`hyprctl reload`) and Waybar (`pkill -SIGUSR2 waybar`).
- Verify: workspace colors, MPRIS labels, battery/time toggles, notification borders, lock screen accents.
- Keep before/after screenshots; update `preview.png` when visuals materially change.

## Commit & Pull Request Guidelines
- Commit format: `type(scope): summary` (e.g., `fix(waybar): clamp MPRIS label`).
  - Common scopes: `waybar`, `hypr`, `alacritty`, `mako`, `neovim`, `assets`.
  - Common types: `feat`, `fix`, `chore`, `refactor`, `style`, `docs`.
- PRs: include concise description, linked issues, screenshots (bar/lock), and testing notes (reloads performed, configs touched).

## Security & Configuration Tips
- Do not commit secrets or user‑machine paths.
- Keep images optimized; prefer <1 MB backgrounds and PNG/JPEG with reasonable compression.
- Changes must remain usable without external dependencies beyond the theme directory.

