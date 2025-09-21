import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """Extract filename from URL or create one if not present."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:  # if URL doesn't have a filename
        filename = "downloaded_image.jpg"
    return filename

def hash_file_content(content):
    """Return an md5 hash of file content (used to check duplicates)."""
    return hashlib.md5(content).hexdigest()

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Ask for one or multiple URLs separated by commas
    urls = input("Please enter the image URL(s), separated by commas: ").split(",")

    # Create directory if it doesn't exist
    os.makedirs("Fetched_Images", exist_ok=True)

    downloaded_hashes = set()

    for url in [u.strip() for u in urls if u.strip()]:
        try:
            # Fetch the image with a timeout
            response = requests.get(url, timeout=10, headers={"User-Agent": "UbuntuFetcher/1.0"})
            response.raise_for_status()  # Raise exception for bad status codes

            # Security precaution: check Content-Type header to confirm it's an image
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"✗ Skipped: {url} (not an image, Content-Type={content_type})")
                continue

            # Avoid duplicates by hashing content
            file_hash = hash_file_content(response.content)
            if file_hash in downloaded_hashes:
                print(f"✗ Skipped duplicate: {url}")
                continue
            downloaded_hashes.add(file_hash)

            # Extract filename from URL
            filename = get_filename_from_url(url)
            filepath = os.path.join("Fetched_Images", filename)

            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}\n")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error for {url}: {e}")
        except Exception as e:
            print(f"✗ An error occurred for {url}: {e}")

    print("Connection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
