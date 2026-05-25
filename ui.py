# ============================================================
# ui.py  —  GUI Utama
# Sistem Informasi Akademik Mahasiswa
# CustomTkinter — ANDROMEDA COMMAND CENTER v4.0
# Futuristic OS · Asymmetrical Layout · Holographic Interface
# ============================================================

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import db
import math

# ============================================================
# TEMA - ANDROMEDA COMMAND CENTER (SPACE STATION 2045)
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

C = {
    # === ANDROMEDA GALAXY PALETTE ===
    # Deep Space Backgrounds
    "bg_main":           "#030508",   # Void - deepest black
    "bg_secondary":      "#060a14",   # Nebula dark
    "bg_tertiary":       "#0a0f1c",   # Cosmic layer

    # Glass Surfaces (floating panels)
    "surface":           "#0b1221",   # Primary glass
    "surface_elevated":  "#0f1829",   # Elevated floating
    "surface_hover":     "#141f35",   # Hover interaction
    "surface_glass":     "#0c1525",   # Transparent glass

    # Neon Accent Colors - Galaxy Andromeda
    "primary":           "#8b5cf6",   # Electric violet
    "primary_glow":      "#a78bfa",   # Violet aura
    "secondary":         "#06b6d4",   # Cyan electric
    "secondary_glow":    "#22d3ee",   # Cyan radiance
    "accent_pink":       "#f472b6",   # Plasma pink
    "accent_pink_glow":  "#fb7185",   # Pink flare
    "accent_amber":      "#fbbf24",   # Stellar gold
    "highlight":         "#c4b5fd",   # Soft lavender

    # Text Hierarchy
    "text_main":         "#f8fafc",   # Crystal white
    "text_secondary":    "#cbd5e1",   # Silver mist
    "text_muted":        "#64748b",   # Shadow gray
    "text_hint":         "#475569",   # Deep shadow

    # Borders & Glows
    "border_solid":      "#1e293b",   # Subtle edge
    "border_glow":       "#334155",   # Glow edge
    "border_accent":     "#6d28d9",   # Violet accent
    "border_cyan":       "#0891b2",   # Cyan accent

    # Status Colors
    "success":           "#10b981",
    "success_bg":        "#022c22",
    "success_glow":      "#34d399",
    "error":             "#ef4444",
    "error_bg":          "#2a0a0a",
    "error_glow":        "#f87171",
    "warning":           "#f59e0b",
    "warning_bg":        "#2d1f00",
    "warning_glow":      "#fcd34d",
    "info":              "#8b5cf6",
    "info_bg":           "#1e1b4b",

    # Particles
    "star_white":        "#ffffff",
    "star_dim":          "#475569",

    # Legacy aliases
    "hijau_hutan":       "#0b1221",
    "hijau_daun":        "#0f1829",
    "hijau_aksen":       "#06b6d4",
    "biru":              "#8b5cf6",
    "biru_muda":         "#060a14",
    "biru_aksen":        "#c4b5fd",
    "abu_bg":            "#030508",
    "abu_card":          "#0b1221",
    "abu_border":        "#1e293b",
    "teks":              "#f8fafc",
    "teks_sub":          "#cbd5e1",
    "teks_input":        "#ffffff",
    "placeholder":       "#64748b",
    "putih":             "#0b1221",
    "hitam_ungu":        "#030508",
    "hijau":             "#10b981",
    "merah":             "#ef4444",
    "kuning":            "#f59e0b",
    "ungu":              "#8b5cf6",
    "glow_primary":      "#a78bfa",
    "glow_secondary":    "#22d3ee",
}

# ── Typography ──────────────────────────────────────────────
F_JUDUL    = ("Segoe UI Variable", 24, "bold")
F_SUBJUDUL = ("Segoe UI Variable", 15, "bold")
F_NORMAL   = ("Segoe UI Variable", 12)
F_KECIL    = ("Segoe UI Variable", 10)
F_MONO     = ("Consolas", 11)
F_TEBEL    = ("Segoe UI Variable", 12, "bold")
F_LOGO     = ("Segoe UI Variable", 28, "bold")
F_NANO     = ("Segoe UI Variable", 9)


# ============================================================
# HELPERS
# ============================================================

def _entry(parent, placeholder="", show="", width=280):
    """Glass-style pill input with neon border glow."""
    return ctk.CTkEntry(
        parent, width=width, height=46,
        placeholder_text=placeholder,
        show=show,
        font=F_NORMAL,
        corner_radius=23,
        border_width=2,
        border_color=C["border_accent"],
        fg_color=C["surface_elevated"],
        text_color=C["text_main"],
        placeholder_text_color=C["text_muted"],
    )


def _btn(parent, text, command, color=None, width=180, height=44, style="primary"):
    """Pill-shape neon button with glow border."""
    color = color or C["primary"]

    if style == "primary":
        return ctk.CTkButton(
            parent, text=text, command=command,
            width=width, height=height,
            font=("Segoe UI Variable", 11, "bold"),
            fg_color=color,
            hover_color=C["glow_primary"],
            corner_radius=22,
            border_width=1,
            border_color=C["highlight"],
        )
    elif style == "secondary":
        return ctk.CTkButton(
            parent, text=text, command=command,
            width=width, height=height,
            font=("Segoe UI Variable", 11, "bold"),
            fg_color="transparent",
            hover_color=C["surface_elevated"],
            corner_radius=22,
            border_width=1,
            border_color=C["secondary"],
            text_color=C["secondary"],
        )
    else:
        return ctk.CTkButton(
            parent, text=text, command=command,
            width=width, height=height,
            font=("Segoe UI Variable", 11, "bold"),
            fg_color=color,
            hover_color=_gelap(color),
            corner_radius=22,
        )


def _gelap(hex_color: str) -> str:
    try:
        r = max(0, int(hex_color[1:3], 16) - 25)
        g = max(0, int(hex_color[3:5], 16) - 25)
        b = max(0, int(hex_color[5:7], 16) - 25)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _terang(hex_color: str) -> str:
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


def _label(parent, text, font=None, color=None, anchor="w"):
    return ctk.CTkLabel(
        parent, text=text,
        font=font or F_NORMAL,
        text_color=color or C["text_main"],
        anchor=anchor,
    )


# ============================================================
# TREEVIEW STYLE — NOVA GALAXY
# ============================================================

def _style_tree():
    s = ttk.Style()
    s.theme_use("clam")

    # Main treeview
    s.configure("App.Treeview",
        background=C["surface"],
        foreground=C["text_main"],
        fieldbackground=C["surface"],
        rowheight=46,
        font=("Segoe UI Variable", 11),
        borderwidth=0,
        relief="flat",
    )
    s.configure("App.Treeview.Heading",
        background=C["surface_elevated"],
        foreground=C["secondary"],
        font=("Segoe UI Variable", 10, "bold"),
        borderwidth=0,
        relief="flat",
        padding=(8, 10),
    )
    s.map("App.Treeview",
        background=[("selected", C["primary"])],
        foreground=[("selected", "#ffffff")],
    )

    # Scrollbar styling
    s.configure("Vertical.TScrollbar",
        background=C["surface_elevated"],
        troughcolor=C["bg_main"],
        arrowcolor=C["text_muted"],
        borderwidth=0,
        relief="flat",
    )


# ============================================================
# GRAFIK CANVAS — Chart helpers (unchanged logic)
# ============================================================

