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
    ## Converts the image into B64 for rendering into flask endpoint
    fig = time_charts_event_count_service()
    img_buffer_event_count = io.BytesIO()
    fig.savefig(img_buffer_event_count, format='png')
    img_buffer_event_count.seek(0)
    plt.close(fig)
    chart_b64 = base64.b64encode(img_buffer_event_count.getvalue()).decode('utf_8')
    return chart_b64

def time_charts_stacked_volumes():
    with sqlite3.connect(db_path_normalized) as conn:
        cursor = conn.cursor()
        ## Selects all the dates and severities and counts them, then groups by date and severity tier
        cursor.execute('''
                       SELECT STRFTIME('%Y-%m-%d', time_stamp) AS date,
                        CASE 
                            WHEN severity >= 4 THEN 'High'
                            WHEN severity = 3 THEN 'Medium'
                            ELSE 'Low'
                       END

                       AS severity_tier,
                        COUNT(*) AS count

                    FROM events_normalized
                    GROUP BY date, severity_tier
                    ORDER BY date ASC
                       ''')

        raw_data = cursor.fetchall()

        ## Makes a dict with the dates as keys and the severity counts as values, filling in missing severity tiers with 0
        data = {}
        for date, tier, count in raw_data:
            if date not in data:
                data[date] = {"low": 0, "medium": 0, "high": 0}
            data[date][tier.lower()] = count

        ## Sets the values for the graph
        x_axis = list(data.keys())
        y_axis_low = [data[date]["low"] for date in x_axis]
        y_axis_medium = [data[date]["medium"] for date in x_axis]
        y_axis_high = [data[date]["high"] for date in x_axis]

        ## All of the parameters for the plot
        fig, ax = plt.subplots(facecolor='#0a1118')

        ax.set_facecolor('#111e2e')
        ax.stackplot(x_axis, y_axis_low, y_axis_medium, y_axis_high, colors=['#1c3d5a', '#334e68', '#FF6600'],
                     linewidth=1)
        ax.grid(color='gray', linestyle='--', linewidth=0.3)
        ax.set_title('Event count daily', color='white')
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Event Count', color='white')
        ax.tick_params(axis='x', rotation=70, colors='white')
        ax.tick_params(axis='y', colors='white', labelleft=True)
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)
        ax.xaxis.set_major_locator(plt.MaxNLocator(15))
        ax.yaxis.set_major_locator(plt.MaxNLocator(10))
        fig.tight_layout()

        img_buffer_event_count = io.BytesIO()
        fig.savefig(img_buffer_event_count, format='png')
        img_buffer_event_count.seek(0)
        plt.close(fig)
        chart_b64 = base64.b64encode(img_buffer_event_count.getvalue()).decode('utf_8')
        return chart_b64



