import sys
import json
import calendar
import math
from datetime import datetime, timedelta
from tkinter import messagebox
import tkinter as tk
import ctypes # Görev çubuğu ikonu için

try:
    import customtkinter as ctk
except ImportError:
    print("CustomTkinter yüklü değil: 'pip install customtkinter'")
    sys.exit(1)

# --- SABİTLER (TEMALAR VE DİL) ---
THEMES = {
    "Midnight": {
        "bg": "#0a0e27", "card": "#151b3d", "sidebar": "#0d1128",
        "accent": "#667eea", "text": "#e2e8f0", "text_dim": "#94a3b8", "danger": "#ef4444"
    },
    "Nordic": {
        "bg": "#2e3440", "card": "#3b4252", "sidebar": "#242933",
        "accent": "#88c0d0", "text": "#eceff4", "text_dim": "#d8dee9", "danger": "#bf616a"
    },
    "Sakura": {
        "bg": "#1a1625", "card": "#2d1b3d", "sidebar": "#231c30",
        "accent": "#e879f9", "text": "#fdf4ff", "text_dim": "#f0abfc", "danger": "#f43f5e"
    },
    "Ocean Deep": {
        "bg": "#0c1821", "card": "#1b2838", "sidebar": "#08131a",
        "accent": "#14b8a6", "text": "#f0fdfa", "text_dim": "#99f6e4", "danger": "#f87171"
    },
    "Monochrome": {
        "bg": "#121212", "card": "#1e1e1e", "sidebar": "#0a0a0a",
        "accent": "#ffffff", "text": "#ffffff", "text_dim": "#a0a0a0", "danger": "#ff5252"
    }
}

TRANSLATIONS = {
    "TR": {
        "app_name": "FocusFlow 2.1",
        "agenda": "📅  Ajanda",
        "notes": "📝  Not Defteri",
        "stats": "📊  İstatistikler",
        "timer": "⏱️  Sayaç",
        "total_time": "⏳  Toplam Süre",
        "settings": "Ayarlar",
        "new_task": "Yeni görev...",
        "no_task": "Görev yok",
        "new_note": "+ Yeni Not",
        "note_title": "Not Başlığı",
        "save": "Kaydet",
        "delete": "Sil",
        "delete_confirm": "Silmek istediğinize emin misiniz?",
        "select_note": "Bir not seçin veya oluşturun",
        "theme": "Tema Seçimi",
        "language": "Dil / Language",
        "data_mgmt": "Veri Yönetimi",
        "delete_all": "TÜM VERİLERİ SİL",
        "delete_all_confirm": "DİKKAT: Tüm veriler silinecek. Devam edilsin mi?",
        "deleted_msg": "Veriler silindi.",
        "apply": "Uygula ve Yenile",
        "weekly_chart": "Haftalık Aktivite",
        "pie_chart": "Tamamlanma Durumu",
        "heatmap": "Aylık Aktivite Haritası",
        "completed": "Tamamlanan",
        "pending": "Bekleyen",
        "today": "Bugün",
        "week": "Bu Hafta",
        "month": "Bu Ay",
        "all_time": "Tümü",
        "start": "Başlat",
        "pause": "Durdur",
        "finish": "Bitir",
        "detach": "Ayır ⧉",
        "timer_task_hint": "Ne üzerinde çalışıyorsun?",
        "timer_saved": "Süre kaydedildi!",
        "total_time_header": "Görev Bazlı Toplam Çalışma Süreleri",
        "no_timer_data": "Henüz sayaç kaydı bulunmuyor.",
        "category": "Kategori",
        "add_cat_title": "Kategori Ekle",
        "add_cat_prompt": "Yeni kategori ismi:",
        "months": ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"],
        "days": ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    },
    "EN": {
        "app_name": "FocusFlow 2.1",
        "agenda": "📅  Agenda",
        "notes": "📝  Notebook",
        "stats": "📊  Statistics",
        "timer": "⏱️  Timer",
        "total_time": "⏳  Total Time",
        "settings": "Settings",
        "new_task": "New task...",
        "no_task": "No tasks",
        "new_note": "+ New Note",
        "note_title": "Note Title",
        "save": "Save",
        "delete": "Delete",
        "delete_confirm": "Are you sure?",
        "select_note": "Select or create a note",
        "theme": "Theme Selection",
        "language": "Language",
        "data_mgmt": "Data Management",
        "delete_all": "DELETE ALL DATA",
        "delete_all_confirm": "All data will be deleted. Proceed?",
        "deleted_msg": "Data deleted.",
        "apply": "Apply & Refresh",
        "weekly_chart": "Weekly Activity",
        "pie_chart": "Completion Status",
        "heatmap": "Monthly Activity Map",
        "completed": "Completed",
        "pending": "Pending",
        "today": "Today",
        "week": "This Week",
        "month": "This Month",
        "all_time": "All Time",
        "start": "Start",
        "pause": "Pause",
        "finish": "Finish",
        "detach": "Detach ⧉",
        "timer_task_hint": "What are you working on?",
        "timer_saved": "Session saved!",
        "total_time_header": "Total Time Spent by Task",
        "no_timer_data": "No timer records found.",
        "category": "Category",
        "add_cat_title": "Add Category",
        "add_cat_prompt": "New category name:",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    }
}

