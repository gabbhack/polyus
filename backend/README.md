1. `poetry install`
2. `poetry run poe autoinstall-torch-cuda`
3. `uvicorn --host=0.0.0.0 --port=8080 app.__main__:app`

## Переменные окружения
- `domain: str` - Домен или IP, который будет использоваться для отдачи
- `big_size: int ` - Размер негабарита по умолчанию
- `video_path: str` - Путь до тестового видео