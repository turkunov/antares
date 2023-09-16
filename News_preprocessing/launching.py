import pathlib
import os

from initial_preprocessing import initial_processing
from perplexity import perplexity
from dedup_fse_training import train_fse
from deduplicate import deduplicate


def launch_preprocessing(data_folder):
    data_paths_IP = list(pathlib.Path(data_folder).glob("*.csv"))
    output_folder = 'pretrain_data'
    out_dir_init = pathlib.Path(os.getcwd()) / output_folder
    initial_processing(data_paths_IP, out_dir_init)
    model_name = pathlib.Path(os.getcwd()) / 'fse.model'
    train_fse(data_folder=str(out_dir_init), model_name=str(model_name))
    index_name = pathlib.Path(os.getcwd()) / 'flat.index'

    out_dir = pathlib.Path(os.getcwd()) / 'dedup_news'
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    deduplicate(data_folder=str(out_dir_init), output_folder=str(out_dir),
                s2v_filename=str(model_name), index_fname=str(index_name))

    data_paths_PERP = list(out_dir.glob("*.jsonl"))

    out_dir = pathlib.Path(os.getcwd()) / 'pretrain_data'

    perplexity(data_paths_PERP, out_dir)


if __name__ == '__main__':

    launch_preprocessing(r'training_data')
