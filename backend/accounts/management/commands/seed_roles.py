from django.core.management.base import BaseCommand
from accounts.models import Role, Region


DEFAULT_ROLES = [
	"SuperAdmin", "Admin", "Agronomist", "Support", "Analyst", "Business", "Development", "User"
]

DEFAULT_REGIONS = [
	"National", "North", "South", "East", "West"
]


class Command(BaseCommand):
	help = "Seed default roles and regions"

	def handle(self, *args, **options):
		for r in DEFAULT_ROLES:
			Role.objects.get_or_create(name=r)
		for rg in DEFAULT_REGIONS:
			Region.objects.get_or_create(name=rg)
		self.stdout.write(self.style.SUCCESS("Seeded roles and regions"))

