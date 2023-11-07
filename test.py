import customtkinter as ctk
import pynput

app = ctk.CTk()
test_button = ctk.CTkButton(master = app, command = lambda: print("Hello"))

def move_mouse(x, y):
    print(x, y)

def click_mouse(x, y, button, pressed):
    if pressed:
        if button == "left":
            print(f"press at {x}, {y}")
        else:
            print(f"bad press at {x}, {y}. \n Button: {str(button) == 'Button.left'}")
    else:
        print("no press")

# listener = pynput.mouse.Listener(move_mouse, click_mouse)
print(f"{app.winfo_screenheight()}x{app.winfo_screenwidth()}")
test_button.place(x = 10, y = 10)
# listener.start()
print("No block")
app.mainloop()
print("no block")