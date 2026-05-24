# ============================================================
# ui.py  —  GUI Utama
# Sistem Informasi Akademik Mahasiswa
# CustomTkinter — Tema Galaxy Andromeda (REDESIGN TOTAL)
# ============================================================

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import db
import math

# ============================================================
# TEMA - GALAXY ANDROMEDA (NEW PALETTE)
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

C = {
    # === GALAXY ANDROMEDA PALETTE ===
    # Background utama - Deep Space Gradient
    "bg_main":        "#07020f",      # Hitam angkasa terdalam
    "bg_secondary":   "#0d0a2e",      # Biru gelap nebula

    # Permukaan / Card
    "surface":        "#130d2e",      # Purple dark surface
    "surface_elevated": "#1a1245",    # Elevated surface

    # Aksen Primer & Sekunder
    "primary":        "#8b5cf6",      # Ungu galaksi - main accent
    "secondary":      "#4f8ef7",      # Biru bintang - secondary accent
    "highlight":      "#c4b5fd",      # Lavender terang - highlights

    # Teks
    "text_main":      "#e2d9f3",      # Teks utama - lavender white
    "text_muted":     "#a78bca",      # Teks sekunder - muted purple

    # Border & Divider
    "border_solid":   "#2d1f4e",      # Solid border for cards

    # Status Colors (adapted to galaxy theme)
    "success":        "#10b981",      # Emerald green
    "success_bg":     "#064e3b",
    "error":          "#ef4444",      # Red
    "error_bg":       "#7f1d1d",
    "warning":        "#f59e0b",      # Amber
    "warning_bg":     "#78350f",
    "info":           "#8b5cf6",      # Galaxy purple
    "info_bg":        "#3b0764",

    # Special Effects
    "glow_primary":   "#a78bfa",      # Glow effect for primary
    "glow_secondary": "#7dd3fc",      # Glow effect for secondary
    "star_white":     "#ffffff",      # Pure white for stars/highlights

    # Legacy aliases for backward compatibility
    "hijau_hutan":    "#130d2e",
    "hijau_daun":     "#1a1245",
    "hijau_aksen":    "#4f8ef7",
    "biru":           "#8b5cf6",
    "biru_muda":      "#0d0a2e",
    "biru_aksen":     "#c4b5fd",
    "abu_bg":         "#07020f",
    "abu_card":       "#130d2e",
    "abu_border":     "#2d1f4e",
    "teks":           "#e2d9f3",
    "teks_sub":       "#a78bca",
    "teks_input":     "#ffffff",
    "placeholder":    "#a78bca",
    "putih":          "#130d2e",
    "hitam_ungu":     "#07020f",
    "hijau":          "#10b981",
    "merah":          "#ef4444",
    "kuning":         "#f59e0b",
    "ungu":           "#8b5cf6",
}

F_JUDUL     = ("Segoe UI", 24, "bold")
F_SUBJUDUL  = ("Segoe UI", 15, "bold")
F_NORMAL    = ("Segoe UI", 12)
F_KECIL     = ("Segoe UI", 10)
F_MONO      = ("Consolas", 11)
F_TEBEL     = ("Segoe UI", 12, "bold")
F_LOGO      = ("Segoe UI", 28, "bold")

# ============================================================
# HELPER - NEW REDESIGN
# ============================================================

def _entry(parent, placeholder="", show="", width=280):
    """Input field dengan desain baru - rounded pill shape dengan glow effect"""
    return ctk.CTkEntry(
        parent, width=width, height=48,
        placeholder_text=placeholder,
        show=show,
        font=F_NORMAL,
        corner_radius=24,  # Pill shape - completely different from before
        border_width=2,
        border_color=C["primary"],
        fg_color=C["surface"],
        text_color=C["text_main"],
        placeholder_text_color=C["text_muted"],
    )


def _btn(parent, text, command, color=None, width=180, height=48, style="primary"):
    """
    Button dengan desain TOTAL BARU:
    - Pill shape (rounded penuh)
    - Ukuran lebih besar
    - Gradient-like hover effect
    - Border glow untuk primary buttons
    """
    color = color or C["primary"]

    if style == "primary":
        # Primary button dengan border glow
        btn = ctk.CTkButton(
            parent, text=text, command=command,
            width=width, height=height,
            font=("Segoe UI", 12, "bold"),
            fg_color=color,
            hover_color=C["glow_primary"],
            corner_radius=24,  # Full rounded - pill shape
            border_width=2,
            border_color=C["highlight"],
        )
    elif style == "secondary":
        # Secondary button dengan outline style
        btn = ctk.CTkButton(
            parent, text=text, command=command,
            width=width, height=height,
            font=("Segoe UI", 12, "bold"),
            fg_color="transparent",
            hover_color=C["surface_elevated"],
            corner_radius=24,
            border_width=2,
            border_color=C["secondary"],
            text_color=C["secondary"],
        )
    else:
        # Default style
        btn = ctk.CTkButton(
            parent, text=text, command=command,
            width=width, height=height,
            font=("Segoe UI", 12, "bold"),
            fg_color=color,
            hover_color=_gelap(color),
            corner_radius=24,
        )

    return btn


def _gelap(hex_color: str) -> str:
    try:
        r = max(0, int(hex_color[1:3], 16) - 25)
        g = max(0, int(hex_color[3:5], 16) - 25)
        b = max(0, int(hex_color[5:7], 16) - 25)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _terang(hex_color: str) -> str:
    """Membuat warna lebih terang untuk hover effect"""
    try:
        r = min(255, int(hex_color[1:3], 16) + 30)
        g = min(255, int(hex_color[3:5], 16) + 30)
        b = min(255, int(hex_color[5:7], 16) + 30)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _bind_enter_chain(entries: list):
    for i, e in enumerate(entries):
        if i < len(entries) - 1:
            nxt = entries[i + 1]
            e.bind("<Return>", lambda ev, n=nxt: n.focus_set())


def _label(parent, text, font=None, color=None, bg=None, anchor="w"):
    return ctk.CTkLabel(
        parent, text=text,
        font=font or F_NORMAL,
        text_color=color or C["text_main"],
        anchor=anchor,
    )


# ============================================================
# TREEVIEW STYLE - REDESIGN
# ============================================================

def _style_tree():
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("App.Treeview",
        background=C["surface"],
        foreground=C["text_main"],
        fieldbackground=C["surface"],
        rowheight=48,  # Taller rows for better readability
        font=("Segoe UI", 12),
        borderwidth=0,
    )
    s.configure("App.Treeview.Heading",
        background=C["primary"],
        foreground="#e2d9f3",
        font=("Segoe UI", 12, "bold"),
        borderwidth=0,
        relief="flat",
        padding=(0, 12),
    )
    s.map("App.Treeview",
        background=[("selected", C["secondary"])],
        foreground=[("selected", "#e2d9f3")]
    )


# ============================================================
# GRAFIK CANVAS — helper fungsi untuk menggambar chart
# ============================================================

