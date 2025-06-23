import sqlite3

def get_latest_device():
    # Verbindung zur SQLite-Datenbank herstellen
    con = sqlite3.connect('sensordata.db')
    con.row_factory = sqlite3.Row  # Ermöglicht Zugriff per Spaltennamen
    cur = con.cursor()

    # Abfrage: neuester Datensatz (nur 1 Zeile)
    cur.execute("""
        SELECT
            d.device_id,
            d.application_id,
            p.temperature,
            p.humidity,
            p.motion,
            p.light,
            p.vdd,
            p.received_at
        FROM
            payloads p
        JOIN
            devices d ON d.id = p.device_id
        ORDER BY
            p.received_at DESC
        LIMIT 1;
    """)

    row = cur.fetchone()
    con.close()

    # Wenn ein Eintrag vorhanden ist, zurückgeben
    if row:
        result = {
            "device_id": row["device_id"],
            "application_id": row["application_id"],
            "temperature": row["temperature"],
            "humidity": row["humidity"],
            "motion": row["motion"],
            "light": row["light"],
            "vdd": row["vdd"],
            "received_at": row["received_at"]
        }
        return result
    else:
        return {"message": "No data found"}