from pathlib import Path
import yaml
import typer
import os



def create_config(config_path : Path):
    typer.echo("Initializing oraculo...")
    persist_directory = typer.prompt("Persist directory: ", default=".chromadb")
    persist_directory = Path(persist_directory)
    persist_directory_str = str(Path(persist_directory))
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)

    chroma_db_impl = typer.prompt(
        "Chroma DB Implementation: ", default="duckdb+parquet"
    )
    config = {
        "chromadb": {
            "persist_directory": persist_directory_str,
            "chroma_db_impl": chroma_db_impl,
        },
    }
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w") as f:
        yaml.dump(config, f)
    print(f"Config file created at {config_path}")
    return config_path

def load_config(config_path : Path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config