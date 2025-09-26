import rasterio
import numpy as np
import os

# Example: Read a GeoTIFF file
def read_geotiff(file_path):
    with rasterio.open(file_path) as src:
        data = src.read()  # reads all bands
        profile = src.profile
    return data, profile

# Example: Save a patch
def save_patch(patch, out_path, profile):
    profile.update({
        'height': patch.shape[1],
        'width': patch.shape[2]
    })
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(patch)
def extract_patches(data, patch_size=64, save_dir="outputs"):
    """
    Cut a multi-band GeoTIFF array into square patches.
    Args:
        data: np.array with shape (bands, height, width)
        patch_size: size of square patch
        save_dir: folder to save patches
    """
    os.makedirs(save_dir, exist_ok=True)
    bands, height, width = data.shape
    patch_count = 0

    for i in range(0, height, patch_size):
        for j in range(0, width, patch_size):
            if i+patch_size <= height and j+patch_size <= width:
                patch = data[:, i:i+patch_size, j:j+patch_size]
                patch_path = os.path.join(save_dir, f"patch_{patch_count}.tif")
                
                # Save patch
                with rasterio.open(
                    patch_path, 'w',
                    driver='GTiff',
                    height=patch.shape[1],
                    width=patch.shape[2],
                    count=bands,
                    dtype=patch.dtype
                ) as dst:
                    dst.write(patch)
                
                patch_count += 1

    print(f"Saved {patch_count} patches in {save_dir}")
if __name__ == "__main__":
    data, profile = read_geotiff("data/sample.tif")
    extract_patches(data, patch_size=64, save_dir="outputs")
