default:
    just --list

update-requirements:
    uv pip compile requirements.in -o requirements.txt && uv pip compile requirements-dev.in -o requirements-dev.txt

install-requirements:
    uv pip sync requirements.txt requirements-dev.txt

# This might be useful if the signal-cli-rest-api container gets out of sync with the
# actual Signal account. It forces it to receive messages it may have missed.
# Use international format for send number, e.g. +1234567890
force-sync-signal-client sender_number:
    docker compose exec signal-cli-rest-api bash -c 'su signal-api -c "signal-cli --config /home/.local/share/signal-cli -a {{sender_number}} receive"'