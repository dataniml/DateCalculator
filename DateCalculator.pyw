import tkinter as tk
from tkinter import ttk
import tempfile, base64, zlib
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# Console output at startup
print("Date Calculator v. 1.1\n2025 © Data Animal")

# Global variables
currentDate = datetime.date.today()
year = currentDate.year
month = currentDate.month
day = currentDate.day

# Transparent icon settings
ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
                                        'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

# Functions
def handleEvent(event):
    entry = event.widget
    entry.delete(0, 'end')
    entry.unbind("<FocusIn>")

def today(placement):
    entries = [
        (DC_StartDayEntry, DC_StartMonthEntry, DC_StartYearEntry),
        (DC_EndDayEntry, DC_EndMonthEntry, DC_EndYearEntry),
        (DA_StartDayEntry, DA_StartMonthEntry, DA_StartYearEntry)
    ]
    day_entry, month_entry, year_entry = entries[placement]
    day_entry.delete(0, "end")
    day_entry.insert(0, day)
    day_entry.unbind("<FocusIn>")
    month_entry.delete(0, "end")
    month_entry.insert(0, month)
    month_entry.unbind("<FocusIn>")
    year_entry.delete(0, "end")
    year_entry.insert(0, year)
    year_entry.unbind("<FocusIn>")

def DC_calculation():
    try:
        if DC_StartDayEntry.get() in ("dd", ""):
            DC_StartDayEntry.delete(0, "end")
            DC_StartDayEntry.insert(0, day)
        currentDay = int(DC_StartDayEntry.get())

        if DC_StartMonthEntry.get() in ("mm", ""):
            DC_StartMonthEntry.delete(0, "end")
            DC_StartMonthEntry.insert(0, month)
        currentMonth = int(DC_StartMonthEntry.get())

        if DC_StartYearEntry.get() in ("yyyy", ""):
            DC_StartYearEntry.delete(0, "end")
            DC_StartYearEntry.insert(0, year)
        currentYear = int(DC_StartYearEntry.get())

        currentDate = datetime.date(currentYear, currentMonth, currentDay)

        if DC_EndDayEntry.get() in ("dd", ""):
            DC_EndDayEntry.delete(0, "end")
            DC_EndDayEntry.insert(0, day)
        daysToAdd = int(DC_EndDayEntry.get())

        if DC_EndMonthEntry.get() in ("mm", ""):
            DC_EndMonthEntry.delete(0, "end")
            DC_EndMonthEntry.insert(0, month)
        monthsToAdd = int(DC_EndMonthEntry.get())

        if DC_EndYearEntry.get() in ("yyyy", ""):
            DC_EndYearEntry.delete(0, "end")
            DC_EndYearEntry.insert(0, year)
        yearsToAdd = int(DC_EndYearEntry.get())

        destinationDate = datetime.date(yearsToAdd, monthsToAdd, daysToAdd)
        DC_outcome.config(text=f"{(destinationDate - currentDate).days} Days")
        addition((destinationDate - currentDate).days, currentDate)

    except ValueError:
        DC_outcome.config(text="Invalid date input")
    except Exception as e:
        DC_outcome.config(text=f"An unexpected error occurred: {e}")

def DA_calculation():
    try:
        currentDay = int(DA_StartDayEntry.get()) if DA_StartDayEntry.get() not in ("dd", "") else day
        currentMonth = int(DA_StartMonthEntry.get()) if DA_StartMonthEntry.get() not in ("mm", "") else month
        currentYear = int(DA_StartYearEntry.get()) if DA_StartYearEntry.get() not in ("yyyy", "") else year
        currentDate = datetime.date(currentYear, currentMonth, currentDay)

        daysToAdd = int(DA_EndDayEntry.get()) if DA_EndDayEntry.get() not in ("dd", "") else 0
        monthsToAdd = int(DA_EndMonthEntry.get()) if DA_EndMonthEntry.get() not in ("mm", "") else 0
        yearsToAdd = int(DA_EndYearEntry.get()) if DA_EndYearEntry.get() not in ("yyyy", "") else 0
        weeksToAdd = int(DA_EndWeekEntry.get()) if DA_EndWeekEntry.get() not in ("ww", "") else 0

        delta = relativedelta(days=daysToAdd, months=monthsToAdd, years=yearsToAdd, weeks=weeksToAdd)
        op_selection = DA_operation.current()
        dt_selection = DA_dateFormat.current()
        if op_selection == 0:
            destinationDate = currentDate + delta
        elif op_selection == 1:
            destinationDate = currentDate - delta
        if dt_selection == 0:
            DA_outcome.config(text=destinationDate.strftime("%d/%m/%Y"))
        elif dt_selection == 1:
            DA_outcome.config(text=destinationDate.strftime("%m/%d/%Y"))

    except ValueError as e:
        DA_outcome.config(text=f"Error: {e}")
    except Exception as e:
        DA_outcome.config(text=f"An unexpected error occurred: {e}")