class Chart:

    @staticmethod
    def bar(canvas, data: list[tuple], colors: list[str] = None,
            title: str = "", x_label: str = "", y_label: str = ""):
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

        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI Variable", 9, "bold"),
                               fill=C["teks"], anchor="center")

        grid_steps = 5
        for i in range(grid_steps + 1):
            gx = PAD_L + int(chart_w * i / grid_steps)
            gy1, gy2 = PAD_T, PAD_T + chart_h
            canvas.create_line(gx, gy1, gx, gy2,
                               fill=C["border_solid"], width=1, dash=(2, 4))
            val_label = int(max_val * i / grid_steps)
            canvas.create_text(gx, PAD_T + chart_h + 10,
                               text=str(val_label),
                               font=("Segoe UI Variable", 7), fill=C["teks_sub"])

        for i, ((label, val), color) in enumerate(zip(data, colors)):
            y1 = PAD_T + gap + i * (bar_h + gap)
            y2 = y1 + bar_h
            bar_len = int(chart_w * val / max_val)

            canvas.create_rectangle(PAD_L, y1, PAD_L + chart_w, y2,
                                    fill=C["surface_elevated"], outline="")
            if bar_len > 0:
                canvas.create_rectangle(PAD_L, y1, PAD_L + bar_len, y2,
                                        fill=color, outline="")
                canvas.create_oval(PAD_L + bar_len - 4, y1,
                                   PAD_L + bar_len + 4, y2,
                                   fill=color, outline="")

            canvas.create_text(PAD_L - 6, (y1 + y2) // 2,
                               text=label, font=("Segoe UI Variable", 8),
                               fill=C["teks"], anchor="e")
            if val > 0:
                canvas.create_text(PAD_L + bar_len + 8, (y1 + y2) // 2,
                                   text=str(val), font=("Segoe UI Variable", 8, "bold"),
                                   fill=color, anchor="w")

    @staticmethod
    def column(canvas, data: list[tuple], colors: list[str] = None,
               title: str = ""):
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

        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI Variable", 9, "bold"),
                               fill=C["teks"], anchor="center")

        grid_steps = 4
        for i in range(grid_steps + 1):
            gy = PAD_T + chart_h - int(chart_h * i / grid_steps)
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                               fill=C["border_solid"], width=1, dash=(2, 4))
            val_label = int(max_val * i / grid_steps)
            canvas.create_text(PAD_L - 6, gy,
                               text=str(val_label),
                               font=("Segoe UI Variable", 7), fill=C["teks_sub"],
                               anchor="e")

        canvas.create_line(PAD_L, PAD_T + chart_h,
                           PAD_L + chart_w, PAD_T + chart_h,
                           fill=C["border_glow"], width=1)

        for i, ((label, val), color) in enumerate(zip(data, colors)):
            x1 = PAD_L + gap + i * (bar_w + gap)
            x2 = x1 + bar_w
            bar_h_px = int(chart_h * val / max_val)
            y1 = PAD_T + chart_h - bar_h_px
            y2 = PAD_T + chart_h

            if bar_h_px > 0:
                canvas.create_rectangle(x1, y1, x2, y2,
                                        fill=color, outline="")

            canvas.create_text((x1 + x2) // 2, PAD_T + chart_h + 12,
                               text=label, font=("Segoe UI Variable", 8),
                               fill=C["teks"], anchor="n")

            if val > 0:
                canvas.create_text((x1 + x2) // 2, y1 - 8,
                                   text=str(val),
                                   font=("Segoe UI Variable", 8, "bold"),
                                   fill=color, anchor="s")

    @staticmethod
    def pie(canvas, data: list[tuple], colors: list[str] = None,
            title: str = ""):
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
                               font=("Segoe UI Variable", 9, "bold"),
                               fill=C["teks"], anchor="center")

        start = 0.0
        slices = [(label, val, color)
                  for (label, val), color in zip(data, colors)
                  if val > 0]

        for label, val, color in slices:
            extent = (val / total) * 360
            canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                              start=start, extent=extent,
                              fill=color, outline=C["bg_main"], width=2)
            start += extent

        lx = cx * 2 + 16
        ly = H // 2 - len(slices) * 18
        for label, val, color in slices:
            pct = val / total * 100
            canvas.create_rectangle(lx, ly, lx + 12, ly + 12,
                                    fill=color, outline="")
            canvas.create_text(lx + 18, ly + 6,
                               text=f"{label}  {val} ({pct:.1f}%)",
                               font=("Segoe UI Variable", 8), fill=C["teks"],
                               anchor="w")
            ly += 22

    @staticmethod
    def line(canvas, datasets: list[tuple], labels: list[str],
             title: str = ""):
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
                               font=("Segoe UI Variable", 9, "bold"),
                               fill=C["teks"], anchor="center")

        grid_steps = 4
        for i in range(grid_steps + 1):
            gy = PAD_T + chart_h - int(chart_h * i / grid_steps)
            gval = min_val + (max_val - min_val) * i / grid_steps
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                               fill=C["border_solid"], width=1, dash=(2, 4))
            canvas.create_text(PAD_L - 6, gy,
                               text=f"{gval:.2f}",
                               font=("Segoe UI Variable", 7), fill=C["teks_sub"],
                               anchor="e")

        if n > 1:
            for i, lbl in enumerate(labels):
                gx = PAD_L + int(chart_w * i / (n - 1))
                canvas.create_text(gx, PAD_T + chart_h + 12,
                                   text=lbl, font=("Segoe UI Variable", 8),
                                   fill=C["teks_sub"])

        for s_label, color, vals in datasets:
            if len(vals) < 2:
                continue
            points = []
            for i, v in enumerate(vals):
                gx = PAD_L + int(chart_w * i / (n - 1))
                gy = PAD_T + chart_h - int(chart_h * (v - min_val) / (max_val - min_val))
                points.append((gx, gy))

            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                canvas.create_line(x1, y1, x2, y2, fill=color, width=2, smooth=True)

            for gx, gy in points:
                canvas.create_oval(gx - 4, gy - 4, gx + 4, gy + 4,
                                   fill=color, outline=C["bg_main"], width=2)

        lx = PAD_L + chart_w - 10
        ly = PAD_T + 6
        for s_label, color, _ in datasets:
            canvas.create_rectangle(lx - 90, ly, lx - 78, ly + 8,
                                    fill=color, outline="")
            canvas.create_text(lx - 72, ly + 4,
                               text=s_label, font=("Segoe UI Variable", 8),
                               fill=C["teks"], anchor="w")
            ly += 16


# ============================================================
# SIDEBAR — FLOATING MINI DOCK (ASYMMETRICAL DESIGN)
# ============================================================

