'''
CLASSES FOR THE MEAL PLANNER
DAY, MEALPLANNER,MEAL
'''

class Day:
    '''
    The program would create an array of days, each one containing
    '''
    def __init__(self, date:str ):
        '''
        creates day but it can add meals and cooks later. Date is required
        '''
        self.__date = date  # date (it cannot be changed, for now)
        self.__meals = []# list of meals objects

    def get_index(self):
        return self.__date # return date when the cook shift is happening

    def add_meal(self, meal): # meal is a Meal() object
        self.__meals.append(meal)

    def get_meals(self):
        return self.__meals

    def get_dictionary(self):
        '''
        Formats all the info of the object into a json format ready to be inserted in mongodb
        '''
        result = {"date":self.get_index(),"meals":{}}

        for meal in self.__meals:
            result["meals"][meal.get_meal_name()] = \
            {"dishes":meal.get_dishes(), "cooks":meal.get_cooks()}

        return result


class MealPlan:
    '''
    This is a MealPlan object, which contains the meal plan. It is made
    up of a name and a list of days.
    '''
    def __init__(self, name:str):
        '''
        creates day but it can add meals and cooks later. Date is required
        '''
        self.__name = name  # Name of the mealplan
        self.__days = [] # list of meals objects

    def get_index(self):
        return self.__name

    def add_day(self, day:Day):
        self.__days.append(day)

    def get_dictionary(self):
        '''
        Formats all the info of the object into a json format ready to be inserted in mongodb
        '''

        result = {"meal_plan":self.get_index(), "date":{}, "recipes":{}, "cooks":{}}

        for day in self.__days:
            result["date"][day.get_index()] = {"meals":{}}

            for meal in day.get_meals():
                result["date"][day.get_index()] = day.get_dictionary()
        print(result)
        return result


class Meal:
    '''
    "meal" is string that describes its (breakfast, lunch, dinner, etc)
    Each meal contains a list of dishes and cooks.
    '''
    def __init__(self, name: str):
        self.__name = name # string (breakfast, lunch, dinner)
        self.__dishes = [] # Dish objects
        self.__cooks = [] # Cook objects
    '''
    dishes an object (recipe object contain name, ingredients, allergies and instructions), meanwhile, string.
    '''
    def get_index(self):
        return self.__name

    def add_dish(self, dish:str ):
        self.__dishes.append(dish) # "recipe" should have an attribute for allergies

    def add_cook(self, new_cook:str ):
        self.__cooks.append(new_cook)# add cook per meal. There is different meals through the day but it can be different cooks

    def get_dishes(self):
        return self.__dishes

    def get_cooks(self):
        return self.__cooks

    def get_meal_name(self):
        return self.__name

    def get_dictionary_meal(self):
        result = {self.get_index():{"dishes":self.get_dishes(), "cooks": self.get_cooks()}}

        return result

'''
CLASSES FOR RECIPES. THESE ARE ADDED INSIDE THE MEALPLANNER database
'''
class Dish:
    '''
    Multiple dishes make up a meal, and each dish consists of its name, a list
    of ingredients, and a recipe.
    '''

    def __init__(self, name:str):
        '''
        creates day but it can add meals and cooks later. Date is required
        '''
        self.__name = name
        self.__ingredients = [] # list of ingredients
        self.__quantities = [] # List of ingredient quantities: indexes match.
        self.__units = [] # Units in which the quantities will be represented
        self.__recipe = ""
        self.__allergens = [] # list of allergens
        self.__restrictions = [] # Vegan, Gluten-Free, etc

    def get_index(self):
        '''
        get_index() is a method present in other classes like Day, Meal and Cook. It has the same name so we can use the same function with all the objects.
        '''
        return self.__name

    def add_recipe(self, recipe:str):
        '''
        Adds a recipe (in the appropriate format) to the dish
        '''
        self.__recipe = recipe

    def add_ingredients(self, ingredients: str):
        '''
        Adds an ingredient to the meal
        '''
        temp = ingredients.split(", ")
        for i in temp:
            self.__ingredients.append(i)

    def define_quantities(self, quantities:str):
        '''
        Defines the quantities of each meal ingredient
        '''
        temp = quantities.split(", ")
        for i in temp:
            self.__quantities.append(i)

    def define_units(self, units:str):
        '''
        Defines the quantities of each meal ingredient
        '''
        temp = units.split(", ")
        for i in temp:
            self.__units.append(i)

    '''
    Notes: My idea is that we have fields for ingredients and their quantities,
    as well as the recipe. Once inserted into their forms, each ingredient and
    quantity field would be added by the add_ingredient and define_quantities
    methods, which could be structured to already take in lists if that is easier
    to do on front-end. Recipe is just a string.

    For the moment, they are currently three strings: one for the ingredients and
    one for the quantities (separated by commas), and the one for the recipe.
    '''


    def add_allergens(self, allergens:str):
        '''
        Adds an allergen to the dish. is probably okay as a string.
        '''
        temp = allergens.split(", ")
        for i in temp:
            self.__allergens.append(i)

    def add_restrictions(self, restrictions:str):
        '''
        Adds a restriction to the dish. is probably okay as a string.
        '''
        temp = restrictions.split(", ")
        for i in temp:
            self.__restrictions.append(i)

    def get_dictionary(self):
        temp = {"title": self.__name,"recipe": self.__recipe, "ingredients": self.__ingredients, \
                "quantities":self.__quantities, "units":self.__units, "allergens":self.__allergens, \
                "restrictions":self.__restrictions}
        return temp


'''
CLASSES FOR COOKS. ADD COOKS INSIDE MEALPLANNER
'''
class Cook:
    '''
    A cook is a person who will cook the meal. Each meal has one or more
    assigned cooks.
    '''

    def __init__(self, name:str):
        '''
        creates day but it can add meals and cooks later. Date is required
        '''
        self.__name = name # Cook's name
        # self.__mealplan = "" # Cook's name
        self.__allergies = [] # Cook's allergier
        self.__restrictions = [] # Vegan, Gluten-free, etc
        self.__email = ""

    def get_index(self):
        return self.__name

    def add_email(self, email:str):
        self.__email = email

    def add_allergies(self, allergies: str):
        '''
        add random info from cook (i.e. allergies, if prefer not to cook meat, etc)
        For now, it will add the info as a lidst of strings, one by one
        '''
        temp = allergies.split(", ")
        for i in temp:
            self.__allergies.append(i)

    def add_restrictions(self, info: str):
        '''
        add random info from cook (i.e. allergies, if prefer not to cook meat, etc)
        For now, it will add the info as a lidst of strings, one by one
        '''
        temp = info.split(", ")
        for i in temp:
            self.__restrictions.append(i)

    def get_dictionary(self):

        temp = {"name": self.__name, "allergies": self.__allergies, "restrictions": self.__restrictions, "email" : self.__email}

        return temp
