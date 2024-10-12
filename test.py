#!/usr/bin/python3

import curses
import operator
import locale

# Ensure proper encoding
locale.setlocale(locale.LC_ALL, '')

# Supported operations
OPERATIONS = {
    '+': operator.add,
    '-': operator.sub,
    '×': operator.mul,
    '÷': operator.truediv
}

# Memory storage
memory = 0.0

def draw_box(win, height, width, begin_y, begin_x, title=""):
    """
    Draws a box with Unicode characters.
    """
    # Draw borders
    win.border()
    if title:
        win.addstr(0, 2, f' {title} ')

def calculator(stdscr):
    global memory
    curses.curs_set(0)  # Hide cursor
    #stdscr.clear()
    height, width = 15, 30
    begin_y, begin_x = 2, 2
    win = curses.newwin(height, width, begin_y, begin_x)
    draw_box(win, height, width, begin_y, begin_x, " TUI Calculator ")

    # Define memory buttons with shortcuts
    memory_buttons = [('MS', 's'), ('MR', 'r'), ('CE', 'e'), ('C', 'c')]

    # Define numeric and operation buttons
    buttons = [
        ['7', '8', '9', '÷'],
        ['4', '5', '6', '×'],
        ['1', '2', '3', '−'],
        ['0', '.', '=', '+']
    ]

    # Display memory buttons with shortcuts
    for idx, (btn, shortcut) in enumerate(memory_buttons):
        win.addstr(2, 2 + idx*7, f"{btn}({shortcut})")

    # Display numeric and operation buttons
    for i, row in enumerate(buttons):
        for j, btn in enumerate(row):
            win.addstr(4 + i*2, 2 + j*7, f" {btn} ")

    # Create windows for input and result
    input_win = curses.newwin(3, width-4, begin_y + height, begin_x + 2)
    input_win.border()
    input_win.addstr(0, 2, " Input ")

    result_win = curses.newwin(3, width-4, begin_y + height + 3, begin_x + 2)
    result_win.border()
    result_win.addstr(0, 2, " Result ")

    expression = ""
    result = ""

    while True:
        # Clear previous content
        input_win.erase()
        input_win.border()
        input_win.addstr(0, 2, " Input ")
        result_win.erase()
        result_win.border()
        result_win.addstr(0, 2, " Result ")

        # Update input and result displays
        input_win.addstr(1, 2, expression.ljust(width-8))
        result_win.addstr(1, 2, result.ljust(width-8))
        input_win.refresh()
        result_win.refresh()
        win.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_ENTER, 10, 13, ord('=')):
            try:
                # Replace Unicode operators with Python operators
                expr = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
                # Evaluate the expression safely
                total = eval(expr)
                result = str(total)
            except Exception:
                result = "Error"
        elif key == ord('q'):
            break
        elif key == curses.KEY_BACKSPACE or key == 127:
            expression = expression[:-1]
        elif key in [ord(shortcut) for (_, shortcut) in memory_buttons]:
            # Handle memory buttons
            for btn, shortcut in memory_buttons:
                if key == ord(shortcut):
                    if btn == 'MS':
                        try:
                            memory = float(result) if result else float(expression)
                        except:
                            memory = 0.0
                    elif btn == 'MR':
                        expression += str(memory)
                    elif btn == 'C':
                        expression = ""
                        result = ""
                    elif btn == 'CE':
                        expression = ""
                    break
        else:
            try:
                char = chr(key)
                if char in '0123456789.+-*/':
                    expression += char
                elif char in ['×', '÷', '−', '+']:
                    expression += char
            except:
                pass  # Ignore non-printable characters

    curses.endwin()

def main():
    curses.wrapper(calculator)

if __name__ == "__main__":
    main()
