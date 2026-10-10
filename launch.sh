VENV=.venv

# Check if venv exists. If it doesn't create it and install the packages
if [ ! -d "$VENV" ]; then
    # Create the venv
    python -m venv --system-site-packages $VENV

    # Activate that venv
    source $VENV/bin/activate

    # Install packages into the venv
    pip install -r requirements.txt
else
    # Activate that venv
    source $VENV/bin/activate
fi

# Launch the tool
python ./main.py

# Deactivate the venv
deactivate
