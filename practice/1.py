# طراحی نرم افزار مشتریان

from tkinter import *


class Main:
    def __init__(self, name, family):  # اصلاح نام تابع سازنده
        self.name = name
        self.family = family

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Family: {self.family}")


# نمونه‌سازی از کلاس Main
customer = Main(name="John", family="Doe")
customer.display_info()

# ایجاد رابط کاربری ساده با Tkinter
root = Tk()
root.title("Customer Information")

# اضافه کردن لیبل‌ها و دکمه‌ها
Label(root, text="Name: " + customer.name).pack()
Label(root, text="Family: " + customer.family).pack()

Button(root, text="Exit", command=root.quit).pack()

root.mainloop()