class Chart:
    """
    Kumpulan fungsi statis untuk menggambar chart di Canvas tkinter.
    Tidak perlu matplotlib — murni Canvas drawing.
    """

    @staticmethod
    def bar(canvas, data: list[tuple], colors: list[str] = None,
            title: str = "", x_label: str = "", y_label: str = ""):
        """
        Bar chart horizontal.
        data: [(label, value), ...]
        """
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        if not data:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["teks_sub"], font=F_KECIL)
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 70, 24, 36, 48
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        max_val = max(v for _, v in data) or 1
        n = len(data)
        gap = 6
        bar_h = max(10, (chart_h - gap * (n + 1)) // n)

        default_colors = [C["biru"], C["hijau"], C["kuning"], C["merah"],
                          C["ungu"], C["biru_aksen"]] * 10
        colors = colors or default_colors

        # Title
        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI", 9, "bold"),
                               fill=C["teks"], anchor="center")

        # Grid lines vertikal
        grid_steps = 5
        for i in range(grid_steps + 1):
            gx = PAD_L + int(chart_w * i / grid_steps)
            gy1, gy2 = PAD_T, PAD_T + chart_h
            canvas.create_line(gx, gy1, gx, gy2,
                               fill="#4a3f5c", width=1, dash=(3, 3))
            val_label = int(max_val * i / grid_steps)
            canvas.create_text(gx, PAD_T + chart_h + 10,
                               text=str(val_label),
                               font=("Segoe UI", 7), fill=C["teks_sub"])

        # Bar-bar
        for i, ((label, val), color) in enumerate(zip(data, colors)):
            y1 = PAD_T + gap + i * (bar_h + gap)
            y2 = y1 + bar_h
            bar_len = int(chart_w * val / max_val)

            # Background track
            canvas.create_rectangle(PAD_L, y1, PAD_L + chart_w, y2,
                                    fill="#2a1f3d", outline="")
            # Bar
            if bar_len > 0:
                canvas.create_rectangle(PAD_L, y1, PAD_L + bar_len, y2,
                                        fill=color, outline="")
                # Rounded cap (simulasi)
                canvas.create_oval(PAD_L + bar_len - 4, y1,
                                   PAD_L + bar_len + 4, y2,
                                   fill=color, outline="")

            # Label kiri
            canvas.create_text(PAD_L - 6, (y1 + y2) // 2,
                               text=label, font=("Segoe UI", 8),
                               fill=C["teks"], anchor="e")

            # Nilai di ujung bar
            if val > 0:
                canvas.create_text(PAD_L + bar_len + 8, (y1 + y2) // 2,
                                   text=str(val), font=("Segoe UI", 8, "bold"),
                                   fill=color, anchor="w")

    @staticmethod
    def column(canvas, data: list[tuple], colors: list[str] = None,
               title: str = ""):
        """
        Column chart (bar vertikal).
        data: [(label, value), ...]
        """
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        if not data:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["teks_sub"], font=F_KECIL)
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 40, 16, 36, 48
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        max_val = max(v for _, v in data) or 1
        n = len(data)
        gap = 8
        bar_w = max(12, (chart_w - gap * (n + 1)) // n)

        default_colors = [C["biru"], C["hijau"], C["kuning"], C["merah"],
                          C["ungu"], C["biru_aksen"]] * 10
        colors = colors or default_colors

        # Title
        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI", 9, "bold"),
                               fill=C["teks"], anchor="center")

        # Grid lines horizontal
        grid_steps = 4
        for i in range(grid_steps + 1):
            gy = PAD_T + chart_h - int(chart_h * i / grid_steps)
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                               fill="#4a3f5c", width=1, dash=(3, 3))
            val_label = int(max_val * i / grid_steps)
            canvas.create_text(PAD_L - 6, gy,
                               text=str(val_label),
                               font=("Segoe UI", 7), fill=C["teks_sub"],
                               anchor="e")

        # Sumbu X
        canvas.create_line(PAD_L, PAD_T + chart_h,
                           PAD_L + chart_w, PAD_T + chart_h,
                           fill=C["abu_border"], width=1)

        for i, ((label, val), color) in enumerate(zip(data, colors)):
            x1 = PAD_L + gap + i * (bar_w + gap)
            x2 = x1 + bar_w
            bar_h_px = int(chart_h * val / max_val)
            y1 = PAD_T + chart_h - bar_h_px
            y2 = PAD_T + chart_h

            # Bar
            if bar_h_px > 0:
                canvas.create_rectangle(x1, y1, x2, y2,
                                        fill=color, outline="")

            # Label bawah
            canvas.create_text((x1 + x2) // 2, PAD_T + chart_h + 12,
                               text=label, font=("Segoe UI", 8),
                               fill=C["teks"], anchor="n")

            # Nilai di atas bar
            if val > 0:
                canvas.create_text((x1 + x2) // 2, y1 - 8,
                                   text=str(val),
                                   font=("Segoe UI", 8, "bold"),
                                   fill=color, anchor="s")

    @staticmethod
    def pie(canvas, data: list[tuple], colors: list[str] = None,
            title: str = ""):
        """
        Pie chart.
        data: [(label, value), ...]
        """
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        total = sum(v for _, v in data if v > 0)
        if total == 0:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["teks_sub"], font=F_KECIL)
            return

        default_colors = [C["biru"], C["hijau"], C["kuning"],
                          C["merah"], C["ungu"], C["biru_aksen"]] * 10
        colors = colors or default_colors

        cx = W * 0.38
        cy = H // 2
        r  = min(cx - 20, H // 2 - 30)

        if title:
            canvas.create_text(W // 2, 14, text=title,
                               font=("Segoe UI", 9, "bold"),
                               fill=C["teks"], anchor="center")

        start = 0.0
        slices = [(label, val, color)
                  for (label, val), color in zip(data, colors)
                  if val > 0]

        for label, val, color in slices:
            extent = (val / total) * 360
            canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                              start=start, extent=extent,
                              fill=color, outline=C["putih"], width=2)
            start += extent

        # Legend kanan
        lx = cx * 2 + 16
        ly = H // 2 - len(slices) * 18
        for label, val, color in slices:
            pct = val / total * 100
            canvas.create_rectangle(lx, ly, lx + 12, ly + 12,
                                    fill=color, outline="")
            canvas.create_text(lx + 18, ly + 6,
                               text=f"{label}  {val} ({pct:.1f}%)",
                               font=("Segoe UI", 8), fill=C["teks"],
                               anchor="w")
            ly += 22

    @staticmethod
    def line(canvas, datasets: list[tuple], labels: list[str],
             title: str = ""):
        """
        Line chart multi-series.
        datasets: [(series_label, color, [values]), ...]
        labels: label sumbu X
        """
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        all_vals = [v for _, _, vals in datasets for v in vals]
        if not all_vals:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["teks_sub"], font=F_KECIL)
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 50, 20, 36, 48
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        max_val = max(all_vals) or 1
        min_val = 0
        n = len(labels)

        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI", 9, "bold"),
                               fill=C["teks"], anchor="center")

        # Grid
        grid_steps = 4
        for i in range(grid_steps + 1):
            gy = PAD_T + chart_h - int(chart_h * i / grid_steps)
            gval = min_val + (max_val - min_val) * i / grid_steps
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                               fill="#4a3f5c", width=1, dash=(3, 3))
            canvas.create_text(PAD_L - 6, gy,
                               text=f"{gval:.2f}",
                               font=("Segoe UI", 7), fill=C["teks_sub"],
                               anchor="e")

        # X labels
        if n > 1:
            for i, lbl in enumerate(labels):
                gx = PAD_L + int(chart_w * i / (n - 1))
                canvas.create_text(gx, PAD_T + chart_h + 12,
                                   text=lbl, font=("Segoe UI", 8),
                                   fill=C["teks_sub"])

        # Lines & dots
        for s_label, color, vals in datasets:
            if len(vals) < 2:
                continue
            points = []
            for i, v in enumerate(vals):
                gx = PAD_L + int(chart_w * i / (n - 1))
                gy = PAD_T + chart_h - int(chart_h * (v - min_val) / (max_val - min_val))
                points.append((gx, gy))

            # Line
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                canvas.create_line(x1, y1, x2, y2, fill=color, width=2, smooth=True)

            # Dots
            for gx, gy in points:
                canvas.create_oval(gx - 4, gy - 4, gx + 4, gy + 4,
                                   fill=color, outline=C["putih"], width=2)

        # Legend
        lx = PAD_L + chart_w - 10
        ly = PAD_T + 6
        for s_label, color, _ in datasets:
            canvas.create_rectangle(lx - 90, ly, lx - 78, ly + 8,
                                    fill=color, outline="")
            canvas.create_text(lx - 72, ly + 4,
                               text=s_label, font=("Segoe UI", 8),
                               fill=C["teks"], anchor="w")
            ly += 16


# ============================================================
# KOMPONEN SIDEBAR - REDESIGN TOTAL
# ============================================================

