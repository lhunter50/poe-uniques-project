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


class ItemCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)   # example: "Helmet", "Boots"
    slot = models.CharField(max_length=20, choices=Slot.choices, default=Slot.OTHER)
    # poe_class is for the base items defined from the raw data from POE itself, it will help us with debugging or adding new bases
    poe_class = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} ({self.slot})"

class BaseItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # Keep both: FK to normalized category + raw class string for debugging/backfills
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT, related_name="bases")
    item_class = models.CharField(max_length=100, blank=True)  # example: Helmets

    def __str__(self):
        return self.name


class UniqueItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    base = models.ForeignKey(BaseItem, on_delete=models.CASCADE, related_name="uniques")
    requirements = models.JSONField(default=dict, blank=True)   # {"level": 70, "str": 85, "dex": 85}
    flavor_text = models.TextField(blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)

    # prepared for later pricing
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.base.name})"


class ItemStat(models.Model):
    unique_item = models.ForeignKey(UniqueItem, related_name="stats", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=[("explicit", "Explicit"), ("implicit", "Implicit")],
    )
    order = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["text"]),
            models.Index(fields=["type"]),
        ]

    def __str__(self):
        return f"{self.unique_item.name} - {self.text}"
