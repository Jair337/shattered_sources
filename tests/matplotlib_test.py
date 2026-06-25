import matplotlib.pyplot as plt
import sqlite3
from config import db_path_normalized

def time_charts_service():
    with sqlite3.connect(db_path_normalized) as conn:
        cursor = conn.cursor()

        ## Pulls all the needed data from the db, STRFTIME slices off everything but the date from the event.
        ## Then it groups the events by date and counts how many events happened on that date.
        cursor.execute('''SELECT STRFTIME ('%Y-%m-%d', time_stamp) AS date, COUNT(*) AS event_count FROM events_normalized GROUP BY date''')
        data = cursor.fetchall()

        ## Split the data into 2 lists to plot it
        dates = [row[0] for row in data]
        event_counts = [row[1] for row in data]

        fig,ax = plt.subplots(facecolor = '#0a1118')
        ax.set_facecolor('#111e2e')

        ax.plot(dates, event_counts, color='#FF6600', marker='o', linestyle='-', markersize=4, markerfacecolor='white', linewidth=1)
        ax.grid(color='gray', linestyle='--', linewidth=0.3)
        ax.set_title('Event count daily', color='white')
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Event Count', color='white')
        ax.tick_params(axis='x', rotation=70, colors='white')
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)
        ax.xaxis.set_major_locator(plt.MaxNLocator(15))  # Show only 15 x-ticks to avoid clutter

        fig.tight_layout()

    return fig