class Sidebar(ctk.CTkFrame):

    MENU = [
        ("Dashboard",       "dashboard"),
        ("Data Mahasiswa",  "mahasiswa"),
        ("Input Nilai",     "nilai"),
        ("Statistik",       "statistik"),
        ("Riwayat",         "riwayat"),
    ]

    def __init__(self, parent, on_navigate):
        super().__init__(parent,
            width=260,  # Lebih lebar untuk desain baru
            corner_radius=0,
            fg_color=C["surface"],  # Surface color untuk sidebar
        )
        self.pack_propagate(False)
        self._nav = on_navigate
        self._btns = {}
        self._aktif = None
        self._build()

    def _build(self):
        # === HEADER DENGAN GRADIENT EFFECT ===
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=24, pady=(32, 24))

        # Logo dengan font lebih besar dan accent
        logo_label = ctk.CTkLabel(header_frame,
            text="✦ Andromeda",
            font=F_LOGO,
            text_color=C["highlight"],
        )
        logo_label.pack(anchor="w")

        # Subtitle dengan style baru
        subtitle_label = ctk.CTkLabel(header_frame,
            text="Sistem Informasi Akademik\nMahasiswa",
            font=("Segoe UI", 10),
            text_color=C["text_muted"],
            wraplength=200,
            justify="left"
        )
        subtitle_label.pack(anchor="w", pady=(8, 0))

        # === DIVIDER DENGAN ACCENT LINE ===
        divider = ctk.CTkFrame(self, height=2, fg_color=C["primary"])
        divider.pack(fill="x", padx=24, pady=(16, 20))

        # === MENU NAVIGATION ===
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(fill="x", padx=16, pady=8)

        for label, key in self.MENU:
            b = ctk.CTkButton(
                menu_frame,
                text=label,
                anchor="w",
                width=228,
                height=50,  # Lebih tinggi untuk touch-friendly
                font=("Segoe UI", 13),
                fg_color="transparent",
                hover_color=C["surface_elevated"],
                text_color=C["text_muted"],
                corner_radius=12,  # Rounded corners untuk setiap item
                border_width=0,
                command=lambda k=key: self._klik(k),
            )
            b.pack(fill="x", pady=3)
            self._btns[key] = b

        # === LOGOUT BUTTON DI BAWAH ===
        logout_frame = ctk.CTkFrame(self, fg_color="transparent")
        logout_frame.pack(side="bottom", fill="x", padx=16, pady=24)

        ctk.CTkButton(
            logout_frame,
            text="⏻ Logout",
            anchor="center",
            width=228,
            height=46,
            font=("Segoe UI", 12, "bold"),
            fg_color=C["error_bg"],
            hover_color=C["error"],
            text_color=C["error"],
            corner_radius=12,
            border_width=2,
            border_color=C["error"],
            command=lambda: self._nav("logout"),
        ).pack()

    def _klik(self, key: str):
        # Reset semua tombol ke state tidak aktif
        for k, b in self._btns.items():
            b.configure(
                fg_color="transparent",
                text_color=C["text_muted"],
                font=("Segoe UI", 13)
            )

        # Set tombol aktif dengan style berbeda
        if key in self._btns:
            self._btns[key].configure(
                fg_color=C["primary"],
                text_color=C["star_white"],
                font=("Segoe UI", 13, "bold"),
            )
        self._aktif = key
        self._nav(key)

    def aktifkan(self, key: str):
        self._klik(key)


# ============================================================
# HALAMAN DASAR - REDESIGN
# ============================================================

class HalamanBase(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=C["bg_main"])

    def _header(self, judul: str, subjudul: str = ""):
        """Header dengan desain baru - floating style dengan gradient accent"""
        hdr = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0, height=90)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        # Content container dengan padding lebih besar
        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.pack(side="left", padx=40, pady=20)

        # Judul dengan font lebih besar dan warna highlight
        ctk.CTkLabel(inner, text=judul, font=F_JUDUL, text_color=C["highlight"]).pack(anchor="w")

        if subjudul:
            ctk.CTkLabel(inner, text=subjudul, font=F_NORMAL, text_color=C["text_muted"]).pack(anchor="w", pady=(4, 0))

        # Divider dengan gradient effect (solid primary color line)
        divider = ctk.CTkFrame(self, height=3, fg_color=C["primary"])
        divider.pack(fill="x")

    def _card(self, parent, **kw):
        """Card dengan desain baru - elevated surface dengan rounded corners"""
        return ctk.CTkFrame(parent,
            fg_color=C["surface"],
            corner_radius=16,  # Lebih rounded untuk look yang modern
            border_width=1,
            border_color=C["border_solid"],
            **kw
        )


# ============================================================
# HALAMAN DASHBOARD - REDESIGN
# ============================================================

