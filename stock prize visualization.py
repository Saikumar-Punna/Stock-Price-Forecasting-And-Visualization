import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
import mplcursors
import pygame
import seaborn as sns
import pandas as pd
from matplotlib.animation import FuncAnimation
import altair as alt

# Function to fetch financial data with error handling
def fetch_financial_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        # Handle the error (provide default data, log the issue, or exit gracefully)
        return pd.DataFrame()

# Download stock price data
symbol = "AAPL"
data = fetch_financial_data(symbol, start_date="2023-10-01", end_date="2023-11-30")

# Define stock split dates (modify as needed)
stock_split_dates = ["2023-01-10", "2023-01-20"]

# Function to generate colors dynamically based on the length of data
def generate_colors(length):
    """Generate a color palette based on the coolwarm scheme.
    
    Parameters:
    - length (int): Number of colors needed.
    
    Returns:
    - list: Color palette.
    """
    return sns.color_palette("coolwarm", n_colors=length - 1)

# Load Seaborn color palette
colors = generate_colors(len(data))

# Set up the figure and axes with adjusted size and DPI
fig, ax = plt.subplots(figsize=(12, 6), dpi=80)  # Adjusted figure size and dpi
mplcursors.cursor(hover=True)

# Slider for controlling the timeframe
ax_slider = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Timeframe', 0, len(data), valinit=len(data), valstep=1)

# Check buttons for interactive legend control
lines = []
rax = plt.axes([0.91, 0.4, 0.1, 0.15], facecolor='lightgoldenrodyellow')
labels = [f'Line {i + 1}' for i in range(len(data))]
visibility = [True] * len(data)
check = CheckButtons(rax, labels, visibility)

# Function to highlight specific dates
def highlight_date(date):
    """Highlight a specific date on the plot.
    
    Parameters:
    - date (str): Date to be highlighted in 'YYYY-MM-DD' format.
    """
    plt.axvline(pd.to_datetime(date), color='green', linestyle='--', linewidth=1)

# Update function for animation
def update(frame):
    """Update function for the animation.
    
    Parameters:
    - frame (int): Frame index.
    """
    plt.cla()
    
    # Ensure the frame is within the valid range
    frame = min(frame, len(data) - 1)
    
    # Plot stock price data
    ax.plot(data.index[:frame + 1], data['Close'][:frame + 1], label='Stock Price', color=colors[min(frame, len(colors) - 1)])
    
    # Plot artistic elements based on financial data trends
    # Example: Highlight stock split dates
    for split_date in stock_split_dates:
        highlight_date(split_date)
    
    # Additional artistic elements or technical indicators can be added here
    
    # Update legend
    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels)
    
    # Additional customization can be done here
    
    # Fading effect for Market Peak annotation
    if frame == len(data) - 1:
        annotation = ax.text(data.index[-1], data['Close'].max(), 'Market Peak', 
                             verticalalignment='bottom', horizontalalignment='right',
                             color='red', fontsize=8)
        animate_annotation(annotation)
    
    plt.title('Stock Price Evolution')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    
    # Add technical indicators on each frame if needed
    plot_technical_indicators()

# Volume control icons
volume_icons_ax = plt.axes([0.91, 0.25, 0.08, 0.1], facecolor='lightgoldenrodyellow')
button_volume_up = Button(volume_icons_ax, 'Volume Up')
button_volume_down = Button(volume_icons_ax, 'Volume Down')

def volume_up(event):
    """Increase the volume by 10%. Example function."""
    current_volume = pygame.mixer.music.get_volume()
    new_volume = min(current_volume + 0.1, 1.0)  # Limit volume to 1.0
    pygame.mixer.music.set_volume(new_volume)

def volume_down(event):
    """Decrease the volume by 10%. Example function."""
    current_volume = pygame.mixer.music.get_volume()
    new_volume = max(current_volume - 0.1, 0.0)  # Limit volume to 0.0
    pygame.mixer.music.set_volume(new_volume)

button_volume_up.on_clicked(volume_up)
button_volume_down.on_clicked(volume_down)

# Date Range Selection Bar
date_range_ax = plt.axes([0.2, 0.06, 0.65, 0.02], facecolor='lightgoldenrodyellow')
date_range_slider = Slider(date_range_ax, 'Date Range', 0, len(data), valinit=len(data), valstep=1)

# Tooltip Enhancements
mplcursor = mplcursors.cursor(hover=True)

