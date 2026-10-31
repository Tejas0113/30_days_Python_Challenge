import math, datetime, tkinter as tk

class CrimsonClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloody Red Clock - Glowing White Accents")
        self.root.geometry("500x500")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=500, height=500, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.cx, self.cy, self.r = 250, 250, 200

        self.draw_face()
        self.update_clock()

    def draw_face(self):
        # Outer dark rim
        self.canvas.create_oval(self.cx - self.r - 8, self.cy - self.r - 8, self.cx + self.r + 8, self.cy + self.r + 8, fill="#1e1e24", outline="")
        # Solid Bloody Red inner face
        self.canvas.create_oval(self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r, fill="#8b0000", outline="")

        # 12 Hour Ticks (Glowing White)
        for h in range(12):
            ang = math.radians(h * 30 - 90)
            x1, y1 = self.cx + (self.r - 35) * math.cos(ang), self.cy + (self.r - 35) * math.sin(ang)
            x2, y2 = self.cx + (self.r - 5) * math.cos(ang), self.cy + (self.r - 5) * math.sin(ang)
            # Outer subtle glow line
            self.canvas.create_line(x1, y1, x2, y2, fill="#ffffff", width=4, capstyle=tk.ROUND)

    def update_clock(self):
        self.canvas.delete("hands")
        now = datetime.datetime.now()
        h, m, s = now.hour % 12, now.minute, now.second + now.microsecond / 1e6

        h_ang = math.radians((h + m / 60 + s / 3600) * 30 - 90)
        m_ang = math.radians((m + s / 60) * 6 - 90)
        s_ang = math.radians(s * 6 - 90)

        # Draw glowing white hands (Hour, Minute, Second)
        for ang, length, width, tail in [(h_ang, 105, 6, 20), (m_ang, 155, 4, 25), (s_ang, 165, 2, 35)]:
            x1, y1 = self.cx - tail * math.cos(ang), self.cy - tail * math.sin(ang)
            x2, y2 = self.cx + length * math.cos(ang), self.cy + length * math.sin(ang)
            self.canvas.create_line(x1, y1, x2, y2, fill="#ffffff", width=width, capstyle=tk.ROUND, tags="hands")

        # Glowing white center pin
        self.canvas.create_oval(self.cx - 6, self.cy - 6, self.cx + 6, self.cy + 6, fill="#ffffff", outline="", tags="hands")
        self.root.after(50, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    clock = CrimsonClock(root)
    root.mainloop()
