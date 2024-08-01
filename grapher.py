import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

def visualize_csv_data(csv_file_path, image_folder_path, plot_title, x_label):
    # Read the CSV file
    csvPlacementFolder = 'Data/csvPlacements/'
    with open(csvPlacementFolder+csv_file_path) as f:
        data = f.read()

    # Parse the data
    items = []
    for line in data.strip().split('\n')[1:]:  # Skip the header
        name, avg_placement, total_placement, count = line.split(',')
        items.append({
            'name': name,
            'avg_placement': float(avg_placement),
            'total_placement': int(total_placement),
            'count': int(count)
        })

    # Create a plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Extract data for plotting
    names = [item['name'] for item in items]
    avg_placements = [item['avg_placement'] for item in items]

    # Create bar chart
    bars = ax.bar(range(len(names)), avg_placements, color='skyblue')
    # Replace item names with images on the x-axis
    for i, item in enumerate(items):
        image_path = os.path.join(image_folder_path, f"{item['name']}.png")
        if os.path.exists(image_path):
            # Open the image and resize it to a fixed size
            img = Image.open(image_path)
            img = img.resize((20, 20), Image.LANCZOS)  # Resize to 20x20 pixels
            img = mpimg.pil_to_array(img)
            imagebox = OffsetImage(img, zoom=1)  # No zoom needed as we resized the image
            if('Traits' == x_label):
                ax.axhspan(-0.5, -.125, facecolor='black', alpha=0.5)  # Add black background behind x label
            ab = AnnotationBbox(imagebox, (i, 0), frameon=False, xybox=(0, -20), xycoords='data', boxcoords="offset points", pad=0)
            ax.add_artist(ab)
                
        else:
            print(f"Image not found for item: {item['name']}")

    # Add labels and title
    ax.set_xlabel(x_label)
    ax.set_ylabel('Average Placement')
    ax.set_title(plot_title)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([''] * len(names))  # Remove text labels

    plt.tight_layout()
    plt.show()


def make_graphs():
    visualize_csv_data('item_placements.csv', 'images/items', 'Average Placement of Items', 'Items')
    visualize_csv_data('unit_placements.csv', 'images/champions', 'Average Placement of Champions', 'Champions')
    visualize_csv_data('total_trait_placement.csv', 'images/traits', 'Average Placement of Traits', 'Traits')
    visualize_csv_data('augment_placements.csv', 'images/augments', 'Average Placement of Augments', 'Augments')