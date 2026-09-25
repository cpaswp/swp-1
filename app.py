import sqlite3
import datetime
import os
import random
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

DB_NAME = "SWPTRADE.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS A (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            A1 TEXT, A2 TEXT, A3 TEXT, A4 TEXT, A5 TEXT, A6 TEXT, 
            A7 TEXT, A8 TEXT, A9 TEXT, A10 INTEGER, A11 TEXT,
            A12 TEXT, A13 TEXT, A14 TEXT, A24 TEXT, A26 TEXT, A28 TEXT, A32 TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS B (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            B1 TEXT, B2 TEXT, B3 INTEGER, B4 TEXT, B5 TEXT, B6 TEXT, 
            B7 TEXT, B8 TEXT, B9 TEXT, B10 REAL, B11 REAL, B12 TEXT, 
            B13 TEXT, B14 TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS C (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            C1 TEXT, C2 TEXT, C3 INTEGER, C4 TEXT, C5 TEXT, 
            C6 TEXT, C7 TEXT, C8 TEXT, C9 REAL, C10 REAL
        )
    ''')
    
    # مستخدم افتراضي عادي للتجربة (كود 123 وكلمة المرور 123)
    cursor.execute("SELECT COUNT(*) FROM A WHERE A10 = '123'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO A (A1, A2, A8, A10, A11, A24) 
            VALUES ('مجموعة أحمد الأعرجي لخدمة الشركات', 'SWP-1', 'مستخدم النظام', '123', '123', 'SWPTRADE.db')
        ''')
    
    conn.commit()
    conn.close()

class SWPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مجموعة أحمد الأعرجي لخدمة الشركات (SWP) - النظام المحاسبي المتكامل")
        self.root.geometry("1024x768")
        self.root.configure(bg="#f0f2f5")
        
        self.generated_code = "" 
        init_db()
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.GROOVE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=480, height=520)
        
        tk.Label(frame, text="تسجيل الدخول - نظام SWP", font=("Arial", 16, "bold"), bg="white", fg="#1a73e8").pack(pady=15)
        
        # اختيار نوع الدخول (مدير نظام أو مستخدم عادي)
        tk.Label(frame, text="اختر نوع المستخدم:", font=("Arial", 11, "bold"), bg="white").pack(anchor="e", padx=30)
        self.user_type_var = tk.StringVar(value="مدير النظام")
        
        type_frame = tk.Frame(frame, bg="white")
        type_frame.pack(fill=tk.X, padx=30, pady=5)
        
        rb_admin = tk.Radiobutton(type_frame, text="مدير النظام (واتساب)", variable=self.user_type_var, value="مدير النظام", font=("Arial", 10), bg="white", command=self.toggle_login_mode)
        rb_admin.pack(side=tk.RIGHT, padx=10)
        
        rb_user = tk.Radiobutton(type_frame, text="مستخدم عادي", variable=self.user_type_var, value="مستخدم عادي", font=("Arial", 10), bg="white", command=self.toggle_login_mode)
        rb_user.pack(side=tk.RIGHT, padx=10)

        # إطار حقول مدير النظام
        self.admin_frame = tk.Frame(frame, bg="white")
        self.admin_frame.pack(fill=tk.X, padx=30, pady=5)
        
        self.btn_send_wa = tk.Button(self.admin_frame, text="إرسال كود التحقق إلى الواتساب", font=("Arial", 11, "bold"), bg="#25d366", fg="white", command=self.send_whatsapp_code)
        self.btn_send_wa.pack(fill=tk.X, pady=5)

        tk.Label(self.admin_frame, text="أدخل كود التحقق المرسل لهاتفك:", font=("Arial", 10), bg="white", fg="#075e54").pack(anchor="e", pady=(5,0))
        self.whatsapp_code_entry = tk.Entry(self.admin_frame, font=("Arial", 13), justify="center")
        self.whatsapp_code_entry.pack(fill=tk.X, pady=5)

        # إطار حقول المستخدم العادي (مخفي افتراضياً)
        self.normal_user_frame = tk.Frame(frame, bg="white")
        
        tk.Label(self.normal_user_frame, text="اسم قاعدة البيانات:", font=("Arial", 10), bg="white").pack(anchor="e")
        self.db_entry = tk.Entry(self.normal_user_frame, font=("Arial", 11), justify="right")
        self.db_entry.insert(0, "SWPTRADE.db")
        self.db_entry.pack(fill=tk.X, pady=3)
        
        tk.Label(self.normal_user_frame, text="كود المستخدم:", font=("Arial", 10), bg="white").pack(anchor="e")
        self.user_entry = tk.Entry(self.normal_user_frame, font=("Arial", 11), justify="right")
        self.user_entry.pack(fill=tk.X, pady=3)
        
        tk.Label(self.normal_user_frame, text="كلمة المرور:", font=("Arial", 10), bg="white").pack(anchor="e")
        self.pass_entry = tk.Entry(self.normal_user_frame, font=("Arial", 11), show="*", justify="right")
        self.pass_entry.pack(fill=tk.X, pady=3)

        self.lbl_status = tk.Label(frame, text="", font=("Arial", 10, "bold"), bg="white", fg="red")
        self.lbl_status.pack(pady=5)
        
        self.btn_login = tk.Button(frame, text="دخول النظام", font=("Arial", 12, "bold"), bg="#34a853", fg="white", command=self.verify_login)
        self.btn_login.pack(fill=tk.X, padx=30, pady=10)
        
        footer = tk.Label(frame, text="الدعم الفني: 00201020980996\nCPASWP@GMAIL.COM", font=("Arial", 8), bg="white", fg="gray")
        footer.pack(pady=5)

    def toggle_login_mode(self):
        mode = self.user_type_var.get()
        if mode == "مدير النظام":
            self.normal_user_frame.pack_forget()
            self.admin_frame.pack(fill=tk.X, padx=30, pady=5)
            self.lbl_status.config(text="")
        else:
            self.admin_frame.pack_forget()
            self.normal_user_frame.pack(fill=tk.X, padx=30, pady=5)
            self.lbl_status.config(text="")

    def send_whatsapp_code(self):
        # توليد كود عشوائي من 4 أرقام وإرساله للرقم 201020980996 دون إظهار الرقم بالشاشة
        self.generated_code = str(random.randint(1000, 9999))
        phone = "201020980996"
        message = f"مرحباً مهندس أحمد، كود الدخول لنظام SWP المحاسبي الخاص بك هو: {self.generated_code}"
        
        url = f"https://wa.me/{phone}?text={message}"
        webbrowser.open(url)
        
        self.lbl_status.config(text="تم إرسال كود التحقق عبر الواتساب إلى هاتفك", fg="green")
        messagebox.showinfo("تم الإرسال", "تم فتح واتساب لإرسال الكود إلى هاتفك بنجاح.")

    def verify_login(self):
        mode = self.user_type_var.get()
        
        if mode == "مدير النظام":
            wa_code = self.whatsapp_code_entry.get().strip()
            if not wa_code:
                messagebox.showerror("خطأ", "يرجى إدخال كود التحقق المرسل إلى هاتفك.")
                return
            if wa_code != self.generated_code:
                messagebox.showerror("خطأ أمني", "كود التحقق غير صحيح! تأكد من الكود الوارد على هاتفك.")
                return
            self.current_user = "أحمد الأعرجي (مدير النظام)"
            self.show_main_menu()
            
        else:
            dbname = self.db_entry.get().strip()
            user_code = self.user_entry.get().strip()
            password = self.pass_entry.get().strip()
            
            if not os.path.exists(dbname):
                messagebox.showerror("خطأ", "اسم قاعدة البيانات غير موجود.")
                return
                
            conn = sqlite3.connect(dbname)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM A WHERE A10 = ? AND A11 = ?", (user_code, password))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                self.current_user = result[8] if result[8] else "مستخدم النظام"
                self.show_main_menu()
            else:
                messagebox.showerror("خطأ", "كود المستخدم أو كلمة المرور غير صحيحة.")

    def show_main_menu(self):
        self.clear_screen()
        
        top_bar = tk.Frame(self.root, bg="#1a73e8", height=50)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        tk.Label(top_bar, text="مجموعة أحمد الأعرجي لخدمة الشركات (SWP) - الصفحة الرئيسية", font=("Arial", 14, "bold"), bg="#1a73e8", fg="white").pack(side=tk.RIGHT, padx=20, pady=10)
        
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        buttons = [
            ("شاشة الضبط", self.open_settings),
            ("شاشة التعريفات", self.open_definitions),
            ("شاشة رصيد أول المدة", self.open_opening_balance),
            ("شاشة المبيعات", self.open_sales),
            ("شاشة مردودات المبيعات", self.open_sales_returns),
            ("شاشة المشتريات", self.open_purchases),
            ("شاشة مردودات المشتريات", self.open_purchases_returns),
            ("شاشة النقدية والبنوك", self.open_cash_banks),
            ("شاشة قيود اليومية", self.open_journal_entries),
            ("شاشة أوراق القبض", self.open_receivables),
            ("شاشة أوراق الدفع", self.open_payables),
            ("شاشة المخازن", self.open_inventory),
            ("شاشة التقارير العامة", self.open_reports),
            ("شاشة الداش بورد", self.open_dashboard),
            ("شاشة نقاط البيع POS", self.open_pos)
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            row = i // 3
            col = i % 3
            btn = tk.Button(main_frame, text=text, font=("Arial", 12, "bold"), bg="white", fg="#333", relief=tk.RAISED, bd=2, command=cmd)
            btn.grid(row=row, column=col, padx=15, pady=15, ipadx=20, ipady=15, sticky="nsew")
            
        for i in range(3):
            main_frame.columnconfigure(i, weight=1)
            
        footer_bar = tk.Frame(self.root, bg="#333", height=30)
        footer_bar.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer_bar, text=f"البرنامج: SWP | المبرمج: أحمد الأعرجي لخدمة الشركات | المستخدم: {getattr(self, 'current_user', 'مستخدم')} | القاعدة: SWPTRADE.db", font=("Arial", 9), bg="#333", fg="white").pack(pady=5)

    def open_settings(self):
        messagebox.showinfo("شاشة الضبط", "تم فتح شاشة الضبط وإنشاء قواعد البيانات بنجاح.")
    def open_definitions(self):
        messagebox.showinfo("شاشة التعريفات", "شاشة إدخال بيانات الشركات والموظفين والإدارات.")
    def open_opening_balance(self):
        messagebox.showinfo("شاشة رصيد أول المدة", "استيراد أرصدة أول المدة من ملفات Excel والتحقق من اتزان الميزان.")
    def open_sales(self):
        messagebox.showinfo("شاشة المبيعات", "إدارة فواتير المبيعات وحركات المخزون المالية.")
    def open_sales_returns(self):
        messagebox.showinfo("شاشة مردودات المبيعات", "إدارة مرتجعات المبيعات وتأثيرها المالي والمخزني.")
    def open_purchases(self):
        messagebox.showinfo("شاشة المشتريات", "إدارة فواتير وحركات المشتريات.")
    def open_purchases_returns(self):
        messagebox.showinfo("شاشة مردودات المشتريات", "إدارة مردودات المشتريات.")
    def open_cash_banks(self):
        messagebox.showinfo("شاشة النقدية والبنوك", "إدارة إيونات الصرف والقبض النقدية والبنوك.")
    def open_journal_entries(self):
        messagebox.showinfo("شاشة قيود اليومية", "إدارة قيود اليومية مع فلاتر متقدمة لكل عمود.")
    def open_receivables(self):
        messagebox.showinfo("شاشة أوراق القبض", "إدارة أوراق القبض والشيكات واستعلاماتها.")
    def open_payables(self):
        messagebox.showinfo("شاشة أوراق الدفع", "إدارة أوراق الدفع والشيكات الصادرة.")
    def open_inventory(self):
        messagebox.showinfo("شاشة المخازن", "إدارة الأذون المخزنية (صرف وإضافة).")
    def open_reports(self):
        messagebox.showinfo("شاشة التقارير العامة", "ميزان المراجعة، تقارير الحسابات، تقارير الأصناف والموظفين.")
    def open_dashboard(self):
        messagebox.showinfo("شاشة الداش بورد", "لوحة المؤشرات الحيوية للمبيعات، التكاليف، مجمل الربح، والمشروعات.")
    def open_pos(self):
        messagebox.showinfo("شاشة نقاط البيع", "شاشة الكاشير السريعة مع طباعة ريسيت البيع وحساب الضرائب والخصومات.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SWPApp(root)
    root.mainloop()