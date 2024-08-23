import os
import pandas as pd
from bokeh.io import output_file, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, ImageURL, HoverTool
from bokeh.layouts import column
import webbrowser
import re

def normalize_name(name):
    # Extract the part after the final underscore
    name = name.rsplit('_', 1)[-1]
    # Add a space before every capital letter other than the first
    name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
    return name

def visualize_csv_data(csv_file_path, image_folder_path, plot_title, x_label):
    # Read the CSV file
    csvPlacementFolder = 'Data/csvPlacements/'
    data = pd.read_csv(csvPlacementFolder + csv_file_path)
    print('Data read from', csvPlacementFolder + csv_file_path)

    # Parse the data
    items = []
    for _, row in data.iterrows():
        items.append({
            'name': row['Name'],
            'avg_placement': float(row['Average Placement']),
            'total_placement': int(row['Total Placement']),
            'count': int(row['Count'])
        })

    # Extract data for plotting
    names = [item['name'] for item in items]
    avg_placements = [item['avg_placement'] for item in items]
    image_urls = []

    for item in items:
        image_path = os.path.join(image_folder_path, f"{item['name']}.png")
        if os.path.exists(image_path):
            # Save the image URL for Bokeh
            image_urls.append(image_path)
        else:
            print(f"Image not found for item: {item['name']}")
            image_urls.append(None)

    # Create a ColumnDataSource
    source = ColumnDataSource(data=dict(
        names=names,
        avg_placements=avg_placements,
        image_urls=image_urls,
        display_names=[normalize_name(name) for name in names]
    ))

    # Create a plot
    p = figure(x_range=[normalize_name(name) for name in names], height=600, width=800, title=plot_title,
               toolbar_location=None, tools="")

    # Add dots
    p.scatter(x='display_names', y='avg_placements', size=10, source=source, legend_field="display_names", line_color='white', fill_color='skyblue')

    # Add images at the bottom
    p.add_glyph(source, ImageURL(url="image_urls", x="display_names", y=0, w=1, h=1, anchor="bottom_center"))

    # Customize plot
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.visible = False  # Hide the x-axis labels
    p.yaxis.axis_label = 'Average Placement'
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    # Add hover tool
    hover = HoverTool()
    hover.tooltips = [
        ("Name", "@display_names"),
        ("Average Placement", "@avg_placements"),
    ]
    p.add_tools(hover)

    return p

def make_graphs():
    plots = []
    plots.append(visualize_csv_data('item_placements.csv', 'images/items', 'Average Placement of Items', 'Items'))
    plots.append(visualize_csv_data('unit_placements.csv', 'images/champions', 'Average Placement of Champions', 'Champions'))
    plots.append(visualize_csv_data('total_trait_placement.csv', 'images/traits', 'Average Placement of Traits', 'Traits'))
    plots.append(visualize_csv_data('augment_placements.csv', 'images/augments', 'Average Placement of Augments', 'Augments'))

    # Arrange plots in a column layout
    layout = column(*plots)

    # Output to a single HTML file
    output_file_path = os.path.abspath("Output/combined_plots.html")
    output_file(output_file_path)
    save(layout)

    # Automatically open the HTML file in the default web browser
    webbrowser.open(output_file_path)

make_graphs()