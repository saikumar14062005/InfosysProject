
import matplotlib.pyplot as plt

def create_pie_chart(sentiment_counts):
    labels = sentiment_counts.keys()
    sizes = sentiment_counts.values()
    colors = ['#76c893', '#f94144', '#f9c74f']  # Positive, Negative, Neutral colors
    explode = (0.1, 0, 0)  # Slightly explode the Positive slice for emphasis

    fig, ax = plt.subplots(figsize = (3,3))
    ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        shadow=True
    )
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    return fig
