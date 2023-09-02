import typer
import subprocess
import chromadb
from rich import print
from chromadb.config import Settings
from rich import print
from pathlib import Path
import yaml
from oraculo.functions.audio import audio_to_text, download_yt
from oraculo.functions.data import get_collections
from oraculo.functions.config import create_config, load_config
from typing_extensions import Annotated
import logging
import glob
from rich.progress import track

logging.basicConfig(level=logging.INFO)

APP_NAME = "oraculo"
app = typer.Typer()

app_dir = typer.get_app_dir(APP_NAME)
config_path: Path = Path(app_dir) / "config/config.yaml"

BASE_DIR = Path(__file__).resolve().parent.parent


@app.command(help="Initialize oraculo, set up config file.")
def init():
    if config_path.exists():
        print("Config file already exists.")
        print("Config file path: " + str(config_path))
        print("Config file content:")
        with open(config_path, "r") as f:
            print(f.read())

        option = typer.confirm("Do you want to overwrite the config file?")
        if option:
            create_config(config_path,)
        else:
            print("Exiting...")

    else:
        print("Initializing oraculo...")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        create_config(config_path,)

@app.command(help="Transcribe an audio file. Accepts .mp3, .wav, .m4a, .flac, .mp4 files. If the output file is not specified, the output file will be saved in the same folder as the input file.")
def transcribe(
    embeddings: Annotated[
        bool,
        typer.Option(
            help="Create embeddings from the segments of the transcription and persists them to a vector database."
        ),
    ] = False,
    collection: Annotated[
        str,
        typer.Option(
            help="Name of the collection to persist the embeddings to. If the collection does not exist, a new collection will be created.",
        ),
    ] = None,
):
    path_str = typer.prompt("Path to audio file: ", default=None)
    path = Path(path_str)
    language = typer.prompt("Input Audio Language: ", default="pt")
    model = typer.prompt("Model: ", default="base")
    # default path is the same as input path but with .txt extension removing the audio extension
    output = typer.prompt("Output file: ", default=path.parent / f"{path.stem}.txt")
    metadata = {}

    config = load_config(config_path)

    persist_directory = config["chromadb"]["persist_directory"]
    chroma_db_impl = config["chromadb"]["chroma_db_impl"]

    client = chromadb.Client(
        Settings(persist_directory=persist_directory, chroma_db_impl=chroma_db_impl)
    )

    if embeddings:
        # check if collections exist
        collections = get_collections(client)
        print("Collections found:")
        print(collections)

        if collection in collections:
            print(f"Collection {collection} found.")
            metadata = {"collection_name": collection}
        else:
            print(f"Collection not found. Creating new collection...")
            if collection is None:
                collection = typer.prompt("Enter collection name")
                metadata = {"collection_name": collection}
            else:
                metadata = {"collection_name": collection}

    print("Transcribing... :floppy_disk:")

    audio_to_text(
        path=path,
        language=language,
        model=model,
        output=output,
        embeddings=embeddings,
        metadata=metadata if embeddings else None,
        client=client if embeddings else None,
    )


@app.command(help="Transcribe all audio files in a folder. Accepts .mp3, .wav, .m4a, .flac, .mp4 files. If the output folder is not specified, the output files will be saved in the same folder as the input files.")
def bulk_transcribe(
    embeddings: Annotated[
        bool,
        typer.Option(
            help="Create embeddings from the segments of the transcription and persists them to a vector database."
        ),
    ] = False,
    collection: Annotated[
        str,
        typer.Option(
            help="Name of the collection to persist the embeddings to. If the collection does not exist, a new collection will be created.",
        ),
    ] = None,
):
    path_str = typer.prompt("Path to folder: ", default=None)
    path = Path(path_str)
    language = typer.prompt("Input Audio Language: ", default="pt")
    model = typer.prompt("Model: ", default="base")
    # default path is the same as input path
    output = typer.prompt("Output folder path: ", default=path)
    metadata = {}

    config = load_config(config_path)

    persist_directory = config["chromadb"]["persist_directory"]
    chroma_db_impl = config["chromadb"]["chroma_db_impl"]

    client = chromadb.Client(
        Settings(persist_directory=persist_directory, chroma_db_impl=chroma_db_impl)
    )

    if embeddings:
        # check if collections exist
        collections = get_collections(client)
        print("Collections found:")
        print(collections)

        if collection in collections:
            print(f"Collection {collection} found.")
            metadata = {"collection_name": collection}
        else:
            print(f"Collection not found. Creating new collection...")
            if collection is None:
                collection = typer.prompt("Enter collection name")
                metadata = {"collection_name": collection}
            else:
                metadata = {"collection_name": collection}
    # read all files in folder that have .mp3, .wav, .m4a, .flac extension
    # Glob the folder for supported audio formats
    audio_extensions = ['mp3', 'wav', 'm4a', 'flac', 'mp4']
    files = [f for ext in audio_extensions for f in path.glob(f'*.{ext}')]

    for file in track(files, "Transcribing... :hourglass:"):
        filename = file.stem  # Gets the filename without the extension
        output_file = path / f"{filename}.txt"  # Use pathlib to form a new Path object
        
        print(f"Transcribing {filename}...")

        audio_to_text(
            path=file,
            language=language,
            model=model,
            output=output_file,
            embeddings=embeddings,
            metadata=metadata if embeddings else None,
            client=client if embeddings else None,
        )


