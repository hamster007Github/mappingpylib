set -e
set -o pipefail

echo "##############################"
echo "# Run python linter"
echo "##############################"
./.venv/bin/ruff check
echo "##############################"
echo "# Run unit tests"
echo "##############################"
./.venv/bin/coverage run -m unittest discover -s ./tests -v
echo "##############################"
echo "# Generate coverage report"
echo "##############################"
./.venv/bin/coverage report
echo "##############################"