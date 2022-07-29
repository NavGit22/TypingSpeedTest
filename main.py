import tkinter as tk
import math

# ---------------------------- CONSTANTS ------------------------------- #
WORK_MIN = 1
BACKGROUND_COLOR = "#FCF8E8"
WHITE = "#FFFFFF"
BROWN = "#D1512D"
BLUE = "#231955"
GREEN = "#2B7A0B"
RED = "#EB1D36"
timer = None
input_text = []
output_text = []
input_words = []


# ---------------------------- OPEN TEXT FILE TO LOAD DATA ------------------------------- #
def display_words():
    global input_text
    # Open text file for words
    tf = open('Input_file.txt')
    data = tf.read()
    # Remove \n and ""
    input_text = data.replace("\n", " ")
    input_text = input_text.split(" ")
    input_text.remove("")

    # Enable the Display text area
    display_text_area.config(state=tk.NORMAL)

    # Display the words in the Text Area
    display_text_area.insert(tk.END, data)

    # Disable the text area so that it cannot be modified
    display_text_area.config(state=tk.DISABLED)

    # Enable Start Test Button to start the test
    button_start.config(state=tk.NORMAL)

    tf.close()


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    # Clear the timer and Completion message
    clear_board()

    # Disabled the Start Test Button
    button_start.config(state=tk.DISABLED)

    # Enabled the Reset Button so that you can reset in between
    button_reset.config(state=tk.NORMAL)

    # Enabled the Enter text area for user
    enter_text_area.config(state=tk.NORMAL)

    # Clear the entered text area
    enter_text_area.delete(1.0, 'end')

    # Start Counter for 1 minute
    work_sec = WORK_MIN * 60
    counter(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def counter(count):
    # Calculate remaining minutes
    count_mins = math.floor(count / 60)

    # Calculate remaining seconds
    count_secs = count % 60

    # If seconds is <= 9 then display with leading 0
    if count_secs <= 9:
        count_secs = f"0{count_secs}"

    # If minutes is <=9 then display with leading 0
    if count_mins <= 9:
        count_mins = f"0{count_mins}"

    # Display current timer count
    timer_count = f"{count_mins}:{count_secs}"
    timer_text.config(text=timer_count)

    # If count > 0 then decrease the count and invoke the counter function again
    if count > 0:
        global timer
        timer = window.after(1000, counter, count - 1)
    else:
        # Cancel the timer after one minute
        window.after_cancel(timer)

        # Enable Start Button
        button_start.config(state=tk.NORMAL)

        # Disable Reset Button
        button_reset.config(state=tk.DISABLED)

        # Disable Entered Text Area so that it cannot be modified after 1 minute
        enter_text_area.config(state=tk.DISABLED)

        # Validate the words in the input list against output list
        validate_entered_words()


def reset_timer():
    # Cancel the timer
    window.after_cancel(timer)

    # Enable Start Button
    button_start.config(state=tk.NORMAL)

    # Disable Reset Button
    button_reset.config(state=tk.DISABLED)

    # Clear the entered text area
    enter_text_area.delete(1.0, 'end')

    # Disable the entered text area
    enter_text_area.config(state=tk.DISABLED)

    # Clear the timer and Completion message
    clear_board()


def clear_board():
    # Clear the output text list
    output_text.clear()

    # Reset the timer text
    timer_text.config(text="00:00")

    # Clear the final message at the bottom
    words_entered.config(text=" ")


def validate_entered_words():
    global output_text
    # Get the entered words from text area
    data = enter_text_area.get("1.0", "end-1c")

    # Do basic edit
    output_text = data.replace("\n", " ")
    output_text = data.split(" ")
    try:
        output_text.remove("")
    except:
        pass
    else:
        pass

    # Calculate the length of output text list
    length_of_output = len(output_text)

    if length_of_output == 0:
        words_entered.config(text=f"No words typed per minute")
    else:
        words_entered.config(text=f"{length_of_output} Words typed per minute")
        if input_text[:length_of_output] == output_text:
            words_entered.config(text=f"{length_of_output} Words typed per minute with correct words")
        else:
            words_entered.config(text=f"{length_of_output} Words typed per minute with incorrect words")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("TypingSpeed App")
window.minsize(width=800, height=600)
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# Show app name
app_name = tk.Label(window, text="Typing Speed Test", font=('Arial', 20, 'italic'), fg=BROWN, bg=BACKGROUND_COLOR)
app_name.grid(column=0, row=0, columnspan=3, sticky='we')

# Create buttons
test_button = tk.Button(text="Show Words", height=1, width=24, bd=0, bg=BACKGROUND_COLOR, fg=GREEN, font=('Arial', 14, 'italic'), highlightthickness=0, command=display_words)
test_button.grid(column=0, row=1)

button_start = tk.Button(text="Start Test", height=1, width=24, bg=BACKGROUND_COLOR, fg=GREEN, bd=0, highlightthickness=0, font=('Arial', 14, 'italic'), command=start_timer, state=tk.DISABLED)
button_start.grid(column=1, row=1)

button_reset = tk.Button(text="Reset Timer", height=1, width=24, bg=BACKGROUND_COLOR, fg=GREEN, bd=0, highlightthickness=0, font=('Arial', 14, 'italic'), command=reset_timer, state=tk.DISABLED)
button_reset.grid(column=2, row=1)

# Show Text from text file
display_text_area = tk.Text(window, width=90, height=8, font=('Arial', 14, 'bold'), state=tk.DISABLED)
display_text_area.grid(column=0, row=2, columnspan=4)

# Show Timer
timer_text = tk.Label(window, text="00:00", font=('Arial', 14, 'bold'), fg=RED, bg=BACKGROUND_COLOR)
timer_text.grid(column=2, row=0, sticky='we')

# Show Text area for typing
enter_text_area_name = tk.Label(window, text="Type Here", font=('Arial', 15, 'italic'), fg=BROWN, bg=BACKGROUND_COLOR)
enter_text_area_name.grid(column=0, row=3, columnspan=3, sticky='we')

enter_text_area = tk.Text(window, width=90, height=8, font=('Arial', 14, 'bold'), state=tk.DISABLED)
enter_text_area.grid(column=0, row=4, columnspan=4)

# Show Number of words entered
words_entered = tk.Label(window, text="", font=('Arial', 15, 'italic'), fg=BROWN, bg=BACKGROUND_COLOR)
words_entered.grid(column=0, row=5, columnspan=3, sticky='we')


window.mainloop()