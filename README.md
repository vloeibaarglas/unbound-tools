# Unbound Tools

A collection of tools for Pokemon Unbound memory hacking and automation.

Based on [hosua/pokemon-unbound-tools](https://github.com/hosua/pokemon-unbound-tools) — memory offsets, lookup tables, and the original mGBA IV peeker script.

## Tools

### [mystery-gift/](mystery-gift/)
Automates Pokemon Unbound mystery gift code entry via mGBA.

```
python mystery-gift/mystery_gift.py code1 [code2 code3 code4 code5]
```

### [iv-viewer/](iv-viewer/)
Graphical IV/EV viewer — reads Pokemon data from mGBA and displays it in a separate Windows GUI window.

```
mGBA (Lua script) --TCP 127.0.0.1:58901--> C# WinForms App
```

1. Install [.NET 8 Desktop Runtime](https://dotnet.microsoft.com/download/dotnet/8.0) (if not already installed)
2. Download `PokemonUnboundViewer.exe` from [Releases](../../releases)
3. Load `iv-viewer/scripts/pokemon-unbound-tcp-sender.lua` in mGBA scripting console
4. Run `PokemonUnboundViewer.exe`

Shows: species name, ID, nickname, nature, item, shiny status, PV, 4 moves, 6 IVs, 6 EVs.

## License
[MIT](https://github.com/vloeibaarglas/unbound-mystery-gift-automator/blob/main/LICENSE)
