# GIBZ-BM_P3-Projekt_Sensor

SQL Query to get information from sensordata.db
```
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
LIMIT 50;
```