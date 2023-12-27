from abc import ABC, abstractmethod
from typing import List, Optional
import json
import os

# класс представляющий пльзователя, содержит имя, логин, айди, пароль
class User:
    def __init__(self, user_id: int, name: str, login: str, password: str):
        self.user_id = user_id
        self.name = name
        self.login = login
        self.password = password

    def __repr__(self):
        return f"User({self.user_id}, '{self.name}', '{self.login}')"

#абстрактный класс, определяющий основные операции:получение элементов, добавление, удаление и обновление
class IDataRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def add(self, item: User):
        pass

    @abstractmethod
    def delete(self, item: User):
        pass

    @abstractmethod
    def update(self, item: User):
        pass

#Расширяет IDataRepository, добавляя методы для поиска пользователей по айди и имени
class IUserRepository(IDataRepository):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> List[User]:
        pass
#абстрактный класс для управления пользователями
#определяющий методы для входа, выхода и проверки состояния
class IUserManager(ABC):
    @abstractmethod
    def login(self, login: str, password: str) -> bool:
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def check_auth(self) -> bool:
        pass

#конкретная реализация IUserManager.Управляет текущим состоянием пользователя и проверяет аутентификацию
class FileUserManager(IUserManager):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.current_user = None

    def login(self, login: str, password: str) -> bool:
        users = self.user_repository.get_all()
        for user in users:
            if user.login == login and user.password == password:
                self.current_user = user
                return True
        return False

    def logout(self):
        self.current_user = None

    def check_auth(self) -> bool:
        return self.current_user is not None

#реализация IUserRepository, использующая файл для хранения данных пользователей
#поддерживает чтение и запись данных в формате JSON
class FileUserRepository(IUserRepository):
    def __init__(self, file_name="users.json"):
        self.file_name = file_name
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                return json.load(file, object_hook=lambda d: User(**d))
        return []

    def save_users(self):
        with open(self.file_name, "w") as file:
            json.dump(self.users, file, default=lambda o: o.__dict__)

    def get_all(self) -> List[User]:
        return self.users

    def add(self, item: User):
        if any(user.login == item.login for user in self.users):
            raise ValueError("Логин уже используется")
        self.users.append(item)
        self.save_users()

    def delete(self, item: User):
        self.users.remove(item)

    def update(self, item: User):
        for i, user in enumerate(self.users):
            if user.user_id == item.user_id:
                self.users[i] = item

    def find_by_id(self, user_id: int) -> Optional[User]:
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def find_by_name(self, name: str) -> List[User]:
        return [user for user in self.users if user.name == name]

STATE_FILE = "user_state.json"

#загружает состояние текущего пользователя из файла
def load_current_user_state(user_repository):
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        try:
            with open(STATE_FILE, "r") as file:
                state = json.load(file)
                user_id = state.get("user_id")
                if user_id is not None:
                    return user_repository.find_by_id(user_id)
        except json.JSONDecodeError as e:
            print(f"Ошибка при чтении файла состояния пользователя: {e}")
    else:
        print("Файл состояния пользователя не найден или пуст.")
    return None

#cохраняет состояние пользователя в файл
def save_current_user_state(user):
    with open(STATE_FILE, "w") as file:
        json.dump({"user_id": user.user_id if user else None}, file)

def main():
    user_repository = FileUserRepository()
    user_manager = FileUserManager(user_repository)
    
    # Попытка загрузить текущего пользователя из файла состояния
    current_user = load_current_user_state(user_repository)
    if current_user:
        user_manager.current_user = current_user
        print(f"Добро пожаловать обратно, {current_user.name}!")

    while True:
        print("\nМеню:")
        if not user_manager.check_auth():
            print("1. Вход в систему")
            print("2. Зарегистрировать нового пользователя")
        else:
            print("3. Выход из системы")
            print("4. Сменить пользователя")

        print("0. Выход из приложения")

        choice = input("Выберите опцию: ")

        if choice == "2":
            name = input("Введите имя: ").strip()
            login = input("Введите логин: ").strip()
            password = input("Введите пароль: ").strip()

            if not name or not login or not password:
                print("Все поля должны быть заполнены.")
                continue

            try:
                user_id = len(user_repository.get_all()) + 1
                new_user = User(user_id, name, login, password)
                user_repository.add(new_user)
                user_manager.current_user = new_user
                save_current_user_state(new_user)
                print("Пользователь успешно зарегистрирован.")
            except ValueError as e:
               print(e)

        elif choice == "1":
            if user_manager.check_auth():
                print("Вы уже вошли в систему.")
                continue

            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            if user_manager.login(login, password):
                print(f"Добро пожаловать, {user_manager.current_user.name}!")
            else:
                print("Неверный логин или пароль.")

        elif choice == "3":
            if not user_manager.check_auth():
                print("Вы не вошли в систему.")
                continue

            user_manager.logout()
            print("Вы вышли из системы.")

        elif choice == "4":
            if not user_manager.check_auth():
                print("Вы не вошли в систему.")
                continue

            user_manager.logout()
            login = input("Введите логин нового пользователя: ")
            password = input("Введите пароль нового пользователя: ")
            if user_manager.login(login, password):
                print(f"Добро пожаловать, {user_manager.current_user.name}!")
            else:
                print("Неверный логин или пароль.")

        elif choice == "0":
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
        save_current_user_state(user_manager.current_user)

if __name__ == "__main__":
    main()


