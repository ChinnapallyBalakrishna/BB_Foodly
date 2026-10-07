import os
import re
import time

import requests

from django.core.management.base import BaseCommand

from core.models import FoodItem


API_URL = "https://foodish-api.com/api/images/{category}"

MEDIA_FOLDER = os.path.join(
    "media",
    "food"
)

REQUEST_DELAY = 1.5

TIMEOUT = 30


class Command(BaseCommand):

    help = "Download food images from Foodish API and assign them to FoodItems."

    def get_category(self, food_name):

        name = food_name.lower()

        # Pizza
        if "pizza" in name:
            return "pizza"

        # Burger
        if "burger" in name:
            return "burger"

        # Biryani
        if "biryani" in name:
            return "biryani"

        # Butter chicken
        if "butter chicken" in name:
            return "butter-chicken"

        # Dosa
        if "dosa" in name:
            return "dosa"

        # Idly / Idli
        if "idly" in name or "idli" in name:
            return "idly"

        # Pasta
        if "pasta" in name:
            return "pasta"

        # Samosa
        if "samosa" in name:
            return "samosa"

        # Rice dishes
        rice_words = [
            "rice",
            "fried rice",
            "hakka",
            "noodles",
            "pulao",
        ]

        if any(word in name for word in rice_words):
            return "rice"

        # Desserts / sweets
        dessert_words = [
            "cake",
            "ice cream",
            "kulfi",
            "gulab",
            "rasmalai",
            "jalebi",
            "halwa",
            "brownie",
            "dessert",
            "sweet",
        ]

        if any(word in name for word in dessert_words):
            return "dessert"

        # Default
        return "dessert"

    def clean_filename(self, name):

        name = name.lower()

        name = re.sub(
            r"[^a-z0-9]+",
            "_",
            name
        )

        name = name.strip("_")

        return name

    def download_image(self, image_url, filename):

        os.makedirs(
            MEDIA_FOLDER,
            exist_ok=True
        )

        file_path = os.path.join(
            MEDIA_FOLDER,
            filename
        )

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140.0 Safari/537.36"
            )
        }

        try:

            response = requests.get(
                image_url,
                headers=headers,
                timeout=TIMEOUT
            )

            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            if not content_type.startswith("image/"):
                self.stdout.write(
                    self.style.WARNING(
                        "    Not an image response"
                    )
                )

                return False

            if len(response.content) < 5000:
                self.stdout.write(
                    self.style.WARNING(
                        "    Image is too small"
                    )
                )

                return False

            with open(
                file_path,
                "wb"
            ) as image_file:

                image_file.write(
                    response.content
                )

            return True

        except requests.RequestException as error:

            self.stdout.write(
                self.style.WARNING(
                    f"    Download failed: {error}"
                )
            )

            return False

        except OSError as error:

            self.stdout.write(
                self.style.WARNING(
                    f"    File error: {error}"
                )
            )

            return False

    def handle(self, *args, **options):

        os.makedirs(
            MEDIA_FOLDER,
            exist_ok=True
        )

        foods = list(
            FoodItem.objects.all().order_by("id")
        )

        total = len(foods)

        if total == 0:

            self.stdout.write(
                self.style.WARNING(
                    "No FoodItems found."
                )
            )

            return

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDownloading images for {total} foods...\n"
            )
        )

        success_count = 0
        failed_count = 0

        used_urls = set()

        for index, food in enumerate(
            foods,
            start=1
        ):

            self.stdout.write(
                f"[{index}/{total}] {food.name}"
            )

            category = self.get_category(
                food.name
            )

            self.stdout.write(
                f"    Category: {category}"
            )

            api_url = API_URL.format(
                category=category
            )

            try:

                response = requests.get(
                    api_url,
                    timeout=TIMEOUT,
                    headers={
                        "User-Agent": (
                            "Foodly Food Image Downloader"
                        )
                    }
                )

                response.raise_for_status()

                data = response.json()

                image_url = data.get(
                    "image"
                )

                if not image_url:

                    self.stdout.write(
                        self.style.WARNING(
                            "    No image returned"
                        )
                    )

                    failed_count += 1

                    time.sleep(
                        REQUEST_DELAY
                    )

                    continue

                # Try another API result if
                # the same image was already used.
                attempts = 0

                while (
                    image_url in used_urls
                    and attempts < 3
                ):

                    time.sleep(0.5)

                    retry_response = requests.get(
                        api_url,
                        timeout=TIMEOUT,
                        headers={
                            "User-Agent": (
                                "Foodly Food Image Downloader"
                            )
                        }
                    )

                    retry_response.raise_for_status()

                    retry_data = retry_response.json()

                    image_url = retry_data.get(
                        "image"
                    )

                    attempts += 1

                if image_url in used_urls:

                    self.stdout.write(
                        self.style.WARNING(
                            "    Could not get a different image"
                        )
                    )

                filename = (
                    self.clean_filename(
                        food.name
                    )
                    + ".jpg"
                )

                success = self.download_image(
                    image_url,
                    filename
                )

                if success:

                    used_urls.add(
                        image_url
                    )

                    # Remove old image file
                    # if FoodItem had another image.
                    if food.image:

                        old_name = str(
                            food.image.name
                        )

                        if old_name != (
                            f"food/{filename}"
                        ):

                            old_path = os.path.join(
                                "media",
                                old_name
                            )

                            if os.path.isfile(
                                old_path
                            ):

                                try:
                                    os.remove(
                                        old_path
                                    )
                                except OSError:
                                    pass

                    food.image = (
                        f"food/{filename}"
                    )

                    food.image_url = ""

                    food.save(
                        update_fields=[
                            "image",
                            "image_url"
                        ]
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"    DOWNLOADED: {filename}"
                        )
                    )

                    success_count += 1

                else:

                    failed_count += 1

            except requests.RequestException as error:

                self.stdout.write(
                    self.style.WARNING(
                        f"    API error: {error}"
                    )
                )

                failed_count += 1

            except ValueError as error:

                self.stdout.write(
                    self.style.WARNING(
                        f"    Invalid API response: {error}"
                    )
                )

                failed_count += 1

            except Exception as error:

                self.stdout.write(
                    self.style.WARNING(
                        f"    Unexpected error: {error}"
                    )
                )

                failed_count += 1

            time.sleep(
                REQUEST_DELAY
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "IMAGE DOWNLOAD COMPLETE"
            )
        )

        self.stdout.write(
            f"Total foods: {total}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Downloaded: {success_count}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Failed: {failed_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )