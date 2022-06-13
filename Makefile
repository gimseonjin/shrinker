typehint: 
	mypy ./

lint: 
	pylint --load-plugins pylint_django --django-settings-module=shrinker.settings shrinker/

checklist: typehint lint

.PHONY:	typehint lint checklist