from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from datetime import datetime
import calendar

app = FastAPI()

class DateList(BaseModel):
    dates: List[str]

def format_calendar(dates: List[str]) -> str:
    # Преобразуем строки в datetime.date
    marked_dates = [datetime.strptime(date_str, "%d-%m-%Y").date() for date_str in dates]
    
    # Все даты должны быть одного месяца
    if not all(date.month == marked_dates[0].month and date.year == marked_dates[0].year for date in marked_dates):
        return "❌ Все даты должны быть в одном месяце и году."

    year = marked_dates[0].year
    month = marked_dates[0].month

    # Календарь на месяц
    cal = calendar.Calendar()
    weeks = cal.monthdayscalendar(year, month)

    # Заголовок
    result = f"Календарь активностей для {year}-{month:02d}:\n"
    result += "Пн Вт Ср Чт Пт Сб Вс\n"

    # Преобразуем даты в список чисел
    marked_day_numbers = [d.day for d in marked_dates]

    for week in weeks:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            elif day in marked_day_numbers:
                line += "✅ "
            elif day < 10:
                line += f"{day}  "
            else:
                line += f"{day} "
        result += line.rstrip() + "\n"

    return result.strip()

@app.post("/calendar")
async def generate_calendar(data: DateList):
    calendar_text = format_calendar(data.dates)
    r
