class MainMenu:

    def __init__(self, root):
        # Clear root window
        for widget in root.winfo_children():
            widget.destroy()
        
        root.title("Monopoly 1920")

