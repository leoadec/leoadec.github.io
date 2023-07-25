const brazilianPlaceNames = new Map([
    ["Amapa", "Amapá"],
    ["Belem", "Belém"],
    ["Brasilia", "Brasília"],
    ["Ceara", "Ceará"],
    ["Cuiaba", "Cuiabá"],
    ["Florianopolis", "Florianópolis"],
    ["Goiania", "Goiânia"],
    ["Goias", "Goiás"],
    ["Joao Pessoa", "João Pessoa"],
    ["Macapa", "Macapá"],
    ["Maceio", "Maceió"],
    ["Maranhao", "Maranhão"],
    ["Para", "Pará"],
    ["Paraiba", "Paraíba"],
    ["Piauí", "Piaui"],
    ["Rondonia", "Rondônia"],
    ["Sao Luis", "São Luís"],
    ["Sao Paulo", "São Paulo"],
    ["Vitoria", "Vitória"],
])


function convertWord(word) {
    if (brazilianPlaceNames.has(word)) {
        return brazilianPlaceNames.get(word);
    };
    return word;
}

function unicodeConversion(text) {
    const words = text.trim().replace(/ +/g, " ").split(" ");

    let updatedWords = words.map(convertWord);

    return updatedWords.join(" ");
}
