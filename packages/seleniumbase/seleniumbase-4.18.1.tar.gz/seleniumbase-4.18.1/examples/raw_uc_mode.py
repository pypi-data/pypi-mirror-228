"""SB Manager using UC Mode for evading bot-detection."""
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.open("https://nowsecure.nl/#relax")
    sb.sleep(3)
    if not sb.is_text_visible("OH YEAH, you passed!", "h1"):
        sb.get_new_driver(undetectable=True)
        sb.open("https://nowsecure.nl/#relax")
        sb.sleep(3)
    if not sb.is_text_visible("OH YEAH, you passed!", "h1"):
        if sb.is_element_visible('iframe[src*="challenge"]'):
            with sb.frame_switch('iframe[src*="challenge"]'):
                sb.click("area")
                sb.sleep(3)
    sb.assert_text("OH YEAH, you passed!", "h1", timeout=3)
