import rasterio
import matplotlib.pyplot as plt

# Replace with your actual GeoTIFF path
file_path = "sample.tif"

with rasterio.open(file_path) as src:
    # For Sentinel-2 → bands 4=Red, 3=Green, 2=Blue
    img = src.read([4, 3, 2])  

    plt.imshow(img.transpose(1, 2, 0))
    plt.title("Satellite Image (RGB Composite)")
    plt.axis("off")
    plt.show()
