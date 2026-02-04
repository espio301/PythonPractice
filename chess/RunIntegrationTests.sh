#!/bin/bash
if [ -f /integration_test_output.txt ]; then
    rm /integration_test_output.txt
fi
python3 -m TestModules.IntegrationTests TestModules/PgnFiles/customFile.pgn custom > integration