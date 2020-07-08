from episcan.scraper.japscan import Japscan

CLASSES = [Japscan, ]

scraper_classes = { cls.__name__ : cls for cls in CLASSES }