class Sidebar(ctk.CTkFrame):

    MENU = [
        ("Dashboard",      "dashboard",  "◈"),
        ("Mahasiswa",      "mahasiswa",  "◉"),
        ("Input Nilai",    "nilai",      "◆"),
        ("Statistik",      "statistik",  "◈"),
        ("Riwayat",        "riwayat",    "◉"),
    ]

    def __init__(self, parent, on_navigate):
        super().__init__(parent,
            width=96,
            corner_radius=0,
            fg_color="transparent",
        )
        self.pack_propagate(False)
        self._nav  = on_navigate
        self._btns = {}
        self._aktif = None
        self._build()

    def _build(self):
        # ── Floating dock container ──────────────────────────
        dock_frame = ctk.CTkFrame(self,
            width=80,
            fg_color=C["surface"],
            corner_radius=24,
            border_width=1,
            border_color=C["border_glow"],
        )
        dock_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ── Top system status indicator ──────────────────────
        status_chip = ctk.CTkFrame(dock_frame,
            width=40, height=40,
            fg_color=C["info_bg"],
            corner_radius=16,
            border_width=1,
            border_color=C["border_accent"],
        )
        status_chip.pack(pady=(20, 12))
        ctk.CTkLabel(status_chip, text="✦",
            font=("Segoe UI Variable", 18, "bold"),
            text_color=C["highlight"],
        ).place(relx=0.5, rely=0.5, anchor="center")

        # ── Navigation buttons (vertical stack) ─────────────
        nav_container = ctk.CTkFrame(dock_frame, fg_color="transparent")
        nav_container.pack(fill="x", padx=8, pady=4)

        for idx, (label, key, icon) in enumerate(self.MENU):
            btn_frame = ctk.CTkFrame(nav_container,
                fg_color="transparent", height=64)
            btn_frame.pack(fill="x", pady=2)
            btn_frame.pack_propagate(False)

            b = ctk.CTkButton(
                btn_frame,
                text=icon,
                anchor="center",
                width=56,
                height=56,
                font=("Segoe UI Variable", 20),
                fg_color="transparent",
                hover_color=C["surface_hover"],
                text_color=C["text_muted"],
                corner_radius=16,
                border_width=1,
                border_color="transparent",
                command=lambda k=key: self._klik(k),
            )
            b.pack()
            self._btns[key] = b

            # Tooltip-style label (appears on hover via placement)
            ctk.CTkLabel(btn_frame,
                text=label,
                font=F_NANO,
                text_color=C["text_hint"],
            ).place(x=64, y=20)

        # ── Bottom logout button ─────────────────────────────
        logout_frame = ctk.CTkFrame(dock_frame, fg_color="transparent")
        logout_frame.pack(side="bottom", pady=(0, 16))

        ctk.CTkButton(
            logout_frame,
            text="⏻",
            anchor="center",
            width=48,
            height=48,
            font=("Segoe UI Variable", 18),
            fg_color=C["error_bg"],
            hover_color="#3d0f0f",
            text_color=C["error_glow"],
            corner_radius=14,
            border_width=1,
            border_color=C["error"],
            command=lambda: self._nav("logout"),
        ).pack()

    def _klik(self, key: str):
        for k, b in self._btns.items():
            b.configure(
                fg_color="transparent",
                text_color=C["text_muted"],
                border_color="transparent",
            )
        if key in self._btns:
            self._btns[key].configure(
                fg_color=C["primary"],
                text_color="#ffffff",
                border_color=C["highlight"],
            )
        self._aktif = key
        self._nav(key)

    def aktifkan(self, key: str):
        self._klik(key)


# ============================================================
# HALAMAN DASAR — BASE PAGE
# ============================================================

