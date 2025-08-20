from django.db import models

class Slot(models.TextChoices):
    ARMOUR = "armour", "Armour"
    WEAPON = "weapon", "Weapon"
    OFFHAND = "offhand", "Off-hand"
    ACCESSORY = "accessory", "Accessory"
    FLASK = "flask", "Flask"
    JEWEL = "jewel", "Jewel"
    GEM = "gem", "Gem"
    MAP = "map", "Map"
    OTHER = "other", "Other"

def base_icon_path(instance, filename):   return f"bases/{instance.id}/{filename}"
def unique_icon_path(instance, filename): return f"uniques/{instance.id}/{filename}"

class ItemCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)          # "Helmet", "Boots"
    slot = models.CharField(max_length=20, choices=Slot.choices, default=Slot.OTHER)
    poe_class = models.CharField(max_length=100, unique=True)     # raw PoE class 

    def __str__(self): return f"{self.name} ({self.slot})"

class BaseItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT, related_name="bases")
    item_class = models.CharField(max_length=100, blank=True)     # raw PoE class duplicate for convenience

    # images
    source_icon_url = models.URLField(blank=True, null=True)
    icon  = models.ImageField(upload_to=base_icon_path, blank=True, null=True)
    thumb = models.ImageField(upload_to=base_icon_path, blank=True, null=True)

    def __str__(self): return self.name

class UniqueItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    base = models.ForeignKey(BaseItem, on_delete=models.CASCADE, related_name="uniques")
    requirements = models.JSONField(default=dict, blank=True)
    flavor_text = models.TextField(blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)             # source URL

    # price placeholder for later
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # cached images
    icon  = models.ImageField(upload_to=unique_icon_path, blank=True, null=True)
    thumb = models.ImageField(upload_to=unique_icon_path, blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=["name"])]

    def __str__(self): return f"{self.name} ({self.base.name})"

class ItemStat(models.Model):
    unique_item = models.ForeignKey(UniqueItem, related_name="stats", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=[("explicit", "Explicit"), ("implicit", "Implicit")])
    order = models.IntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=["text"]), models.Index(fields=["type"])]

    def __str__(self): return f"{self.unique_item.name} - {self.text}"
