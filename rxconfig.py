import reflex as rx
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
	app_name="codoc_in_plantuml",
	plugins=[
		rx.plugins.TailwindV3Plugin(
			config={
				# Reflex 0.10 compiles components into .web/app_components/, which the
				# default content globs (app/, utils/) miss, so their classes go ungenerated.
				"content": [
					"./app/**/*.{js,ts,jsx,tsx}",
					"./app_components/**/*.{js,ts,jsx,tsx}",
					"./utils/**/*.{js,ts,jsx,tsx}",
				],
				"plugins": ["@tailwindcss/typography@0.5.20"],
			}
		),
		rx.plugins.RadixThemesPlugin(theme=rx.theme(appearance="light")),
	],
	disable_plugins=[rx.plugins.SitemapPlugin],
)