class HalamanBase(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=C["bg_main"])

    def _header(self, judul: str, subjudul: str = ""):
        """Cinematic header with gradient separator and neon typography."""
        hdr = ctk.CTkFrame(self, fg_color=C["bg_secondary"], corner_radius=0, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.pack(side="left", padx=36, pady=0)
        inner.pack_configure(pady=0)

        # Accent dot
        dot_row = ctk.CTkFrame(inner, fg_color="transparent")
        dot_row.pack(anchor="w", pady=(18, 0))
        ctk.CTkFrame(dot_row, width=8, height=8,
            fg_color=C["secondary"], corner_radius=4
        ).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(dot_row, text=subjudul.upper() if subjudul else "",
            font=("Segoe UI Variable", 9, "bold"),
            text_color=C["secondary"], anchor="w",
        ).pack(side="left")

        ctk.CTkLabel(inner, text=judul,
            font=F_JUDUL, text_color=C["text_main"], anchor="w",
        ).pack(anchor="w", pady=(2, 14))

        # Neon divider
        div_frame = ctk.CTkFrame(self, height=2, fg_color="transparent",
                                 corner_radius=0)
        div_frame.pack(fill="x")
        ctk.CTkFrame(div_frame, height=2,
            fg_color=C["primary"], corner_radius=1,
        ).pack(fill="x", padx=0)

    def _card(self, parent, **kw):
        """Glass-morphism floating card."""
        return ctk.CTkFrame(parent,
            fg_color=C["surface_glass"],
            corner_radius=20,
            border_width=1,
            border_color=C["border_glow"],
            **kw
        )

    def _neon_card(self, parent, accent=None, **kw):
        """Card with neon accent border."""
        accent = accent or C["primary"]
        return ctk.CTkFrame(parent,
            fg_color=C["surface"],
            corner_radius=20,
            border_width=1,
            border_color=accent,
            **kw
        )


# ============================================================
# HALAMAN DASHBOARD — NOVA GALAXY REDESIGN
# ============================================================

class HalamanDashboard(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._build_cinematic_header()
        self._build()

    def _build_cinematic_header(self):
        """Large cinematic header with gradient overlay."""
        header = ctk.CTkFrame(self, fg_color="transparent", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Gradient background strip
        gradient = tk.Canvas(header, bg=C["bg_secondary"], highlightthickness=0, height=100)
        gradient.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Animated gradient line
        gradient.create_rectangle(0, 0, 2000, 2, fill=C["primary"], outline="")
        gradient.create_rectangle(0, 98, 2000, 2, fill=C["secondary"], outline="")

        # Title area
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.place(x=40, y=20)

        ctk.CTkLabel(title_frame,
            text="ANDROMEDA COMMAND CENTER",
            font=("Segoe UI Variable", 28, "bold"),
            text_color=C["text_main"],
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(title_frame,
            text="Sistem Informasi Akademik · Real-time Monitoring",
            font=F_KECIL,
            text_color=C["secondary"],
            anchor="w",
        ).pack(anchor="w", pady=(4, 0))

        # System status badge (top right)
        status_badge = ctk.CTkFrame(header,
            fg_color=C["info_bg"],
            corner_radius=20,
            border_width=1,
            border_color=C["border_accent"],
            width=140, height=32)
        status_badge.place(relx=1.0, x=-40, y=34, anchor="ne")

        ctk.CTkLabel(status_badge,
            text="● SYSTEM ONLINE",
            font=("Segoe UI Variable", 9, "bold"),
            text_color=C["secondary"],
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _build(self):
        # Main content area with asymmetrical grid
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=24, pady=(10, 20))

        # LEFT COLUMN - Hero section + Stats (wider)
        left_col = ctk.CTkFrame(main_container, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # RIGHT COLUMN - Vertical analytics panel (narrower)
        right_col = ctk.CTkFrame(main_container, fg_color="transparent")
        right_col.pack(side="right", fill="y", padx=(8, 0))
        right_col.pack_propagate(False)

        # === HERO SECTION - Best Student Spotlight ===
        hero_card = ctk.CTkFrame(left_col,
            fg_color=C["surface"],
            corner_radius=28,
            border_width=2,
            border_color=C["border_accent"],
            height=180)
        hero_card.pack(fill="x", pady=(0, 12))
        hero_card.pack_propagate(False)

        # Glowing corner accents
        ctk.CTkFrame(hero_card, width=40, height=3,
            fg_color=C["primary"], corner_radius=2).place(x=0, y=0)
        ctk.CTkFrame(hero_card, width=3, height=40,
            fg_color=C["primary"], corner_radius=2).place(x=0, y=0)

        ctk.CTkLabel(hero_card,
            text="⬥ TOP PERFORMER",
            font=("Segoe UI Variable", 10, "bold"),
            text_color=C["accent_pink"],
        ).place(x=24, y=16)

        self._lbl_best = ctk.CTkLabel(hero_card, text="—",
            font=("Segoe UI Variable", 26, "bold"),
            text_color=C["highlight"],
            wraplength=400, justify="left")
        self._lbl_best.place(x=24, y=42)

        self._lbl_best_ipk = ctk.CTkLabel(hero_card, text="",
            font=("Segoe UI Variable", 14),
            text_color=C["text_muted"])
        self._lbl_best_ipk.place(x=24, y=82)

        # IPK Max/Min display
        ipk_frame = ctk.CTkFrame(hero_card, fg_color="transparent")
        ipk_frame.place(relx=1.0, x=-28, y=24, anchor="ne")

        ctk.CTkLabel(ipk_frame,
            text="IPK TERTINGGI",
            font=F_NANO,
            text_color=C["text_hint"],
        ).pack(anchor="e")
        self._lbl_ipk_max = ctk.CTkLabel(ipk_frame, text="0.00",
            font=("Segoe UI Variable", 32, "bold"),
            text_color=C["success"])
        self._lbl_ipk_max.pack(anchor="e")

        ctk.CTkLabel(ipk_frame,
            text="IPK TERENDAH",
            font=F_NANO,
            text_color=C["text_hint"],
        ).pack(anchor="e", pady=(8, 0))
        self._lbl_ipk_min = ctk.CTkLabel(ipk_frame, text="0.00",
            font=("Segoe UI Variable", 24, "bold"),
            text_color=C["error"])
        self._lbl_ipk_min.pack(anchor="e")

        # === HORIZONTAL SCROLL STATS ===
        stats_scroll_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        stats_scroll_frame.pack(fill="x", pady=(0, 12))

        self._cards = {}
        specs = [
            ("total",       "TOTAL",         C["secondary"],    "◈"),
            ("sudah_nilai", "DINILAI",       C["success"],      "◉"),
            ("rata_ipk",    "RATA IPK",      C["highlight"],    "✦"),
            ("belum_nilai", "BELUM DINILAI", C["accent_pink"],  "◆"),
        ]

        for key, label, warna, icon in specs:
            stat_card = ctk.CTkFrame(stats_scroll_frame,
                fg_color=C["surface_glass"],
                corner_radius=20,
                border_width=1,
                border_color=C["border_glow"],
                width=180, height=110)
            stat_card.pack(side="left", padx=6)
            stat_card.pack_propagate(False)

            # Icon badge
            icon_chip = ctk.CTkFrame(stat_card,
                width=44, height=44,
                fg_color=C["surface_elevated"],
                corner_radius=14,
                border_width=1,
                border_color=warna)
            icon_chip.place(x=16, y=14)
            ctk.CTkLabel(icon_chip, text=icon,
                font=("Segoe UI Variable", 18),
                text_color=warna).place(relx=0.5, rely=0.5, anchor="center")

            # Label
            ctk.CTkLabel(stat_card, text=label,
                font=("Segoe UI Variable", 8, "bold"),
                text_color=C["text_muted"],
            ).place(x=16, y=66)

            # Value
            val_lbl = ctk.CTkLabel(stat_card, text="0",
                font=("Segoe UI Variable", 28, "bold"),
                text_color=warna)
            val_lbl.place(x=16, y=80)

            self._cards[key] = val_lbl

        # === ACTIVITY TERMINAL (Bottom section) ===
        terminal_card = ctk.CTkFrame(left_col,
            fg_color=C["surface"],
            corner_radius=24,
            border_width=1,
            border_color=C["border_glow"])
        terminal_card.pack(fill="both", expand=True)

        # Terminal header
        term_hdr = ctk.CTkFrame(terminal_card, fg_color="transparent")
        term_hdr.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(term_hdr,
            text="◉ LIVE ACTIVITY TERMINAL",
            font=("Segoe UI Variable", 11, "bold"),
            text_color=C["secondary"],
        ).pack(side="left")

        ctk.CTkLabel(term_hdr,
            text="last 10 operations",
            font=F_NANO,
            text_color=C["text_hint"],
        ).pack(side="right", pady=4)

        # Terminal display (monospace style)
        self._riwayat_frame = ctk.CTkScrollableFrame(
            terminal_card,
            fg_color=C["surface_elevated"],
            corner_radius=12,
            border_width=0)
        self._riwayat_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # === RIGHT COLUMN - Vertical Analytics ===
        # Distribution panel
        dist_card = ctk.CTkFrame(right_col,
            fg_color=C["surface"],
            corner_radius=24,
            border_width=1,
            border_color=C["border_glow"],
            width=220)
        dist_card.pack(fill="y", expand=True)
        dist_card.pack_propagate(False)

        ctk.CTkLabel(dist_card,
            text="◇ GRADE DISTRIBUTION",
            font=("Segoe UI Variable", 10, "bold"),
            text_color=C["primary"],
        ).place(x=18, y=16)

        self._dist_labels = {}
        predikat_specs = [
            ("Cumlaude",        C["primary"]),
            ("Sangat Baik",     C["success"]),
            ("Baik",            C["secondary"]),
            ("Cukup",           C["warning"]),
            ("Perlu Perbaikan", C["error"]),
        ]

        for idx, (nama, warna) in enumerate(predikat_specs):
            y_pos = 48 + idx * 38

            ctk.CTkLabel(dist_card, text=nama,
                font=("Segoe UI Variable", 8),
                text_color=C["text_muted"],
            ).place(x=18, y=y_pos)

            lbl_val = ctk.CTkLabel(dist_card, text="0",
                font=("Segoe UI Variable", 18, "bold"),
                text_color=warna)
            lbl_val.place(relx=1.0, x=-18, y=y_pos, anchor="ne")

            # Progress bar background
            ctk.CTkFrame(dist_card,
                width=120, height=4,
                fg_color=C["surface_elevated"],
                corner_radius=2).place(x=18, y=y_pos + 22)

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
            "TAMBAH": C["success"],
            "HAPUS":  C["error"],
            "NILAI":  C["secondary"],
            "EDIT":   C["warning"],
        }
        for w in self._riwayat_frame.winfo_children():
            w.destroy()
        for h in db.get_riwayat()[:10]:
            row = ctk.CTkFrame(self._riwayat_frame,
                fg_color=C["surface_elevated"],
                corner_radius=10, height=38)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)
            warna_aksi = aksi_warna.get(h["aksi"], C["text_muted"])

            ctk.CTkLabel(row, text=h["waktu"], width=148,
                font=F_NANO, text_color=C["text_muted"], anchor="w",
            ).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(row, text=h["aksi"], width=78,
                font=("Segoe UI Variable", 9, "bold"),
                text_color=warna_aksi, anchor="w",
            ).pack(side="left")
            ctk.CTkLabel(row, text=h["detail"],
                font=F_NANO, text_color=C["text_secondary"],
                anchor="w", wraplength=420,
            ).pack(side="left", padx=(8, 0))


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
        toolbar = ctk.CTkFrame(self,
            fg_color=C["surface"], corner_radius=0, height=60)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        inner_tb = ctk.CTkFrame(toolbar, fg_color="transparent")
        inner_tb.pack(fill="x", padx=24, pady=10)

        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self.refresh())

        search = ctk.CTkEntry(
            inner_tb, width=260, height=36,
            placeholder_text="⌕  Cari NIM atau nama...",
            textvariable=self._search_var,
            font=F_KECIL,
            corner_radius=18,
            border_width=1,
            border_color=C["border_glow"],
            fg_color=C["surface_elevated"],
            text_color=C["text_main"],
            placeholder_text_color=C["text_muted"],
        )
        search.pack(side="left")

        # Action buttons
        btn_specs = [
            ("+ Tambah",    self._form_tambah, C["primary"],    130),
            ("✎ Edit Nama", self._form_edit,   C["warning"],    120),
            ("◉ Nilai",     self._ke_nilai,    C["success"],    100),
            ("✕ Hapus",     self._hapus,       C["error"],       90),
        ]
        for txt, cmd, col, w in reversed(btn_specs):
            _btn(inner_tb, txt, cmd, color=col, width=w, height=36
                 ).pack(side="right", padx=4)

        # Table card
        tbl_frame = ctk.CTkFrame(self,
            fg_color=C["surface"],
            corner_radius=0,
            border_width=0)
        tbl_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Table header strip
        hdr_strip = ctk.CTkFrame(tbl_frame,
            fg_color=C["surface_elevated"], height=2)
        hdr_strip.pack(fill="x")

        cols = ("nim", "nama", "semester_terisi", "ipk", "total_sks", "predikat")
        self._tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
            style="App.Treeview", selectmode="browse")

        hdrs = {
            "nim":             ("NIM",             140),
            "nama":            ("Nama Lengkap",    280),
            "semester_terisi": ("Semester Terisi", 160),
            "ipk":             ("IPK",              90),
            "total_sks":       ("Total SKS",       110),
            "predikat":        ("Predikat",        170),
        }
        for col, (head, w) in hdrs.items():
            self._tree.heading(col, text=head, anchor="center")
            anc = "w" if col == "nama" else "center"
            self._tree.column(col, width=w, anchor=anc, minwidth=60)

        vsb = ttk.Scrollbar(tbl_frame, orient="vertical",
                            command=self._tree.yview,
                            style="Vertical.TScrollbar")
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._tree.tag_configure("cumlaude",  foreground=C["primary"])
        self._tree.tag_configure("sangat",    foreground=C["success"])
        self._tree.tag_configure("baik",      foreground=C["secondary"])
        self._tree.tag_configure("cukup",     foreground=C["warning"])
        self._tree.tag_configure("perlu",     foreground=C["error"])

        self._tree.bind("<Double-1>", lambda e: self._detail())

        self._sbar = ctk.CTkLabel(self, text="",
            font=F_NANO, text_color=C["text_muted"])
        self._sbar.pack(anchor="w", padx=24, pady=4)

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
            text=f"  Menampilkan {len(rows)} dari {db.statistik()['total']} mahasiswa")

    def _selected_nim(self) -> str | None:
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Perhatian", "Pilih mahasiswa terlebih dahulu.")
            return None
        return sel[0]

    def _form_tambah(self):
        win = ctk.CTkToplevel(self)
        win.title("Tambah Mahasiswa")
        win.geometry("440x320")
        win.resizable(False, False)
        win.configure(fg_color=C["bg_main"])
        win.grab_set()

        ctk.CTkLabel(win,
            text="✦  Tambah Mahasiswa Baru",
            font=F_SUBJUDUL, text_color=C["highlight"],
        ).pack(pady=(28, 18))

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
        _btn(win, "Simpan", simpan, width=300).pack(pady=20)
        e_nim.focus_set()

    def _form_edit(self):
        nim = self._selected_nim()
        if not nim: return
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return

        win = ctk.CTkToplevel(self)
        win.title("Edit Nama")
        win.geometry("440x260")
        win.resizable(False, False)
        win.configure(fg_color=C["bg_main"])
        win.grab_set()

        ctk.CTkLabel(win,
            text=f"✎  Edit Nama  —  NIM {nim}",
            font=F_SUBJUDUL, text_color=C["highlight"],
        ).pack(pady=(28, 18))

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
        _btn(win, "Simpan", simpan, width=300).pack(pady=20)
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
        win.geometry("520x580")
        win.configure(fg_color=C["bg_main"])
        win.grab_set()

        ipk  = db.ipk_mahasiswa(mhs)
        pred = db.predikat(ipk)

        ctk.CTkLabel(win, text=mhs["nama"],
            font=F_JUDUL, text_color=C["text_main"],
        ).pack(padx=24, pady=(22, 2), anchor="w")
        ctk.CTkLabel(win, text=f"NIM {mhs['nim']}",
            font=F_KECIL, text_color=C["text_muted"],
        ).pack(padx=24, anchor="w")

        badge = ctk.CTkFrame(win,
            fg_color=C["surface"], corner_radius=20,
            border_width=1, border_color=C["border_accent"])
        badge.pack(fill="x", padx=24, pady=14)
        ctk.CTkLabel(badge, text=f"{ipk:.2f}",
            font=("Segoe UI Variable", 36, "bold"),
            text_color=C["primary"],
        ).pack(side="left", padx=20, pady=14)
        info = ctk.CTkFrame(badge, fg_color="transparent")
        info.pack(side="left", pady=14)
        ctk.CTkLabel(info, text=pred,
            font=("Segoe UI Variable", 13, "bold"),
            text_color=C["highlight"],
        ).pack(anchor="w")
        ctk.CTkLabel(info,
            text=f"{db.total_sks(mhs)} SKS  ·  Semester terisi: {db.semester_terisi(mhs)}",
            font=F_KECIL, text_color=C["text_muted"],
        ).pack(anchor="w")

        ctk.CTkLabel(win, text="◈  Rincian Semester",
            font=F_SUBJUDUL, text_color=C["secondary"],
        ).pack(padx=24, pady=(4, 6), anchor="w")

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        for smt_key in sorted(mhs["semester"].keys(), key=int):
            data = mhs["semester"][smt_key]
            ips  = db.hitung_ips(data)

            smt_hdr = ctk.CTkFrame(scroll,
                fg_color=C["surface_elevated"], corner_radius=14)
            smt_hdr.pack(fill="x", pady=(8, 2))
            ctk.CTkLabel(smt_hdr, text=f"Semester {smt_key}",
                font=("Segoe UI Variable", 11, "bold"),
                text_color=C["secondary"],
            ).pack(side="left", padx=14, pady=8)
            ctk.CTkLabel(smt_hdr, text=f"IPS: {ips:.2f}",
                font=("Segoe UI Variable", 11, "bold"),
                text_color=C["success"],
            ).pack(side="right", padx=14)

            for mk in data:
                row = ctk.CTkFrame(scroll,
                    fg_color=C["surface"],
                    border_width=1, border_color=C["border_solid"],
                    corner_radius=12)
                row.pack(fill="x", pady=1)
                ctk.CTkLabel(row, text=mk["nama"],
                    font=F_NORMAL, text_color=C["text_main"],
                ).pack(side="left", padx=14, pady=6)
                ctk.CTkLabel(row, text=f"SKS {mk['sks']}",
                    font=F_KECIL, text_color=C["text_muted"],
                ).pack(side="right", padx=8)
                ctk.CTkLabel(row,
                    text=f"{mk['nilai']:.0f}  /  {mk['grade']}",
                    font=("Segoe UI Variable", 10, "bold"),
                    text_color=C["secondary"],
                ).pack(side="right", padx=10)


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
        # Top panel
        top = ctk.CTkFrame(self,
            fg_color=C["surface"], corner_radius=0,
            border_width=0)
        top.pack(fill="x")

        row1 = ctk.CTkFrame(top, fg_color="transparent")
        row1.pack(fill="x", padx=24, pady=16)

        ctk.CTkLabel(row1, text="◈  Mahasiswa",
            font=("Segoe UI Variable", 9, "bold"),
            text_color=C["secondary"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        self._search = ctk.CTkEntry(row1, width=280, height=38,
            placeholder_text="Cari NIM atau nama...",
            font=("Segoe UI Variable", 11),
            corner_radius=10,
            border_width=1,
            border_color=C["border_glow"],
            fg_color=C["surface_elevated"],
            text_color=C["text_main"],
            placeholder_text_color=C["text_muted"],
        )
        self._search.grid(row=1, column=0, padx=(0, 16))
        self._search.bind("<KeyRelease>", self._update_dropdown)

        self._dd_var  = tk.StringVar()
        self._dd_data = {}
        self._combo   = ttk.Combobox(row1, textvariable=self._dd_var,
            state="readonly", width=32,
            font=("Segoe UI Variable", 10))
        self._combo.grid(row=1, column=1, padx=(0, 16))
        self._combo.bind("<<ComboboxSelected>>", self._pilih_mahasiswa)
        self._combo.configure(background=C["surface_elevated"],
                              foreground=C["text_main"])

        ctk.CTkLabel(row1, text="◈  Semester",
            font=("Segoe UI Variable", 9, "bold"),
            text_color=C["secondary"],
        ).grid(row=0, column=2, sticky="w", pady=(0, 4))
        self._smt_var = tk.StringVar(value="1")
        smt_cb = ttk.Combobox(row1, textvariable=self._smt_var,
            values=["1", "2", "3", "4", "5", "6"],
            state="readonly", width=10,
            font=("Segoe UI Variable", 10))
        smt_cb.grid(row=1, column=2)
        smt_cb.bind("<<ComboboxSelected>>", self._load_form)
        smt_cb.configure(background=C["surface_elevated"],
                         foreground=C["text_main"])

        row1.columnconfigure((0, 1, 2), pad=8)

        info_frame = ctk.CTkFrame(top, fg_color="transparent")
        info_frame.pack(fill="x", padx=24, pady=(4, 12))
        ctk.CTkFrame(info_frame, width=3, height=22,
            fg_color=C["secondary"], corner_radius=2,
        ).pack(side="left", padx=(0, 10))
        self._lbl_info = ctk.CTkLabel(info_frame, text="",
            font=("Segoe UI Variable", 10, "bold"),
            text_color=C["text_main"])
        self._lbl_info.pack(side="left")

        # Neon separator
        ctk.CTkFrame(self, height=1,
            fg_color=C["border_glow"], corner_radius=0,
        ).pack(fill="x")

        self._form_card = ctk.CTkFrame(self,
            fg_color=C["surface"], corner_radius=0,
            border_width=0)
        self._form_card.pack(fill="both", expand=True)

        self._placeholder()
        self._update_dropdown()

    def _placeholder(self):
        for w in self._form_card.winfo_children():
            w.destroy()
        ctk.CTkLabel(self._form_card,
            text="◈  Pilih mahasiswa dan semester untuk mulai input nilai.",
            font=F_NORMAL, text_color=C["text_muted"],
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
                text=f"IPK saat ini: {ipk:.2f}  ·  Semester sudah terisi: {terisi}")
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
        ctk.CTkLabel(header,
            text=f"◉  Nilai Semester {smt}",
            font=F_SUBJUDUL, text_color=C["text_main"],
        ).pack(side="left")

        semua    = db.get_semua()
        mhs      = next((m for m in semua if m["nim"] == self._nim_aktif), None)
        existing = mhs["semester"].get(str(smt), []) if mhs else []

        scroll = ctk.CTkScrollableFrame(self._form_card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        for i, (nama_mk, sks) in enumerate(matkul):
            row = ctk.CTkFrame(scroll,
                fg_color=C["surface_elevated"],
                corner_radius=14,
                border_width=1,
                border_color=C["border_solid"])
            row.pack(fill="x", pady=5)

            mk_frame = ctk.CTkFrame(row, fg_color="transparent")
            mk_frame.pack(side="left", fill="x", expand=True, padx=(14, 0), pady=10)

            ctk.CTkLabel(mk_frame, text=nama_mk,
                font=("Segoe UI Variable", 11, "bold"),
                text_color=C["text_main"], anchor="w",
                wraplength=340,
            ).pack(anchor="w")
            ctk.CTkLabel(mk_frame,
                text=f"✦  {sks} SKS",
                font=F_NANO, text_color=C["secondary"],
            ).pack(anchor="w", pady=(2, 0))

            ctk.CTkFrame(row, width=1, height=28,
                fg_color=C["border_solid"],
            ).pack(side="left", padx=14, pady=8)

            grade_lbl = ctk.CTkLabel(row, text="--", width=40, height=32,
                font=("Segoe UI Variable", 11, "bold"),
                text_color=C["text_muted"],
                corner_radius=10,
                fg_color=C["surface"])
            grade_lbl.pack(side="right", padx=(0, 8), pady=8)

            e = ctk.CTkEntry(row, width=70, height=32,
                font=("Segoe UI Variable", 11, "bold"),
                corner_radius=10, justify="center",
                placeholder_text="0-100",
                border_width=1, border_color=C["border_accent"],
                fg_color=C["surface"])
            e.pack(side="right", padx=(0, 8), pady=8)

            if i < len(existing):
                e.insert(0, str(int(existing[i]["nilai"])))

            def update_grade(event, el=e, gl=grade_lbl):
                try:
                    g, _ = db.nilai_ke_grade(float(el.get()))
                    colors = {
                        "A":  C["success"],  "A-": C["success"],
                        "B+": "#16A34A",     "B":  C["secondary"],
                        "B-": C["secondary"],"C+": C["warning"],
                        "C":  C["warning"],  "D":  C["error"],
                        "E":  C["error"],
                    }
                    gl.configure(text=g, text_color=colors.get(g, C["text_muted"]),
                        fg_color=C["surface_elevated"])
                except Exception:
                    gl.configure(text="--", text_color=C["text_muted"],
                        fg_color=C["surface"])

            e.bind("<KeyRelease>", update_grade)
            update_grade(None, e, grade_lbl)
            self._entries.append(e)

        for i in range(len(self._entries) - 1):
            nxt = self._entries[i + 1]
            self._entries[i].bind("<Return>", lambda ev, n=nxt: n.focus_set())

        foot = ctk.CTkFrame(self._form_card, fg_color="transparent")
        foot.pack(fill="x", padx=20, pady=12)
        _btn(foot, "◉  Simpan Nilai", self._simpan, width=180).pack(side="right")
        _btn(foot, "Batal", self._placeholder,
             color=C["text_muted"], width=100).pack(side="right", padx=(0, 8))

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
            text=f"IPK saat ini: {ipk:.2f}  ·  Semester sudah terisi: {terisi}")
        self._load_form()


# ============================================================
# HALAMAN STATISTIK
# ============================================================

class HalamanStatistik(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Statistik Kelas", "Visualisasi data akademik seluruh mahasiswa")
        self._build()

    def _build(self):
        bar = ctk.CTkFrame(self, fg_color=C["surface"], height=50, corner_radius=0)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        inner_bar = ctk.CTkFrame(bar, fg_color="transparent")
        inner_bar.pack(fill="x", padx=24, pady=8)

        self._filter_smt = tk.StringVar(value="Semua")
        ctk.CTkLabel(inner_bar, text="Filter Semester:",
            font=F_KECIL, text_color=C["text_muted"],
        ).pack(side="left", padx=(0, 8))

        smt_opts = ["Semua", "1", "2", "3", "4", "5", "6"]
        smt_cb = ttk.Combobox(inner_bar, textvariable=self._filter_smt,
            values=smt_opts, state="readonly", width=10,
            font=("Segoe UI Variable", 10))
        smt_cb.pack(side="left")
        smt_cb.bind("<<ComboboxSelected>>", lambda *_: self.refresh())
        smt_cb.configure(background=C["surface_elevated"], foreground=C["text_main"])

        _btn(inner_bar, "⟳  Refresh", self.refresh, width=110, height=32,
             ).pack(side="right")

        ctk.CTkFrame(self, height=1,
            fg_color=C["border_glow"], corner_radius=0,
        ).pack(fill="x")

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=(12, 0))

        # Row 1: IPK bar + Predikat pie
        row1 = ctk.CTkFrame(scroll, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 12))
        row1.columnconfigure(0, weight=3)
        row1.columnconfigure(1, weight=2)

        card_ipk = self._card(row1)
        card_ipk.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        ctk.CTkLabel(card_ipk, text="◈  Distribusi Rentang IPK",
            font=F_SUBJUDUL, text_color=C["text_main"],
        ).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_ipk = tk.Canvas(card_ipk, height=220,
            bg=C["surface_glass"], highlightthickness=0)
        self._canvas_ipk.pack(fill="x", padx=16, pady=(0, 14))

        card_pred = self._card(row1)
        card_pred.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        ctk.CTkLabel(card_pred, text="◉  Sebaran Predikat",
            font=F_SUBJUDUL, text_color=C["text_main"],
        ).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_pred = tk.Canvas(card_pred, height=220,
            bg=C["surface_glass"], highlightthickness=0)
        self._canvas_pred.pack(fill="x", padx=16, pady=(0, 14))

        # Row 2: IPS line chart
        card_ips = self._card(scroll)
        card_ips.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card_ips, text="◈  Rata-rata IPS per Semester",
            font=F_SUBJUDUL, text_color=C["text_main"],
        ).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_ips = tk.Canvas(card_ips, height=200,
            bg=C["surface_glass"], highlightthickness=0)
        self._canvas_ips.pack(fill="x", padx=16, pady=(0, 14))

        # Row 3: Grade distribution
        card_grade = self._card(scroll)
        card_grade.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card_grade, text="◉  Distribusi Grade (Semua Mata Kuliah)",
            font=F_SUBJUDUL, text_color=C["text_main"],
        ).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_grade = tk.Canvas(card_grade, height=200,
            bg=C["surface_glass"], highlightthickness=0)
        self._canvas_grade.pack(fill="x", padx=16, pady=(0, 14))

        # Row 4: Summary
        card_sum = self._card(scroll)
        card_sum.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(card_sum, text="✦  Ringkasan Statistik",
            font=F_SUBJUDUL, text_color=C["text_main"],
        ).pack(padx=16, pady=(14, 6), anchor="w")
        self._sum_frame = ctk.CTkFrame(card_sum, fg_color="transparent")
        self._sum_frame.pack(fill="x", padx=16, pady=(0, 14))

        self.refresh()

    def _get_data(self):
        semua = db.get_semua()
        filter_smt = self._filter_smt.get()

        ipk_list = []
        for m in semua:
            if not m["semester"]:
                continue
            if filter_smt != "Semua":
                if filter_smt not in m["semester"]:
                    continue
            ipk_list.append(db.ipk_mahasiswa(m))

        rentang = [
            ("0.00 - 1.99", 0), ("2.00 - 2.49", 0),
            ("2.50 - 2.99", 0), ("3.00 - 3.49", 0),
            ("3.50 - 3.74", 0), ("3.75 - 4.00", 0),
        ]
        for ipk in ipk_list:
            if ipk < 2.0:   rentang[0] = (rentang[0][0], rentang[0][1] + 1)
            elif ipk < 2.5: rentang[1] = (rentang[1][0], rentang[1][1] + 1)
            elif ipk < 3.0: rentang[2] = (rentang[2][0], rentang[2][1] + 1)
            elif ipk < 3.5: rentang[3] = (rentang[3][0], rentang[3][1] + 1)
            elif ipk < 3.75:rentang[4] = (rentang[4][0], rentang[4][1] + 1)
            else:           rentang[5] = (rentang[5][0], rentang[5][1] + 1)

        pred_dist = {"Cumlaude": 0, "Sangat Baik": 0, "Baik": 0,
                     "Cukup": 0, "Perlu Perbaikan": 0}
        for ipk in ipk_list:
            p = db.predikat(ipk)
            pred_dist[p] = pred_dist.get(p, 0) + 1

        ips_per_smt = {}
        grade_dist  = {}
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
        self.update_idletasks()

        colors_ipk = [
            C["merah"], C["kuning"], "#F59E0B",
            C["biru"], C["hijau"], "#059669"
        ]
        Chart.bar(self._canvas_ipk, data["rentang"],
                  colors=colors_ipk, title="Jumlah mahasiswa per rentang IPK")

        pred_data = [(k, v) for k, v in data["pred_dist"].items() if v > 0]
        pred_colors = [C["ungu"], C["hijau"], C["biru"], C["kuning"], C["merah"]]
        Chart.pie(self._canvas_pred, pred_data,
                  colors=pred_colors, title="Sebaran predikat mahasiswa")

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

        grade_order = ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "E"]
        grade_data = [(g, data["grade_dist"].get(g, 0)) for g in grade_order]
        grade_colors = [
            "#059669", "#16A34A", "#22C55E", "#4ADE80", "#86EFAC",
            "#F59E0B", "#D97706", "#EA580C", "#DC2626"
        ]
        Chart.column(self._canvas_grade, grade_data,
                     colors=grade_colors,
                     title="Distribusi grade seluruh mata kuliah")

        for w in self._sum_frame.winfo_children():
            w.destroy()

        ipk_list = data["ipk_list"]
        stats = [
            ("Mahasiswa Dinilai",     str(len(ipk_list)),
             C["secondary"]),
            ("Rata-rata IPK",
             f"{sum(ipk_list)/len(ipk_list):.2f}" if ipk_list else "0.00",
             C["highlight"]),
            ("IPK Tertinggi",
             f"{max(ipk_list):.2f}" if ipk_list else "0.00",
             C["success"]),
            ("IPK Terendah",
             f"{min(ipk_list):.2f}" if ipk_list else "0.00",
             C["error"]),
            ("Total Terdaftar",       str(data["total"]),
             C["text_main"]),
        ]

        self._sum_frame.columnconfigure(tuple(range(len(stats))), weight=1, uniform="s")
        for col, (label, val, color) in enumerate(stats):
            box = ctk.CTkFrame(self._sum_frame,
                fg_color=C["surface_elevated"],
                corner_radius=16,
                border_width=1,
                border_color=C["border_glow"])
            box.grid(row=0, column=col, padx=6, sticky="nsew")
            ctk.CTkLabel(box, text=label,
                font=("Segoe UI Variable", 8),
                text_color=C["text_muted"],
            ).pack(padx=12, pady=(10, 2), anchor="w")
            ctk.CTkLabel(box, text=val,
                font=("Segoe UI Variable", 22, "bold"),
                text_color=color,
            ).pack(padx=12, pady=(0, 10), anchor="w")


