import matplotlib.pyplot as plt
import sqlite3
from config import db_path_normalized
import base64
import io

def country_chart_service():
    with sqlite3.connect(db_path_normalized) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT city, COUNT(*) AS city_count FROM events_normalized GROUP BY city ORDER BY COUNT(*) DESC LIMIT 10
                       ''')
        raw_data = cursor.fetchall()

        print(raw_data)

        cities, counts = zip(*raw_data)

        print(cities)
        print(counts)

        ## Create a simple horizontal bar chart
        fig, ax = plt.subplots(facecolor='#0a1118')

        ax.set_facecolor('#111e2e')
        ax.bar(cities, counts, color='#1f77b4')
        ax.grid(color='gray', linestyle='--', linewidth=0.3)
        ax.set_title('Top 10 cities by event count', color='white')
        ax.set_xlabel('City', color='white')
        ax.set_ylabel('Count', color='white')
        ax.tick_params(axis='x', rotation=45, colors='white')
        ax.tick_params(axis='y', colors='white', labelleft=True)
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)

        fig.tight_layout()


    img_buffer_event_count = io.BytesIO()
    fig.savefig(img_buffer_event_count, format='png')
    img_buffer_event_count.seek(0)
    plt.close(fig)
    chart_b64 = base64.b64encode(img_buffer_event_count.getvalue()).decode('utf_8')
    return chart_b64