def addition(days, current):
    end_date = current + timedelta(days=days)

    rd = relativedelta(end_date, current)
    years = rd.years
    months = rd.months
    days_remaining = rd.days
    if days > 365:
        if months != 0:
            DC_outcomeAdd.config(text=f"{years} years, {months} months, {days_remaining} days")
        else:
            DC_outcomeAdd.config(text=f"{years} years, {days_remaining} days")
    elif days <= 365 and days >= 31:
        DC_outcomeAdd.config(text=f"{months} months, {days_remaining} days")
    else:
        DC_outcomeAdd.config(text="")

'''
def addition(days, current):
    end_date = current + datetime.timedelta(days=days)
    years = end_date.year - current.year
    months = ((end_date.month - current.month) + years * 12) -1
    days_remaining = (end_date - datetime.date(end_date.year, end_date.month, 1)).days +1

    if months <= 0:
      DC_outcomeAdd.config(text="")
    elif years == 0:
        DC_outcomeAdd.config(text=f"{months} months, {days_remaining} days")
    elif months < 12:
        DC_outcomeAdd.config(text=f"{years} years, {months} months, {days_remaining} days")
    else:
      DC_outcomeAdd.config(text=f"{years} years, {months % 12} months, {days_remaining} days")
'''

# Window settings
root = tk.Tk()
root.title("Date Calculator")
root.iconbitmap(default=ICON_PATH)
root.geometry("400x260")
root.resizable(False, False)

# Tab settings
notebook = ttk.Notebook(root)
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
notebook.add(tab1,text="Day Counter")
notebook.add(tab2,text="Day Adder")
notebook.pack(expand=True,fill="both")