# ============================================================
# HALAMAN RIWAYAT
# ============================================================

class HalamanRiwayat(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Riwayat Aktivitas", "Log 20 operasi terakhir")
        _style_tree()
        self._build()

    def _build(self):
        toolbar = ctk.CTkFrame(self,
            fg_color=C["surface"], corner_radius=0, height=50)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        _btn(toolbar, "⟳  Refresh", self.refresh,
             width=110, height=32,
             ).pack(side="right", padx=16, pady=9)

        ctk.CTkFrame(self, height=1,
            fg_color=C["border_glow"], corner_radius=0,
        ).pack(fill="x")

        card = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0)
        card.pack(fill="both", expand=True)

        cols = ("waktu", "aksi", "detail")
        self._tree = ttk.Treeview(card, columns=cols, show="headings",
            style="App.Treeview")
        self._tree.heading("waktu",  text="Waktu",  anchor="center")
        self._tree.heading("aksi",   text="Aksi",   anchor="center")
        self._tree.heading("detail", text="Detail", anchor="w")
        self._tree.column("waktu",  width=160, anchor="center")
        self._tree.column("aksi",   width=100, anchor="center")
        self._tree.column("detail", width=500, anchor="w")

        self._tree.tag_configure("TAMBAH", foreground=C["success"])
        self._tree.tag_configure("HAPUS",  foreground=C["error"])
        self._tree.tag_configure("NILAI",  foreground=C["secondary"])
        self._tree.tag_configure("EDIT",   foreground=C["warning"])

        vsb = ttk.Scrollbar(card, orient="vertical",
                            command=self._tree.yview,
                            style="Vertical.TScrollbar")
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
# HALAMAN LOGIN — NOVA GALAXY REDESIGN
# ============================================================

