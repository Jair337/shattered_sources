import base64
import io
from encodings import utf_8

import matplotlib.pyplot as plt
import sqlite3
from config import db_path_normalized
from flask import render_template



def time_charts_event_count_service():
    with sqlite3.connect(db_path_normalized) as conn:
        cursor = conn.cursor()

        ## Pulls all the needed data from the db, STRFTIME slices off everything but the date from the event.
        ## Then it groups the events by date and counts how many events happened on that date.
        cursor.execute('''SELECT STRFTIME('%Y-%m-%d', time_stamp) AS date, COUNT(*) AS event_count
                          FROM events_normalized
                          GROUP BY date''')
        data = cursor.fetchall()

        ## Split the data into 2 lists to plot it
        dates = [row[0] for row in data]
        event_counts = [row[1] for row in data]

        ## All of the parameters for the plot
        fig, ax = plt.subplots(facecolor='#0a1118')

        ax.set_facecolor('#111e2e')
        ax.plot(dates, event_counts, color='#FF6600', marker='o', linestyle='-', markersize=4, markerfacecolor='white',
                linewidth=1)
        ax.grid(color='gray', linestyle='--', linewidth=0.3)
        ax.set_title('Event count daily', color='white')
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Event Count', color='white')
        ax.tick_params(axis='x', rotation=70, colors='white')
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)
        ax.xaxis.set_major_locator(plt.MaxNLocator(15))

        fig.tight_layout()

    return fig

def time_charts_event_count_memory():
    fig = time_charts_event_count_service()
    img_buffer_event_count = io.BytesIO()
    fig.savefig(img_buffer_event_count, format='png')
    img_buffer_event_count.seek(0)
    plt.close(fig)
    chart_b64 = base64.b64encode(img_buffer_event_count.getvalue()).decode('utf_8')
    return chart_b64



