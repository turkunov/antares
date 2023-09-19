import React from 'react'
import style from "./MainWindow.module.css"
import { Link } from 'react-router-dom';

const MainWindow = () => {
    return (
        <div className={style.main}>
            <p><b>Выберите действие:</b> <br /> Загрузить датасет  или создать новость</p>
            <div className={style.btns}>
                <Link to="/AiNews/news">
                    <button className={style.btnOne}>Создать новость</button>
                </Link>
                <Link to="/AiNews/dataset">
                    <button className={style.btnTwo}>Загрузить датасет</button>
                </Link>
            </div>
        </div>
    )
}

export default MainWindow