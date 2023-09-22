import React, { useState } from 'react';
import Modal from 'react-modal';
import { Link } from 'react-router-dom';
import style from "./AddNews.module.css";

const AddNews = () => {
    // Создаем состояния для хранения заголовка, описания и классификации новости
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [classification, setClassification] = useState(null);
    const [modalIsOpen, setModalIsOpen] = useState(false);

    // Стили для модального окна
    const customStyles = {
        content: {
            top: '50%',
            left: '50%',
            right: 'auto',
            bottom: 'auto',
            marginRight: '-50%',
            transform: 'translate(-50%, -50%)',
            maxWidth: '80%',
            padding: '20px',
        },
    };

    // Функция для отправки запроса на API и определения класса новости
    const handleClassAndDuplicates = async () => {
        try {
            // Создаем URL для запроса, добавляя параметры title и description
            const url = `https://antares-production.up.railway.app/api/single_inference/?channelid=${encodeURIComponent(title)}&text=${encodeURIComponent(description)}`;

            // Отправляем GET запрос на указанный URL
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            // Проверяем, был ли успешный ответ от сервера
            if (!response.ok) {
                throw new Error('Не смог получить интерфейс');
            }

            // Получаем ответ от сервера в формате JSON
            const inference = await response.json();

            // Устанавливаем результат классификации в состояние
            setClassification(inference.classification);

            // Выводим результат классификации в консоль
            console.log('Класс новости:', inference.classification);
        } catch (error) {
            // Обрабатываем ошибку, если запрос не удался
            console.error(error);
        }
    }

    const closeModal = () => {
        setModalIsOpen(false);
    }

    return (
        <div className={style.news}>
            <p>Создайте <b>новость!</b></p>
            <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder='Введите заголовок' />
            <textarea onChange={(e) => setDescription(e.target.value)} value={description} placeholder='Введите описание'></textarea>
            <div className={style.btns}>
                {/* Вызываем функцию handleClassAndDuplicates при клике на кнопке */}
                <button onClick={handleClassAndDuplicates}>Определить класс и дубликаты</button>
                <Link to="/AiNews/">
                    <button>Отменить</button>
                </Link>
            </div>
            {/* Отображаем результат классификации, если он есть */}<Modal
                isOpen={modalIsOpen}
                onRequestClose={closeModal}
                style={customStyles}
                contentLabel="Результат классификации"
            >
                <h2>Результат классификации</h2>
                {classification && <p>Класс новости: {classification}</p>}
                <button onClick={closeModal}>Закрыть</button>
            </Modal>
        </div>
    );
}

export default AddNews;