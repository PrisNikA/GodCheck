#Импорт библиотеки requests для HTTP запросов к сайту Годвилля
import requests

def get_hero(godname:str, API:str) -> list:
    """Получаем информацию о герое в виде словаря"""

    #Словарь для хранения информации о герое
    hero_dict = {}

    #Получаем данные в формате JSON с помощью API
    html = requests.get(f"https://godville.net/gods/api/{godname}/{API}")
    hero_json = html.json()

    #Извлекаем все нужные данные в словарь
    #Имя бога и героя
    hero_dict["godname"] = hero_json["godname"]
    hero_dict["name"] = hero_json["name"]

    #Пол героя
    if hero_json["gender"] == "male":
        hero_dict["gender"] = "Мужской"
    else:
        hero_dict["gender"] = "Женский"

    #Здоровье героя
    hero_dict["health"] = [hero_json['health'], hero_json['max_health']]
    
    #Уровень героя
    hero_dict["level"] = [hero_json['level'], hero_json['exp_progress']]
    
    #Золото
    hero_dict["gold"] = hero_json["gold_approx"]

    #Прана
    hero_dict["power"] = hero_json['godpower']

    #Квест
    hero_dict["quest"] = [hero_json['quest'], hero_json['quest_progress']]

    #Характер
    hero_dict["alignment"] = hero_json["alignment"]

    #Гильдия
    hero_dict["clan"] = f"{hero_json['clan']} ({hero_json['clan_position']})"

    #Девиз
    hero_dict["motto"] = hero_json["motto"]

    #Кол-во столбов от столицы
    hero_dict["distance"] = hero_json["distance"]

    #Инвентарь
    hero_dict["inventory"] = [hero_json['inventory_num'], hero_json['inventory_max_num']]

    #Статистика на арене
    hero_dict["arena"] = f"{hero_json['arena_won']}/{hero_json['arena_lost']}"

    #Последняя запись в дневнике
    hero_dict["diary_last"] = hero_json["diary_last"]

    #Тип боя
    if hero_json["arena_fight"]:
        match hero_json["fight_type"]:
            case "arena":
                hero_dict["fight_type"] = "Сцепился в схватке на арене."
            case "boss":
                hero_dict["fight_type"] = "Дерется с боссом."
            case "boss_m":
                hero_dict["fight_type"] = "Дерется с боссом, потому что так было задумано."
            case "challenge":
                hero_dict["fight_type"] = "Тренирует друга."
            case "dungeon":
                hero_dict["fight_type"] = "Покоряет сокровищницы."
            case "multi_monster":
                hero_dict["fight_type"] = "Нарвался на толпу хулиганов."
            case "sail":
                hero_dict["fight_type"] = "Покоряет дальние берега."
            case "range":
                hero_dict["fight_type"] = "На полигоне."
    else:
        hero_dict["fight_type"] = "В странствиях"

    #Аура
    if "aura" in hero_json.keys():
        hero_dict["aura"] = hero_json["aura"]
    else:
        hero_dict["aura"] = "Отсутствует"

    
    #Питомец
    pet = {}

    #Имя и вид питомца
    pet["name"] = hero_json["pet"]["pet_name"]
    pet["type"] = hero_json["pet"]["pet_class"]
    
    #Уровень питомца
    if "wounded" in hero_json["pet"].keys():
        pet["level"] = "Отсутствует (питомец контужен)"
    else:
        pet["level"] = hero_json["pet"]["pet_level"]


    #Возвращаем героя и питомца
    return [hero_dict, pet]