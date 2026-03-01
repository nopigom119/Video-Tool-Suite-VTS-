import customtkinter as ctk

class ScrollableTaskFrame(ctk.CTkScrollableFrame):
    def __init__(self, container, **kwargs):
        """
        Custom scrollable frame for task list using CustomTkinter.
        Inherits from CTkScrollableFrame for modern look and feel.
        """
        super().__init__(container, fg_color="#2E2E2E", label_text="", **kwargs)
        # Configure grid to allow children to expand
        self.grid_columnconfigure(0, weight=1)

    def clear(self):
        """Remove all task widgets from the frame."""
        for widget in self.winfo_children():
            widget.destroy()