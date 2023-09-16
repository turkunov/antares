import json
import faiss
import os
import jsonlines
from tqdm import tqdm
from fse.models.base_s2v import BaseSentence2VecModel



def deduplicate(data_folder: str = './news_2014', output_folder: str = './output_data', s2v_filename: str = 'fse.model', index_fname: str = 'flat.index'):
    """
    Функция для дедубликации данных. Требует созданную папку с исходными файлами JSON Lines
    Input:
        data_folder: str = './data' - папка с исходными файлами формата .jsonl
        output_folder: str = './output_data' - папка, в которую будут сохраняться новые файлы
    """
    dim = 100

    s2v = BaseSentence2VecModel.load(s2v_filename)

    if os.path.isfile(index_fname):
        index = faiss.read_index(index_fname)
    else:
        index = faiss.IndexFlatL2(dim)
    for file in tqdm(os.listdir(data_folder), desc='Folder'):
        try:
            with open(os.path.join(data_folder, file), 'r') as f:
                json_list = list(f)

            output_json = []
            for json_str in tqdm(json_list, desc='File'):
                js = json.loads(json_str)
                data = js['text']
                vec = s2v.infer([(data.split(), 0)])
                D, I = index.search(vec, 2)
                if D[0][0] > 0.2 or I[0][0] == -1:
                    index.add(vec)
                    output_json.append(js)

            with jsonlines.open(os.path.join(output_folder, file), 'w') as out_f:
                out_f.write_all(output_json)
        except Exception as e:
            print(f'{e} error in {file} file, ensure all files >0kb')

    faiss.write_index(index, "flat.index")


# if __name__ == '__main__':
#     deduplicate()