.PHONY: test run repl format cpp-build cpp-run

test:
	.venv/bin/python -m pytest

run:
	python freedon.py examples/hello.fd

repl:
	python freedon.py

cpp-build:
	cmake -S cpp -B cpp/build
	cmake --build cpp/build --config Release

cpp-run: cpp-build
	@echo "Run: cpp/build/freedon_cpp (Unix/Ninja) or cpp/build/Release/freedon_cpp.exe (VS generator)"
