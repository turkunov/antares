import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import style from "./AddDateset.module.css";

const AddDateset = () => {
    // Создаем состояние для хранения выбранного файла
    const [selectedFile, setSelectedFile] = useState(null);

    // Функция для обработки загрузки файла
    const handleFileUpload = async () => {
        // Проверяем, был ли выбран файл
        if (selectedFile) {
            // Создаем объект FormData для отправки файла на сервер
            const formData = new FormData();
            formData.append('dataset', selectedFile); // Добавляем файл в FormData

            try {
                // Отправляем POST запрос на сервер с использованием FormData
                const response = await fetch('https://antares-production.up.railway.app/api/dataset_inference', {
                    method: 'POST', // Используем метод POST
                    body: formData, // Передаем FormData с файлом
                });

                // Проверяем, был ли успешный ответ от сервера
                if (!response.ok) {
                    throw new Error('Не удалось загрузить файл на сервер');
                }

                // Ваш код для обработки успешной загрузки файла
                console.log('Файл успешно загружен на сервер');
            } catch (error) {
                // Обработка ошибок, если загрузка не удалась
                console.error(error);
            }
        } else {
            // Обработка случая, когда файл не выбран
            console.warn('Выберите файл для загрузки');
        }
    };

    return (
        <div className={style.main}>
            <label className={style.window}>
                <input type="file" onChange={event => setSelectedFile(event.target.files[0])} accept=".xlsx" />
                {selectedFile ? (
                    <span>Вы выбрали файл: {selectedFile.name}</span>
                ) : (
                    <span>Перетащите файл сюда <br /> или нажмите для выбора</span>
                )}
            </label>
            <div className={style.btns}>
                <button onClick={handleFileUpload}>Сохранить</button>
                <Link to="/AiNews/">
                    <button>Отменить</button>
                </Link>
            </div>
        </div>
    );
};

export default AddDateset;