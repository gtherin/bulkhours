import glob
import random
import os


def generate_file_data(columns=2):
    lines = [",".join([f"c{u}" for u in range(columns)])]
    lines += [",".join([str(random.random()) for _ in range(columns)]) for _ in range(10_000)]
    return "\n".join(lines)


def generate_random_files(nfiles=1_000, path="/content/tmp", columns=2):
    from tqdm import tqdm

    # create a local directory to save files
    os.makedirs(path, exist_ok=True)

    # create all files
    for i in tqdm(range(nfiles), f"Generate {nfiles} random files"):
        with open(f"{path}/data-{i:04d}.csv", "w") as handle:
            handle.write(generate_file_data(columns=columns))


def get_random_filenames(nfiles=1_000, force_generation=False, path="/content/tmp", columns=2):

    if force_generation:
        os.system(f"rm -rf {path}/*")

    if len(glob.glob(f"{path}/*")) == 0:
        generate_random_files(nfiles=nfiles, path=path, columns=columns)
    return glob.glob(f"{path}/*")
