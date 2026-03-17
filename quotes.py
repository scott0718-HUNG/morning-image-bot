"""
quotes.py — 經典勵志語錄資料庫
包含 50 則古今中外精選語錄
"""

import random

QUOTES = [
    {
        "id": 1,
        "quote": "千里之行，始於足下。",
        "author": "老子",
        "source": "《道德經》",
        "category": "perseverance",
        "bg_prompt": "misty mountain path at sunrise, golden light filtering through ancient trees, serene and majestic, photorealistic"
    },
    {
        "id": 2,
        "quote": "不積跬步，無以至千里；不積小流，無以成江海。",
        "author": "荀子",
        "source": "《勸學》",
        "category": "perseverance",
        "bg_prompt": "a great river flowing from small streams, aerial view at dawn, golden hour light, majestic landscape"
    },
    {
        "id": 3,
        "quote": "天行健，君子以自強不息。",
        "author": "《周易》",
        "source": "《易經·乾卦》",
        "category": "courage",
        "bg_prompt": "powerful sun rising over mountains, dramatic sky, rays of light breaking through clouds, epic landscape"
    },
    {
        "id": 4,
        "quote": "知之者不如好之者，好之者不如樂之者。",
        "author": "孔子",
        "source": "《論語·雍也》",
        "category": "wisdom",
        "bg_prompt": "ancient Chinese scholar reading under a blossoming tree, warm spring morning, peaceful garden"
    },
    {
        "id": 5,
        "quote": "路漫漫其修遠兮，吾將上下而求索。",
        "author": "屈原",
        "source": "《離騷》",
        "category": "dream",
        "bg_prompt": "endless starry sky over mountains, milky way visible, long winding road disappearing into horizon, night photography"
    },
    {
        "id": 6,
        "quote": "鍥而不捨，金石可鏤。",
        "author": "荀子",
        "source": "《勸學》",
        "category": "perseverance",
        "bg_prompt": "water carving through stone canyon, dramatic lighting, turquoise water, geological wonder"
    },
    {
        "id": 7,
        "quote": "有志者，事竟成。",
        "author": "《後漢書》",
        "source": "《耿弇傳》",
        "category": "dream",
        "bg_prompt": "mountain climber reaching summit at sunrise, triumphant moment, vast landscape below, golden light"
    },
    {
        "id": 8,
        "quote": "學而不思則罔，思而不學則殆。",
        "author": "孔子",
        "source": "《論語·為政》",
        "category": "wisdom",
        "bg_prompt": "open book with light emanating from pages, surrounded by nature, calm morning, philosophical atmosphere"
    },
    {
        "id": 9,
        "quote": "生當作人傑，死亦為鬼雄。",
        "author": "李清照",
        "source": "《夏日絕句》",
        "category": "courage",
        "bg_prompt": "heroic eagle soaring above dramatic storm clouds, lightning in distance, powerful and majestic"
    },
    {
        "id": 10,
        "quote": "寶劍鋒從磨礪出，梅花香自苦寒來。",
        "author": "古諺",
        "source": "中國古典諺語",
        "category": "growth",
        "bg_prompt": "plum blossoms blooming in snow, delicate pink flowers against white snow, serene winter morning"
    },
    {
        "id": 11,
        "quote": "己所不欲，勿施於人。",
        "author": "孔子",
        "source": "《論語·顏淵》",
        "category": "wisdom",
        "bg_prompt": "two people helping each other climb a mountain, sunrise, warm golden light, friendship and cooperation"
    },
    {
        "id": 12,
        "quote": "窮則變，變則通，通則久。",
        "author": "《周易》",
        "source": "《易經·繫辭下傳》",
        "category": "wisdom",
        "bg_prompt": "river changing course through landscape, aerial view, fluid shapes in earth, natural adaptation"
    },
    {
        "id": 13,
        "quote": "人生如逆旅，我亦是行人。",
        "author": "蘇軾",
        "source": "《臨江仙·送錢穆父》",
        "category": "happiness",
        "bg_prompt": "solo traveler on scenic mountain road, warm autumn colors, journey at golden hour"
    },
    {
        "id": 14,
        "quote": "人生得意須盡歡，莫使金樽空對月。",
        "author": "李白",
        "source": "《將進酒》",
        "category": "happiness",
        "bg_prompt": "full moon over a lake, warm campfire reflection, starry sky, celebratory atmosphere"
    },
    {
        "id": 15,
        "quote": "臨淵羨魚，不如退而結網。",
        "author": "《漢書》",
        "source": "《漢書·董仲舒傳》",
        "category": "wisdom",
        "bg_prompt": "fisherman casting net at sunrise on calm lake, misty morning, action and purpose"
    },
    {
        "id": 16,
        "quote": "Imagination is more important than knowledge.",
        "author": "Albert Einstein",
        "source": "",
        "category": "dream",
        "bg_prompt": "surreal dreamlike landscape with floating islands and colorful aurora, creative fantasy world, vivid colors"
    },
    {
        "id": 17,
        "quote": "In the middle of every difficulty lies opportunity.",
        "author": "Albert Einstein",
        "source": "",
        "category": "courage",
        "bg_prompt": "sunlight breaking through dark storm clouds, dramatic contrast, hopeful rays illuminating landscape"
    },
    {
        "id": 18,
        "quote": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "source": "Stanford Commencement Speech, 2005",
        "category": "dream",
        "bg_prompt": "creative workspace with morning light, passionate artist or craftsman at work, warm inspiring atmosphere"
    },
    {
        "id": 19,
        "quote": "It does not matter how slowly you go as long as you do not stop.",
        "author": "Confucius",
        "source": "",
        "category": "perseverance",
        "bg_prompt": "tortoise on a long winding path through beautiful garden, dawn light, patient and steady journey"
    },
    {
        "id": 20,
        "quote": "The future belongs to those who believe in the beauty of their dreams.",
        "author": "Eleanor Roosevelt",
        "source": "",
        "category": "dream",
        "bg_prompt": "hot air balloons floating over misty valleys at sunrise, colorful and hopeful, dreamy atmosphere"
    },
    {
        "id": 21,
        "quote": "You miss 100% of the shots you don't take.",
        "author": "Wayne Gretzky",
        "source": "",
        "category": "courage",
        "bg_prompt": "basketball court at dusk, single player taking a shot, dramatic stadium lighting, determination"
    },
    {
        "id": 22,
        "quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "author": "Winston Churchill",
        "source": "",
        "category": "perseverance",
        "bg_prompt": "lighthouse standing strong against crashing waves at storm, beacon of light in darkness, resilience"
    },
    {
        "id": 23,
        "quote": "The greatest glory in living lies not in never falling, but in rising every time we fall.",
        "author": "Nelson Mandela",
        "source": "",
        "category": "perseverance",
        "bg_prompt": "phoenix rising from flames, dramatic golden light, powerful transformation symbol, majestic"
    },
    {
        "id": 24,
        "quote": "Spread love everywhere you go. Let no one ever come to you without leaving happier.",
        "author": "Mother Teresa",
        "source": "",
        "category": "love",
        "bg_prompt": "field of sunflowers at sunrise, warm golden light, joyful nature scene, abundance of warmth"
    },
    {
        "id": 25,
        "quote": "When you reach the end of your rope, tie a knot in it and hang on.",
        "author": "Franklin D. Roosevelt",
        "source": "",
        "category": "perseverance",
        "bg_prompt": "climber holding on to cliff edge, sunrise breaking through clouds below, determination and strength"
    },
    {
        "id": 26,
        "quote": "Always remember that you are absolutely unique. Just like everyone else.",
        "author": "Margaret Mead",
        "source": "",
        "category": "growth",
        "bg_prompt": "single colorful flower blooming among green grass, dew drops, morning light, unique beauty"
    },
    {
        "id": 27,
        "quote": "Do not go where the path may lead, go instead where there is no path and leave a trail.",
        "author": "Ralph Waldo Emerson",
        "source": "",
        "category": "courage",
        "bg_prompt": "explorer walking through untouched snow-covered forest, creating first footprints, winter sunrise"
    },
    {
        "id": 28,
        "quote": "You will face many defeats in life, but never let yourself be defeated.",
        "author": "Maya Angelou",
        "source": "",
        "category": "courage",
        "bg_prompt": "warrior standing on mountain top after storm, clear sky emerging, victory and strength"
    },
    {
        "id": 29,
        "quote": "The purpose of our lives is to be happy.",
        "author": "Dalai Lama",
        "source": "",
        "category": "happiness",
        "bg_prompt": "Tibetan monk walking through colorful prayer flags with mountains in background, peaceful morning"
    },
    {
        "id": 30,
        "quote": "Life is what happens when you're busy making other plans.",
        "author": "John Lennon",
        "source": "",
        "category": "happiness",
        "bg_prompt": "spontaneous moment of joy, children playing in autumn leaves park, candid happiness, warm light"
    },
    {
        "id": 31,
        "quote": "仁者愛人，有禮者敬人。愛人者，人恆愛之；敬人者，人恆敬之。",
        "author": "孟子",
        "source": "《孟子·離婁下》",
        "category": "love",
        "bg_prompt": "family gathering around warm fire, generations together, loving atmosphere, golden evening light"
    },
    {
        "id": 32,
        "quote": "富貴不能淫，貧賤不能移，威武不能屈，此之謂大丈夫。",
        "author": "孟子",
        "source": "《孟子·滕文公下》",
        "category": "courage",
        "bg_prompt": "lone tree standing firm against storm winds, roots deep in earth, resilience and integrity"
    },
    {
        "id": 33,
        "quote": "不患人之不己知，患不知人也。",
        "author": "孔子",
        "source": "《論語·學而》",
        "category": "wisdom",
        "bg_prompt": "scholar observing the world from hilltop at dawn, contemplative, wisdom and self-reflection"
    },
    {
        "id": 34,
        "quote": "聖人千慮，必有一失；愚人千慮，必有一得。",
        "author": "《晏子春秋》",
        "source": "《晏子春秋·雜下》",
        "category": "wisdom",
        "bg_prompt": "balance scales with light and shadow, philosophical concept art, morning enlightenment"
    },
    {
        "id": 35,
        "quote": "業精於勤，荒於嬉；行成於思，毀於隨。",
        "author": "韓愈",
        "source": "《進學解》",
        "category": "growth",
        "bg_prompt": "student studying by candlelight in traditional setting, dedication and learning, warm focused atmosphere"
    },
    {
        "id": 36,
        "quote": "In three words I can sum up everything I've learned about life: it goes on.",
        "author": "Robert Frost",
        "source": "",
        "category": "wisdom",
        "bg_prompt": "river flowing endlessly through changing seasons, time lapse concept, continuity of nature"
    },
    {
        "id": 37,
        "quote": "Twenty years from now you will be more disappointed by the things you didn't do than by the ones you did.",
        "author": "Mark Twain",
        "source": "",
        "category": "courage",
        "bg_prompt": "traveler standing at crossroads at sunrise, open roads to adventure, choice and opportunity"
    },
    {
        "id": 38,
        "quote": "It is during our darkest moments that we must focus to see the light.",
        "author": "Aristotle",
        "source": "",
        "category": "perseverance",
        "bg_prompt": "single candle flame in complete darkness, warm glow, hope and light in difficult times"
    },
    {
        "id": 39,
        "quote": "Believe you can and you're halfway there.",
        "author": "Theodore Roosevelt",
        "source": "",
        "category": "dream",
        "bg_prompt": "confident person looking towards bright horizon, sunrise over ocean, belief and possibility"
    },
    {
        "id": 40,
        "quote": "I alone cannot change the world, but I can cast a stone across the waters to create many ripples.",
        "author": "Mother Teresa",
        "source": "",
        "category": "love",
        "bg_prompt": "stone thrown in calm lake creating beautiful ripple patterns, reflection of sunrise, peaceful impact"
    },
    {
        "id": 41,
        "quote": "問渠那得清如許？為有源頭活水來。",
        "author": "朱熹",
        "source": "《觀書有感》",
        "category": "growth",
        "bg_prompt": "crystal clear mountain spring source, water flowing from pristine mountain, fresh morning mist"
    },
    {
        "id": 42,
        "quote": "少年易老學難成，一寸光陰不可輕。",
        "author": "朱熹",
        "source": "《勸學詩》",
        "category": "growth",
        "bg_prompt": "young person reading under cherry blossoms, petals falling, precious moment of spring learning"
    },
    {
        "id": 43,
        "quote": "海闊憑魚躍，天高任鳥飛。",
        "author": "古諺",
        "source": "中國古典詩詞",
        "category": "dream",
        "bg_prompt": "eagle soaring over vast ocean at sunrise, infinite blue sky and sea, freedom and possibility"
    },
    {
        "id": 44,
        "quote": "苟日新，日日新，又日新。",
        "author": "商湯",
        "source": "《大學》引",
        "category": "growth",
        "bg_prompt": "sunrise every morning over mountain horizon, new day concept, fresh start and renewal"
    },
    {
        "id": 45,
        "quote": "Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate; only love can do that.",
        "author": "Martin Luther King Jr.",
        "source": "《Strength to Love》",
        "category": "love",
        "bg_prompt": "sunrise breaking through storm clouds over city, light overcoming darkness, hope and peace"
    },
    {
        "id": 46,
        "quote": "The best time to plant a tree was 20 years ago. The second best time is now.",
        "author": "中國古諺（廣為流傳）",
        "source": "",
        "category": "wisdom",
        "bg_prompt": "person planting a young tree at dawn, soil and nature, new beginning, morning light"
    },
    {
        "id": 47,
        "quote": "An unexamined life is not worth living.",
        "author": "Socrates",
        "source": "《Apology》",
        "category": "wisdom",
        "bg_prompt": "philosopher sitting in contemplation on cliff edge overlooking sunrise, reflection and wisdom"
    },
    {
        "id": 48,
        "quote": "Happiness is not something readymade. It comes from your own actions.",
        "author": "Dalai Lama",
        "source": "",
        "category": "happiness",
        "bg_prompt": "monk tending garden with joy, colorful flowers, peaceful monastery at dawn, contentment"
    },
    {
        "id": 49,
        "quote": "志不強者智不達，言不信者行不果。",
        "author": "墨子",
        "source": "《墨子·修身》",
        "category": "courage",
        "bg_prompt": "determined archer aiming at distant target, focus and determination, early morning practice"
    },
    {
        "id": 50,
        "quote": "知足者富。",
        "author": "老子",
        "source": "《道德經》",
        "category": "happiness",
        "bg_prompt": "simple beautiful life, person sitting peacefully in nature, morning tea in garden, contentment and gratitude"
    },
]


def get_random_quote():
    """隨機取得一則語錄"""
    return random.choice(QUOTES)


def get_quote_by_id(quote_id: int):
    """依 ID 取得語錄"""
    for q in QUOTES:
        if q["id"] == quote_id:
            return q
    return None


def get_quotes_by_category(category: str):
    """依分類取得語錄列表"""
    return [q for q in QUOTES if q["category"] == category]


if __name__ == "__main__":
    quote = get_random_quote()
    print(f"語錄：{quote['quote']}")
    print(f"作者：{quote['author']}")
    print(f"出處：{quote['source']}")