class HalamanLogin(ctk.CTkFrame):

    def __init__(self, parent, on_login):
        super().__init__(parent, corner_radius=0, fg_color=C["bg_main"])
        self._on_login = on_login
        self._build()

    def _build(self):
        # ── Star field canvas background ───────────────────
        stars_canvas = tk.Canvas(self, bg=C["bg_main"], highlightthickness=0)
        stars_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._paint_stars(stars_canvas)

        # ── Left branding panel ────────────────────────────
        kiri = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0)
        kiri.place(relx=0, rely=0, relwidth=0.46, relheight=1)

        # Neon right border on left panel
        ctk.CTkFrame(kiri, width=2, fg_color=C["primary"],
                     corner_radius=0).place(relx=1.0, x=-2, y=0, relheight=1)

        # Glowing orbit rings (simulated with canvas)
        orbit_canvas = tk.Canvas(kiri, bg=C["surface"], highlightthickness=0,
                                 width=360, height=360)
        orbit_canvas.place(relx=0.5, rely=0.38, anchor="center")
        self._draw_orbits(orbit_canvas)

        # Logo text centered on orbit
        ctk.CTkLabel(kiri,
            text="✦",
            font=("Segoe UI Variable", 56, "bold"),
            text_color=C["highlight"],
        ).place(relx=0.5, rely=0.34, anchor="center")

        ctk.CTkLabel(kiri,
            text="SIMA",
            font=("Segoe UI Variable", 44, "bold"),
            text_color=C["text_main"],
        ).place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkLabel(kiri,
            text="Nova Galaxy Edition",
            font=("Segoe UI Variable", 13, "bold"),
            text_color=C["secondary"],
        ).place(relx=0.5, rely=0.53, anchor="center")

        ctk.CTkLabel(kiri,
            text="Sistem Informasi Akademik Mahasiswa\nPendidikan Teknik Otomasi Industri & Robotika",
            font=("Segoe UI Variable", 11),
            text_color=C["text_muted"],
            justify="center",
        ).place(relx=0.5, rely=0.63, anchor="center")

        # Version tag
        ctk.CTkFrame(kiri,
            fg_color=C["info_bg"],
            corner_radius=20,
            border_width=1,
            border_color=C["border_accent"],
            width=140, height=28,
        ).place(relx=0.5, rely=0.74, anchor="center")
        ctk.CTkLabel(kiri,
            text="v3.0 · 2025 · Galaxy",
            font=F_NANO,
            text_color=C["highlight"],
        ).place(relx=0.5, rely=0.74, anchor="center")

        # ── Right login panel ──────────────────────────────
        kanan = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        kanan.place(relx=0.46, rely=0, relwidth=0.54, relheight=1)

        # Centered glass card
        card = ctk.CTkFrame(kanan,
            fg_color=C["surface"],
            width=420, corner_radius=28,
            border_width=1, border_color=C["border_accent"])
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Card top neon line
        ctk.CTkFrame(card, height=3,
            fg_color=C["primary"], corner_radius=2,
        ).pack(fill="x", padx=0, pady=0)

        # Header
        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=40, pady=(28, 10))

        ctk.CTkLabel(hdr,
            text="Masuk ke Sistem",
            font=("Segoe UI Variable", 24, "bold"),
            text_color=C["text_main"],
        ).pack(anchor="w")
        ctk.CTkLabel(hdr,
            text="Autentikasi diperlukan untuk melanjutkan",
            font=F_KECIL, text_color=C["text_muted"],
        ).pack(anchor="w", pady=(6, 0))

        # Separator
        ctk.CTkFrame(card, height=1,
            fg_color=C["border_glow"],
        ).pack(fill="x", padx=40, pady=(12, 0))

        # Form
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(fill="x", padx=40, pady=(18, 10))

        ctk.CTkLabel(form, text="Username",
            font=("Segoe UI Variable", 10, "bold"),
            text_color=C["text_secondary"],
        ).pack(anchor="w")
        self._e_user = _entry(form, placeholder="Masukkan username", width=340)
        self._e_user.pack(pady=(6, 16))

        ctk.CTkLabel(form, text="Password",
            font=("Segoe UI Variable", 10, "bold"),
            text_color=C["text_secondary"],
        ).pack(anchor="w")
        self._e_pass = _entry(form, placeholder="Masukkan password", show="*", width=340)
        self._e_pass.pack(pady=(6, 6))

        _bind_enter_chain([self._e_user, self._e_pass])
        self._e_pass.bind("<Return>", lambda e: self._login())

        _btn(card, "⬡  Masuk ke Sistem", self._login,
             width=340, height=48, style="primary").pack(pady=(8, 6))

        self._lbl_err = ctk.CTkLabel(card, text="",
            font=F_KECIL, text_color=C["error_glow"])
        self._lbl_err.pack(pady=(0, 28))

        self._e_user.focus_set()

    def _paint_stars(self, canvas):
        import random
        random.seed(7)
        self.update_idletasks()
        w = self.winfo_width() or 1280
        h = self.winfo_height() or 740
        for _ in range(180):
            x = random.randint(0, w)
            y = random.randint(0, h)
            r = random.choice([1, 1, 1, 1, 2])
            col = random.choice([
                "#ffffff", "#b6b8d6", "#2b3a67",
                "#4c3080", "#164e6b",
            ])
            canvas.create_oval(x-r, y-r, x+r, y+r, fill=col, outline="")

    def _draw_orbits(self, canvas):
        cx, cy = 180, 180
        for r, col, dash in [
            (140, C["border_glow"],   (4, 8)),
            (100, C["border_accent"], (3, 6)),
            (60,  C["border_cyan"],   (2, 4)),
        ]:
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                               outline=col, width=1, dash=dash)

    def _login(self):
        u = self._e_user.get().strip()
        p = self._e_pass.get()
        if db.cek_login(u, p):
            self._on_login()
        else:
            self._lbl_err.configure(text="✕  Username atau password salah.")


