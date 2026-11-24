from database.db_manager import get_events
import pandas as pd

events = get_events()

if not events:
    print("No events found.")
else:
    df = pd.DataFrame(
        events,
        columns=["ID", "Event Type", "Object ID", "Timestamp", "Details"]
    )

    print("\n===== VISIONGUARD AI EVENT LOG =====\n")
    print(df.to_string(index=False))

    print("\n===== EVENT SUMMARY =====\n")
    print(df["Event Type"].value_counts())