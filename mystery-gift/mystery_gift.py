import time
import sys
import pydirectinput
import pygetwindow as gw

# =============================================================================
# CONFIGURATION
# =============================================================================
KEY_UP    = 'up'
KEY_DOWN  = 'down'
KEY_LEFT  = 'left'
KEY_RIGHT = 'right'
KEY_A     = 'x'
KEY_START = 'enter'
KEY_SEL   = 'backspace'

KEY_HOLD      = 0.08   
KEY_GAP       = 0.12   
TAB_DELAY     = 0.35   
CONFIRM_DELAY = 0.15   

# --- KEYBOARD GRID LAYOUTS ---
LAYOUT_UPPER = [
    ['A', 'B', 'C', 'D', 'E', 'F', ' ',   ',' ],
    ['G', 'H', 'I', 'J', 'K', 'L', ' ',   ';' ],
    ['M', 'N', 'O', 'P', 'Q', 'R', 'S',   ' ' ],
    ['T', 'U', 'V', 'W', 'X', 'Y', 'Z',   ' ' ],
]

LAYOUT_LOWER = [['a', 'b', 'c', 'd', 'e', 'f', ' ', '.'], ['g', 'h', 'i', 'j', 'k', 'l', ' ', ','], ['m', 'n', 'o', 'p', 'q', 'r', 's', ' '], ['t', 'u', 'v', 'w', 'x', 'y', 'z', ' ']]
LAYOUT_OTHERS = [['0', '1', '2', '3', '4', ' '], ['5', '6', '7', '8', '9', ' '], ['!', '?', '♂', '♀', '/', '-'], ['\u2026', '\u201c', '\u201d', '\u2018', '\u2019', ' ']]

LAYOUTS = [LAYOUT_UPPER, LAYOUT_LOWER, LAYOUT_OTHERS]
LAYOUT_NAMES = ['UPPER', 'lower', 'others']
AIRGAP_AFTER_COL = 6   
AIRGAP_LAYOUTS = [0, 1]

# =============================================================================
# Helpers
# =============================================================================

def press(key: str, presses: int = 1):
    for _ in range(presses):
        pydirectinput.keyDown(key)
        time.sleep(KEY_HOLD)
        pydirectinput.keyUp(key)
        time.sleep(KEY_GAP)

def find_char(layout, char):
    for r, row in enumerate(layout):
        for c, cell in enumerate(row):
            if cell == char: return r, c
    return None

def move_cursor(layout_idx, curr_r, curr_c, tgt_r, tgt_c):
    dr = tgt_r - curr_r
    if dr > 0: press(KEY_DOWN, dr)
    elif dr < 0: press(KEY_UP, -dr)
    dc = tgt_c - curr_c
    if dc == 0: return
    has_airgap = layout_idx in AIRGAP_LAYOUTS
    key = KEY_RIGHT if dc > 0 else KEY_LEFT
    if not has_airgap: press(key, abs(dc)); return
    lo, hi = (curr_c, tgt_c) if dc > 0 else (tgt_c, curr_c)
    crosses_gap = lo <= AIRGAP_AFTER_COL < hi
    press(key, abs(dc) + (1 if crosses_gap else 0))

def switch_tab(current_idx, target_idx, curr_r, curr_c):
    while current_idx != target_idx:
        press(KEY_SEL)
        time.sleep(TAB_DELAY)
        current_idx = (current_idx + 1) % len(LAYOUTS)
        curr_r = min(curr_r, len(LAYOUTS[current_idx]) - 1)
        curr_c = min(curr_c, len(LAYOUTS[current_idx][curr_r]) - 1)
    return current_idx, curr_r, curr_c

def focus_mgba():
    windows = gw.getWindowsWithTitle('mGBA')
    if windows:
        windows[0].activate()
        time.sleep(0.5)
        return True
    return False

def npc_conversation():
    """Navigate through the NPC conversation (start or return to entry screen)."""
    time.sleep(3.0)
    press(KEY_A)
    time.sleep(3.0)
    press(KEY_A)
    time.sleep(2.0)
    press(KEY_A)
    time.sleep(1.0)

# =============================================================================
# Main Logic
# =============================================================================

def run_code_sequence(code):
    print(f"\n[>>>] Processing Code: {code}")
    
    # 1. Force reset keyboard to UPPER(0,0) before typing
    current_layout_idx, curr_r, curr_c = 0, 0, 0
    while current_layout_idx != 0:
        press(KEY_SEL)
        time.sleep(TAB_DELAY)
        current_layout_idx = (current_layout_idx + 1) % len(LAYOUTS)

    # 2. Type the code
    first_char = True
    for char in code:
        target_layout_idx = next(idx for idx, L in enumerate(LAYOUTS) if find_char(L, char) is not None)
        if current_layout_idx != target_layout_idx:
            current_layout_idx, curr_r, curr_c = switch_tab(current_layout_idx, target_layout_idx, curr_r, curr_c)
        tgt_r, tgt_c = find_char(LAYOUTS[current_layout_idx], char)
        move_cursor(current_layout_idx, curr_r, curr_c, tgt_r, tgt_c)
        curr_r, curr_c = tgt_r, tgt_c
        press(KEY_A)
        time.sleep(CONFIRM_DELAY)
        
        if first_char and current_layout_idx == 0:
            current_layout_idx = 1
        first_char = False

    # 3. Submit and Post-Sequence
    press(KEY_START)
    time.sleep(1.0)
    press(KEY_A)
    # The time needed for the game to process the gift
    time.sleep(7.0) 
    press(KEY_A)

def main():
    # Capture up to 4 codes from command line arguments
    codes = sys.argv[1:5]
    
    if not codes:
        print("Usage: python poke_input.py CODE1 [CODE2 CODE3 CODE4]")
        return

    if not focus_mgba():
        print("[!] Warning: Could not find mGBA window. Manually focus it.")
        time.sleep(3)

    # Initiation Sequence (Run once at start)
    print("Initiating NPC conversation...")
    npc_conversation()

    # Loop through provided codes
    for i, code in enumerate(codes):
        run_code_sequence(code)
        
        if i < len(codes) - 1:
            print("Returning to entry screen for next code...")
            npc_conversation()

    print("\n✓ Batch complete!")

if __name__ == '__main__':
    main()