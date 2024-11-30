import hashlib
import time

class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = hashlib.sha256(password.encode()).hexdigest()  # Хэшируем пароль
        self.age = age

class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        """Метод для авторизации пользователя"""
        for user in self.users:
            if user.nickname == nickname and user.password == hashlib.sha256(password.encode()).hexdigest():
                self.current_user = user
                print(f"Вход выполнен. Добро пожаловать, {nickname}!")
                return
        print("Неверный логин или пароль!")

    def register(self, nickname, password, age):
        """Метод для регистрации пользователя"""
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        print(f"Пользователь {nickname} зарегистрирован!")
        
    def log_out(self):
        """Метод для выхода пользователя из аккаунта"""
        self.current_user = None
        print("Выход из аккаунта выполнен")

    def add(self, *videos):
        """Метод для добавления видео"""
        for video in videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)
                print(f"Видео '{video.title}' добавлено")
            else:
                print(f"Видео '{video.title}' уже существует")

    def get_videos(self, search_term):
        """Метод для поиска видео по ключевому слову"""
        search_term = search_term.lower()
        return [video.title for video in self.videos if search_term in video.title.lower()]

    def watch_video(self, title):
        """Метод для просмотра видео"""
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return
        # Поиск видео по названию
        video = next((v for v in self.videos if v.title == title), None)
        if not video:
            print("Видео не найдено!")
            return
        if video.adult_mode and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
            return
        # Просмотр видео
        print(f"Просмотр видео '{title}' начат.")
        while video.time_now < video.duration:
            time.sleep(1)
            video.time_now += 1
            print(f"{video.time_now} сек. просмотрено...")
        print("Конец видео")
        video.time_now = 0  # Сброс времени просмотра

# Создание платформы UrTube
ur = UrTube()

# Создание видео
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска видео
print(ur.get_videos('лучший'))  # ['Лучший язык программирования 2024 года']
print(ur.get_videos('ПРОГ'))    # ['Лучший язык программирования 2024 года']

# Проверка регистрации и просмотра видео
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Попытка входа в аккаунт другого пользователя
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
