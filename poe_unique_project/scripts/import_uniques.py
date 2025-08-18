import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "poe_unique_project.settings")
django.setup()

from uniques import BaseItem, UniqueItem

def main():
  url = "https://lvlvllvlvllvlvl.github.io/RePoE/uniques_poewiki.json"
  response = requests.get(url)
  response.raise_for_status()
  data = response.json()

  print(f"Importing {len(data)} unique items...")

  for entry in data:
    unique_name = entry.get('name')
    base_name = entry.get('base')
    requirements = entry.get('requirements', {})
    stats = entry.get('explicit', [] + entry.get('implicit', []))
    flavour = entry.get('flavourText', '')
    icon = entry.get('icon', '')

    if not unique_name or not base_name:
      continue

  base_item, _ = BaseItem.objects.get_or_create(name=base_name)
  unique_item, created = UniqueItem.objects.get_or_create(
    name = unique_name,
    defaults={
      'base': base_item,
      'requirements' : requirements,
      'stats' : stats,
      'flavor_text' : flavour,
      'icon_url' : icon
    },
  )

  if not created:
    unique_item.base = base_item
    unique_item.requirements = requirements
    unique_item.stats = stats
    unique_item.flavour_text = flavour
    unique_item.icon_url = icon
    unique_item.save()

  print('import complete')

if __name__ == '__main__':
  main()