def hover_callback(sel):
    """Show additional information in the tooltip. Example function."""
    date = data.index[int(sel.target[0])]
    close_price = data['Close'].iloc[int(sel.target[0])]
    mplcursor.annotate(f"{date}\nClose: {close_price:.2f}", xy=sel.target, xytext=(-10, 10),
                       textcoords='offset points', arrowprops=dict(facecolor='black', arrowstyle='wedge,tail_width=0.7'))

mplcursor.connect("add", hover_callback)

# Color Palette Customization
palette_ax = plt.axes([0.91, 0.15, 0.08, 0.1], facecolor='lightgoldenrodyellow')
palette_button = Button(palette_ax, 'Customize Palette')

def customize_palette(event):
    """Allow users to choose a different color palette. Example function."""
    new_palette = sns.color_palette("husl", n_colors=len(data) - 1)
    for i, line in enumerate(lines):
        line.set_color(new_palette[i])

palette_button.on_clicked(customize_palette)

# Download Option
download_ax = plt.axes([0.91, 0.05, 0.08, 0.05], facecolor='lightgoldenrodyellow')
download_button = Button(download_ax, 'Download Image')

def download_image(event):
    """Save the current figure as a PNG image with adjusted DPI. Example function."""
    plt.savefig('static_visualization.png', bbox_inches='tight', dpi=300)

download_button.on_clicked(download_image)

# Function to plot technical indicators
def plot_technical_indicators():
    """Plot technical indicators. Example function."""
    # Example: Plot a 50-day simple moving average
    ma_50 = data['Close'].rolling(window=50).mean()
    ax.plot(data.index, ma_50, label='50-Day MA', linestyle='--', color='orange')
    
    # Add additional indicators as needed
    # ...

# Function for interactive annotations
def annotate_event(event):
    """Allow users to add/edit annotations on double-click. Example function."""
    if event.dblclick:
        annotation_text = input("Enter annotation text: ")
        ax.annotate(annotation_text, (event.xdata, event.ydata),
                    xytext=(-10, 10), textcoords='offset points',
                    arrowprops=dict(facecolor='black', arrowstyle='wedge,tail_width=0.7'))
        plt.draw()

# Connect the annotation function to the figure
fig.canvas.mpl_connect('button_press_event', annotate_event)

# Function to highlight specific dates
def highlight_date(date):
    """Highlight a specific date on the plot. Example function."""
    plt.axvline(pd.to_datetime(date), color='green', linestyle='--', linewidth=1)

# Function to generate a fading effect for annotations
def animate_annotation(annotation, duration=1.0):
    """Generate a fading effect for annotations. Example function."""
    annotation.set_animated(True)
    alpha_values = [annotation.get_alpha(), 0.0]  # Start from current alpha to fully transparent
    annotation.set_alpha(alpha_values[0])
    
    def update_alpha(frame):
        alpha = alpha_values[frame]
        annotation.set_alpha(alpha)
        return annotation,
    
    anim = FuncAnimation(fig, update_alpha, frames=len(alpha_values), interval=duration * 1000 / len(alpha_values), blit=True)

# Create animation
animation = FuncAnimation(fig, update, frames=len(data) + 1, interval=100, repeat=False)

# Save the animation as a GIF with adjusted DPI
animation.save('stock_price_animation.gif', writer='pillow', fps=10, dpi=300)

# Display the saved GIF
plt.show()

# Print the first few rows of the data
print(data.head())

# Design a simple scatter plot with color representing closing prices
plt.scatter(data.index, data['Close'], c=data['Close'], cmap='viridis')
plt.title('Closing Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.colorbar(label='Closing Price')
plt.show()

# Connect data to art: Use a scatter plot with colors based on closing prices
plt.scatter(data.index, data['Close'], c=data['Close'], cmap='plasma')
plt.title('Closing Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.colorbar(label='Closing Price')
plt.show()

# Experiment with a line plot and color gradient based on closing prices
plt.plot(data.index, data['Close'], color='blue', linewidth=2, alpha=0.7)
plt.fill_between(data.index, data['Close'], color='blue', alpha=0.2)
plt.title('Closing Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.show()

# Remove one of the sliders
# ax_slider = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
# slider = Slider(ax_slider, 'Timeframe', 0, len(data), valinit=len(data), valstep=1)

# Add a slider for controlling the time frame
ax_slider = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Timeframe', 0, len(data), valinit=len(data), valstep=1)

# Update function for animation
def update(frame):
    """Update function for the animation.
    
    Parameters:
    - frame (int): Frame index.
    """
    plt.cla()
    ax.plot(data.index[:frame + 1], data['Close'][:frame + 1], color='blue', linewidth=2, alpha=0.7)
    plt.title('Closing Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')

slider.on_changed(update)
plt.show()