class HalamanDashboard(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Dashboard", "Selamat datang di Andromeda")
        self._build()

    def _build(self):
        # === ROW 1: STATS CARDS DENGAN LAYOUT BARU ===
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=40, pady=(30, 15))

        self._cards = {}
        specs = [
            ("total",       "Total Mahasiswa",  C["secondary"],   "orang terdaftar"),
            ("sudah_nilai", "Sudah Input Nilai", C["success"],  "mahasiswa"),
            ("rata_ipk",    "Rata-rata IPK",     C["warning"], "dari 4.00"),
            ("belum_nilai", "Belum Input Nilai", C["error"],  "mahasiswa"),
        ]
        for col, (key, label, warna, satuan) in enumerate(specs):
            card = self._card(row1, height=150)
            card.grid(row=0, column=col, padx=10, sticky="nsew")
            card.grid_propagate(False)
            row1.columnconfigure(col, weight=1)

            # Accent bar di kiri card dengan warna dinamis
            ctk.CTkFrame(card, width=6, fg_color=warna, corner_radius=8
                ).place(x=0, y=0, relheight=1)

            # Label dengan font lebih kecil dan muted
            ctk.CTkLabel(card, text=label.upper(),
                font=("Segoe UI", 9, "bold"), text_color=C["text_muted"]
            ).place(x=26, y=18)

            # Value dengan font besar dan warna accent
            val_lbl = ctk.CTkLabel(card, text="0",
                font=("Segoe UI", 36, "bold"), text_color=warna)
            val_lbl.place(x=26, y=45)

            # Unit text
            ctk.CTkLabel(card, text=satuan,
                font=("Segoe UI", 9), text_color=C["text_muted"]
            ).place(x=28, y=110)

            self._cards[key] = val_lbl

        # === ROW 2: INFO PANELS ===
        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(fill="x", padx=40, pady=(0, 15))
        row2.columnconfigure(0, weight=2)
        row2.columnconfigure(1, weight=3)

        info_card = self._card(row2, height=160)
        info_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        info_card.grid_propagate(False)

        # Header section
        ctk.CTkLabel(info_card, text="✦ MAHASISWA TERBAIK",
            font=("Segoe UI", 10, "bold"), text_color=C["highlight"]
        ).place(x=24, y=20)

        self._lbl_best = ctk.CTkLabel(info_card, text="Belum ada data",
            font=("Segoe UI", 14, "bold"), text_color=C["secondary"],
            wraplength=200, justify="left")
        self._lbl_best.place(x=24, y=48)

        self._lbl_best_ipk = ctk.CTkLabel(info_card, text="",
            font=("Segoe UI", 11), text_color=C["text_muted"])
        self._lbl_best_ipk.place(x=24, y=90)

        # Divider vertical
        ctk.CTkFrame(info_card, width=2, fg_color=C["border_solid"]
            ).place(relx=0.55, y=15, relheight=0.8)

        # IPK section
        ctk.CTkLabel(info_card, text="IPK TERTINGGI",
            font=("Segoe UI", 9, "bold"), text_color=C["text_muted"]
        ).place(relx=0.58, y=20)
        self._lbl_ipk_max = ctk.CTkLabel(info_card, text="0.00",
            font=("Segoe UI", 24, "bold"), text_color=C["success"])
        self._lbl_ipk_max.place(relx=0.58, y=48)

        ctk.CTkLabel(info_card, text="IPK TERENDAH",
            font=("Segoe UI", 8), text_color=C["teks_sub"]
        ).place(relx=0.59, y=66)
        self._lbl_ipk_min = ctk.CTkLabel(info_card, text="0.00",
            font=("Segoe UI", 20, "bold"), text_color=C["merah"])
        self._lbl_ipk_min.place(relx=0.59, y=84)

        dist_card = self._card(row2, height=110)
        dist_card.grid(row=0, column=1, padx=(6, 0), sticky="nsew")
        dist_card.grid_propagate(False)

        ctk.CTkLabel(dist_card, text="DISTRIBUSI PREDIKAT",
            font=("Segoe UI", 8, "bold"), text_color=C["teks_sub"]
        ).place(x=18, y=14)

        self._dist_labels = {}
        predikat_specs = [
            ("Cumlaude",        "#7C3AED"),
            ("Sangat Baik",     C["hijau"]),
            ("Baik",            C["biru"]),
            ("Cukup",           C["kuning"]),
            ("Perlu Perbaikan", C["merah"]),
        ]
        for idx, (nama, warna) in enumerate(predikat_specs):
            ctk.CTkLabel(dist_card, text=nama,
                font=("Segoe UI", 8), text_color=C["teks_sub"]
            ).place(x=18 + idx * 145, y=36)
            lbl_val = ctk.CTkLabel(dist_card, text="0",
                font=("Segoe UI", 24, "bold"), text_color=warna)
            lbl_val.place(x=18 + idx * 145, y=58)
            self._dist_labels[nama] = lbl_val

        riwayat_card = self._card(self)
        riwayat_card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        hdr_row = ctk.CTkFrame(riwayat_card, fg_color="transparent")
        hdr_row.pack(fill="x", padx=20, pady=(14, 0))
        ctk.CTkLabel(hdr_row, text="Aktivitas Terbaru",
            font=F_SUBJUDUL, text_color=C["teks"]).pack(side="left")
        ctk.CTkLabel(hdr_row, text="10 operasi terakhir",
            font=F_KECIL, text_color=C["teks_sub"]).pack(side="right")

        col_hdr = ctk.CTkFrame(riwayat_card, fg_color=C["abu_card"], height=28)
        col_hdr.pack(fill="x", padx=20, pady=(8, 0))
        col_hdr.pack_propagate(False)
        for txt, w in [("Waktu", 150), ("Aksi", 80), ("Detail", 0)]:
            ctk.CTkLabel(col_hdr, text=txt, width=w,
                font=("Segoe UI", 9, "bold"), text_color=C["teks_sub"],
                anchor="w").pack(side="left", padx=(10, 0))

        self._riwayat_frame = ctk.CTkScrollableFrame(
            riwayat_card, fg_color="transparent")
        self._riwayat_frame.pack(fill="both", expand=True, padx=20, pady=(4, 14))

        self.refresh()

    def refresh(self):
        stat  = db.statistik()
        semua = db.get_semua()

        total = stat["total"]
        sudah = stat["sudah_nilai"]

        self._cards["total"].configure(text=str(total))
        self._cards["sudah_nilai"].configure(text=str(sudah))
        self._cards["rata_ipk"].configure(text=str(stat["rata_ipk"]))
        self._cards["belum_nilai"].configure(text=str(total - sudah))

        if stat["terbaik"] != "-":
            self._lbl_best.configure(text=stat["terbaik"])
            self._lbl_best_ipk.configure(text=f"IPK {stat['terbaik_ipk']:.2f}")
        else:
            self._lbl_best.configure(text="belum ada data")
            self._lbl_best_ipk.configure(text="")

        ipk_vals = [db.ipk_mahasiswa(m) for m in semua if m["semester"]]
        if ipk_vals:
            self._lbl_ipk_max.configure(text=f"{max(ipk_vals):.2f}")
            self._lbl_ipk_min.configure(text=f"{min(ipk_vals):.2f}")
        else:
            self._lbl_ipk_max.configure(text="0.00")
            self._lbl_ipk_min.configure(text="0.00")

        dist = {"Cumlaude": 0, "Sangat Baik": 0, "Baik": 0,
                "Cukup": 0, "Perlu Perbaikan": 0}
        for m in semua:
            if m["semester"]:
                p = db.predikat(db.ipk_mahasiswa(m))
                if p in dist:
                    dist[p] += 1
        for nama, lbl in self._dist_labels.items():
            lbl.configure(text=str(dist.get(nama, 0)))

        aksi_warna = {
            "TAMBAH": C["hijau"], "HAPUS": C["merah"],
            "NILAI":  C["biru"],  "EDIT":  C["kuning"],
        }
        for w in self._riwayat_frame.winfo_children():
            w.destroy()
        for h in db.get_riwayat()[:10]:
            row = ctk.CTkFrame(self._riwayat_frame, fg_color="transparent", height=30)
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)
            warna_aksi = aksi_warna.get(h["aksi"], C["teks_sub"])
            ctk.CTkLabel(row, text=h["waktu"], width=150,
                font=F_KECIL, text_color=C["teks_sub"], anchor="w"
            ).pack(side="left", padx=(4, 0))
            ctk.CTkLabel(row, text=h["aksi"], width=72,
                font=("Segoe UI", 9, "bold"),
                text_color=warna_aksi, anchor="w"
            ).pack(side="left")
            ctk.CTkLabel(row, text=h["detail"],
                font=F_KECIL, text_color=C["teks"], anchor="w"
            ).pack(side="left", padx=(4, 0))


# ============================================================
# HALAMAN DATA MAHASISWA
# ============================================================

