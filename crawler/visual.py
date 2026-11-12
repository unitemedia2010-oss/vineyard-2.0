"""
Visual Auditor and Multi-Viewport Screenshot Capturer using Playwright
"""
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, ViewportSize
from crawler.config import config

logger = logging.getLogger("crawler.visual")

class VisualAuditor:
    def __init__(self):
        self.screenshots_dir = config.screenshots_path
        self.viewports = {
            "desktop": config.viewport_desktop,
            "tablet": config.viewport_tablet,
            "mobile": config.viewport_mobile
        }

    def _slugify_url(self, url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        if not path:
            return "homepage"
        clean = re.sub(r"[^a-zA-Z0-9_\-]+", "-", path).strip("-")
        return clean or "page"

    def audit_page(self, url: str, capture_screenshots: bool = True) -> Dict[str, Any]:
        """
        Audit visual tokens, CSS attributes, typography, color palette, animations, and take screenshots across 3 viewports.
        """
        slug = self._slugify_url(url)
        report: Dict[str, Any] = {
            "url": url,
            "slug": slug,
            "typography": {},
            "colors": {},
            "components": {},
            "animations": [],
            "screenshots": {}
        }

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            for vp_name, vp_dims in self.viewports.items():
                context = browser.new_context(
                    viewport=ViewportSize(width=vp_dims["width"], height=vp_dims["height"]),
                    user_agent=config.user_agent,
                    device_scale_factor=1
                )
                page = context.new_page()

                try:
                    logger.info(f"Navigating to {url} [{vp_name} {vp_dims['width']}x{vp_dims['height']}]")
                    page.goto(url, wait_until="networkidle", timeout=config.timeout * 1000)

                    # Extract CSS Design Tokens only on desktop pass
                    if vp_name == "desktop":
                        audit_script = """
                        () => {
                            const styles = {
                                colors: new Set(),
                                fonts: new Set(),
                                headings: {},
                                buttons: [],
                                animations: []
                            };

                            const bodyStyle = window.getComputedStyle(document.body);
                            styles.body = {
                                fontFamily: bodyStyle.fontFamily,
                                fontSize: bodyStyle.fontSize,
                                color: bodyStyle.color,
                                backgroundColor: bodyStyle.backgroundColor
                            };

                            // Scan all elements for unique fonts and colors
                            document.querySelectorAll('*').forEach(el => {
                                const cs = window.getComputedStyle(el);
                                if (cs.color) styles.colors.add(cs.color);
                                if (cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)') {
                                    styles.colors.add(cs.backgroundColor);
                                }
                                if (cs.fontFamily) styles.fonts.add(cs.fontFamily);
                                if (cs.transition && cs.transition !== 'all 0s ease 0s' && cs.transition !== 'none') {
                                    styles.animations.push({ tag: el.tagName, transition: cs.transition });
                                }
                            });

                            // Capture header and button specifics
                            const btn = document.querySelector('button, .btn, .button, a[class*="btn"]');
                            if (btn) {
                                const bcs = window.getComputedStyle(btn);
                                styles.sampleButton = {
                                    backgroundColor: bcs.backgroundColor,
                                    color: bcs.color,
                                    borderRadius: bcs.borderRadius,
                                    padding: bcs.padding,
                                    fontSize: bcs.fontSize
                                };
                            }

                            return {
                                body: styles.body,
                                colors: Array.from(styles.colors).slice(0, 20),
                                fonts: Array.from(styles.fonts).slice(0, 10),
                                sampleButton: styles.sampleButton,
                                animationsCount: styles.animations.length
                            };
                        }
                        """
                        try:
                            token_data = page.evaluate(audit_script)
                            report["typography"]["body"] = token_data.get("body")
                            report["typography"]["fonts"] = token_data.get("fonts")
                            report["colors"]["palette"] = token_data.get("colors")
                            report["components"]["sampleButton"] = token_data.get("sampleButton")
                            report["animations_detected"] = token_data.get("animationsCount")
                        except Exception as e:
                            logger.warning(f"Error evaluating tokens: {e}")

                    # Capture screenshot
                    if capture_screenshots:
                        out_dir = self.screenshots_dir / vp_name
                        out_dir.mkdir(parents=True, exist_ok=True)
                        file_path = out_dir / f"{slug}.png"

                        # Full page screenshot
                        page.screenshot(path=str(file_path), full_page=True)
                        report["screenshots"][vp_name] = str(file_path)
                        logger.info(f"Captured screenshot: {file_path}")

                except Exception as e:
                    logger.warning(f"Error capturing visual audit for {url} ({vp_name}): {e}")
                finally:
                    context.close()

            browser.close()

        return report
