import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import style from "./AddNews.module.css"

const AddNews = () => {

    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")

    const handleClassAndDuplicates = () => {
        // Запрос на сервер для загрузки данных в базу данных
        fetch('ссылка_на_API', {
            method: 'POST',
            body: JSON.stringify({ title, description })
        })
            .then(response => response.json())
            .then(data => {
                const { removed, classes } = data;
                console.log('Removed duplicates:', removed);
                console.log('Classes:', classes);
                // Здесь можно обработать полученные данные
            });
    };


    return (
        <div className={style.news}>
            <p>Создайте <b>новость!</b></p>
            <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder='Введите заголовок' />
            <textarea onChange={(e) => setDescription(e.target.value)} value={description} placeholder='Введите описание'></textarea>
            <div className={style.btns}>
                <button onClick={handleClassAndDuplicates}>Определить класс и дубликаты</button>
                <Link to="/AiNews/">
                    <button>Отменить</button>
                </Link>
            </div>
        </div>
    )
}

export default AddNews