class HalamanMahasiswa(HalamanBase):

    def __init__(self, parent, on_nilai):
        super().__init__(parent)
        self._on_nilai = on_nilai
        self._header("Data Mahasiswa", "Kelola data mahasiswa terdaftar")
        _style_tree()
        self._build()
        self.refresh()

    def _build(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=28, pady=14)

        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self.refresh())
        search = ctk.CTkEntry(
            toolbar, width=260, height=38,
            placeholder_text="Cari NIM atau nama...",
            textvariable=self._search_var,
            font=F_NORMAL,
            corner_radius=8,
        )
        search.pack(side="left")

        _btn(toolbar, "+ Tambah", self._form_tambah, width=130).pack(side="right", padx=(6, 0))
        _btn(toolbar, "Edit Nama", self._form_edit, color=C["kuning"], width=110).pack(side="right", padx=6)
        _btn(toolbar, "Input Nilai", self._ke_nilai, color=C["hijau"], width=110).pack(side="right", padx=6)
        _btn(toolbar, "Hapus", self._hapus, color=C["merah"], width=90).pack(side="right")

        tbl_frame = ctk.CTkFrame(self, fg_color=C["putih"],
            corner_radius=12, border_width=1, border_color=C["abu_border"])
        tbl_frame.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        cols = ("nim", "nama", "semester_terisi", "ipk", "total_sks", "predikat")
        self._tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
            style="App.Treeview", selectmode="browse")

        hdrs = {
            "nim":             ("NIM",             140),
            "nama":            ("Nama Lengkap",    260),
            "semester_terisi": ("Semester Terisi", 160),
            "ipk":             ("IPK",              90),
            "total_sks":       ("Total SKS",       110),
            "predikat":        ("Predikat",        160),
        }
        for col, (head, w) in hdrs.items():
            self._tree.heading(col, text=head, anchor="center")
            anc = "center" if col not in ("nama",) else "w"
            self._tree.column(col, width=w, anchor=anc, minwidth=80)

        vsb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)
        vsb.pack(side="right", fill="y")

        self._tree.tag_configure("cumlaude",  foreground="#7C3AED")
        self._tree.tag_configure("sangat",    foreground=C["hijau"])
        self._tree.tag_configure("baik",      foreground=C["biru"])
        self._tree.tag_configure("cukup",     foreground=C["kuning"])
        self._tree.tag_configure("perlu",     foreground=C["merah"])

        self._tree.bind("<Double-1>", lambda e: self._detail())

        self._sbar = ctk.CTkLabel(self, text="", font=F_KECIL, text_color=C["teks_sub"])
        self._sbar.pack(anchor="w", padx=28, pady=(0, 8))

    def refresh(self):
        for i in self._tree.get_children():
            self._tree.delete(i)

        keyword = self._search_var.get()
        rows = db.cari(keyword) if keyword else db.get_semua()

        tag_map = {
            "Cumlaude":        "cumlaude",
            "Sangat Baik":     "sangat",
            "Baik":            "baik",
            "Cukup":           "cukup",
            "Perlu Perbaikan": "perlu",
        }

        for m in rows:
            ipk  = db.ipk_mahasiswa(m)
            pred = db.predikat(ipk)
            self._tree.insert("", "end", iid=m["nim"], values=(
                m["nim"],
                m["nama"],
                db.semester_terisi(m),
                f"{ipk:.2f}",
                db.total_sks(m),
                pred,
            ), tags=(tag_map.get(pred, ""),))

        self._sbar.configure(
            text=f"Menampilkan {len(rows)} dari {db.statistik()['total']} mahasiswa")

    def _selected_nim(self) -> str | None:
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Perhatian", "Pilih mahasiswa terlebih dahulu.")
            return None
        return sel[0]

    def _form_tambah(self):
        win = ctk.CTkToplevel(self)
        win.title("Tambah Mahasiswa")
        win.geometry("420x300")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text="Tambah Mahasiswa Baru",
            font=F_SUBJUDUL).pack(pady=(24, 16))

        e_nim  = _entry(win, placeholder="NIM (angka)")
        e_nim.pack(pady=6)
        e_nama = _entry(win, placeholder="Nama lengkap")
        e_nama.pack(pady=6)

        _bind_enter_chain([e_nim, e_nama])

        def simpan(*_):
            try:
                db.tambah_mahasiswa(e_nim.get(), e_nama.get())
                self.refresh()
                win.destroy()
                messagebox.showinfo("Berhasil", "Mahasiswa berhasil ditambahkan.")
            except ValueError as err:
                messagebox.showerror("Gagal", str(err))

        e_nama.bind("<Return>", simpan)
        _btn(win, "Simpan", simpan, width=280).pack(pady=18)
        e_nim.focus_set()

    def _form_edit(self):
        nim = self._selected_nim()
        if not nim: return
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return

        win = ctk.CTkToplevel(self)
        win.title("Edit Nama")
        win.geometry("420x240")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text=f"Edit Nama  —  NIM {nim}",
            font=F_SUBJUDUL).pack(pady=(24, 16))

        e_nama = _entry(win, placeholder="Nama baru")
        e_nama.insert(0, mhs["nama"])
        e_nama.pack(pady=6)

        def simpan(*_):
            try:
                db.edit_mahasiswa(nim, e_nama.get())
                self.refresh()
                win.destroy()
            except ValueError as err:
                messagebox.showerror("Gagal", str(err))

        e_nama.bind("<Return>", simpan)
        _btn(win, "Simpan", simpan, width=280).pack(pady=18)
        e_nama.focus_set()

    def _hapus(self):
        nim = self._selected_nim()
        if not nim: return
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return
        if messagebox.askyesno("Konfirmasi",
                f"Hapus {mhs['nama']} ({nim})?\n\nSemua data nilai ikut terhapus."):
            try:
                db.hapus_mahasiswa(nim)
                self.refresh()
            except ValueError as err:
                messagebox.showerror("Gagal", str(err))

    def _ke_nilai(self):
        nim = self._selected_nim()
        if nim:
            self._on_nilai(nim)

    def _detail(self):
        nim = self._selected_nim()
        if not nim: return
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return

        win = ctk.CTkToplevel(self)
        win.title(f"Detail — {mhs['nama']}")
        win.geometry("520x560")
        win.grab_set()

        ipk  = db.ipk_mahasiswa(mhs)
        pred = db.predikat(ipk)

        ctk.CTkLabel(win, text=mhs["nama"], font=F_JUDUL).pack(padx=24, pady=(20, 2), anchor="w")
        ctk.CTkLabel(win, text=f"NIM {mhs['nim']}", font=F_KECIL,
            text_color=C["teks_sub"]).pack(padx=24, anchor="w")

        badge = ctk.CTkFrame(win, fg_color=C["biru_muda"], corner_radius=10)
        badge.pack(fill="x", padx=24, pady=14)
        ctk.CTkLabel(badge, text=f"{ipk:.2f}",
            font=("Segoe UI", 36, "bold"), text_color=C["biru"]).pack(side="left", padx=20, pady=14)
        info = ctk.CTkFrame(badge, fg_color="transparent")
        info.pack(side="left", pady=14)
        ctk.CTkLabel(info, text=pred, font=("Segoe UI", 13, "bold"),
            text_color=C["biru"]).pack(anchor="w")
        ctk.CTkLabel(info, text=f"{db.total_sks(mhs)} SKS  |  Semester terisi: {db.semester_terisi(mhs)}",
            font=F_KECIL, text_color=C["teks_sub"]).pack(anchor="w")

        ctk.CTkLabel(win, text="Rincian Semester",
            font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=24, pady=(4, 6), anchor="w")

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        for smt_key in sorted(mhs["semester"].keys(), key=int):
            data = mhs["semester"][smt_key]
            ips  = db.hitung_ips(data)

            smt_hdr = ctk.CTkFrame(scroll, fg_color=C["abu_card"], corner_radius=8)
            smt_hdr.pack(fill="x", pady=(8, 2))
            ctk.CTkLabel(smt_hdr, text=f"Semester {smt_key}",
                font=("Segoe UI", 11, "bold"), text_color=C["biru"]).pack(side="left", padx=14, pady=8)
            ctk.CTkLabel(smt_hdr, text=f"IPS: {ips:.2f}",
                font=("Segoe UI", 11, "bold"), text_color=C["hijau"]).pack(side="right", padx=14)

            for mk in data:
                row = ctk.CTkFrame(scroll, fg_color=C["putih"],
                    border_width=1, border_color=C["abu_border"], corner_radius=6)
                row.pack(fill="x", pady=1)
                ctk.CTkLabel(row, text=mk["nama"], font=F_NORMAL,
                    text_color=C["teks"]).pack(side="left", padx=14, pady=6)
                ctk.CTkLabel(row, text=f"SKS {mk['sks']}",
                    font=F_KECIL, text_color=C["teks_sub"]).pack(side="right", padx=8)
                ctk.CTkLabel(row, text=f"{mk['nilai']:.0f}  /  {mk['grade']}",
                    font=("Segoe UI", 10, "bold"), text_color=C["biru"]).pack(side="right", padx=10)


# ============================================================
# HALAMAN INPUT NILAI
# ============================================================

