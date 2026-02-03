import reflex as rx
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
	app_name="codoc_in_plantuml",
	plugins=[rx.plugins.TailwindV3Plugin()],
	disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
