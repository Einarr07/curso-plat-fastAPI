from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def root():
    return {'Message': 'Hello World'}

country_timezones = {
    "CO": "America/Bogota",
    "US": "America/New_York",
    "EC": "America/Guayaquil",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
}

@app.get("/get-time/{iso_code}")
async def get_time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = ZoneInfo(timezone_str)
    now = datetime.now(tz)
    return f'La hora en {timezone_str} es: {now.isoformat()}'

@app.get("/format/{frt}")
async def get_hour(frt: str, iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)

    if timezone_str is None:
        raise HTTPException(status_code=404, detail="Pais no encontrado")

    tz = ZoneInfo(timezone_str)
    now = datetime.now(tz)

    try:
        formatted = now.strftime(frt)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Formato de fecha y hora no valido")

    return {
        "country_code": iso,
        'timezone': timezone_str,
        'formatted': frt,
        'time': formatted
    }