class HalamanNilai(HalamanBase):

    def __init__(self, parent, on_selesai):
        super().__init__(parent)
        self._on_selesai = on_selesai
        self._nim_aktif  = None
        self._entries    = []
        self._header("Input Nilai", "Pilih mahasiswa dan semester, lalu isi nilai")
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color=C["putih"],
            corner_radius=12, border_width=1, border_color=C["abu_border"])
        top.pack(fill="x", padx=28, pady=16)

        row1 = ctk.CTkFrame(top, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=14)

        ctk.CTkLabel(row1, text="Mahasiswa", font=F_KECIL,
            text_color=C["teks_sub"]).grid(row=0, column=0, sticky="w")
        self._search = ctk.CTkEntry(row1, width=260, height=38,
            placeholder_text="Ketik NIM atau nama...", font=F_NORMAL, corner_radius=8)
        self._search.grid(row=1, column=0, padx=(0, 16))
        self._search.bind("<KeyRelease>", self._update_dropdown)

        self._dd_var  = tk.StringVar()
        self._dd_data = {}
        self._combo   = ttk.Combobox(row1, textvariable=self._dd_var,
            state="readonly", width=30, font=("Segoe UI", 10))
        self._combo.grid(row=1, column=1, padx=(0, 16))
        self._combo.bind("<<ComboboxSelected>>", self._pilih_mahasiswa)

        ctk.CTkLabel(row1, text="Semester", font=F_KECIL,
            text_color=C["teks_sub"]).grid(row=0, column=2, sticky="w")
        self._smt_var = tk.StringVar(value="1")
        smt_cb = ttk.Combobox(row1, textvariable=self._smt_var,
            values=["1", "2", "3", "4", "5", "6"],
            state="readonly", width=8, font=("Segoe UI", 10))
        smt_cb.grid(row=1, column=2)
        smt_cb.bind("<<ComboboxSelected>>", self._load_form)

        row1.columnconfigure((0, 1, 2), pad=8)

        self._lbl_info = ctk.CTkLabel(top, text="",
            font=F_KECIL, text_color=C["teks_sub"])
        self._lbl_info.pack(anchor="w", padx=20, pady=(0, 10))

        self._form_card = ctk.CTkFrame(self, fg_color=C["putih"],
            corner_radius=12, border_width=1, border_color=C["abu_border"])
        self._form_card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        self._placeholder()
        self._update_dropdown()

    def _placeholder(self):
        for w in self._form_card.winfo_children():
            w.destroy()
        ctk.CTkLabel(self._form_card,
            text="Pilih mahasiswa dan semester untuk mulai input nilai.",
            font=F_NORMAL, text_color=C["teks_sub"]
        ).pack(expand=True)

    def _update_dropdown(self, event=None):
        keyword = self._search.get()
        rows = db.cari(keyword) if keyword else db.get_semua()
        opts = [f"{m['nim']}  —  {m['nama']}" for m in rows]
        nims = {f"{m['nim']}  —  {m['nama']}": m["nim"] for m in rows}
        self._dd_data = nims
        self._combo["values"] = opts
        if opts and not self._combo.get():
            self._combo.set(opts[0])
            self._pilih_mahasiswa()

    def _pilih_mahasiswa(self, event=None):
        label = self._dd_var.get()
        nim   = self._dd_data.get(label)
        if not nim: return
        self._nim_aktif = nim
        semua = db.get_semua()
        mhs   = next((m for m in semua if m["nim"] == nim), None)
        if mhs:
            ipk    = db.ipk_mahasiswa(mhs)
            terisi = db.semester_terisi(mhs)
            self._lbl_info.configure(
                text=f"IPK saat ini: {ipk:.2f}  |  Semester sudah terisi: {terisi}")
        self._load_form()

    def _load_form(self, event=None):
        if not self._nim_aktif:
            return

        smt    = int(self._smt_var.get())
        matkul = db.KURIKULUM[smt]

        for w in self._form_card.winfo_children():
            w.destroy()

        self._entries = []

        header = ctk.CTkFrame(self._form_card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(14, 8))
        ctk.CTkLabel(header, text=f"Nilai Semester {smt}",
            font=F_SUBJUDUL, text_color=C["teks"]).pack(side="left")

        semua    = db.get_semua()
        mhs      = next((m for m in semua if m["nim"] == self._nim_aktif), None)
        existing = mhs["semester"].get(str(smt), []) if mhs else []

        scroll = ctk.CTkScrollableFrame(self._form_card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        for i, (nama_mk, sks) in enumerate(matkul):
            row = ctk.CTkFrame(scroll, fg_color=C["abu_card"], corner_radius=8)
            row.pack(fill="x", pady=4)

            ctk.CTkLabel(row,
                text=f"{nama_mk}",
                font=F_NORMAL, text_color=C["teks"], anchor="w", width=320
            ).pack(side="left", padx=14, pady=10)

            ctk.CTkLabel(row, text=f"{sks} SKS",
                font=F_KECIL, text_color=C["teks_sub"]).pack(side="left", padx=8)

            e = ctk.CTkEntry(row, width=80, height=34,
                font=F_NORMAL, corner_radius=6,
                justify="center",
                placeholder_text="0-100")
            e.pack(side="right", padx=14)

            if i < len(existing):
                e.insert(0, str(int(existing[i]["nilai"])))

            grade_lbl = ctk.CTkLabel(row, text="", width=36,
                font=("Segoe UI", 10, "bold"), text_color=C["biru"])
            grade_lbl.pack(side="right")

            def update_grade(event, el=e, gl=grade_lbl):
                try:
                    g, _ = db.nilai_ke_grade(float(el.get()))
                    colors = {
                        "A": C["hijau"], "A-": C["hijau"],
                        "B+": "#16A34A", "B": C["biru"], "B-": C["biru"],
                        "C+": C["kuning"], "C": C["kuning"],
                        "D": C["merah"], "E": C["merah"],
                    }
                    gl.configure(text=g, text_color=colors.get(g, C["teks_sub"]))
                except Exception:
                    gl.configure(text="", text_color=C["teks_sub"])

            e.bind("<KeyRelease>", update_grade)
            update_grade(None, e, grade_lbl)
            self._entries.append(e)

        for i in range(len(self._entries) - 1):
            nxt = self._entries[i + 1]
            self._entries[i].bind("<Return>", lambda ev, n=nxt: n.focus_set())

        foot = ctk.CTkFrame(self._form_card, fg_color="transparent")
        foot.pack(fill="x", padx=20, pady=12)
        _btn(foot, "Simpan Nilai", self._simpan, width=180).pack(side="right")
        _btn(foot, "Batal", self._placeholder, color=C["teks_sub"], width=100).pack(side="right", padx=(0, 8))

        if self._entries:
            self._entries[0].focus_set()

    def _simpan(self):
        if not self._nim_aktif:
            messagebox.showwarning("Perhatian", "Pilih mahasiswa terlebih dahulu.")
            return
        try:
            nilai_list = [float(e.get()) for e in self._entries]
            db.simpan_nilai(self._nim_aktif, int(self._smt_var.get()), nilai_list)
            messagebox.showinfo("Berhasil", "Nilai berhasil disimpan.")
            self._load_form()
            self._on_selesai()
        except ValueError as err:
            messagebox.showerror("Gagal", str(err))

    def set_nim(self, nim: str):
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return
        label = f"{nim}  —  {mhs['nama']}"
        self._dd_data[label] = nim
        vals = list(self._combo["values"])
        if label not in vals:
            vals.insert(0, label)
        self._combo["values"] = vals
        self._combo.set(label)
        self._nim_aktif = nim
        ipk    = db.ipk_mahasiswa(mhs)
        terisi = db.semester_terisi(mhs)
        self._lbl_info.configure(
            text=f"IPK saat ini: {ipk:.2f}  |  Semester sudah terisi: {terisi}")
        self._load_form()


# ============================================================
# HALAMAN STATISTIK — dengan grafik canvas
# ============================================================

class HalamanStatistik(HalamanBase):
    """
    Dashboard statistik penuh dengan 4 grafik:
    1. Distribusi IPK (bar horizontal — rentang 0-4)
    2. Distribusi Predikat (pie chart)
    3. Rata-rata IPS per Semester (line chart)
    4. Distribusi Grade per Semester (column chart)
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Statistik Kelas", "Visualisasi data akademik seluruh mahasiswa")
        self._build()

    def _build(self):
        # Toolbar refresh
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=28, pady=(12, 4))
        self._filter_smt = tk.StringVar(value="Semua")
        ctk.CTkLabel(bar, text="Filter Semester:", font=F_KECIL,
                     text_color=C["teks_sub"]).pack(side="left", padx=(0, 8))
        smt_opts = ["Semua", "1", "2", "3", "4", "5", "6"]
        smt_cb = ttk.Combobox(bar, textvariable=self._filter_smt,
                              values=smt_opts, state="readonly", width=10,
                              font=("Segoe UI", 10))
        smt_cb.pack(side="left")
        smt_cb.bind("<<ComboboxSelected>>", lambda *_: self.refresh())
        _btn(bar, "Refresh", self.refresh, width=100).pack(side="right")

        # Scrollable area untuk semua grafik
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        # Row 1: distribusi IPK (bar) + predikat (pie)
        row1 = ctk.CTkFrame(scroll, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 12))
        row1.columnconfigure(0, weight=3)
        row1.columnconfigure(1, weight=2)

        card_ipk = self._card(row1)
        card_ipk.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        ctk.CTkLabel(card_ipk, text="Distribusi Rentang IPK",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_ipk = tk.Canvas(card_ipk, height=220,
                                     bg=C["putih"], highlightthickness=0)
        self._canvas_ipk.pack(fill="x", padx=16, pady=(0, 14))

        card_pred = self._card(row1)
        card_pred.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        ctk.CTkLabel(card_pred, text="Sebaran Predikat",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_pred = tk.Canvas(card_pred, height=220,
                                      bg=C["putih"], highlightthickness=0)
        self._canvas_pred.pack(fill="x", padx=16, pady=(0, 14))

        # Row 2: rata-rata IPS per semester (line)
        card_ips = self._card(scroll)
        card_ips.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card_ips, text="Rata-rata IPS per Semester",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_ips = tk.Canvas(card_ips, height=200,
                                     bg=C["putih"], highlightthickness=0)
        self._canvas_ips.pack(fill="x", padx=16, pady=(0, 14))

        # Row 3: distribusi grade per semester (column)
        card_grade = self._card(scroll)
        card_grade.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card_grade, text="Distribusi Grade (Semua Mata Kuliah)",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_grade = tk.Canvas(card_grade, height=200,
                                       bg=C["putih"], highlightthickness=0)
        self._canvas_grade.pack(fill="x", padx=16, pady=(0, 14))

        # Row 4: ringkasan teks
        card_sum = self._card(scroll)
        card_sum.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card_sum, text="Ringkasan Statistik",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._sum_frame = ctk.CTkFrame(card_sum, fg_color="transparent")
        self._sum_frame.pack(fill="x", padx=16, pady=(0, 14))

        self.refresh()

    def _get_data(self):
        """Ambil dan hitung semua data statistik sekali jalan."""
        semua = db.get_semua()
        filter_smt = self._filter_smt.get()

        # Kumpulkan semua IPK
        ipk_list = []
        for m in semua:
            if not m["semester"]:
                continue
            if filter_smt != "Semua":
                if filter_smt not in m["semester"]:
                    continue
            ipk_list.append(db.ipk_mahasiswa(m))

        # Distribusi rentang IPK
        rentang = [
            ("0.00 - 1.99", 0),
            ("2.00 - 2.49", 0),
            ("2.50 - 2.99", 0),
            ("3.00 - 3.49", 0),
            ("3.50 - 3.74", 0),
            ("3.75 - 4.00", 0),
        ]
        for ipk in ipk_list:
            if ipk < 2.0:
                rentang[0] = (rentang[0][0], rentang[0][1] + 1)
            elif ipk < 2.5:
                rentang[1] = (rentang[1][0], rentang[1][1] + 1)
            elif ipk < 3.0:
                rentang[2] = (rentang[2][0], rentang[2][1] + 1)
            elif ipk < 3.5:
                rentang[3] = (rentang[3][0], rentang[3][1] + 1)
            elif ipk < 3.75:
                rentang[4] = (rentang[4][0], rentang[4][1] + 1)
            else:
                rentang[5] = (rentang[5][0], rentang[5][1] + 1)

        # Distribusi predikat
        pred_dist = {"Cumlaude": 0, "Sangat Baik": 0, "Baik": 0,
                     "Cukup": 0, "Perlu Perbaikan": 0}
        for ipk in ipk_list:
            p = db.predikat(ipk)
            pred_dist[p] = pred_dist.get(p, 0) + 1

        # Rata-rata IPS per semester
        ips_per_smt = {}  # {smt: [ips, ...]}
        grade_dist  = {}  # {grade: count}
        for m in semua:
            for smt_key, mk_list in m["semester"].items():
                if filter_smt != "Semua" and smt_key != filter_smt:
                    continue
                ips = db.hitung_ips(mk_list)
                ips_per_smt.setdefault(smt_key, []).append(ips)
                for mk in mk_list:
                    g = mk.get("grade", "E")
                    grade_dist[g] = grade_dist.get(g, 0) + 1

        avg_ips = {}
        for smt, vals in ips_per_smt.items():
            avg_ips[smt] = round(sum(vals) / len(vals), 2)

        return {
            "ipk_list":  ipk_list,
            "rentang":   rentang,
            "pred_dist": pred_dist,
            "avg_ips":   avg_ips,
            "grade_dist": grade_dist,
            "total":     len(semua),
        }

    def refresh(self, *_):
        data = self._get_data()

        # Tunggu canvas siap (width bisa 0 sebelum render)
        self.update_idletasks()

        # --- 1. Bar chart distribusi IPK ---
        colors_ipk = [
            C["merah"], C["kuning"], "#F59E0B",
            C["biru"], C["hijau"], "#059669"
        ]
        Chart.bar(self._canvas_ipk, data["rentang"],
                  colors=colors_ipk, title="Jumlah mahasiswa per rentang IPK")

        # --- 2. Pie chart predikat ---
        pred_data = [(k, v) for k, v in data["pred_dist"].items() if v > 0]
        pred_colors = [C["ungu"], C["hijau"], C["biru"], C["kuning"], C["merah"]]
        Chart.pie(self._canvas_pred, pred_data,
                  colors=pred_colors, title="Sebaran predikat mahasiswa")

        # --- 3. Line chart rata-rata IPS per semester ---
        smts = sorted(data["avg_ips"].keys(), key=int)
        ips_vals = [data["avg_ips"][s] for s in smts]
        smt_labels = [f"Smt {s}" for s in smts]
        if len(ips_vals) >= 2:
            Chart.line(self._canvas_ips,
                       datasets=[("Rata-rata IPS", C["biru"], ips_vals)],
                       labels=smt_labels,
                       title="Tren rata-rata IPS per semester")
        else:
            self._canvas_ips.delete("all")
            self._canvas_ips.update_idletasks()
            w = self._canvas_ips.winfo_width() or 400
            self._canvas_ips.create_text(
                w // 2, 100,
                text="Butuh minimal 2 semester untuk menampilkan tren.",
                fill=C["teks_sub"], font=F_KECIL
            )

        # --- 4. Column chart distribusi grade ---
        grade_order = ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "E"]
        grade_data = [(g, data["grade_dist"].get(g, 0)) for g in grade_order]

        grade_colors = [
            "#059669", "#16A34A", "#22C55E", "#4ADE80", "#86EFAC",
            "#F59E0B", "#D97706", "#EA580C", "#DC2626"
        ]
        Chart.column(self._canvas_grade, grade_data,
                     colors=grade_colors,
                     title="Distribusi grade seluruh mata kuliah")

        # --- 5. Ringkasan teks ---
        for w in self._sum_frame.winfo_children():
            w.destroy()

        ipk_list = data["ipk_list"]
        stats = [
            ("Mahasiswa dengan nilai",    str(len(ipk_list)),                    C["biru"]),
            ("Rata-rata IPK",             f"{sum(ipk_list)/len(ipk_list):.2f}" if ipk_list else "0.00", C["biru"]),
            ("IPK tertinggi",             f"{max(ipk_list):.2f}" if ipk_list else "0.00", C["hijau"]),
            ("IPK terendah",              f"{min(ipk_list):.2f}" if ipk_list else "0.00", C["merah"]),
            ("Total mahasiswa terdaftar", str(data["total"]),                    C["teks"]),
        ]

        self._sum_frame.columnconfigure(tuple(range(len(stats))), weight=1, uniform="s")
        for col, (label, val, color) in enumerate(stats):
            box = ctk.CTkFrame(self._sum_frame, fg_color=C["abu_card"],
                               corner_radius=10)
            box.grid(row=0, column=col, padx=6, sticky="nsew")
            ctk.CTkLabel(box, text=label, font=("Segoe UI", 8),
                         text_color=C["teks_sub"]).pack(padx=12, pady=(10, 2), anchor="w")
            ctk.CTkLabel(box, text=val,
                         font=("Segoe UI", 20, "bold"),
                         text_color=color).pack(padx=12, pady=(0, 10), anchor="w")


# ============================================================
# HALAMAN RIWAYAT
# ============================================================

class HalamanRiwayat(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Riwayat Aktivitas", "20 operasi terakhir")
        _style_tree()
        self._build()

    def _build(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=28, pady=12)
        _btn(toolbar, "Refresh", self.refresh, width=100).pack(side="right")

        card = ctk.CTkFrame(self, fg_color=C["putih"],
            corner_radius=12, border_width=1, border_color=C["abu_border"])
        card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        cols = ("waktu", "aksi", "detail")
        self._tree = ttk.Treeview(card, columns=cols, show="headings",
            style="App.Treeview")
        self._tree.heading("waktu",  text="Waktu",  anchor="center")
        self._tree.heading("aksi",   text="Aksi",   anchor="center")
        self._tree.heading("detail", text="Detail", anchor="w")
        self._tree.column("waktu",  width=150, anchor="center")
        self._tree.column("aksi",   width=90,  anchor="center")
        self._tree.column("detail", width=450, anchor="w")

        self._tree.tag_configure("TAMBAH", foreground=C["hijau"])
        self._tree.tag_configure("HAPUS",  foreground=C["merah"])
        self._tree.tag_configure("NILAI",  foreground=C["biru"])
        self._tree.tag_configure("EDIT",   foreground=C["kuning"])

        vsb = ttk.Scrollbar(card, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True, pady=1, padx=(1, 0))
        vsb.pack(side="right", fill="y")

        self.refresh()

    def refresh(self):
        for i in self._tree.get_children():
            self._tree.delete(i)
        for h in db.get_riwayat():
            self._tree.insert("", "end",
                values=(h["waktu"], h["aksi"], h["detail"]),
                tags=(h["aksi"],))


# ============================================================
# HALAMAN LOGIN - REDESIGN TOTAL
# ============================================================

class HalamanLogin(ctk.CTkFrame):

    def __init__(self, parent, on_login):
        super().__init__(parent, corner_radius=0, fg_color=C["bg_main"])
        self._on_login = on_login
        self._build()

    def _build(self):
        # === LAYOUT BARU: Centered Card dengan Cosmic Background ===

        # Background frame dengan gradient effect simulation
        bg_frame = ctk.CTkFrame(self, fg_color="transparent")
        bg_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # === PANEL KIRI - BRANDING DENGAN GRADIENT ===
        kiri = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0)
        kiri.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # Decorative circles untuk cosmic effect
        decor1 = ctk.CTkFrame(kiri, width=300, height=300,
                              fg_color=C["primary"], corner_radius=150)
        decor1.place(relx=0.5, rely=0.3, anchor="center")

        decor2 = ctk.CTkFrame(kiri, width=200, height=200,
                              fg_color=C["secondary"], corner_radius=100)
        decor2.place(relx=0.5, rely=0.35, anchor="center")

        # Logo di atas decorative elements
        ctk.CTkLabel(kiri, text="✦ Andromeda",
            font=("Segoe UI", 48, "bold"), text_color=C["star_white"]
        ).place(relx=0.5, rely=0.38, anchor="center")

        ctk.CTkLabel(kiri,
            text="Sistem Informasi Akademik Mahasiswa\nPendidikan Teknik Otomasi Industri dan Robotika",
            font=("Segoe UI", 14), text_color=C["highlight"],
            justify="center"
        ).place(relx=0.5, rely=0.52, anchor="center")

        # === PANEL KANAN - LOGIN FORM ===
        kanan = ctk.CTkFrame(self, fg_color=C["bg_secondary"], corner_radius=0)
        kanan.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # Login card centered dengan elevated design
        card = ctk.CTkFrame(kanan, fg_color=C["surface"],
                           width=420, corner_radius=24,
                           border_width=2, border_color=C["primary"])
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Header card
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(40, 20))

        ctk.CTkLabel(header_frame, text="Selamat Datang",
            font=("Segoe UI", 28, "bold"), text_color=C["highlight"]
        ).pack(anchor="w")

        ctk.CTkLabel(header_frame, text="Silakan masuk untuk melanjutkan",
            font=F_NORMAL, text_color=C["text_muted"]
        ).pack(anchor="w", pady=(8, 0))

        # Form fields
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(fill="x", padx=40, pady=(20, 30))

        ctk.CTkLabel(form_frame, text="Username", font=F_TEBEL,
            text_color=C["text_main"]).pack(anchor="w")
        self._e_user = _entry(form_frame, placeholder="Masukkan username", width=340)
        self._e_user.pack(pady=(8, 20))

        ctk.CTkLabel(form_frame, text="Password", font=F_TEBEL,
            text_color=C["text_main"]).pack(anchor="w")
        self._e_pass = _entry(form_frame, placeholder="Masukkan password", show="*", width=340)
        self._e_pass.pack(pady=(8, 8))

        _bind_enter_chain([self._e_user, self._e_pass])
        self._e_pass.bind("<Return>", lambda e: self._login())

        # Login button - full width dengan style baru
        _btn(card, "Masuk →", self._login, width=340, height=52, style="primary").pack(pady=(10, 10))

        # Error label
        self._lbl_err = ctk.CTkLabel(card, text="",
            font=F_KECIL, text_color=C["error"])
        self._lbl_err.pack(pady=(0, 30))

        self._e_user.focus_set()

    def _login(self):
        u = self._e_user.get().strip()
        p = self._e_pass.get()
        if db.cek_login(u, p):
            self._on_login()
        else:
            self._lbl_err.configure(text="Username atau password salah.")


# ============================================================
# APLIKASI UTAMA
# ============================================================

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Sistem Informasi Akademik Mahasiswa")
        self.geometry("1280x740")
        self.minsize(1024, 640)
        self.configure(fg_color=C["bg_main"])
        _style_tree()
        self._tampil_login()

    def _tampil_login(self):
        self._bersih()
        HalamanLogin(self, self._setelah_login).pack(fill="both", expand=True)

    def _setelah_login(self):
        self._bersih()
        self._bangun_shell()
        self._sidebar.aktifkan("dashboard")

    def _bangun_shell(self):
        self._sidebar = Sidebar(self, self._navigasi)
        self._sidebar.pack(side="left", fill="y")

        # Main content area dengan background baru
        self._area = ctk.CTkFrame(self, corner_radius=0, fg_color=C["bg_main"])
        self._area.pack(side="left", fill="both", expand=True)

        self._dash      = HalamanDashboard(self._area)
        self._mhs       = HalamanMahasiswa(self._area, on_nilai=self._buka_nilai)
        self._nilai     = HalamanNilai(self._area, on_selesai=self._selesai_nilai)
        self._statistik = HalamanStatistik(self._area)
        self._riwayat   = HalamanRiwayat(self._area)

        self._halaman_aktif = None

    def _navigasi(self, key: str):
        if key == "logout":
            if messagebox.askyesno("Logout", "Yakin ingin keluar?"):
                self._tampil_login()
            return

        mapping = {
            "dashboard":  self._dash,
            "mahasiswa":  self._mhs,
            "nilai":      self._nilai,
            "statistik":  self._statistik,
            "riwayat":    self._riwayat,
        }

        target = mapping.get(key)
        if not target or target is self._halaman_aktif:
            return

        if self._halaman_aktif:
            self._halaman_aktif.pack_forget()

        target.pack(fill="both", expand=True)
        self._halaman_aktif = target

        if key == "dashboard":   self._dash.refresh()
        if key == "mahasiswa":   self._mhs.refresh()
        if key == "statistik":   self._statistik.refresh()
        if key == "riwayat":     self._riwayat.refresh()

    def _buka_nilai(self, nim: str):
        self._sidebar.aktifkan("nilai")
        self._nilai.set_nim(nim)

    def _selesai_nilai(self):
        self._dash.refresh()
        self._mhs.refresh()

    def _bersih(self):
        for w in self.winfo_children():
            w.destroy()