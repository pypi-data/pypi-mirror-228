from enum import Enum
from typing import Optional, List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class CodeblockNameEnum(Enum):
    CALL_FUNCTION = "CALL FUNCTION"
    CONTROL = "CONTROL"
    ELSE = "ELSE"
    ENTITY_ACTION = "ENTITY ACTION"
    ENTITY_EVENT = "ENTITY EVENT"
    FUNCTION = "FUNCTION"
    GAME_ACTION = "GAME ACTION"
    IF_ENTITY = "IF ENTITY"
    IF_GAME = "IF GAME"
    IF_PLAYER = "IF PLAYER"
    IF_VARIABLE = "IF VARIABLE"
    PLAYER_ACTION = "PLAYER ACTION"
    PLAYER_EVENT = "PLAYER EVENT"
    PROCESS = "PROCESS"
    REPEAT = "REPEAT"
    SELECT_OBJECT = "SELECT OBJECT"
    SET_VARIABLE = "SET VARIABLE"
    START_PROCESS = "START PROCESS"


class Text(Enum):
    EMPTY = ""
    X_F_F_55_A_A_OR = "§x§f§f§5§5§a§aOR"


class ReturnTypeEnum(Enum):
    ANY_TYPE = "ANY_TYPE"
    BLOCK = "BLOCK"
    BLOCK_TAG = "BLOCK_TAG"
    DICT = "DICT"
    ENTITY_TYPE = "ENTITY_TYPE"
    ITEM = "ITEM"
    LIST = "LIST"
    LOCATION = "LOCATION"
    NONE = "NONE"
    NUMBER = "NUMBER"
    PARTICLE = "PARTICLE"
    POTION = "POTION"
    PROJECTILE = "PROJECTILE"
    SOUND = "SOUND"
    SPAWN_EGG = "SPAWN_EGG"
    TEXT = "TEXT"
    VARIABLE = "VARIABLE"
    VECTOR = "VECTOR"
    VEHICLE = "VEHICLE"


class Argument:
    type: Optional[ReturnTypeEnum]
    plural: Optional[bool]
    optional: Optional[bool]
    description: Optional[List[str]]
    notes: Optional[List[List[str]]]
    text: Optional[Text]

    def __init__(self, type: Optional[ReturnTypeEnum], plural: Optional[bool], optional: Optional[bool], description: Optional[List[str]], notes: Optional[List[List[str]]], text: Optional[Text]) -> None:
        self.type = type
        self.plural = plural
        self.optional = optional
        self.description = description
        self.notes = notes
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'Argument':
        assert isinstance(obj, dict)
        type = from_union([ReturnTypeEnum, from_none], obj.get("type"))
        plural = from_union([from_bool, from_none], obj.get("plural"))
        optional = from_union([from_bool, from_none], obj.get("optional"))
        description = from_union([lambda x: from_list(from_str, x), from_none], obj.get("description"))
        notes = from_union([lambda x: from_list(lambda x: from_list(from_str, x), x), from_none], obj.get("notes"))
        text = from_union([Text, from_none], obj.get("text"))
        return Argument(type, plural, optional, description, notes, text)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([lambda x: to_enum(ReturnTypeEnum, x), from_none], self.type)
        if self.plural is not None:
            result["plural"] = from_union([from_bool, from_none], self.plural)
        if self.optional is not None:
            result["optional"] = from_union([from_bool, from_none], self.optional)
        if self.description is not None:
            result["description"] = from_union([lambda x: from_list(from_str, x), from_none], self.description)
        if self.notes is not None:
            result["notes"] = from_union([lambda x: from_list(lambda x: from_list(from_str, x), x), from_none], self.notes)
        if self.text is not None:
            result["text"] = from_union([lambda x: to_enum(Text, x), from_none], self.text)
        return result


