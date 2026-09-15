#!/usr/bin/env python3
"""
deploy.py — CommerceOS Deployment Script
Uploads index.html to HuggingFace Space

Usage:
    python3 deploy.py                # Deploy to HF Space
    python3 deploy.py --create       # Create the Space first, then deploy

Before first run:
    pip install huggingface_hub
    huggingface-cli login
"""

import os
import sys
from pathlib import Path

REPO_ID = "ShivanshiNigam/commerceos"   # Change if your HF username is different
HF_SPACE_URL = f"https://huggingface.co/spaces/{REPO_ID}"
INDEX_FILE = Path(__file__).parent / "index.html"

def upload():
    """Upload index.html and README.md to the HF Space."""
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        print(f"\n🤗 Uploading to HuggingFace Space: {REPO_ID}")

        # Upload index.html
        print("   📤 Uploading index.html...")
        api.upload_file(
            path_or_fileobj=str(INDEX_FILE),
            path_in_repo="index.html",
            repo_id=REPO_ID,
            repo_type="space",
            commit_message="CommerceOS — Revert to Serverless (Static) Architecture"
        )
        print("   ✅ index.html uploaded!")

        # Upload README.md if it exists
        readme = Path(__file__).parent / "README.md"
        if readme.exists():
            print("   📤 Uploading README.md...")
            api.upload_file(
                path_or_fileobj=str(readme),
                path_in_repo="README.md",
                repo_id=REPO_ID,
                repo_type="space",
                commit_message="Update README (sdk: static)"
            )
            print("   ✅ README.md uploaded!")

        print(f"\n✅ Deployment complete!")
        print(f"🔗 {HF_SPACE_URL}")
        print("⏳ Wait ~10 seconds, then Cmd+Shift+R to refresh the Space.")
        return True
    except ImportError:
        print("❌ huggingface_hub not installed. Run: pip install huggingface_hub")
        return False
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        print("   Did you run: huggingface-cli login ?")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("   CommerceOS — Serverless Deploy Script")
    print(f"   Target: {REPO_ID}")
    print("=" * 60)

    # Upload
    success = upload()
    sys.exit(0 if success else 1)
