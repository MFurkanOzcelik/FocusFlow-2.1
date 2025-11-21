import sys
import json
import calendar
import math
from datetime import datetime, timedelta
from tkinter import messagebox
import tkinter as tk

try:
    import customtkinter as ctk
except ImportError:
    print("CustomTkinter yüklü değil: 'pip install customtkinter'")
    sys.exit(1)

# --- SABİTLER (TEMALAR VE DİL) ---
THEMES = {
    "Dark Purple": {
        "bg": "#1a1625", "card": "#2d2438", "sidebar": "#231c30",
        "accent": "#9d4edd", "text": "#ffffff", "text_dim": "#a8a8b8", "danger": "#ff4444"
    },
    "Ocean Blue": {
        "bg": "#0f172a", "card": "#1e293b", "sidebar": "#020617",
        "accent": "#38bdf8", "text": "#f8fafc", "text_dim": "#94a3b8", "danger": "#ef4444"
    },
    "Forest Green": {
        "bg": "#1a2e1a", "card": "#2d4a2d", "sidebar": "#142414",
        "accent": "#4ade80", "text": "#f0fdf4", "text_dim": "#86efac", "danger": "#ef4444"
    },
    "Sunset Orange": {
        "bg": "#2a1a1a", "card": "#452525", "sidebar": "#1f1010",
        "accent": "#fb923c", "text": "#fff7ed", "text_dim": "#fdba74", "danger": "#ef4444"
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
        frame = ctk.CTkFrame(self.tooltip_window, fg_color="#2b2b2b", corner_radius=6, border_width=1, border_color="#555555")
        frame.pack()
        ctk.CTkLabel(frame, text=self.text, text_color="#ffffff", padx=10, pady=5, font=("Arial", 12), justify="left").pack()

    def hide_tip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class PersonalAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.config = self.load_config()
        self.current_lang_code = self.config.get("language", "TR")
        self.current_theme_name = self.config.get("theme", "Dark Purple")
        self.theme = THEMES[self.current_theme_name]
        self.lang = TRANSLATIONS[self.current_lang_code]
        
        self.title("FocusFlow 2.1")
        self.geometry("1100x700")
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

        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=self.theme["sidebar"], corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.main_area = ctk.CTkFrame(self, fg_color=self.theme["bg"], corner_radius=0)
        self.main_area.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(self.sidebar, text=self.t("app_name"), font=("Arial", 24, "bold"), 
                     text_color=self.theme["accent"]).pack(pady=(40, 40))
        
        self.btn_agenda = self.create_menu_btn(self.t("agenda"), self.show_agenda)
        self.btn_notes = self.create_menu_btn(self.t("notes"), self.show_notes)
        self.btn_timer = self.create_menu_btn(self.t("timer"), self.show_timer)
        self.btn_stats = self.create_menu_btn(self.t("stats"), self.show_stats)
        self.btn_total = self.create_menu_btn(self.t("total_time"), self.show_total_time)
        
        self.top_bar = ctk.CTkFrame(self.main_area, height=50, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=20, pady=(10, 0))
        
        settings_btn = ctk.CTkButton(self.top_bar, text="⚙", width=40, height=40,
                                     fg_color="transparent", hover_color=self.theme["card"],
                                     text_color=self.theme["text_dim"], font=("Arial", 20),
                                     corner_radius=20, command=self.open_settings)
        settings_btn.pack(side="right")

        self.view_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.view_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.reset_active_states()
        self.show_agenda()

    def create_menu_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, anchor="w", height=50,
                            fg_color="transparent", hover_color=self.theme["card"],
                            text_color=self.theme["text"], font=("Arial", 14, "bold"),
                            command=command)
        btn.pack(fill="x", padx=10, pady=5)
        return btn

    def set_active_menu(self, active_btn):
        self.btn_agenda.configure(fg_color="transparent", text_color=self.theme["text"])
        self.btn_notes.configure(fg_color="transparent", text_color=self.theme["text"])
        self.btn_stats.configure(fg_color="transparent", text_color=self.theme["text"])
        self.btn_timer.configure(fg_color="transparent", text_color=self.theme["text"])
        self.btn_total.configure(fg_color="transparent", text_color=self.theme["text"])
        active_btn.configure(fg_color=self.theme["card"], text_color=self.theme["accent"])

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
        
        left_panel = ctk.CTkFrame(split, width=350, fg_color=self.theme["card"], corner_radius=20)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)
        
        cal_header = ctk.CTkFrame(left_panel, fg_color="transparent")
        cal_header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkButton(cal_header, text="<", width=30, height=30, fg_color=self.theme["bg"], 
                     text_color=self.theme["text"], hover_color=self.theme["accent"],
                     command=lambda: self.change_month(-1)).pack(side="left")
        
        self.month_label = ctk.CTkLabel(cal_header, text="", font=("Arial", 16, "bold"), text_color=self.theme["text"])
        self.month_label.pack(side="left", expand=True)
        
        ctk.CTkButton(cal_header, text=">", width=30, height=30, fg_color=self.theme["bg"], 
                     text_color=self.theme["text"], hover_color=self.theme["accent"],
                     command=lambda: self.change_month(1)).pack(side="right")
        
        self.cal_grid_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.cal_grid_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        right_panel = ctk.CTkFrame(split, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.date_label = ctk.CTkLabel(right_panel, text="", font=("Arial", 20, "bold"), text_color=self.theme["accent"])
        self.date_label.pack(anchor="w", pady=(0, 15))
        
        input_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 15))
        
        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text=self.t("new_task"), height=45,
                                      fg_color=self.theme["card"], border_width=0, text_color=self.theme["text"])
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        ctk.CTkButton(input_frame, text="+", width=45, height=45,
                     fg_color=self.theme["accent"], hover_color=self.theme["accent"],
                     text_color="#000000", corner_radius=22, command=self.add_task).pack(side="right")
        
        self.task_list_frame = ctk.CTkScrollableFrame(right_panel, fg_color=self.theme["card"], corner_radius=20)
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
            self.cal_grid_frame.columnconfigure(i, weight=1)
            ctk.CTkLabel(self.cal_grid_frame, text=d, text_color=self.theme["text_dim"], font=("Arial", 10)).grid(row=0, column=i)
        month_days = calendar.monthcalendar(self.calendar_date.year, self.calendar_date.month)
        for r, week in enumerate(month_days):
            for c, day in enumerate(week):
                if day != 0:
                    date_str = f"{self.calendar_date.year}-{self.calendar_date.month:02d}-{day:02d}"
                    is_sel = (date_str == self.selected_date)
                    has_task = any(t["date"] == date_str for t in self.tasks)
                    bg = self.theme["accent"] if is_sel else (self.theme["bg"] if has_task else "transparent")
                    fg = "#000000" if is_sel else self.theme["text"]
                    btn = ctk.CTkButton(self.cal_grid_frame, text=str(day), width=30, height=30, fg_color=bg,
                                      text_color=fg, hover_color=self.theme["bg"], corner_radius=15,
                                      command=lambda d=date_str: self.select_date(d))
                    btn.grid(row=r+1, column=c, padx=2, pady=2)

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
            ctk.CTkLabel(self.task_list_frame, text=self.t("no_task"), text_color=self.theme["text_dim"]).pack(pady=20)
            return
        for task in tasks:
            f = ctk.CTkFrame(self.task_list_frame, fg_color="transparent")
            f.pack(fill="x", pady=5, padx=5)
            done = task["done"]
            chk = ctk.CTkButton(f, text="✓" if done else "", width=24, height=24, corner_radius=12,
                               fg_color=self.theme["accent"] if done else "transparent", border_width=2,
                               border_color=self.theme["accent"], text_color="black",
                               command=lambda t=task: self.toggle_task(t))
            chk.pack(side="left")
            lbl = ctk.CTkLabel(f, text=task["task"], text_color=self.theme["text_dim"] if done else self.theme["text"])
            lbl.pack(side="left", padx=10)
            ctk.CTkButton(f, text="✕", width=30, fg_color="transparent", hover_color=self.theme["danger"],
                         text_color="#ff6666", command=lambda t=task: self.delete_task(t)).pack(side="right")

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
        
        list_panel = ctk.CTkFrame(split, width=250, fg_color=self.theme["card"], corner_radius=20)
        list_panel.pack(side="left", fill="y", padx=(0, 20))
        list_panel.pack_propagate(False)
        
        ctk.CTkButton(list_panel, text=self.t("new_note"), fg_color=self.theme["accent"], text_color="black",
                     command=self.create_new_note).pack(fill="x", padx=15, pady=15)
        
        self.note_list_frame = ctk.CTkScrollableFrame(list_panel, fg_color="transparent")
        self.note_list_frame.pack(fill="both", expand=True, padx=5)
        
        self.editor_panel = ctk.CTkFrame(split, fg_color=self.theme["card"], corner_radius=20)
        self.editor_panel.pack(side="right", fill="both", expand=True)
        
        self.refresh_note_list()
        self.show_empty_editor()

    def show_empty_editor(self):
        for w in self.editor_panel.winfo_children(): w.destroy()
        ctk.CTkLabel(self.editor_panel, text=self.t("select_note"), 
                     text_color=self.theme["text_dim"]).pack(expand=True)

    def refresh_note_list(self):
        for w in self.note_list_frame.winfo_children(): w.destroy()
        for i, note in enumerate(reversed(self.notes)):
            idx = len(self.notes) - 1 - i
            btn = ctk.CTkButton(self.note_list_frame, text=note.get("title", "Başlıksız"), anchor="w",
                               fg_color="transparent", hover_color=self.theme["bg"], text_color=self.theme["text"],
                               command=lambda x=idx: self.load_note_editor(x))
            btn.pack(fill="x", pady=2)

    def create_new_note(self):
        self.load_note_editor(None)

    def load_note_editor(self, index):
        for w in self.editor_panel.winfo_children(): w.destroy()
        current_note = self.notes[index] if index is not None else {"title": "", "content": ""}
        
        title_entry = ctk.CTkEntry(self.editor_panel, placeholder_text=self.t("note_title"), 
                                  font=("Arial", 20, "bold"), fg_color=self.theme["bg"],
                                  text_color=self.theme["text"], border_width=0, height=50, corner_radius=10)
        title_entry.pack(fill="x", padx=20, pady=(20, 10))
        title_entry.insert(0, current_note["title"])
        
        content_txt = ctk.CTkTextbox(self.editor_panel, fg_color=self.theme["bg"], text_color=self.theme["text"], font=("Arial", 14))
        content_txt.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        content_txt.insert("0.0", current_note["content"])
        
        btn_frame = ctk.CTkFrame(self.editor_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        if index is not None:
            ctk.CTkButton(btn_frame, text=self.t("delete"), fg_color=self.theme["danger"], width=80,
                         command=lambda: self.delete_note(index)).pack(side="left")
        
        ctk.CTkButton(btn_frame, text=self.t("save"), fg_color=self.theme["accent"], text_color="black", width=100,
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
                                       font=("Arial", 80, "bold"), text_color=self.theme["accent"])
        self.timer_label.pack(pady=(0, 30))
        
        # GÖREV & KATEGORİ GİRİŞİ
        input_frame = ctk.CTkFrame(container, fg_color="transparent")
        input_frame.pack(pady=(0, 30))
        
        self.category_var = ctk.StringVar(value=self.categories[0] if self.categories else "Genel")
        self.cat_menu = ctk.CTkComboBox(input_frame, values=self.categories, variable=self.category_var,
                                       width=120, height=40, fg_color=self.theme["card"], 
                                       text_color=self.theme["text"], border_width=0)
        self.cat_menu.pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(input_frame, text="+", width=40, height=40, fg_color=self.theme["card"], 
                     text_color=self.theme["accent"], command=self.add_category_dialog).pack(side="left", padx=(0, 10))
        
        self.timer_entry = ctk.CTkEntry(input_frame, placeholder_text=self.t("timer_task_hint"),
                                       width=250, height=40, font=("Arial", 14),
                                       fg_color=self.theme["card"], text_color=self.theme["text"], border_width=0)
        self.timer_entry.pack(side="left")
        
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack()
        
        ctk.CTkButton(btn_frame, text=self.t("start"), width=100, height=40,
                     fg_color=self.theme["accent"], text_color="black", corner_radius=20,
                     command=self.start_timer).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_frame, text=self.t("pause"), width=100, height=40,
                     fg_color="#f59e0b", text_color="black", corner_radius=20,
                     command=self.pause_timer).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_frame, text=self.t("finish"), width=100, height=40,
                     fg_color=self.theme["danger"], text_color="white", corner_radius=20,
                     command=self.reset_timer).pack(side="left", padx=10)
                     
        ctk.CTkButton(btn_frame, text=self.t("save"), width=100, height=40,
                     fg_color="#3b82f6", text_color="white", corner_radius=20,
                     command=self.save_timer_session).pack(side="left", padx=10)
                     
        ctk.CTkButton(btn_frame, text=self.t("detach"), width=80, height=40,
                     fg_color=self.theme["card"], text_color=self.theme["text_dim"], corner_radius=20,
                     command=self.open_mini_timer).pack(side="left", padx=10)

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
        self.mini_window.geometry("300x130")
        self.mini_window.configure(fg_color=self.theme["bg"])
        self.mini_window.attributes('-topmost', True)
        self.mini_window.overrideredirect(True) 
        
        self.mini_window.bind("<ButtonPress-1>", self.start_move)
        self.mini_window.bind("<ButtonRelease-1>", self.stop_move)
        self.mini_window.bind("<B1-Motion>", self.do_move)
        
        main_frame = ctk.CTkFrame(self.mini_window, fg_color=self.theme["card"], border_width=2, border_color=self.theme["accent"])
        main_frame.pack(fill="both", expand=True)
        
        close_btn = ctk.CTkButton(main_frame, text="✕", width=25, height=25, fg_color="transparent", 
                                 text_color=self.theme["danger"], hover_color=self.theme["bg"],
                                 command=self.close_mini_timer)
        close_btn.place(relx=0.98, rely=0.02, anchor="ne")
        
        self.mini_timer_label = ctk.CTkLabel(main_frame, text=self.format_timer_time(self.timer_seconds),
                                            font=("Arial", 36, "bold"), text_color=self.theme["text"])
        self.mini_timer_label.pack(pady=(25, 5))
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        ctk.CTkButton(btn_frame, text="⏯", width=50, height=30, fg_color=self.theme["accent"], text_color="black",
                     command=self.toggle_timer_from_mini).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="💾", width=50, height=30, fg_color="#3b82f6", text_color="white",
                     command=self.save_from_mini).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="⏹", width=50, height=30, fg_color=self.theme["danger"], 
                     command=self.reset_timer).pack(side="left", padx=5)

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
        
        ctk.CTkLabel(container, text=self.t("total_time_header"), font=("Arial", 24, "bold"), 
                     text_color=self.theme["text"]).pack(anchor="w", pady=(0, 20))
        
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
            ctk.CTkLabel(scroll, text=self.t("no_timer_data"), text_color=self.theme["text_dim"]).pack(pady=50)
            return
            
        sorted_data = sorted(grouped_data.items(), key=lambda x: x[1], reverse=True)
        
        for name, total_seconds in sorted_data:
            card = ctk.CTkFrame(scroll, fg_color=self.theme["card"], corner_radius=10)
            card.pack(fill="x", pady=5)
            
            ctk.CTkLabel(card, text=name, font=("Arial", 16, "bold"), text_color=self.theme["text"]).pack(side="left", padx=20, pady=15)
            ctk.CTkLabel(card, text=self.format_timer_time(total_seconds), font=("Arial", 16, "bold"), 
                         text_color=self.theme["accent"]).pack(side="right", padx=20)

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
        pie_card = ctk.CTkFrame(scroll_container, fg_color=self.theme["card"], corner_radius=20)
        pie_card.pack(fill="x", pady=10, padx=10)
        
        pie_header = ctk.CTkFrame(pie_card, fg_color="transparent")
        pie_header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(pie_header, text=self.t("pie_chart"), font=("Arial", 16, "bold"), 
                     text_color=self.theme["text"]).pack(side="left")
                     
        self.pie_period_var = ctk.StringVar(value=self.t("all_time"))
        seg_btn = ctk.CTkSegmentedButton(pie_header, values=[self.t("today"), self.t("week"), self.t("month"), self.t("all_time")],
                                         variable=self.pie_period_var, command=self.update_pie_chart,
                                         selected_color=self.theme["accent"], selected_hover_color=self.theme["accent"],
                                         unselected_color=self.theme["bg"], unselected_hover_color=self.theme["bg"])
        seg_btn.pack(side="right")
        
        self.pie_canvas_frame = ctk.CTkFrame(pie_card, fg_color="transparent")
        self.pie_canvas_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.update_pie_chart(self.t("all_time"))

        # --- ISI HARİTASI ---
        self.heat_card = ctk.CTkFrame(scroll_container, fg_color=self.theme["card"], corner_radius=20)
        self.heat_card.pack(fill="x", pady=10, padx=10)
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
            ctk.CTkLabel(parent, text=self.t("no_task"), text_color=self.theme["text_dim"]).pack(pady=20)
            return
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(pady=10)
        size = 160
        canvas = tk.Canvas(container, width=size, height=size, bg=self.theme["card"], highlightthickness=0)
        canvas.pack(side="left", padx=30)
        angle_done = (done / total) * 360
        angle_pending = 360 - angle_done
        if done > 0:
            canvas.create_arc(10, 10, size-10, size-10, start=0, extent=angle_done, 
                              fill=self.theme["accent"], outline="")
        if pending > 0:
            canvas.create_arc(10, 10, size-10, size-10, start=angle_done, extent=angle_pending, 
                              fill=self.theme["bg"], outline="")
        legend = ctk.CTkFrame(container, fg_color="transparent")
        legend.pack(side="left", padx=20)
        self.create_legend_item(legend, self.theme["accent"], f"{self.t('completed')}: {done} ({int(done/total*100)}%)")
        self.create_legend_item(legend, self.theme["bg"], f"{self.t('pending')}: {pending} ({int(pending/total*100)}%)")

    def create_legend_item(self, parent, color, text):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(anchor="w", pady=5)
        ctk.CTkFrame(row, width=15, height=15, fg_color=color, corner_radius=4).pack(side="left", padx=8)
        ctk.CTkLabel(row, text=text, font=("Arial", 14), text_color=self.theme["text"]).pack(side="left")

    def draw_activity_heatmap(self, parent):
        for w in parent.winfo_children(): w.destroy()
        ctk.CTkLabel(parent, text=self.t("heatmap"), font=("Arial", 16, "bold"), 
                     text_color=self.theme["text"]).pack(pady=15)
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkButton(header, text="<", width=25, height=25, fg_color=self.theme["bg"],
                     text_color=self.theme["text"], hover_color=self.theme["accent"],
                     command=lambda: self.change_heatmap_month(-1)).pack(side="left")
        months_list = self.t("months")
        month_name = f"{months_list[self.heatmap_date.month-1]} {self.heatmap_date.year}"
        ctk.CTkLabel(header, text=month_name, font=("Arial", 14, "bold"), text_color=self.theme["text_dim"]).pack(side="left", expand=True)
        ctk.CTkButton(header, text=">", width=25, height=25, fg_color=self.theme["bg"],
                     text_color=self.theme["text"], hover_color=self.theme["accent"],
                     command=lambda: self.change_heatmap_month(1)).pack(side="right")
        grid = ctk.CTkFrame(parent, fg_color="transparent")
        grid.pack(pady=10)
        data_map = {}
        for t in self.tasks:
            d = t["date"]
            if d not in data_map: data_map[d] = []
            data_map[d].append(t)
        days_list = self.t("days")
        for i, d_name in enumerate(days_list):
            ctk.CTkLabel(grid, text=d_name, text_color=self.theme["text_dim"], font=("Arial", 10)).grid(row=0, column=i)
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
                    color = self.adjust_color(self.theme["accent"], 0.6)
                    text_color = "#000000"
                if completed_count >= 3: 
                    color = self.theme["accent"]
                    text_color = "#000000"
                box = ctk.CTkFrame(grid, width=35, height=35, fg_color=color, corner_radius=5)
                box.grid(row=r+1, column=c, padx=3, pady=3)
                ctk.CTkLabel(box, text=str(day), text_color=text_color, font=("Arial", 11, "bold")).place(relx=0.5, rely=0.5, anchor="center")
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
        win.geometry("400x500")
        win.configure(fg_color=self.theme["bg"])
        win.transient(self)
        win.grab_set()
        win.focus_force()
        win.lift()
        win.attributes('-topmost', True)
        container = ctk.CTkFrame(win, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        ctk.CTkLabel(container, text=self.t("settings"), font=("Arial", 20, "bold"), text_color=self.theme["text"]).pack(pady=(0, 20))
        ctk.CTkLabel(container, text=self.t("theme"), font=("Arial", 14, "bold"), text_color=self.theme["accent"]).pack(anchor="w", pady=(10, 5))
        theme_var = ctk.StringVar(value=self.current_theme_name)
        theme_menu = ctk.CTkOptionMenu(container, variable=theme_var, values=list(THEMES.keys()),
                                      fg_color=self.theme["card"], button_color=self.theme["accent"],
                                      text_color=self.theme["text"])
        theme_menu.pack(fill="x")
        ctk.CTkLabel(container, text=self.t("language"), font=("Arial", 14, "bold"), text_color=self.theme["accent"]).pack(anchor="w", pady=(20, 5))
        lang_var = ctk.StringVar(value=self.current_lang_code)
        lang_frame = ctk.CTkFrame(container, fg_color="transparent")
        lang_frame.pack(fill="x")
        ctk.CTkRadioButton(lang_frame, text="Türkçe", variable=lang_var, value="TR", text_color=self.theme["text"], fg_color=self.theme["accent"]).pack(side="left", padx=10)
        ctk.CTkRadioButton(lang_frame, text="English", variable=lang_var, value="EN", text_color=self.theme["text"], fg_color=self.theme["accent"]).pack(side="left", padx=10)
        ctk.CTkLabel(container, text=self.t("data_mgmt"), font=("Arial", 14, "bold"), text_color=self.theme["accent"]).pack(anchor="w", pady=(30, 5))
        ctk.CTkButton(container, text=self.t("delete_all"), fg_color=self.theme["danger"], hover_color="#cc0000",
                     command=lambda: self.delete_all_data(win)).pack(fill="x")
        ctk.CTkButton(container, text=self.t("apply"), fg_color=self.theme["accent"], text_color="black", height=40,
                     command=lambda: self.apply_settings(win, theme_var.get(), lang_var.get())).pack(side="bottom", fill="x")

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
        try:
            with open("config.json", "r", encoding="utf-8") as f: return json.load(f)
        except: return {"theme": "Dark Purple", "language": "TR"}

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