import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import style from "./AddDateset.module.css"

const AddDateset = () => {

    const [selectedFile, setSelectedFile] = useState(null)

    const handleFileUpload = event => {
        const file = event.target.files[0];
        setSelectedFile(file);
    };

    return (
        <div className={style.main}>
            <label className={style.window}>
                <input type="file" onChange={handleFileUpload} accept=".csv, .xlsx" />
                {selectedFile ? (
                    <span>Вы выбрали файл: {selectedFile.name}</span>
                ) : (
                    <span>Перетащите файл сюда <br /> или нажмите для выбора</span>
                )}
            </label>
            <div className={style.btns}>
                <button >Сохранить</button>
                <Link to="/AiNews/">
                    <button>Отменить</button>
                </Link>
            </div>
        </div>
    )
}

export default AddDateset