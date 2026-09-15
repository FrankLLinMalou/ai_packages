.PHONY: validate package clean

validate:
	python3 scripts/validate_repo.py

package: validate
	python3 scripts/package_skill.py

clean:
	python3 -c "from pathlib import Path; import shutil; shutil.rmtree(Path('dist'), ignore_errors=True)"
