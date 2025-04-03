import aiohttp
import asyncio

url_word_counts = {}
frequencies = {}
files = {}

async def main(url, words_file):

    # хеширование запроса
    if url not in url_word_counts:
        url_word_counts[url] = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()

        # создание словаря содержания запроса {слово: количество в responde}
        for word in data.split():
            if word not in url_word_counts[url]:
                url_word_counts[url][word] = 1
            else:
                url_word_counts[url][word] += 1

    # хеширование открытия файла в сет:
    if words_file not in files:
        files[words_file] = set()
        with open(words_file, 'r') as file:
            for line in file:
                word = line.strip()
                files[words_file].add(word)

    for word in files[words_file]:
        try:
            frequencies[word] = url_word_counts[url][word]
        except KeyError as e: # если нет слова из words в ответе url
            frequencies[word] = 0
    
    print(frequencies)
    return frequencies

words_file = "words.txt"
url = "https://eng.mipt.ru/why-mipt/"

if __name__ == "__main__":
    asyncio.run(main(url, words_file))