from database.db_manager import (
    initialize_database,
    save_event,
    get_events
)

initialize_database()

save_event(
    "Restricted Zone Intrusion",
    101,
    "00:00:12",
    "Person entered restricted area"
)

save_event(
    "Loitering",
    102,
    "00:00:25",
    "Person remained in monitored area"
)

save_event(
    "Potential Unattended Object",
    103,
    "00:00:40",
    "Stationary bag detected"
)

print("\nDATABASE EVENTS:\n")

for event in get_events():
    print(event)