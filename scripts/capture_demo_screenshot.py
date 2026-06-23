from pathlib import Path

from playwright.sync_api import sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_PATH = PROJECT_ROOT / "314831018_HW7.png"
EDGE_PATH = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
APP_URL = "http://127.0.0.1:7860"


def main() -> None:
    if not EDGE_PATH.exists():
        raise FileNotFoundError(f"Microsoft Edge was not found at {EDGE_PATH}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=str(EDGE_PATH),
            headless=True,
            args=["--disable-gpu"],
        )
        page = browser.new_page(viewport={"width": 1440, "height": 1200})
        page.goto(APP_URL, wait_until="networkidle")
        page.get_by_text("TurtleCare AI", exact=True).wait_for(timeout=30000)

        textareas = page.locator("textarea")
        textareas.nth(0).fill("我的烏龜需要 UVB 嗎？")
        page.get_by_role("button", name="產生回答").click()
        page.wait_for_function(
            "() => document.querySelectorAll('textarea')[1]?.value?.includes('Mock TurtleCare AI answer')",
            timeout=30000,
        )

        page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
        browser.close()

    print(f"Saved demo screenshot: {SCREENSHOT_PATH}")


if __name__ == "__main__":
    main()
