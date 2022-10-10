from typing import Protocol, TypeAlias, NamedTuple
from collections.abc import Iterator
from faker import Faker
import string
import logging
import random


T_LOGIN: TypeAlias = str
T_PASSWORD: TypeAlias = str

faker = Faker()

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)



class UserProtocol(Protocol):
    login: T_LOGIN
    password: T_PASSWORD

class User(NamedTuple):
    login: str
    password: str
    def __str__(self):
        print(f"{self.login}: {self.password}")


def validate(users: list[UserProtocol], amount: int) -> None:
    logins = set(map(lambda user: user.login, users))
    if amount != (amount_of_logins := len(logins)):
        raise ValueError(
            f'Not enough of unique items. Required: "{amount}". Provided: "{amount_of_logins}"'
        )

def generate_login(key: int | None = None):
    login = faker.user_name()
    if key:
        login = f"{login}_{random.randint(0, key)}"

    return login

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(random.randint(0, 16)))

    return password

def generate_users(amount: int) -> Iterator[User]:
    logins = set()
    counter = 1
    while len(logins) < amount:
        login = generate_login(key=amount)

        if login in logins:
            log.info(f'-------------------------------------------------------------- non-unique user: {(login)}. Total non-unique: {counter}')
            counter += 1
            continue

        logins.add(login)
        log.info(f'Generated unique combination of login and password for user: {len(logins)}')


        yield User(
            login=login,
            password=generate_password(),
        )


def main():
    amount = 100_000
    users = list(generate_users(amount=amount))
    validate(users=users, amount=amount)
    print(users)


if __name__ == "__main__":
    main()