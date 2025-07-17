import os
from PIL import Image, ImageChops
from playwright.sync_api import Page
import shutil

def get_snapshot_paths(name: str):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    snapshots_dir = os.path.join(project_root, "snapshots")
    os.makedirs(snapshots_dir, exist_ok=True)

    baseline = os.path.join(snapshots_dir, f"{name}_baseline.png")
    current = os.path.join(snapshots_dir, f"{name}_current.png")
    diff = os.path.join(snapshots_dir, f"{name}_diff.png")
    return baseline, current, diff

def compare_images(baseline_path, current_path, diff_path):
    baseline = Image.open(baseline_path)
    current = Image.open(current_path)
    diff = ImageChops.difference(baseline, current)

    if diff.getbbox() is None:
        return True
    else:
        diff.save(diff_path)
        return False

def assert_visual_match(page: Page, name: str):
    baseline_path, current_path, diff_path = get_snapshot_paths(name)

    # Good for ensuring page is stable before capturing a screen.
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    page.screenshot(path=current_path, full_page=True)
    # First time: save as baseline
    if not os.path.exists(baseline_path):
        print(f"[INFO] No baseline found for '{name}'. Saving current as baseline.")
        shutil.copy(current_path, baseline_path)
        return

    assert compare_images(baseline_path, current_path, diff_path), f"Visual regression detected for '{name}'!"
