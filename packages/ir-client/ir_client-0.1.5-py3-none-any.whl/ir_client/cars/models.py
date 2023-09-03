from dataclasses import dataclass

@dataclass
class Car:
    id: int
    name: str


@dataclass
class Cars:
    cars: list[Car]
