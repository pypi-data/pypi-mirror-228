import json
import requests
import typer
import os
import subprocess
import re

from .auth import host, getConfigFromFile

app = typer.Typer()

@app.command()
def install(
    cli: bool = typer.Option(None),
    key: str = typer.Option(None)
):

    typer.secho("Installing BitScreen Plugin.")
    try:
        subprocess.call(["go", "install", "github.com/Murmuration-Labs/bitscreen/cmd/bitscreen@latest"], stdout=subprocess.DEVNULL)
    except OSError as e:
        print(e)
        return

    typer.secho("Installing BitScreen Updater.")
    try:
        subprocess.call(["pip3", "install", "bitscreen-updater"], stdout=subprocess.DEVNULL)
    except OSError as e:
        print(e)
        return

    privateKey = key
    seedPhrase = None

    if cli is True:
        autoAuth = True
    else:
        autoAuth = typer.confirm("Would you like to authenticate the BitScreen Updater with your CLI credentials?")

    if autoAuth and not privateKey:
        try:
            privateKey = getConfigFromFile("eth_private_key")
        except:
            typer.secho("Config file not found. Are you logged in?")
        if not privateKey:
            typer.secho("Private key not found. Maybe you didn't choose to save it.")
    if not privateKey:
        typer.secho("Proceeding with manual authentication.")
        authMethod = typer.prompt("How would you like to authenticate? [0] -> Private Key [1] -> Seed Phrase")
        if authMethod == "0":
            privateKey = typer.prompt("Please insert your private key: ", hide_input=True)
        if authMethod == "1":
            seedPhrase = typer.prompt("Please insert your seed phrase: ", hide_input=True)

        if not privateKey and not seedPhrase:
            raise typer.Exit("Invalid option selected")

    typer.secho("Writing environment init script.")
    typer.secho("You can find it at ~/.murmuration/updater_config.sh and execute it before using BitScreen Updater");
    typer.secho("Example: source ~/.murmuration/updater_config.sh")

    fullPath = os.path.expanduser("~/.murmuration/updater_config.sh")
    configDir = os.path.dirname(fullPath)
    if not os.path.exists(configDir):
        os.makedirs(configDir)

    with open(fullPath, "w") as f:
        f.write("export BITSCREEN_SOCKET_PORT=5555\n");
        f.write("export BITSCREEN_BACKEND_HOST=https://backend.bitscreen.co\n");
        f.write("export FILECOIN_CIDS_FILE=~/.murmuration/bitscreen\n");
        f.write("export IPFS_CIDS_FILE=~/.config/ipfs/denylists/bitscreen.deny\n");
        f.write("export LOTUS_BLOCK_FROM_FILE=0\n");

        if privateKey:
            f.write(f"export BITSCREEN_PROVIDER_KEY={privateKey}\n");
        if seedPhrase:
            f.write(f"export BITSCREEN_PROVIDER_SEED_PHRASE={seedPhrase}\n");

    typer.secho("Configuring Lotus Miner to use BitScreen Filter.")
    minerConfigPath = os.getenv('LOTUS_MINER_PATH')
    if minerConfigPath is None or len(minerConfigPath) == 0:
        raise typer.Exit("LOTUS_MINER_PATH environment variable not found. Could not configure BitScreen for the Lotus Miner")

    goPath = subprocess.check_output(["go", "env", "GOPATH"]).decode().strip()
    if goPath is None or len(goPath) == 0:
        raise typer.Exit("GOPATH environment variable not found. Could not configure BitScreen for the Lotus Miner")

    goPath += "/bin/bitscreen"
    goPath = os.path.expanduser(goPath)
    minerConfigPath = os.path.expanduser(minerConfigPath)
    minerConfigPath = os.path.join(minerConfigPath, "config.toml")
    with open(minerConfigPath, "r+") as f1:
        contents = f1.read()
        match = re.search(r'\s\sFilter\s=\s".*"', contents)
        if match:
            contents = re.sub(r'\s\sFilter\s=\s".*"', f'  Filter = "{goPath}"', contents)
        else:
            match = re.search(r'#Filter\s=\s".*"', contents)
            if match:
                contents = re.sub(r'#Filter\s=\s".*"', f'  Filter = "{goPath}"', contents)
            else:
                contents += f'\n  Filter = "{goPath}"'

        match = re.search(r'\s\sRetrievalFilter\s=\s".*"', contents)
        if match:
            contents = re.sub(r'\s\sRetrievalFilter\s=\s".*"', f'  RetrievalFilter = "{goPath}"', contents)
        else:
            match = re.search(r'#RetrievalFilter\s=\s".*"', contents)
            if match:
                contents = re.sub(r'#RetrievalFilter\s=\s".*"', f'  RetrievalFilter = "{goPath}"', contents)
            else:
                contents += f'\n  RetrievalFilter = "{goPath}"'

        f1.seek(0)
        f1.truncate()
        f1.write(contents)

    typer.secho("Done.")

if __name__ == "__main__":
    app()
