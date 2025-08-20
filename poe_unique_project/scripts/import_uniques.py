import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poe_unique_project.settings")
django.setup()

from uniques.models import BaseItem, UniqueItem, ItemStat

def main():
    url = "https://lvlvllvlvllvlvl.github.io/RePoE/uniques_poewiki.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    print(f"Importing {len(data)} unique items...")

    for entry in data:
        unique_name = entry.get("name")
        base_name = entry.get("base")

        if not unique_name or not base_name:
            continue

        # Handle base + unique
        base_item, _ = BaseItem.objects.get_or_create(name=base_name)
        unique_item, created = UniqueItem.objects.get_or_create(
            name=unique_name,
            defaults={
                "base": base_item,
                "requirements": entry.get("requirements", {}),
                "flavor_text": entry.get("flavourText", ""),
                "icon_url": entry.get("icon", ""),
            },
        )

        if not created:
            unique_item.base = base_item
            unique_item.requirements = entry.get("requirements", {})
            unique_item.flavor_text = entry.get("flavourText", "")
            unique_item.icon_url = entry.get("icon", "")
            unique_item.save()

        # Clear old stats (in case of re-import)
        ItemStat.objects.filter(unique_item=unique_item).delete()

        # Insert implicit stats
        for i, stat in enumerate(entry.get("implicit", [])):
            ItemStat.objects.create(
                unique_item=unique_item,
                text=stat,
                type="implicit",
                order=i,
            )

        # Insert explicit stats
        for i, stat in enumerate(entry.get("explicit", [])):
            ItemStat.objects.create(
                unique_item=unique_item,
                text=stat,
                type="explicit",
                order=i + len(entry.get("implicit", [])),
            )

    print("Import complete.")

if __name__ == "__main__":
    main()
