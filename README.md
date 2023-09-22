# Team Antares 
#### @turkunov (Backend/ML/DS), @kyyoto (ML/DS), @Aspir01 (Frontend/React)

Микросервис для дедупликации и классификации новостей ТГ-каналов

**Архитектура нашего репозитория**:

**|_backend**: бекенд, на котором происходит инференс модели
<br /> 
‎ ‎ |_research: наши исследования моделей как глубокого обучения на основе ruBert, так и простых ML моделей
<br /> 
‎ ‎‎ ‎ |_utils: утилиты для модели (тренер и оптимизатор)
<br /> 
‎ ‎ |_utils: утилиты для предобработки массивов данных (удаление дубликатов, конвертация в эмбеддинги...)
<br /> 
**|_frontend**: интерфейс для взаимодействия с моделью
<br /> 
**|_data**: данные, на которых происходило обучение


**Развернуть контейнер можно с помощью команды**:
`docker compose up` 

**После развертывания будут доступны следующие сервера**:
* `http://localhost:8080/docs`: Документация к API (включая непосредственные эндпоинты для инференса)
* `http://localhost:3030/`: UI для взаимодействия