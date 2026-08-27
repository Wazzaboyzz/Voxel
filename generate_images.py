"""
generate_images.py
Per-slide image generation step for the Voxel pipeline.
Tries providers in order until one succeeds: Gemini -> Cloudflare Workers AI (FLUX) -> hosted FLUX API.
Runs inside GitHub Actions (not locally) so it can reach these APIs even though
local dev hardware has no GPU.

Required repo secrets (set whichever you have — script skips ones that are missing):
  GEMINI_API_KEY            - Google AI Studio key (free tier: 500 images/day)
  CLOUDFLARE_ACCOUNT_ID     - Cloudflare account ID
  CLOUDFLARE_API_TOKEN      - Cloudflare API token with Workers AI access
  FLUX_API_KEY              - key for your chosen hosted-FLUX free-tier provider
  FLUX_API_URL              - that provider's endpoint (varies by provider)
"""

import os
import base64
import requests

OUTPUT_DIR = "output/images"


def _save(image_bytes: bytes, out_path: str):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(image_bytes)


def try_gemini(prompt: str, out_path: str) -> bool:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return False
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash-image:generateContent?key={key}"
    )
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                _save(img_bytes, out_path)
                return True
        return False
    except Exception as e:
        print(f"[gemini] failed: {e}")
        return False


def try_cloudflare(prompt: str, out_path: str) -> bool:
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not account_id or not token:
        return False
    url = (
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}"
        "/ai/run/@cf/black-forest-labs/flux-1-schnell"
    )
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.post(url, headers=headers, json={"prompt": prompt}, timeout=60)
        r.raise_for_status()
        data = r.json()
        img_b64 = data["result"]["image"]
        img_bytes = base64.b64decode(img_b64)
        _save(img_bytes, out_path)
        return True
    except Exception as e:
        print(f"[cloudflare] failed: {e}")
        return False


def try_flux_hosted(prompt: str, out_path: str) -> bool:
    api_url = os.environ.get("FLUX_API_URL")
    api_key = os.environ.get("FLUX_API_KEY")
    if not api_url or not api_key:
        return False
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        r = requests.post(api_url, headers=headers, json={"prompt": prompt}, timeout=90)
        r.raise_for_status()
        img_bytes = r.content
        _save(img_bytes, out_path)
        return True
    except Exception as e:
        print(f"[flux_hosted] failed: {e}")
        return False


def generate_image(prompt: str, slide_id: str) -> str | None:
    """Tries each provider in order. Returns output path on success, None if all fail."""
    out_path = os.path.join(OUTPUT_DIR, f"{slide_id}.png")
    for provider_fn in (try_gemini, try_cloudflare, try_flux_hosted):
        if provider_fn(prompt, out_path):
            print(f"[generate_image] {slide_id} -> {out_path} (via {provider_fn.__name__})")
            return out_path
    print(f"[generate_image] {slide_id}: ALL PROVIDERS FAILED, no image generated")
    return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python generate_images.py <prompt> <slide_id>")
        sys.exit(1)
    generate_image(sys.argv[1], sys.argv[2])