class Color:
    red: int
    green: int
    blue: int

    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def from_dict(obj: Any) -> 'Color':
        assert isinstance(obj, dict)
        red = from_int(obj.get("red"))
        green = from_int(obj.get("green"))
        blue = from_int(obj.get("blue"))
        return Color(red, green, blue)

    def to_dict(self) -> dict:
        result: dict = {}
        result["red"] = from_int(self.red)
        result["green"] = from_int(self.green)
        result["blue"] = from_int(self.blue)
        return result


class LoadedItem(Enum):
    ARROW = "ARROW"
    EMPTY = ""
    FIREWORK_ROCKET = "FIREWORK_ROCKET"


class RequiredRank(Enum):
    DEV = "Dev"
    EMPEROR = "Emperor"
    EMPTY = ""
    MYTHIC = "Mythic"
    NOBLE = "Noble"
    OVERLORD = "Overlord"


class Icon:
    material: str
    name: str
    deprecated_note: List[str]
    description: List[str]
    example: List[str]
    works_with: List[str]
    additional_info: List[List[str]]
    required_rank: RequiredRank
    require_tokens: bool
    require_rank_and_tokens: bool
    advanced: bool
    loaded_item: LoadedItem
    tags: Optional[int]
    arguments: Optional[List[Argument]]
    head: Optional[str]
    color: Optional[Color]
    cancellable: Optional[bool]
    cancelled_automatically: Optional[bool]
    return_type: Optional[ReturnTypeEnum]
    return_description: Optional[List[str]]

    def __init__(self, material: str, name: str, deprecated_note: List[str], description: List[str], example: List[str], works_with: List[str], additional_info: List[List[str]], required_rank: RequiredRank, require_tokens: bool, require_rank_and_tokens: bool, advanced: bool, loaded_item: LoadedItem, tags: Optional[int], arguments: Optional[List[Argument]], head: Optional[str], color: Optional[Color], cancellable: Optional[bool], cancelled_automatically: Optional[bool], return_type: Optional[ReturnTypeEnum], return_description: Optional[List[str]]) -> None:
        self.material = material
        self.name = name
        self.deprecated_note = deprecated_note
        self.description = description
        self.example = example
        self.works_with = works_with
        self.additional_info = additional_info
        self.required_rank = required_rank
        self.require_tokens = require_tokens
        self.require_rank_and_tokens = require_rank_and_tokens
        self.advanced = advanced
        self.loaded_item = loaded_item
        self.tags = tags
        self.arguments = arguments
        self.head = head
        self.color = color
        self.cancellable = cancellable
        self.cancelled_automatically = cancelled_automatically
        self.return_type = return_type
        self.return_description = return_description

    @staticmethod
    def from_dict(obj: Any) -> 'Icon':
        assert isinstance(obj, dict)
        material = from_str(obj.get("material"))
        name = from_str(obj.get("name"))
        deprecated_note = from_list(from_str, obj.get("deprecatedNote"))
        description = from_list(from_str, obj.get("description"))
        example = from_list(from_str, obj.get("example"))
        works_with = from_list(from_str, obj.get("worksWith"))
        additional_info = from_list(lambda x: from_list(from_str, x), obj.get("additionalInfo"))
        required_rank = RequiredRank(obj.get("requiredRank"))
        require_tokens = from_bool(obj.get("requireTokens"))
        require_rank_and_tokens = from_bool(obj.get("requireRankAndTokens"))
        advanced = from_bool(obj.get("advanced"))
        loaded_item = LoadedItem(obj.get("loadedItem"))
        tags = from_union([from_int, from_none], obj.get("tags"))
        arguments = from_union([lambda x: from_list(Argument.from_dict, x), from_none], obj.get("arguments"))
        head = from_union([from_str, from_none], obj.get("head"))
        color = from_union([Color.from_dict, from_none], obj.get("color"))
        cancellable = from_union([from_bool, from_none], obj.get("cancellable"))
        cancelled_automatically = from_union([from_bool, from_none], obj.get("cancelledAutomatically"))
        return_type = from_union([ReturnTypeEnum, from_none], obj.get("returnType"))
        return_description = from_union([lambda x: from_list(from_str, x), from_none], obj.get("returnDescription"))
        return Icon(material, name, deprecated_note, description, example, works_with, additional_info, required_rank, require_tokens, require_rank_and_tokens, advanced, loaded_item, tags, arguments, head, color, cancellable, cancelled_automatically, return_type, return_description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["material"] = from_str(self.material)
        result["name"] = from_str(self.name)
        result["deprecatedNote"] = from_list(from_str, self.deprecated_note)
        result["description"] = from_list(from_str, self.description)
        result["example"] = from_list(from_str, self.example)
        result["worksWith"] = from_list(from_str, self.works_with)
        result["additionalInfo"] = from_list(lambda x: from_list(from_str, x), self.additional_info)
        result["requiredRank"] = to_enum(RequiredRank, self.required_rank)
        result["requireTokens"] = from_bool(self.require_tokens)
        result["requireRankAndTokens"] = from_bool(self.require_rank_and_tokens)
        result["advanced"] = from_bool(self.advanced)
        result["loadedItem"] = to_enum(LoadedItem, self.loaded_item)
        if self.tags is not None:
            result["tags"] = from_union([from_int, from_none], self.tags)
        if self.arguments is not None:
            result["arguments"] = from_union([lambda x: from_list(lambda x: to_class(Argument, x), x), from_none], self.arguments)
        if self.head is not None:
            result["head"] = from_union([from_str, from_none], self.head)
        if self.color is not None:
            result["color"] = from_union([lambda x: to_class(Color, x), from_none], self.color)
        if self.cancellable is not None:
            result["cancellable"] = from_union([from_bool, from_none], self.cancellable)
        if self.cancelled_automatically is not None:
            result["cancelledAutomatically"] = from_union([from_bool, from_none], self.cancelled_automatically)
        if self.return_type is not None:
            result["returnType"] = from_union([lambda x: to_enum(ReturnTypeEnum, x), from_none], self.return_type)
        if self.return_description is not None:
            result["returnDescription"] = from_union([lambda x: from_list(from_str, x), from_none], self.return_description)
        return result


class SubActionBlock(Enum):
    IF_ENTITY = "if_entity"
    IF_GAME = "if_game"
    IF_PLAYER = "if_player"
    IF_VAR = "if_var"


class Option:
    name: str
    icon: Icon
    aliases: List[str]

    def __init__(self, name: str, icon: Icon, aliases: List[str]) -> None:
        self.name = name
        self.icon = icon
        self.aliases = aliases

    @staticmethod
    def from_dict(obj: Any) -> 'Option':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        icon = Icon.from_dict(obj.get("icon"))
        aliases = from_list(from_str, obj.get("aliases"))
        return Option(name, icon, aliases)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["icon"] = to_class(Icon, self.icon)
        result["aliases"] = from_list(from_str, self.aliases)
        return result


class Tag:
    name: str
    options: List[Option]
    default_option: str
    slot: int

    def __init__(self, name: str, options: List[Option], default_option: str, slot: int) -> None:
        self.name = name
        self.options = options
        self.default_option = default_option
        self.slot = slot

    @staticmethod
    def from_dict(obj: Any) -> 'Tag':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        options = from_list(Option.from_dict, obj.get("options"))
        default_option = from_str(obj.get("defaultOption"))
        slot = from_int(obj.get("slot"))
        return Tag(name, options, default_option, slot)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["options"] = from_list(lambda x: to_class(Option, x), self.options)
        result["defaultOption"] = from_str(self.default_option)
        result["slot"] = from_int(self.slot)
        return result


class Action:
    name: str
    codeblock_name: CodeblockNameEnum
    tags: List[Tag]
    aliases: List[str]
    icon: Icon
    sub_action_blocks: Optional[List[SubActionBlock]]

    def __init__(self, name: str, codeblock_name: CodeblockNameEnum, tags: List[Tag], aliases: List[str], icon: Icon, sub_action_blocks: Optional[List[SubActionBlock]]) -> None:
        self.name = name
        self.codeblock_name = codeblock_name
        self.tags = tags
        self.aliases = aliases
        self.icon = icon
        self.sub_action_blocks = sub_action_blocks

    @staticmethod
    def from_dict(obj: Any) -> 'Action':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        codeblock_name = CodeblockNameEnum(obj.get("codeblockName"))
        tags = from_list(Tag.from_dict, obj.get("tags"))
        aliases = from_list(from_str, obj.get("aliases"))
        icon = Icon.from_dict(obj.get("icon"))
        sub_action_blocks = from_union([lambda x: from_list(SubActionBlock, x), from_none], obj.get("subActionBlocks"))
        return Action(name, codeblock_name, tags, aliases, icon, sub_action_blocks)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["codeblockName"] = to_enum(CodeblockNameEnum, self.codeblock_name)
        result["tags"] = from_list(lambda x: to_class(Tag, x), self.tags)
        result["aliases"] = from_list(from_str, self.aliases)
        result["icon"] = to_class(Icon, self.icon)
        if self.sub_action_blocks is not None:
            result["subActionBlocks"] = from_union([lambda x: from_list(lambda x: to_enum(SubActionBlock, x), x), from_none], self.sub_action_blocks)
        return result


class Codeblock:
    name: CodeblockNameEnum
    identifier: str
    item: Icon

    def __init__(self, name: CodeblockNameEnum, identifier: str, item: Icon) -> None:
        self.name = name
        self.identifier = identifier
        self.item = item

    @staticmethod
    def from_dict(obj: Any) -> 'Codeblock':
        assert isinstance(obj, dict)
        name = CodeblockNameEnum(obj.get("name"))
        identifier = from_str(obj.get("identifier"))
        item = Icon.from_dict(obj.get("item"))
        return Codeblock(name, identifier, item)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = to_enum(CodeblockNameEnum, self.name)
        result["identifier"] = from_str(self.identifier)
        result["item"] = to_class(Icon, self.item)
        return result


class CategoryClass:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'CategoryClass':
        assert isinstance(obj, dict)
        return CategoryClass()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class CosmeticName(Enum):
    BOOSTERS = "Boosters"
    CODE = "Code"
    COSMETICS = "Cosmetics"
    GADGETS = "Gadgets"
    PETS = "Pets"
    PLOT = "Plot"
    PRIZE_TICKET_SHOP = "Prize Ticket Shop"
    TOGGLES = "Toggles"


class CurrencyType(Enum):
    PRIZE_TICKET = "Prize Ticket"
    TOKEN = "Token"


class Purchasable:
    item: Icon
    id: Optional[str]
    price: Optional[int]
    currency_type: Optional[CurrencyType]
    one_time_purchase: Optional[bool]

    def __init__(self, item: Icon, id: Optional[str], price: Optional[int], currency_type: Optional[CurrencyType], one_time_purchase: Optional[bool]) -> None:
        self.item = item
        self.id = id
        self.price = price
        self.currency_type = currency_type
        self.one_time_purchase = one_time_purchase

    @staticmethod
    def from_dict(obj: Any) -> 'Purchasable':
        assert isinstance(obj, dict)
        item = Icon.from_dict(obj.get("item"))
        id = from_union([from_none, from_str], obj.get("id"))
        price = from_union([from_int, from_none], obj.get("price"))
        currency_type = from_union([CurrencyType, from_none], obj.get("currencyType"))
        one_time_purchase = from_union([from_bool, from_none], obj.get("oneTimePurchase"))
        return Purchasable(item, id, price, currency_type, one_time_purchase)

    def to_dict(self) -> dict:
        result: dict = {}
        result["item"] = to_class(Icon, self.item)
        result["id"] = from_union([from_none, from_str], self.id)
        if self.price is not None:
            result["price"] = from_union([from_int, from_none], self.price)
        if self.currency_type is not None:
            result["currencyType"] = from_union([lambda x: to_enum(CurrencyType, x), from_none], self.currency_type)
        if self.one_time_purchase is not None:
            result["oneTimePurchase"] = from_union([from_bool, from_none], self.one_time_purchase)
        return result


class Cosmetic:
    id: str
    icon: Optional[Icon]
    name: Optional[CosmeticName]
    slot: Optional[int]
    category: Optional[CategoryClass]
    purchasables: Optional[List[Purchasable]]

    def __init__(self, id: str, icon: Optional[Icon], name: Optional[CosmeticName], slot: Optional[int], category: Optional[CategoryClass], purchasables: Optional[List[Purchasable]]) -> None:
        self.id = id
        self.icon = icon
        self.name = name
        self.slot = slot
        self.category = category
        self.purchasables = purchasables

    @staticmethod
    def from_dict(obj: Any) -> 'Cosmetic':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        icon = from_union([Icon.from_dict, from_none], obj.get("icon"))
        name = from_union([CosmeticName, from_none], obj.get("name"))
        slot = from_union([from_int, from_none], obj.get("slot"))
        category = from_union([CategoryClass.from_dict, from_none], obj.get("category"))
        purchasables = from_union([lambda x: from_list(Purchasable.from_dict, x), from_none], obj.get("purchasables"))
        return Cosmetic(id, icon, name, slot, category, purchasables)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        if self.icon is not None:
            result["icon"] = from_union([lambda x: to_class(Icon, x), from_none], self.icon)
        if self.name is not None:
            result["name"] = from_union([lambda x: to_enum(CosmeticName, x), from_none], self.name)
        if self.slot is not None:
            result["slot"] = from_union([from_int, from_none], self.slot)
        if self.category is not None:
            result["category"] = from_union([lambda x: to_class(CategoryClass, x), from_none], self.category)
        if self.purchasables is not None:
            result["purchasables"] = from_union([lambda x: from_list(lambda x: to_class(Purchasable, x), x), from_none], self.purchasables)
        return result


class GameValueCategoryElement:
    identifier: str
    gui_slot: int
    icon: Icon

    def __init__(self, identifier: str, gui_slot: int, icon: Icon) -> None:
        self.identifier = identifier
        self.gui_slot = gui_slot
        self.icon = icon

    @staticmethod
    def from_dict(obj: Any) -> 'GameValueCategoryElement':
        assert isinstance(obj, dict)
        identifier = from_str(obj.get("identifier"))
        gui_slot = from_int(obj.get("guiSlot"))
        icon = Icon.from_dict(obj.get("icon"))
        return GameValueCategoryElement(identifier, gui_slot, icon)

    def to_dict(self) -> dict:
        result: dict = {}
        result["identifier"] = from_str(self.identifier)
        result["guiSlot"] = from_int(self.gui_slot)
        result["icon"] = to_class(Icon, self.icon)
        return result


class GameValueCategory(Enum):
    EVENT_VALUES = "Event Values"
    INFORMATIONAL_VALUES = "Informational Values"
    ITEM_VALUES = "Item Values"
    LOCATIONAL_VALUES = "Locational Values"
    PLOT_VALUES = "Plot Values"
    STATISTICAL_VALUES = "Statistical Values"


class GameValue:
    aliases: List[str]
    category: GameValueCategory
    icon: Icon

    def __init__(self, aliases: List[str], category: GameValueCategory, icon: Icon) -> None:
        self.aliases = aliases
        self.category = category
        self.icon = icon

    @staticmethod
    def from_dict(obj: Any) -> 'GameValue':
        assert isinstance(obj, dict)
        aliases = from_list(from_str, obj.get("aliases"))
        category = GameValueCategory(obj.get("category"))
        icon = Icon.from_dict(obj.get("icon"))
        return GameValue(aliases, category, icon)

    def to_dict(self) -> dict:
        result: dict = {}
        result["aliases"] = from_list(from_str, self.aliases)
        result["category"] = to_enum(GameValueCategory, self.category)
        result["icon"] = to_class(Icon, self.icon)
        return result


class ParticleCategoryCategory(Enum):
    AMBIENT_BLOCK_PARTICLES = "Ambient Block Particles"
    AMBIENT_ENTITY_PARTICLES = "Ambient Entity Particles"
    AMBIENT_PARTICLES = "Ambient Particles"
    BLOCK_BEHAVIOR_PARTICLES = "Block Behavior Particles"
    ENTITY_ATTACK_PARTICLES = "Entity Attack Particles"
    ENTITY_BEHAVIOR_PARTICLES = "Entity Behavior Particles"
    LIQUID_PARTICLES = "Liquid Particles"


class Field(Enum):
    COLOR = "Color"
    COLOR_VARIATION = "Color Variation"
    MATERIAL = "Material"
    MOTION = "Motion"
    MOTION_VARIATION = "Motion Variation"
    ROLL = "Roll"
    SIZE = "Size"
    SIZE_VARIATION = "Size Variation"


class Particle:
    particle: str
    icon: Icon
    category: Optional[ParticleCategoryCategory]
    fields: List[Field]

    def __init__(self, particle: str, icon: Icon, category: Optional[ParticleCategoryCategory], fields: List[Field]) -> None:
        self.particle = particle
        self.icon = icon
        self.category = category
        self.fields = fields

    @staticmethod
    def from_dict(obj: Any) -> 'Particle':
        assert isinstance(obj, dict)
        particle = from_str(obj.get("particle"))
        icon = Icon.from_dict(obj.get("icon"))
        category = from_union([from_none, ParticleCategoryCategory], obj.get("category"))
        fields = from_list(Field, obj.get("fields"))
        return Particle(particle, icon, category, fields)

    def to_dict(self) -> dict:
        result: dict = {}
        result["particle"] = from_str(self.particle)
        result["icon"] = to_class(Icon, self.icon)
        result["category"] = from_union([from_none, lambda x: to_enum(ParticleCategoryCategory, x)], self.category)
        result["fields"] = from_list(lambda x: to_enum(Field, x), self.fields)
        return result


class Potion:
    potion: str
    icon: Icon

    def __init__(self, potion: str, icon: Icon) -> None:
        self.potion = potion
        self.icon = icon

    @staticmethod
    def from_dict(obj: Any) -> 'Potion':
        assert isinstance(obj, dict)
        potion = from_str(obj.get("potion"))
        icon = Icon.from_dict(obj.get("icon"))
        return Potion(potion, icon)

    def to_dict(self) -> dict:
        result: dict = {}
        result["potion"] = from_str(self.potion)
        result["icon"] = to_class(Icon, self.icon)
        return result


class SoundCategory:
    identifier: str
    icon: Icon
    has_sub_categories: bool

    def __init__(self, identifier: str, icon: Icon, has_sub_categories: bool) -> None:
        self.identifier = identifier
        self.icon = icon
        self.has_sub_categories = has_sub_categories

    @staticmethod
    def from_dict(obj: Any) -> 'SoundCategory':
        assert isinstance(obj, dict)
        identifier = from_str(obj.get("identifier"))
        icon = Icon.from_dict(obj.get("icon"))
        has_sub_categories = from_bool(obj.get("hasSubCategories"))
        return SoundCategory(identifier, icon, has_sub_categories)

    def to_dict(self) -> dict:
        result: dict = {}
        result["identifier"] = from_str(self.identifier)
        result["icon"] = to_class(Icon, self.icon)
        result["hasSubCategories"] = from_bool(self.has_sub_categories)
        return result


class Sound:
    sound: str
    icon: Icon

    def __init__(self, sound: str, icon: Icon) -> None:
        self.sound = sound
        self.icon = icon

    @staticmethod
    def from_dict(obj: Any) -> 'Sound':
        assert isinstance(obj, dict)
        sound = from_str(obj.get("sound"))
        icon = Icon.from_dict(obj.get("icon"))
        return Sound(sound, icon)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sound"] = from_str(self.sound)
        result["icon"] = to_class(Icon, self.icon)
        return result


class Dfdb:
    codeblocks: List[Codeblock]
    actions: List[Action]
    game_value_categories: List[GameValueCategoryElement]
    game_values: List[GameValue]
    particle_categories: List[Particle]
    particles: List[Particle]
    sound_categories: List[SoundCategory]
    sounds: List[Sound]
    potions: List[Potion]
    cosmetics: List[Cosmetic]
    shops: List[Cosmetic]

    def __init__(self, codeblocks: List[Codeblock], actions: List[Action], game_value_categories: List[GameValueCategoryElement], game_values: List[GameValue], particle_categories: List[Particle], particles: List[Particle], sound_categories: List[SoundCategory], sounds: List[Sound], potions: List[Potion], cosmetics: List[Cosmetic], shops: List[Cosmetic]) -> None:
        self.codeblocks = codeblocks
        self.actions = actions
        self.game_value_categories = game_value_categories
        self.game_values = game_values
        self.particle_categories = particle_categories
        self.particles = particles
        self.sound_categories = sound_categories
        self.sounds = sounds
        self.potions = potions
        self.cosmetics = cosmetics
        self.shops = shops

    @staticmethod
    def from_dict(obj: Any) -> 'Dfdb':
        assert isinstance(obj, dict)
        codeblocks = from_list(Codeblock.from_dict, obj.get("codeblocks"))
        actions = from_list(Action.from_dict, obj.get("actions"))
        game_value_categories = from_list(GameValueCategoryElement.from_dict, obj.get("gameValueCategories"))
        game_values = from_list(GameValue.from_dict, obj.get("gameValues"))
        particle_categories = from_list(Particle.from_dict, obj.get("particleCategories"))
        particles = from_list(Particle.from_dict, obj.get("particles"))
        sound_categories = from_list(SoundCategory.from_dict, obj.get("soundCategories"))
        sounds = from_list(Sound.from_dict, obj.get("sounds"))
        potions = from_list(Potion.from_dict, obj.get("potions"))
        cosmetics = from_list(Cosmetic.from_dict, obj.get("cosmetics"))
        shops = from_list(Cosmetic.from_dict, obj.get("shops"))
        return Dfdb(codeblocks, actions, game_value_categories, game_values, particle_categories, particles, sound_categories, sounds, potions, cosmetics, shops)

    def to_dict(self) -> dict:
        result: dict = {}
        result["codeblocks"] = from_list(lambda x: to_class(Codeblock, x), self.codeblocks)
        result["actions"] = from_list(lambda x: to_class(Action, x), self.actions)
        result["gameValueCategories"] = from_list(lambda x: to_class(GameValueCategoryElement, x), self.game_value_categories)
        result["gameValues"] = from_list(lambda x: to_class(GameValue, x), self.game_values)
        result["particleCategories"] = from_list(lambda x: to_class(Particle, x), self.particle_categories)
        result["particles"] = from_list(lambda x: to_class(Particle, x), self.particles)
        result["soundCategories"] = from_list(lambda x: to_class(SoundCategory, x), self.sound_categories)
        result["sounds"] = from_list(lambda x: to_class(Sound, x), self.sounds)
        result["potions"] = from_list(lambda x: to_class(Potion, x), self.potions)
        result["cosmetics"] = from_list(lambda x: to_class(Cosmetic, x), self.cosmetics)
        result["shops"] = from_list(lambda x: to_class(Cosmetic, x), self.shops)
        return result


def dfdb_from_dict(s: Any) -> Dfdb:
    return Dfdb.from_dict(s)


def dfdb_to_dict(x: Dfdb) -> Any:
    return to_class(Dfdb, x)
