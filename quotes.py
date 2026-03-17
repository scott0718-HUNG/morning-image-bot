"""
quotes.py — 經典中文勵志語錄資料庫（純中文版）
"""

import random

QUOTES = [
    {"id": 1, "quote": "千里之行，始於足下。", "author": "老子", "source": "《道德經》", "category": "perseverance", "bg_prompt": "misty mountain path at sunrise, golden light through ancient Chinese pine trees"},
    {"id": 2, "quote": "不積跬步，無以至千里；不積小流，無以成江海。", "author": "荀子", "source": "《勸學》", "category": "perseverance", "bg_prompt": "great Chinese river at dawn, small streams merging, golden morning mist"},
    {"id": 3, "quote": "天行健，君子以自強不息。", "author": "《周易》", "source": "《易經·乾卦》", "category": "courage", "bg_prompt": "powerful sunrise over Chinese mountains, dramatic golden sky, epic landscape"},
    {"id": 4, "quote": "知之者不如好之者，好之者不如樂之者。", "author": "孔子", "source": "《論語·雍也》", "category": "wisdom", "bg_prompt": "ancient Chinese scholar reading under blossoming cherry tree, warm spring morning"},
    {"id": 5, "quote": "路漫漫其修遠兮，吾將上下而求索。", "author": "屈原", "source": "《離騷》", "category": "dream", "bg_prompt": "endless starry sky over Chinese mountains, milky way, long winding road to horizon"},
    {"id": 6, "quote": "鍥而不捨，金石可鏤。", "author": "荀子", "source": "《勸學》", "category": "perseverance", "bg_prompt": "water carving through mountain stone canyon, turquoise water, dawn light"},
    {"id": 7, "quote": "有志者，事竟成。", "author": "《後漢書》", "source": "《耿弇傳》", "category": "dream", "bg_prompt": "mountain climber reaching summit at sunrise, vast landscape below, golden light"},
    {"id": 8, "quote": "學而不思則罔，思而不學則殆。", "author": "孔子", "source": "《論語·為政》", "category": "wisdom", "bg_prompt": "open ancient book with soft morning light, surrounded by nature, calm atmosphere"},
    {"id": 9, "quote": "生當作人傑，死亦為鬼雄。", "author": "李清照", "source": "《夏日絕句》", "category": "courage", "bg_prompt": "eagle soaring above storm clouds, powerful and majestic dawn"},
    {"id": 10, "quote": "寶劍鋒從磨礪出，梅花香自苦寒來。", "author": "古諺", "source": "中國古典諺語", "category": "growth", "bg_prompt": "plum blossoms blooming in snow, pink flowers against white snow, serene winter morning"},
    {"id": 11, "quote": "己所不欲，勿施於人。", "author": "孔子", "source": "《論語·顏淵》", "category": "wisdom", "bg_prompt": "two people helping each other on mountain path, sunrise, warm golden light"},
    {"id": 12, "quote": "人生如逆旅，我亦是行人。", "author": "蘇軾", "source": "《臨江仙·送錢穆父》", "category": "happiness", "bg_prompt": "solo traveler on scenic mountain road, warm autumn colors, golden hour journey"},
    {"id": 13, "quote": "臨淵羨魚，不如退而結網。", "author": "《漢書》", "source": "《漢書·董仲舒傳》", "category": "wisdom", "bg_prompt": "fisherman casting net at sunrise on calm Chinese lake, misty morning"},
    {"id": 14, "quote": "天將降大任於斯人也，必先苦其心志，勞其筋骨。", "author": "孟子", "source": "《孟子·告子下》", "category": "perseverance", "bg_prompt": "storm before dawn breaking into brilliant sunrise, dramatic transformation, hope"},
    {"id": 15, "quote": "老驥伏櫪，志在千里；烈士暮年，壯心不已。", "author": "曹操", "source": "《步出夏門行》", "category": "dream", "bg_prompt": "majestic horse running free on open plains at sunrise, spirit and determination"},
    {"id": 16, "quote": "長風破浪會有時，直掛雲帆濟滄海。", "author": "李白", "source": "《行路難》", "category": "courage", "bg_prompt": "sailing ship breaking through ocean waves at sunrise, full sails, adventurous spirit"},
    {"id": 17, "quote": "會當凌絕頂，一覽眾山小。", "author": "杜甫", "source": "《望嶽》", "category": "dream", "bg_prompt": "view from mountaintop looking down at clouds and smaller peaks, sunrise, achievement"},
    {"id": 18, "quote": "讀萬卷書，行萬里路。", "author": "劉彝", "source": "《畫旨》", "category": "growth", "bg_prompt": "traveler with map on scenic mountain road, exploration and knowledge, morning light"},
    {"id": 19, "quote": "但願人長久，千里共嬋娟。", "author": "蘇軾", "source": "《水調歌頭》", "category": "love", "bg_prompt": "full moon over misty mountains, peaceful night sky, togetherness across distance"},
    {"id": 20, "quote": "山重水複疑無路，柳暗花明又一村。", "author": "陸游", "source": "《遊山西村》", "category": "perseverance", "bg_prompt": "winding path through mountains opening to beautiful valley, hope after hardship"},
    {"id": 21, "quote": "不經一番寒徹骨，怎得梅花撲鼻香。", "author": "黃蘖禪師", "source": "《上堂開示頌》", "category": "growth", "bg_prompt": "white plum blossoms against blue winter sky, snow on branches, pure and strong"},
    {"id": 22, "quote": "欲窮千里目，更上一層樓。", "author": "王之渙", "source": "《登鸛雀樓》", "category": "dream", "bg_prompt": "ancient Chinese tower with panoramic view, golden sunrise, vast horizon"},
    {"id": 23, "quote": "海內存知己，天涯若比鄰。", "author": "王勃", "source": "《送杜少府之任蜀州》", "category": "love", "bg_prompt": "two roads meeting at mountain pass at sunrise, friendship across distance, warm light"},
    {"id": 24, "quote": "精誠所至，金石為開。", "author": "《後漢書》", "source": "《後漢書·廣陵思王荊傳》", "category": "perseverance", "bg_prompt": "sunlight breaking through solid rock formation, determination and persistence, dramatic light"},
    {"id": 25, "quote": "勝人者有力，自勝者強。", "author": "老子", "source": "《道德經》", "category": "courage", "bg_prompt": "person meditating on mountain peak at dawn, inner strength, peaceful power"},
    {"id": 26, "quote": "問渠那得清如許？為有源頭活水來。", "author": "朱熹", "source": "《觀書有感》", "category": "growth", "bg_prompt": "crystal clear mountain spring source, water flowing from pristine mountain, fresh morning mist"},
    {"id": 27, "quote": "少年易老學難成，一寸光陰不可輕。", "author": "朱熹", "source": "《勸學詩》", "category": "growth", "bg_prompt": "young person reading under cherry blossoms, petals falling, precious spring morning"},
    {"id": 28, "quote": "海闊憑魚躍，天高任鳥飛。", "author": "古諺", "source": "中國古典詩詞", "category": "dream", "bg_prompt": "eagle soaring over vast ocean at sunrise, infinite blue sky and sea, freedom"},
    {"id": 29, "quote": "苟日新，日日新，又日新。", "author": "商湯", "source": "《大學》引", "category": "growth", "bg_prompt": "sunrise over mountain horizon, new day concept, fresh renewal, golden light"},
    {"id": 30, "quote": "上善若水，水善利萬物而不爭。", "author": "老子", "source": "《道德經》", "category": "wisdom", "bg_prompt": "gentle waterfall into clear mountain pool, morning light through forest, peaceful power"},
    {"id": 31, "quote": "三人行，必有我師焉。", "author": "孔子", "source": "《論語·述而》", "category": "wisdom", "bg_prompt": "three friends walking on mountain trail at sunrise, learning and sharing, warm light"},
    {"id": 32, "quote": "博學之，審問之，慎思之，明辨之，篤行之。", "author": "《中庸》", "source": "《禮記·中庸》", "category": "growth", "bg_prompt": "ancient Chinese library with sunbeams streaming through windows, books and learning"},
    {"id": 33, "quote": "君子坦蕩蕩，小人長戚戚。", "author": "孔子", "source": "《論語·述而》", "category": "wisdom", "bg_prompt": "open vast grassland under wide blue sky at sunrise, freedom and openness"},
    {"id": 34, "quote": "見賢思齊焉，見不賢而內自省也。", "author": "孔子", "source": "《論語·里仁》", "category": "growth", "bg_prompt": "mirror reflecting morning sky, self-reflection by calm lake, growth and improvement"},
    {"id": 35, "quote": "為者常成，行者常至。", "author": "《晏子春秋》", "source": "《晏子春秋·內篇雜下》", "category": "perseverance", "bg_prompt": "determined hiker walking steadily on long mountain trail, morning mist, step by step"},
    {"id": 36, "quote": "不飛則已，一飛沖天；不鳴則已，一鳴驚人。", "author": "司馬遷", "source": "《史記·滑稽列傳》", "category": "courage", "bg_prompt": "eagle launching from cliff into brilliant sunrise sky, explosive moment of flight"},
    {"id": 37, "quote": "學如逆水行舟，不進則退。", "author": "左宗棠", "source": "古諺", "category": "growth", "bg_prompt": "boat rowing upstream against gentle current, determination, dawn on peaceful river"},
    {"id": 38, "quote": "業精於勤，荒於嬉；行成於思，毀於隨。", "author": "韓愈", "source": "《進學解》", "category": "growth", "bg_prompt": "student studying by candlelight, dedication and focus, warm morning atmosphere"},
    {"id": 39, "quote": "富貴不能淫，貧賤不能移，威武不能屈，此之謂大丈夫。", "author": "孟子", "source": "《孟子·滕文公下》", "category": "courage", "bg_prompt": "lone ancient pine tree standing firm against storm winds, roots deep in rock"},
    {"id": 40, "quote": "吾日三省吾身：為人謀而不忠乎？與朋友交而不信乎？傳不習乎？", "author": "曾子", "source": "《論語·學而》", "category": "wisdom", "bg_prompt": "peaceful meditation by still lake at dawn, reflection in water, serene atmosphere"},
    {"id": 41, "quote": "正心、修身、齊家、治國、平天下。", "author": "《大學》", "source": "《禮記·大學》", "category": "wisdom", "bg_prompt": "traditional Chinese family home at sunrise, harmony and order, warm morning light"},
    {"id": 42, "quote": "桃李不言，下自成蹊。", "author": "司馬遷", "source": "《史記》", "category": "wisdom", "bg_prompt": "peach and plum trees in full bloom, path worn by visitors, spring morning beauty"},
    {"id": 43, "quote": "春蠶到死絲方盡，蠟炬成灰淚始乾。", "author": "李商隱", "source": "《無題》", "category": "love", "bg_prompt": "single candle glowing warmly in morning mist, devotion and warmth, soft light"},
    {"id": 44, "quote": "人生得意須盡歡，莫使金樽空對月。", "author": "李白", "source": "《將進酒》", "category": "happiness", "bg_prompt": "full moon over Chinese lake, warm reflection on water, starry sky, peaceful night"},
    {"id": 45, "quote": "知足者富。", "author": "老子", "source": "《道德經》", "category": "happiness", "bg_prompt": "simple beautiful life, morning tea in Chinese garden, contentment, soft sunlight"},
    {"id": 46, "quote": "不患人之不己知，患不知人也。", "author": "孔子", "source": "《論語·學而》", "category": "wisdom", "bg_prompt": "scholar observing world from hilltop at dawn, contemplative, wisdom and reflection"},
    {"id": 47, "quote": "窮則變，變則通，通則久。", "author": "《周易》", "source": "《易經·繫辭下傳》", "category": "wisdom", "bg_prompt": "river changing course through landscape, aerial dawn view, fluid shapes in nature"},
    {"id": 48, "quote": "志不強者智不達，言不信者行不果。", "author": "墨子", "source": "《墨子·修身》", "category": "courage", "bg_prompt": "determined archer aiming at distant target, focus, early morning practice, mist"},
    {"id": 49, "quote": "仁者愛人，有禮者敬人。愛人者，人恆愛之。", "author": "孟子", "source": "《孟子·離婁下》", "category": "love", "bg_prompt": "family gathering in traditional Chinese garden, warm evening lantern light"},
    {"id": 50, "quote": "己欲立而立人，己欲達而達人。", "author": "孔子", "source": "《論語·雍也》", "category": "love", "bg_prompt": "person helping another climb mountain, teamwork at sunrise, warm golden light"},
]


def get_random_quote():
    return random.choice(QUOTES)

def get_quote_by_id(quote_id: int):
    for q in QUOTES:
        if q["id"] == quote_id:
            return q
    return None

def get_quotes_by_category(category: str):
    return [q for q in QUOTES if q["category"] == category]

if __name__ == "__main__":
    quote = get_random_quote()
    print(f"語錄：{quote['quote']}")
    print(f"作者：{quote['author']}")
    print(f"出處：{quote['source']}")
