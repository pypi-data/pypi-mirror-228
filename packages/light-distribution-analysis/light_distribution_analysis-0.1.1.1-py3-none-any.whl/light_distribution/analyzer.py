def rgb_to_wavelength(r, g, b):
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    hue = 0

    if max_val == min_val:
        hue = 0
    elif max_val == r:
        hue = (60 * ((g - b) / (max_val - min_val)) + 360) % 360
    elif max_val == g:
        hue = (60 * ((b - r) / (max_val - min_val)) + 120) % 360
    elif max_val == b:
        hue = (60 * ((r - g) / (max_val - min_val)) + 240) % 360

    if 0 <= hue < 60:
        return 620 + (hue / 60) * (740 - 620)
    elif 60 <= hue < 180:
        return 495 + ((hue - 60) / 120) * (570 - 495)
    elif 180 <= hue < 300:
        return 450 + ((hue - 180) / 120) * (495 - 450)
    else:
        return 620 + ((hue - 300) / 60) * (740 - 620)

def wavelength_to_frequency(wavelength):
    c = 299792458 
    return c / wavelength

def save_image(image, path, cmap=None):
    plt.imshow(image, cmap=cmap)
    plt.axis('off')
    plt.savefig(path, bbox_inches='tight', pad_inches=0)
    plt.close()

def save_image(image, path, cmap=None):
    plt.imshow(image, cmap=cmap)
    plt.axis('off')
    plt.savefig(path, bbox_inches='tight', pad_inches=0)
    plt.close()

def process_single_image(image_path, final_dir):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    save_image(image_rgb, f'{final_dir}/rgb_{os.path.basename(image_path)}')

    wavelength_image = np.apply_along_axis(lambda x: rgb_to_wavelength(x[0], x[1], x[2]), axis=2, arr=image_rgb) * 1e-9
    frequency_image = wavelength_to_frequency(wavelength_image)

    save_image(wavelength_image * 1e9, f'{final_dir}/wavelength_{os.path.basename(image_path)}', cmap='nipy_spectral')
    save_image(frequency_image / 1e12, f'{final_dir}/frequency_{os.path.basename(image_path)}', cmap='jet')

def ltd(path_to_image_1, path_to_image_2, final_dir='final_dir'):
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    process_single_image(path_to_image_1, final_dir)
    process_single_image(path_to_image_2, final_dir)

def calculate_flux(intensity_image, quantity_image):
    flux_image = intensity_image * quantity_image
    return np.sum(flux_image)