# ============================================================
# APLIKASI UTAMA
# ============================================================

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("SIMA — Andromeda Command Center v4.0")
        self.geometry("1440x820")
        self.minsize(1200, 700)
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
        # Main shell with transparent background
        shell_frame = ctk.CTkFrame(self, fg_color="transparent")
        shell_frame.pack(fill="both", expand=True)

        # Floating mini dock sidebar (left, but not full height)
        self._sidebar = Sidebar(shell_frame, self._navigasi)
        self._sidebar.pack(side="left", fill="y", padx=(16, 8), pady=20)

        # Content area
        self._area = ctk.CTkFrame(shell_frame,
            corner_radius=0, fg_color="transparent")
        self._area.pack(side="left", fill="both", expand=True, padx=(0, 16), pady=20)

        self._dash      = HalamanDashboard(self._area)
        self._mhs       = HalamanMahasiswa(self._area, on_nilai=self._buka_nilai)
        self._nilai     = HalamanNilai(self._area, on_selesai=self._selesai_nilai)
        self._statistik = HalamanStatistik(self._area)
        self._riwayat   = HalamanRiwayat(self._area)

        self._halaman_aktif = None

    def _navigasi(self, key: str):
        if key == "logout":
            if messagebox.askyesno("Konfirmasi Logout",
                    "Yakin ingin keluar dari sistem?"):
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

        if key == "dashboard":  self._dash.refresh()
        if key == "mahasiswa":  self._mhs.refresh()
        if key == "statistik":  self._statistik.refresh()
        if key == "riwayat":    self._riwayat.refresh()

    def _buka_nilai(self, nim: str):
        self._sidebar.aktifkan("nilai")
        self._nilai.set_nim(nim)

    def _selesai_nilai(self):
        self._dash.refresh()
        self._mhs.refresh()

    def _bersih(self):
        for w in self.winfo_children():
            w.destroy()