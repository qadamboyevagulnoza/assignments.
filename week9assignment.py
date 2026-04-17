from dataclasses import dataclass, field

@dataclass
class Ingredient:
    name: str
    grams: float
    calories_per_gram: float

    def total_calories(self) -> float:
        return self.grams * self.calories_per_gram
    
@dataclass
class Recipe:
    title: str
    servings: int
    ingredients: list = field(default_factory=list)
    total_calories: float = field(init=False)

    def __post_init__(self):
        self.update_total()

    def update_total(self):
        self.total_calories = sum(i.total_calories() for i in self.ingredients)

    def add_ingredient(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)
        self.update_total()

    def calories_per_serving(self) -> float:
         return self.total_calories / self.servings
    
    def scale(self, new_servings: int):
        ratio = new_servings / self.servings
        for item in self.ingredients:
            item.grams *= ratio

        self.servings = new_servings
        self.update_total()


    def display(self) -> str:
        result = f"{self.title} ({self.servings} servings):\n"
        for i in self.ingredients:
            result += f"  {i.name}: {i.grams}g ({i.total_calories()} cal)\n"
        result += f"Per serving: {self.calories_per_serving()} cal"
        return result
    

r = Recipe("Pancakes", 4)
r.add_ingredient(Ingredient("Flour", 200.0, 3.64))
r.add_ingredient(Ingredient("Milk", 300.0, 0.42))
r.add_ingredient(Ingredient("Egg", 100.0, 1.55))

print(r.total_calories)
print(r.calories_per_serving())
print(r.display())

r.scale(2)
print(r.display())

