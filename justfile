default:
    just --list

update-requirements:
    uv pip compile requirements.in -o requirements.txt && uv pip compile requirements-dev.in -o requirements-dev.txt

install-requirements:
    uv pip sync requirements.txt requirements-dev.txt