# Widget settings
DC_StartDate = tk.Label(tab1, text="Start Date", font=("Arial", 20))
DC_TodayStart = tk.Button(tab1, text="Today", command= lambda : today(0))
DC_StartDay = tk.Label(tab1, text="Day:")
DC_StartDayEntry = tk.Entry(tab1, width=3)
DC_StartDayEntry.insert(0,"dd")
DC_StartDayEntry.bind("<FocusIn>", handleEvent)
DC_StartMonth = tk.Label(tab1, text="Month:")
DC_StartMonthEntry = tk.Entry(tab1, width=3)
DC_StartMonthEntry.insert(0,"mm")
DC_StartMonthEntry.bind("<FocusIn>", handleEvent)
DC_StartYear = tk.Label(tab1, text="Year:")
DC_StartYearEntry = tk.Entry(tab1, width=4)
DC_StartYearEntry.insert(0,"yyyy")
DC_StartYearEntry.bind("<FocusIn>", handleEvent)
DC_EndDay = tk.Label(tab1, text="Day:")
DC_EndDayEntry = tk.Entry(tab1, width=3)
DC_EndDayEntry.insert(0,"dd")
DC_EndDayEntry.bind("<FocusIn>", handleEvent)
DC_EndMonth = tk.Label(tab1, text="Month:")
DC_EndMonthEntry = tk.Entry(tab1, width=3)
DC_EndMonthEntry.insert(0,"mm")
DC_EndMonthEntry.bind("<FocusIn>", handleEvent)
DC_EndYear = tk.Label(tab1, text="Year:")
DC_EndYearEntry = tk.Entry(tab1, width=4)
DC_EndYearEntry.insert(0,"yyyy")
DC_EndYearEntry.bind("<FocusIn>", handleEvent)
DC_EndDate = tk.Label(tab1, text="End Date", font=("Arial", 20))
DC_TodayEnd = tk.Button(tab1, text="Today", command= lambda : today(1))
DC_calculate = tk.Button(tab1, text="Calculate duration", command=DC_calculation)
DC_outcome = tk.Label(tab1, text="", font=("Arial", 20))
DC_outcomeAdd = tk.Label(tab1, text="")
DA_StartDate = tk.Label(tab2, text="Start Date", font=("Arial", 20))
DA_TodayStart = tk.Button(tab2, text="Today", command= lambda : today(2))
DA_StartDay = tk.Label(tab2, text="Day:")
DA_StartDayEntry = tk.Entry(tab2, width=3)
DA_StartDayEntry.insert(0,"dd")
DA_StartDayEntry.bind("<FocusIn>", handleEvent)
DA_StartMonth = tk.Label(tab2, text="Month:")
DA_StartMonthEntry = tk.Entry(tab2, width=3)
DA_StartMonthEntry.insert(0,"mm")
DA_StartMonthEntry.bind("<FocusIn>", handleEvent)
DA_StartYear = tk.Label(tab2, text="Year:")
DA_StartYearEntry = tk.Entry(tab2, width=4)
DA_StartYearEntry.insert(0,"yyyy")
DA_StartYearEntry.bind("<FocusIn>", handleEvent)
DA_operation = ttk.Combobox(tab2, state="readonly", width=14, values=["Add", "Subtract"])
DA_operation.current(0)
DA_EndDay = tk.Label(tab2, text="Days")
DA_EndDayEntry = tk.Entry(tab2, width=5)
DA_EndDayEntry.bind("<FocusIn>", handleEvent)
DA_EndWeek = tk.Label(tab2, text="Weeks:")
DA_EndWeekEntry = tk.Entry(tab2, width=5)
DA_EndWeekEntry.bind("<FocusIn>", handleEvent)
DA_EndMonth = tk.Label(tab2, text="Months:")
DA_EndMonthEntry = tk.Entry(tab2, width=5)
DA_EndMonthEntry.bind("<FocusIn>", handleEvent)
DA_EndYear = tk.Label(tab2, text="Years:")
DA_EndYearEntry = tk.Entry(tab2, width=5)
DA_EndYearEntry.bind("<FocusIn>", handleEvent)
DA_calculate = tk.Button(tab2, text="Calculate new date", command=DA_calculation)
DA_outcome = tk.Label(tab2, text="", font=("Arial", 20))
DA_dateFormat = ttk.Combobox(tab2, state="readonly", width=14, values=["dd/mm/yyyy", "mm/dd/yyyy"])
DA_dateFormat.current(0)

# Widget placements
DC_StartDate.place(x=10,y=10)
DC_TodayStart.place(x=10,y=115)
DC_StartDay.place(x=10,y=65)
DC_StartDayEntry.place(x=13,y=90)
DC_StartMonth.place(x=60,y=65)
DC_StartMonthEntry.place(x=63,y=90)
DC_StartYear.place(x=110,y=65)
DC_StartYearEntry.place(x=113,y=90)
DC_EndDate.place(x=200,y=10)
DC_TodayEnd.place(x=200,y=115)
DC_EndDay.place(x=200,y=65)
DC_EndDayEntry.place(x=203,y=90)
DC_EndMonth.place(x=250,y=65)
DC_EndMonthEntry.place(x=253,y=90)
DC_EndYear.place(x=300,y=65)
DC_EndYearEntry.place(x=303,y=90)
DC_calculate.place(x=10,y=180)
DC_outcome.place(x=200,y=175)
DC_outcomeAdd.place(x=200,y=210)
DA_StartDate.place(x=10,y=10)
DA_TodayStart.place(x=10,y=115)
DA_StartDay.place(x=10,y=65)
DA_StartDayEntry.place(x=13,y=90)
DA_StartMonth.place(x=60,y=65)
DA_StartMonthEntry.place(x=63,y=90)
DA_StartYear.place(x=110,y=65)
DA_StartYearEntry.place(x=113,y=90)
DA_operation.place(x=200,y=20)
DA_EndDay.place(x=200,y=65)
DA_EndDayEntry.place(x=203,y=90)
DA_EndWeek.place(x=250,y=65)
DA_EndWeekEntry.place(x=253,y=90)
DA_EndMonth.place(x=300,y=65)
DA_EndMonthEntry.place(x=303,y=90)
DA_EndYear.place(x=350,y=65)
DA_EndYearEntry.place(x=353,y=90)
DA_calculate.place(x=10,y=180)
DA_outcome.place(x=200,y=175)
DA_dateFormat.place(x=10,y=210)

if __name__ == "__main__":
    root.mainloop()