@app.command()
def webapp():
    print("Starting webapp...")
    print(f"BASE_DIR: {BASE_DIR}")
    subprocess.run(
        [
            "streamlit",
            "run",
            str(BASE_DIR / "oraculo/webapp.py"),
            "--server.port=8501",
            "--server.address=0.0.0.0",
        ]
    )



@app.command()
def transcribe_yt(
    embeddings: Annotated[
        bool,
        typer.Option(
            help="Create embeddings from the segments of the transcription and persists them to a vector database."
        ),
    ] = False,
    collection: Annotated[
        str,
        typer.Option(
            help="Name of the collection to persist the embeddings to. If the collection does not exist, a new collection will be created.",
        ),
    ] = None,
):
    path_str = typer.prompt("Folder path: ", default=None)
    path = Path(path_str)
    url = typer.prompt("Youtube URL: ", default=None)
    language = typer.prompt("Input Audio Language: ", default="pt")
    model = typer.prompt("Model: ", default="base")
    metadata = {}

    config = load_config(config_path)

    persist_directory = config["chromadb"]["persist_directory"]
    chroma_db_impl = config["chromadb"]["chroma_db_impl"]

    client = chromadb.Client(
        Settings(persist_directory=persist_directory, chroma_db_impl=chroma_db_impl)
    )


    if embeddings:
        # check if collections exist
        collections = get_collections(client)
        print("Collections found:")
        print(collections)

        if collection in collections:
            print(f"Collection {collection} found.")
            metadata = {"collection_name": collection}
        else:
            print(f"Collection not found. Creating new collection...")
            if collection is None:
                collection = typer.prompt("Enter collection name")
                metadata = {"collection_name": collection}
            else:
                metadata = {"collection_name": collection}

    print("Transcribing... :floppy_disk:")

    # download video
    audio_path , audio_metadata = download_yt(url, path)

    if audio_path is None:
        print("Download failed.")
        return None

    metadata = {**metadata, **audio_metadata}

    audio_to_text(
        path=audio_path,
        language=language,
        model=model,
        output=path / f"{audio_path.stem}.txt",
        embeddings=embeddings,
        metadata=metadata if embeddings else None,
        client=client if embeddings else None,
    )



@app.command()
def test():
    audio_to_text(
        path="/home/jrtedeschi/projetos/Gravando.m4a",
        language="pt",
        model="base",
        output="/home/jrtedeschi/projetos/Gravando.txt",
        embeddings=True,
        metadata={"collection_name": "teste"},
    )

@app.command(help="Converts files with different video formats to .mp4")
def convert_video(bulk : Annotated[bool, typer.Option(help="Converts all files with video extensions in a folder")] = False, output_directory : Annotated[str, typer.Option(help="Output folder path")] = None):

    if bulk:
        path_str = typer.prompt("Source Directory Path: ", default=None)
        path = Path(path_str)
        audio_extensions = ['mp3', 'wav', 'm4a', 'flac', 'mp4', 'mkv', 'avi']
        files = [f for ext in audio_extensions for f in path.glob(f'*.{ext}')]

        if output_directory is None:
            output = path
        else:
            output = Path(output_directory)

        for file in track(files, "Converting... :hourglass:"):
            filename = file.stem
            output_file = output / f"{filename}.mp4"
            print(f"Converting {filename}...")
            subprocess.run(["ffmpeg", "-i", file, output_file])
    else:
        path_str = typer.prompt("Source File Path: ", default=None)
        path = Path(path_str)
        if output_directory is None:
            output = path.parent
        else:
            output = Path(output_directory)
        filename = path.stem
        output_file = output / f"{filename}.mp4"
        print(f"Converting {filename}...")
        subprocess.run(["ffmpeg", "-i", path, output_file])


if __name__ == "__main__":
    app()
