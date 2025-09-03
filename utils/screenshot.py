import os
from datetime import datetime

def take_screenshot(driver, class_name, method_name):
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = os.path.join('utils', 'screenshots', 'error_screenshots', today)
    os.makedirs(directory, exist_ok=True)
    filename = f"{class_name}.{method_name}_{timestamp}.png"
    driver.save_screenshot(os.path.join(directory, filename))