# --- TOOLTIP CLASS ---
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
        self.widget.bind("<Button-1>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tooltip_window or not self.text: return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        self.tooltip_window.attributes('-topmost', True)
        frame = ctk.CTkFrame(self.tooltip_window, fg_color="#1e1e1e", corner_radius=8, border_width=0)
        frame.pack()
        ctk.CTkLabel(frame, text=self.text, text_color="#ffffff", padx=12, pady=8, font=("Arial", 11), justify="left").pack()

    def hide_tip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class PersonalAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Görev Çubuğu İkonu Düzeltme
        myappid = 'mycompany.focusflow.version.2.1'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass
        
        # İkon Yükleme
        try:
            self.iconbitmap("logo.ico")
        except:
            pass # Logo yoksa devam et

        self.config = self.load_config()
        self.current_lang_code = self.config.get("language", "TR")
        self.current_theme_name = self.config.get("theme", "Midnight")
        self.theme = THEMES[self.current_theme_name]
        self.lang = TRANSLATIONS[self.current_lang_code]
        
        self.title("FocusFlow 2.1")
        self.geometry("1200x750")
        self.minsize(900, 600)
        
        self.tasks = self.load_data("agenda_data.json")
        self.notes = self.load_data("notes_data.json")
        self.categories = self.load_data("categories.json")
        if not self.categories: self.categories = ["Genel", "İş", "Ders", "Spor"]
        
        self.selected_date = datetime.now().strftime("%Y-%m-%d")
        self.calendar_date = datetime.now()
        self.heatmap_date = datetime.now()
        
        # Timer Değişkenleri
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_job = None
        self.mini_window = None 
        self._drag_data = {"x": 0, "y": 0}
        
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.theme["bg"])
        
        self.setup_ui()

    def t(self, key):
        return self.lang.get(key, key)

    def setup_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.sidebar = ctk.CTkFrame(self, width=240, fg_color=self.theme["sidebar"], corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.main_area = ctk.CTkFrame(self, fg_color=self.theme["bg"], corner_radius=0)
        self.main_area.pack(side="right", fill="both", expand=True)

        # Logo/Başlık
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(50, 60))
        
        ctk.CTkLabel(logo_frame, text=self.t("app_name"), font=("Arial", 26, "bold"), 
                     text_color=self.theme["accent"]).pack()
        ctk.CTkLabel(logo_frame, text="━━━━━━━━", font=("Arial", 8), 
                     text_color=self.theme["accent"]).pack()
        
        self.btn_agenda = self.create_menu_btn(self.t("agenda"), self.show_agenda)
        self.btn_notes = self.create_menu_btn(self.t("notes"), self.show_notes)
        self.btn_timer = self.create_menu_btn(self.t("timer"), self.show_timer)
        self.btn_stats = self.create_menu_btn(self.t("stats"), self.show_stats)
        self.btn_total = self.create_menu_btn(self.t("total_time"), self.show_total_time)
        
        self.top_bar = ctk.CTkFrame(self.main_area, height=60, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=30, pady=(20, 0))
        
        settings_btn = ctk.CTkButton(self.top_bar, text="⚙", width=44, height=44,
                                     fg_color=self.theme["card"], hover_color=self.theme["accent"],
                                     text_color=self.theme["text_dim"], font=("Arial", 22),
                                     corner_radius=22, border_width=0, command=self.open_settings)
        settings_btn.pack(side="right")

        self.view_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.view_frame.pack(fill="both", expand=True, padx=30, pady=20)

        self.reset_active_states()
        self.show_agenda()

    def create_menu_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, anchor="w", height=52,
                            fg_color="transparent", hover_color=self.theme["card"],
                            text_color=self.theme["text_dim"], font=("Arial", 15, "normal"),
                            command=command, border_spacing=15)
        btn.pack(fill="x", padx=15, pady=4)
        return btn

    def set_active_menu(self, active_btn):
        self.btn_agenda.configure(fg_color="transparent", text_color=self.theme["text_dim"], font=("Arial", 15, "normal"))
        self.btn_notes.configure(fg_color="transparent", text_color=self.theme["text_dim"], font=("Arial", 15, "normal"))
        self.btn_stats.configure(fg_color="transparent", text_color=self.theme["text_dim"], font=("Arial", 15, "normal"))
        self.btn_timer.configure(fg_color="transparent", text_color=self.theme["text_dim"], font=("Arial", 15, "normal"))
        self.btn_total.configure(fg_color="transparent", text_color=self.theme["text_dim"], font=("Arial", 15, "normal"))
        active_btn.configure(fg_color=self.theme["card"], text_color=self.theme["accent"], font=("Arial", 15, "bold"))

    def reset_active_states(self):
        self.agenda_active = False 
        self.notes_active = False
        self.stats_active = False
        self.timer_active = False
        self.total_active = False

    def clear_view(self):
        for widget in self.view_frame.winfo_children():
            widget.destroy()

    # --- AJANDA ---
    def show_agenda(self):
        if hasattr(self, 'agenda_active') and self.agenda_active: return 
        self.reset_active_states()
        self.agenda_active = True
        self.set_active_menu(self.btn_agenda)
        self.clear_view()
        
        split = ctk.CTkFrame(self.view_frame, fg_color="transparent")
        split.pack(fill="both", expand=True)
        
        left_panel = ctk.CTkFrame(split, width=380, fg_color=self.theme["card"], corner_radius=16)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)
        
        cal_header = ctk.CTkFrame(left_panel, fg_color="transparent")
        cal_header.pack(fill="x", padx=25, pady=(30, 20))
        
        ctk.CTkButton(cal_header, text="‹", width=36, height=36, fg_color="transparent", 
                     text_color=self.theme["text"], hover_color=self.theme["bg"],
                     font=("Arial", 20), border_width=0,
                     command=lambda: self.change_month(-1)).pack(side="left")
        
        self.month_label = ctk.CTkLabel(cal_header, text="", font=("Arial", 18, "bold"), text_color=self.theme["text"])
        self.month_label.pack(side="left", expand=True)
        
        ctk.CTkButton(cal_header, text="›", width=36, height=36, fg_color="transparent", 
                     text_color=self.theme["text"], hover_color=self.theme["bg"],
                     font=("Arial", 20), border_width=0,
                     command=lambda: self.change_month(1)).pack(side="right")
        
        self.cal_grid_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.cal_grid_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        right_panel = ctk.CTkFrame(split, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.date_label = ctk.CTkLabel(right_panel, text="", font=("Arial", 24, "bold"), text_color=self.theme["text"])
        self.date_label.pack(anchor="w", pady=(0, 20))
        
        input_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 20))
        
        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text=self.t("new_task"), height=50,
                                      fg_color=self.theme["card"], border_width=0, text_color=self.theme["text"],
                                      font=("Arial", 14), corner_radius=12)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        ctk.CTkButton(input_frame, text="+", width=50, height=50,
                     fg_color=self.theme["accent"], hover_color=self.theme["accent"],
                     text_color=self.theme["bg"], corner_radius=25, font=("Arial", 24, "bold"),
                     border_width=0, command=self.add_task).pack(side="right")
        
        self.task_list_frame = ctk.CTkScrollableFrame(right_panel, fg_color=self.theme["card"], corner_radius=16)
        self.task_list_frame.pack(fill="both", expand=True)
        
        self.render_calendar_grid()
        self.refresh_task_list()
        self.update_date_labels()

    def render_calendar_grid(self):
        for w in self.cal_grid_frame.winfo_children(): w.destroy()
        
        months_list = self.t("months")
        self.month_label.configure(text=f"{months_list[self.calendar_date.month-1]} {self.calendar_date.year}")
        
        days_list = self.t("days")
        
        for i, d in enumerate(days_list):
            self.cal_grid_frame.columnconfigure(i, weight=1, uniform="day_col")
            ctk.CTkLabel(self.cal_grid_frame, text=d, text_color=self.theme["text_dim"], 
                         font=("Arial", 11, "bold")).grid(row=0, column=i, pady=(0, 10))
        
        self.cal_grid_frame.rowconfigure(0, weight=0)

        month_days = calendar.monthcalendar(self.calendar_date.year, self.calendar_date.month)
        
        for r, week in enumerate(month_days):
            self.cal_grid_frame.rowconfigure(r+1, weight=1, uniform="week_row")
            
            for c, day in enumerate(week):
                if day != 0:  
                    date_str = f"{self.calendar_date.year}-{self.calendar_date.month:02d}-{day:02d}"
                    is_sel = (date_str == self.selected_date)
                    has_task = any(t["date"] == date_str for t in self.tasks)
                    
                    if is_sel:
                        bg = self.theme["accent"]
                        fg = self.theme["bg"]
                        font_style = ("Arial", 13, "bold")
                    elif has_task:
                        bg = self.theme["bg"]
                        fg = self.theme["text"]
                        font_style = ("Arial", 13, "normal")
                    else:
                        bg = "transparent"
                        fg = self.theme["text_dim"]
                        font_style = ("Arial", 13, "normal")
                    
                    btn = ctk.CTkButton(self.cal_grid_frame, text=str(day), width=0, height=0, fg_color=bg,
                                      text_color=fg, hover_color=self.theme["accent"], corner_radius=19,
                                      font=font_style, border_width=0,
                                      command=lambda d=date_str: self.select_date(d))
                    btn.grid(row=r+1, column=c, padx=3, pady=3, sticky="nsew")

    def change_month(self, d):
        m, y = self.calendar_date.month + d, self.calendar_date.year
        if m > 12: m, y = 1, y + 1
        elif m < 1: m, y = 12, y - 1
        self.calendar_date = self.calendar_date.replace(year=y, month=m, day=1)
        self.render_calendar_grid()

    def select_date(self, date_str):
        self.selected_date = date_str
        self.render_calendar_grid()
        self.refresh_task_list()
        self.update_date_labels()

    def update_date_labels(self):
        try:
            dt = datetime.strptime(self.selected_date, "%Y-%m-%d")
            self.date_label.configure(text=dt.strftime("%d.%m.%Y"))
        except: pass

    def refresh_task_list(self):
        for w in self.task_list_frame.winfo_children(): w.destroy()
        tasks = [t for t in self.tasks if t["date"] == self.selected_date]
        if not tasks:
            ctk.CTkLabel(self.task_list_frame, text=self.t("no_task"), text_color=self.theme["text_dim"], 
                         font=("Arial", 14)).pack(pady=40)
            return
        for task in tasks:
            f = ctk.CTkFrame(self.task_list_frame, fg_color="transparent")
            f.pack(fill="x", pady=6, padx=8)
            done = task["done"]
            chk = ctk.CTkButton(f, text="✓" if done else "", width=28, height=28, corner_radius=14,
                               fg_color=self.theme["accent"] if done else "transparent", border_width=2,
                               border_color=self.theme["accent"], text_color=self.theme["bg"],
                               font=("Arial", 14, "bold"),
                               command=lambda t=task: self.toggle_task(t))
            chk.pack(side="left", padx=(0, 12))
            lbl = ctk.CTkLabel(f, text=task["task"], text_color=self.theme["text_dim"] if done else self.theme["text"],
                              font=("Arial", 14))
            lbl.pack(side="left", padx=0, fill="x", expand=True)
            ctk.CTkButton(f, text="✕", width=32, height=32, fg_color="transparent", hover_color=self.theme["danger"],
                         text_color=self.theme["text_dim"], font=("Arial", 16),
                         command=lambda t=task: self.delete_task(t)).pack(side="right")

    def add_task(self):
        txt = self.task_entry.get().strip()
        if txt:
            self.tasks.append({"task": txt, "date": self.selected_date, "done": False})
            self.save_data("agenda_data.json", self.tasks)
            self.task_entry.delete(0, "end")
            self.refresh_task_list()
            self.render_calendar_grid()

    def toggle_task(self, task):
        task["done"] = not task["done"]
        self.save_data("agenda_data.json", self.tasks)
        self.refresh_task_list()

    def delete_task(self, task):
        self.tasks.remove(task)
        self.save_data("agenda_data.json", self.tasks)
        self.refresh_task_list()
        self.render_calendar_grid()

    # --- NOT DEFTERİ ---
    def show_notes(self):
        if hasattr(self, 'notes_active') and self.notes_active: return
        self.reset_active_states()
        self.notes_active = True
        self.set_active_menu(self.btn_notes)
        self.clear_view()
        
        split = ctk.CTkFrame(self.view_frame, fg_color="transparent")
        split.pack(fill="both", expand=True)
        
        list_panel = ctk.CTkFrame(split, width=280, fg_color=self.theme["card"], corner_radius=16)
        list_panel.pack(side="left", fill="y", padx=(0, 20))
        list_panel.pack_propagate(False)
        
        ctk.CTkButton(list_panel, text=self.t("new_note"), fg_color=self.theme["accent"], text_color=self.theme["bg"],
                      font=("Arial", 14, "bold"), height=48, corner_radius=12, border_width=0,
                      command=self.create_new_note).pack(fill="x", padx=20, pady=20)
        
        self.note_list_frame = ctk.CTkScrollableFrame(list_panel, fg_color="transparent")
        self.note_list_frame.pack(fill="both", expand=True, padx=8)
        
        self.editor_panel = ctk.CTkFrame(split, fg_color=self.theme["card"], corner_radius=16)
        self.editor_panel.pack(side="right", fill="both", expand=True)
        
        self.refresh_note_list()
        self.show_empty_editor()

    def show_empty_editor(self):
        for w in self.editor_panel.winfo_children(): w.destroy()
        ctk.CTkLabel(self.editor_panel, text=self.t("select_note"), 
                     text_color=self.theme["text_dim"], font=("Arial", 15)).pack(expand=True)

    def refresh_note_list(self):
        for w in self.note_list_frame.winfo_children(): w.destroy()
        for i, note in enumerate(reversed(self.notes)):
            idx = len(self.notes) - 1 - i
            btn = ctk.CTkButton(self.note_list_frame, text=note.get("title", "Başlıksız"), anchor="w",
                                fg_color="transparent", hover_color=self.theme["bg"], text_color=self.theme["text"],
                                font=("Arial", 14), height=44, corner_radius=10,
                                command=lambda x=idx: self.load_note_editor(x))
            btn.pack(fill="x", pady=3, padx=4)

    def create_new_note(self):
        self.load_note_editor(None)

    def load_note_editor(self, index):
        for w in self.editor_panel.winfo_children(): w.destroy()
        current_note = self.notes[index] if index is not None else {"title": "", "content": ""}
        
        title_entry = ctk.CTkEntry(self.editor_panel, placeholder_text=self.t("note_title"), 
                                  font=("Arial", 22, "bold"), fg_color=self.theme["bg"],
                                  text_color=self.theme["text"], border_width=0, height=60, corner_radius=12)
        title_entry.pack(fill="x", padx=25, pady=(25, 15))
        title_entry.insert(0, current_note["title"])
        
        content_txt = ctk.CTkTextbox(self.editor_panel, fg_color=self.theme["bg"], text_color=self.theme["text"], 
                                    font=("Arial", 14), corner_radius=12, border_width=0)
        content_txt.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        content_txt.insert("0.0", current_note["content"])
        
        btn_frame = ctk.CTkFrame(self.editor_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=(0, 25))
        
        if index is not None:
            ctk.CTkButton(btn_frame, text=self.t("delete"), fg_color=self.theme["danger"], width=100, height=44,
                          font=("Arial", 14, "bold"), corner_radius=12, border_width=0,
                          command=lambda: self.delete_note(index)).pack(side="left")
        
        ctk.CTkButton(btn_frame, text=self.t("save"), fg_color=self.theme["accent"], text_color=self.theme["bg"], 
                      width=120, height=44, font=("Arial", 14, "bold"), corner_radius=12, border_width=0,
                      command=lambda: self.save_note(index, title_entry.get(), content_txt.get("0.0", "end-1c"))).pack(side="right")

    def save_note(self, index, title, content):
        if not title.strip(): return
        note_data = {"title": title, "content": content, "date": datetime.now().strftime("%Y-%m-%d")}
        if index is not None:
            self.notes[index] = note_data
        else:
            self.notes.append(note_data)
            index = len(self.notes) - 1
        self.save_data("notes_data.json", self.notes)
        self.refresh_note_list()
        self.load_note_editor(index)

    def delete_note(self, index):
        if messagebox.askyesno(self.t("delete"), self.t("delete_confirm")):
            del self.notes[index]
            self.save_data("notes_data.json", self.notes)
            self.show_notes()

    # --- SAYAÇ (TIMER) ---
    def show_timer(self):
        if hasattr(self, 'timer_active') and self.timer_active: return
        self.reset_active_states()
        self.timer_active = True
        self.set_active_menu(self.btn_timer)
        self.clear_view()
        
        container = ctk.CTkFrame(self.view_frame, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.timer_label = ctk.CTkLabel(container, text=self.format_timer_time(self.timer_seconds), 
                                        font=("Arial", 92, "bold"), text_color=self.theme["accent"])
        self.timer_label.pack(pady=(0, 40))
        
        # GÖREV & KATEGORİ GİRİŞİ
        input_frame = ctk.CTkFrame(container, fg_color="transparent")
        input_frame.pack(pady=(0, 40))
        
        self.category_var = ctk.StringVar(value=self.categories[0] if self.categories else "Genel")
        self.cat_menu = ctk.CTkComboBox(input_frame, values=self.categories, variable=self.category_var,
                                        width=140, height=48, fg_color=self.theme["card"], 
                                        text_color=self.theme["text"], border_width=0, corner_radius=12,
                                        font=("Arial", 14), dropdown_font=("Arial", 13))
        self.cat_menu.pack(side="left", padx=(0, 8))
        
        ctk.CTkButton(input_frame, text="+", width=48, height=48, fg_color=self.theme["card"], 
                      text_color=self.theme["accent"], font=("Arial", 20), corner_radius=12,
                      command=self.add_category_dialog).pack(side="left", padx=(0, 12))
        
        self.timer_entry = ctk.CTkEntry(input_frame, placeholder_text=self.t("timer_task_hint"),
                                        width=280, height=48, font=("Arial", 14),
                                        fg_color=self.theme["card"], text_color=self.theme["text"], 
                                        border_width=0, corner_radius=12)
        self.timer_entry.pack(side="left")
        
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack()
        
        ctk.CTkButton(btn_frame, text=self.t("start"), width=110, height=48,
                      fg_color=self.theme["accent"], text_color=self.theme["bg"], corner_radius=24,
                      font=("Arial", 14, "bold"), border_width=0,
                      command=self.start_timer).pack(side="left", padx=8)
        
        ctk.CTkButton(btn_frame, text=self.t("pause"), width=110, height=48,
                      fg_color="#f59e0b", text_color="#000000", corner_radius=24,
                      font=("Arial", 14, "bold"), border_width=0,
                      command=self.pause_timer).pack(side="left", padx=8)
        
        ctk.CTkButton(btn_frame, text=self.t("finish"), width=110, height=48,
                      fg_color=self.theme["danger"], text_color="white", corner_radius=24,
                      font=("Arial", 14, "bold"), border_width=0,
                      command=self.reset_timer).pack(side="left", padx=8)
                      
        ctk.CTkButton(btn_frame, text=self.t("save"), width=110, height=48,
                      fg_color="#3b82f6", text_color="white", corner_radius=24,
                      font=("Arial", 14, "bold"), border_width=0,
                      command=self.save_timer_session).pack(side="left", padx=8)
                      
        ctk.CTkButton(btn_frame, text=self.t("detach"), width=90, height=48,
                      fg_color=self.theme["card"], text_color=self.theme["text_dim"], corner_radius=24,
                      font=("Arial", 14, "bold"), border_width=0,
                      command=self.open_mini_timer).pack(side="left", padx=8)

    def add_category_dialog(self):
        dialog = ctk.CTkInputDialog(text=self.t("add_cat_prompt"), title=self.t("add_cat_title"))
        new_cat = dialog.get_input()
        if new_cat:
            new_cat = new_cat.strip()
            if new_cat not in self.categories:
                self.categories.append(new_cat)
                self.save_data("categories.json", self.categories)
                if hasattr(self, 'cat_menu'):
                    self.cat_menu.configure(values=self.categories)
                    self.category_var.set(new_cat)

    # --- MINI TIMER PENCERESİ ---
    def open_mini_timer(self):
        if self.mini_window is not None:
            self.mini_window.lift()
            return
            
        self.mini_window = ctk.CTkToplevel(self)
        self.mini_window.title("Sayaç")
        self.mini_window.geometry("320x140")
        self.mini_window.configure(fg_color=self.theme["bg"])
        self.mini_window.attributes('-topmost', True)
        self.mini_window.overrideredirect(True) 
        
        self.mini_window.bind("<ButtonPress-1>", self.start_move)
        self.mini_window.bind("<ButtonRelease-1>", self.stop_move)
        self.mini_window.bind("<B1-Motion>", self.do_move)
        
        main_frame = ctk.CTkFrame(self.mini_window, fg_color=self.theme["card"], border_width=1, border_color=self.theme["accent"],
                                 corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        close_btn = ctk.CTkButton(main_frame, text="✕", width=28, height=28, fg_color="transparent", 
                                  text_color=self.theme["danger"], hover_color=self.theme["bg"],
                                  font=("Arial", 16), corner_radius=14,
                                  command=self.close_mini_timer)
        close_btn.place(relx=0.97, rely=0.03, anchor="ne")
        
        self.mini_timer_label = ctk.CTkLabel(main_frame, text=self.format_timer_time(self.timer_seconds),
                                            font=("Arial", 42, "bold"), text_color=self.theme["text"])
        self.mini_timer_label.pack(pady=(30, 8))
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=8)
        
        ctk.CTkButton(btn_frame, text="⏯", width=56, height=36, fg_color=self.theme["accent"], text_color=self.theme["bg"],
                      font=("Arial", 18), corner_radius=10,
                      command=self.toggle_timer_from_mini).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="💾", width=56, height=36, fg_color="#3b82f6", text_color="white",
                      font=("Arial", 18), corner_radius=10,
                      command=self.save_from_mini).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="⏹", width=56, height=36, fg_color=self.theme["danger"], text_color="white",
                      font=("Arial", 18), corner_radius=10,
                      command=self.reset_timer).pack(side="left", padx=6)

    def start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def stop_move(self, event):
        self._drag_data["x"] = None
        self._drag_data["y"] = None

    def do_move(self, event):
        deltax = event.x - self._drag_data["x"]
        deltay = event.y - self._drag_data["y"]
        x = self.mini_window.winfo_x() + deltax
        y = self.mini_window.winfo_y() + deltay
        self.mini_window.geometry(f"+{x}+{y}")

    def close_mini_timer(self):
        if self.mini_window:
            self.mini_window.destroy()
            self.mini_window = None

    def toggle_timer_from_mini(self):
        if self.timer_running:
            self.pause_timer()
        else:
            self.start_timer()

    def save_from_mini(self):
        if self.timer_seconds < 10:
            messagebox.showinfo("Bilgi", "Çok kısa süreler kaydedilmez.")
            return
            
        was_running = self.timer_running
        self.pause_timer()
        
        dialog = ctk.CTkInputDialog(text="Görev ismi nedir?", title="Kaydet")
        task_name = dialog.get_input()
        
        if task_name:
            duration_str = self.format_timer_time(self.timer_seconds)
            full_task_text = f"[Genel] {task_name} ({duration_str})"
            
            today = datetime.now().strftime("%Y-%m-%d")
            self.tasks.append({"task": full_task_text, "date": today, "done": True})
            self.save_data("agenda_data.json", self.tasks)
            
            self.reset_timer()
        elif was_running:
            self.start_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer_loop()

    def pause_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.timer_seconds = 0
        time_str = self.format_timer_time(0)
        
        if hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
            self.timer_label.configure(text=time_str)
            
        if self.mini_window and hasattr(self, 'mini_timer_label') and self.mini_timer_label.winfo_exists():
            self.mini_timer_label.configure(text=time_str)

    def save_timer_session(self):
        if self.timer_seconds < 10:
            messagebox.showinfo("Bilgi", "Çok kısa süreler kaydedilmez.")
            return
            
        task_name = self.timer_entry.get().strip()
        if not task_name:
            task_name = "Çalışma Oturumu"
            
        category = self.category_var.get()
        duration_str = self.format_timer_time(self.timer_seconds)
        full_task_text = f"[{category}] {task_name} ({duration_str})"
        
        today = datetime.now().strftime("%Y-%m-%d")
        self.tasks.append({"task": full_task_text, "date": today, "done": True})
        self.save_data("agenda_data.json", self.tasks)
        
        self.reset_timer()
        self.timer_entry.delete(0, "end")
        messagebox.showinfo("Başarılı", self.t("timer_saved"))

    def update_timer_loop(self):
        if self.timer_running:
            self.timer_seconds += 1
            time_str = self.format_timer_time(self.timer_seconds)
            
            if hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
                self.timer_label.configure(text=time_str)
                
            if self.mini_window and hasattr(self, 'mini_timer_label') and self.mini_timer_label.winfo_exists():
                self.mini_timer_label.configure(text=time_str)
                
            self.after(1000, self.update_timer_loop)

    def format_timer_time(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    # --- TOPLAM SÜRE MENÜSÜ ---
    def show_total_time(self):
        if hasattr(self, 'total_active') and self.total_active: return
        self.reset_active_states()
        self.total_active = True
        self.set_active_menu(self.btn_total)
        self.clear_view()
        
        container = ctk.CTkFrame(self.view_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(container, text=self.t("total_time_header"), font=("Arial", 28, "bold"), 
                     text_color=self.theme["text"]).pack(anchor="w", pady=(0, 25))
        
        scroll = ctk.CTkScrollableFrame(container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        grouped_data = {}
        
        for task in self.tasks:
            name, seconds = self.parse_duration(task.get("task", ""))
            if seconds > 0:
                if name in grouped_data:
                    grouped_data[name] += seconds
                else:
                    grouped_data[name] = seconds
        
        if not grouped_data:
            ctk.CTkLabel(scroll, text=self.t("no_timer_data"), text_color=self.theme["text_dim"],
                         font=("Arial", 15)).pack(pady=60)
            return
            
        sorted_data = sorted(grouped_data.items(), key=lambda x: x[1], reverse=True)
        
        for name, total_seconds in sorted_data:
            card = ctk.CTkFrame(scroll, fg_color=self.theme["card"], corner_radius=12)
            card.pack(fill="x", pady=6)
            
            ctk.CTkLabel(card, text=name, font=("Arial", 16), text_color=self.theme["text"]).pack(side="left", padx=25, pady=18)
            ctk.CTkLabel(card, text=self.format_timer_time(total_seconds), font=("Arial", 18, "bold"), 
                         text_color=self.theme["accent"]).pack(side="right", padx=25)

    def parse_duration(self, task_str):
        try:
            if not task_str.endswith(")"): return None, 0
            name_part, _, time_part = task_str.rpartition('(')
            time_str = time_part.strip(")")
            h, m, s = map(int, time_str.split(':'))
            seconds = h * 3600 + m * 60 + s
            return name_part.strip(), seconds
        except:
            return None, 0

    # --- İSTATİSTİKLER ---
    def show_stats(self):
        if hasattr(self, 'stats_active') and self.stats_active: return
        self.reset_active_states()
        self.stats_active = True
        self.set_active_menu(self.btn_stats)
        self.clear_view()

        scroll_container = ctk.CTkScrollableFrame(self.view_frame, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True)
        
        # --- PASTA GRAFİK (Filtreli) ---
        pie_card = ctk.CTkFrame(scroll_container, fg_color=self.theme["card"], corner_radius=16)
        pie_card.pack(fill="x", pady=12, padx=12)
        
        pie_header = ctk.CTkFrame(pie_card, fg_color="transparent")
        pie_header.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(pie_header, text=self.t("pie_chart"), font=("Arial", 20, "bold"), 
                     text_color=self.theme["text"]).pack(side="left")
                     
        self.pie_period_var = ctk.StringVar(value=self.t("all_time"))
        seg_btn = ctk.CTkSegmentedButton(pie_header, values=[self.t("today"), self.t("week"), self.t("month"), self.t("all_time")],
                                         variable=self.pie_period_var, command=self.update_pie_chart,
                                         selected_color=self.theme["accent"], selected_hover_color=self.theme["accent"],
                                         unselected_color=self.theme["bg"], unselected_hover_color=self.theme["bg"],
                                         font=("Arial", 13))
        seg_btn.pack(side="right")
        
        self.pie_canvas_frame = ctk.CTkFrame(pie_card, fg_color="transparent")
        self.pie_canvas_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.update_pie_chart(self.t("all_time"))

        # --- ISI HARİTASI ---
        self.heat_card = ctk.CTkFrame(scroll_container, fg_color=self.theme["card"], corner_radius=16)
        self.heat_card.pack(fill="x", pady=12, padx=12)
        self.draw_activity_heatmap(self.heat_card)

    def update_pie_chart(self, period):
        for w in self.pie_canvas_frame.winfo_children(): w.destroy()
        today = datetime.now()
        filtered_tasks = []
        
        if period == self.t("today"):
            target = today.strftime("%Y-%m-%d")
            filtered_tasks = [t for t in self.tasks if t["date"] == target]
        elif period == self.t("week"):
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            for t in self.tasks:
                try:
                    t_date = datetime.strptime(t["date"], "%Y-%m-%d")
                    if start_week <= t_date <= end_week: filtered_tasks.append(t)
                except: pass
        elif period == self.t("month"):
            for t in self.tasks:
                try:
                    t_date = datetime.strptime(t["date"], "%Y-%m-%d")
                    if t_date.month == today.month and t_date.year == today.year: filtered_tasks.append(t)
                except: pass
        else:
            filtered_tasks = self.tasks
            
        self.draw_status_pie(self.pie_canvas_frame, filtered_tasks)

    def draw_status_pie(self, parent, tasks_list):
        total = len(tasks_list)
        done = len([t for t in tasks_list if t["done"]])
        pending = total - done
        if total == 0:
            ctk.CTkLabel(parent, text=self.t("no_task"), text_color=self.theme["text_dim"],
                         font=("Arial", 14)).pack(pady=30)
            return
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(pady=15)
        size = 180
        canvas = tk.Canvas(container, width=size, height=size, bg=self.theme["card"], highlightthickness=0)
        canvas.pack(side="left", padx=40)
        angle_done = (done / total) * 360
        angle_pending = 360 - angle_done
        if done > 0:
            canvas.create_arc(10, 10, size-10, size-10, start=0, extent=angle_done, 
                              fill=self.theme["accent"], outline="")
        if pending > 0:
            canvas.create_arc(10, 10, size-10, size-10, start=angle_done, extent=angle_pending, 
                              fill=self.theme["bg"], outline="")
        legend = ctk.CTkFrame(container, fg_color="transparent")
        legend.pack(side="left", padx=25)
        self.create_legend_item(legend, self.theme["accent"], f"{self.t('completed')}: {done} ({int(done/total*100)}%)")
        self.create_legend_item(legend, self.theme["bg"], f"{self.t('pending')}: {pending} ({int(pending/total*100)}%)")

    def create_legend_item(self, parent, color, text):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(anchor="w", pady=8)
        ctk.CTkFrame(row, width=18, height=18, fg_color=color, corner_radius=4).pack(side="left", padx=10)
        ctk.CTkLabel(row, text=text, font=("Arial", 15), text_color=self.theme["text"]).pack(side="left")

    def draw_activity_heatmap(self, parent):
        for w in parent.winfo_children(): w.destroy()
        ctk.CTkLabel(parent, text=self.t("heatmap"), font=("Arial", 20, "bold"), 
                     text_color=self.theme["text"]).pack(pady=20)
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(0, 15))
        ctk.CTkButton(header, text="‹", width=32, height=32, fg_color="transparent",
                      text_color=self.theme["text"], hover_color=self.theme["bg"],
                      font=("Arial", 18),
                      command=lambda: self.change_heatmap_month(-1)).pack(side="left")
        months_list = self.t("months")
        month_name = f"{months_list[self.heatmap_date.month-1]} {self.heatmap_date.year}"
        ctk.CTkLabel(header, text=month_name, font=("Arial", 15, "bold"), text_color=self.theme["text_dim"]).pack(side="left", expand=True)
        ctk.CTkButton(header, text="›", width=32, height=32, fg_color="transparent",
                      text_color=self.theme["text"], hover_color=self.theme["bg"],
                      font=("Arial", 18),
                      command=lambda: self.change_heatmap_month(1)).pack(side="right")
        grid = ctk.CTkFrame(parent, fg_color="transparent")
        grid.pack(pady=15)
        data_map = {}
        for t in self.tasks:
            d = t["date"]
            if d not in data_map: data_map[d] = []
            data_map[d].append(t)
        days_list = self.t("days")
        for i, d_name in enumerate(days_list):
            ctk.CTkLabel(grid, text=d_name, text_color=self.theme["text_dim"], font=("Arial", 11, "bold")).grid(row=0, column=i, pady=(0, 8))
        month_days = calendar.monthcalendar(self.heatmap_date.year, self.heatmap_date.month)
        for r, week in enumerate(month_days):
            for c, day in enumerate(week):
                if day == 0: continue
                date_str = f"{self.heatmap_date.year}-{self.heatmap_date.month:02d}-{day:02d}"
                tasks_list = data_map.get(date_str, [])
                completed_count = len([t for t in tasks_list if t["done"]])
                color = self.theme["bg"]
                text_color = self.theme["text"]
                if completed_count >= 1: 
                    color = self.adjust_color(self.theme["accent"], 0.5)
                    text_color = self.theme["bg"]
                if completed_count >= 3: 
                    color = self.theme["accent"]
                    text_color = self.theme["bg"]
                box = ctk.CTkFrame(grid, width=40, height=40, fg_color=color, corner_radius=8)
                box.grid(row=r+1, column=c, padx=4, pady=4)
                ctk.CTkLabel(box, text=str(day), text_color=text_color, font=("Arial", 13, "bold")).place(relx=0.5, rely=0.5, anchor="center")
                tooltip_text = f"{date_str}\n"
                if tasks_list:
                    for t in tasks_list:
                        status = "✓" if t["done"] else "○"
                        tooltip_text += f"{status} {t['task']}\n"
                else:
                    tooltip_text += self.t("no_task")
                ToolTip(box, tooltip_text)

    def change_heatmap_month(self, d):
        m, y = self.heatmap_date.month + d, self.heatmap_date.year
        if m > 12: m, y = 1, y + 1
        elif m < 1: m, y = 12, y - 1
        self.heatmap_date = self.heatmap_date.replace(year=y, month=m, day=1)
        self.draw_activity_heatmap(self.heat_card)

    def adjust_color(self, hex_color, factor):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f'#{r:02x}{g:02x}{b:02x}'

    # --- AYARLAR ---
    def open_settings(self):
        win = ctk.CTkToplevel(self)
        win.title(self.t("settings"))
        win.geometry("440x540")
        win.configure(fg_color=self.theme["bg"])
        win.transient(self)
        win.grab_set()
        win.focus_force()
        win.lift()
        win.attributes('-topmost', True)
        container = ctk.CTkFrame(win, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=35, pady=35)
        ctk.CTkLabel(container, text=self.t("settings"), font=("Arial", 26, "bold"), 
                     text_color=self.theme["text"]).pack(pady=(0, 30))
        ctk.CTkLabel(container, text=self.t("theme"), font=("Arial", 15, "bold"), 
                     text_color=self.theme["accent"]).pack(anchor="w", pady=(15, 8))
        theme_var = ctk.StringVar(value=self.current_theme_name)
        theme_menu = ctk.CTkOptionMenu(container, variable=theme_var, values=list(THEMES.keys()),
                                      fg_color=self.theme["card"], button_color=self.theme["accent"],
                                      text_color=self.theme["text"], font=("Arial", 14),
                                      dropdown_font=("Arial", 13), corner_radius=12, height=48)
        theme_menu.pack(fill="x")
        ctk.CTkLabel(container, text=self.t("language"), font=("Arial", 15, "bold"), 
                     text_color=self.theme["accent"]).pack(anchor="w", pady=(25, 8))
        lang_var = ctk.StringVar(value=self.current_lang_code)
        lang_frame = ctk.CTkFrame(container, fg_color="transparent")
        lang_frame.pack(fill="x")
        ctk.CTkRadioButton(lang_frame, text="Türkçe", variable=lang_var, value="TR", 
                          text_color=self.theme["text"], fg_color=self.theme["accent"],
                          font=("Arial", 14)).pack(side="left", padx=12)
        ctk.CTkRadioButton(lang_frame, text="English", variable=lang_var, value="EN", 
                          text_color=self.theme["text"], fg_color=self.theme["accent"],
                          font=("Arial", 14)).pack(side="left", padx=12)
        ctk.CTkLabel(container, text=self.t("data_mgmt"), font=("Arial", 15, "bold"), 
                     text_color=self.theme["accent"]).pack(anchor="w", pady=(35, 8))
        ctk.CTkButton(container, text=self.t("delete_all"), fg_color=self.theme["danger"], hover_color="#cc0000",
                     font=("Arial", 14, "bold"), height=48, corner_radius=12,
                     command=lambda: self.delete_all_data(win)).pack(fill="x")
        ctk.CTkButton(container, text=self.t("apply"), fg_color=self.theme["accent"], text_color=self.theme["bg"], 
                     height=52, font=("Arial", 15, "bold"), corner_radius=12,
                     command=lambda: self.apply_settings(win, theme_var.get(), lang_var.get())).pack(side="bottom", fill="x", pady=(20, 0))

    def apply_settings(self, window, theme, lang):
        self.config["theme"] = theme
        self.config["language"] = lang
        self.save_config()
        self.current_theme_name = theme
        self.current_lang_code = lang
        self.theme = THEMES[theme]
        self.lang = TRANSLATIONS[lang]
        self.configure(fg_color=self.theme["bg"])
        self.setup_ui()
        window.destroy()

    def delete_all_data(self, window):
        window.attributes('-topmost', False)
        if messagebox.askyesno(self.t("delete_all"), self.t("delete_all_confirm")):
            self.tasks = []
            self.notes = []
            self.save_data("agenda_data.json", [])
            self.save_data("notes_data.json", [])
            messagebox.showinfo(self.t("data_mgmt"), self.t("deleted_msg"))
            self.show_agenda()
        window.attributes('-topmost', True)

    def load_config(self):
        defaults = {"theme": "Midnight", "language": "TR"}
        try:
            with open("config.json", "r", encoding="utf-8") as f: 
                data = json.load(f)
                if data.get("theme") not in THEMES:
                    data["theme"] = "Midnight"
                return data
        except: 
            return defaults

    def save_config(self):
        with open("config.json", "w", encoding="utf-8") as f: json.dump(self.config, f, indent=2)

    def load_data(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f: return json.load(f)
        except: return []

    def save_data(self, filename, data):
        with open(filename, "w", encoding="utf-8") as f: json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    app = PersonalAssistantApp()
    app.mainloop()