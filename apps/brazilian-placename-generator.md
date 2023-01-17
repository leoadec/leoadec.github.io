---
layout: default
title: Brazilian Placename Generator
---
Pick two words from the list, the output will be
an old Brazilian-sounding placename with the same meaning.

<script>
class Word {
  constructor(initialForm, finalForm) {
    this.initialForm = initialForm;
    this.finalForm = finalForm;
  }

  hasInitialForm() {
    if (this.initialForm == "") return false;
    return true;
  }
}

var wordList = {
  "big": new Word("", "gua&ccedil;u"),
  "bird": new Word("Guyra", "guyra"),
  "black": new Word("", "una"),
  "blue": new Word("", "oby"),
  "devil": new Word("Anhanga", "anhanga"),
  "earth": new Word("Yby", "yby"),
  "father": new Word("Tuba", "ruba"),
  "fire": new Word("Tata", "tata"),
  "fish": new Word("Pira", "pira"),
  "fruit": new Word("Yba", "yba"),
  "green": new Word("", "oby"),
  "house": new Word("Oca", "oca"),
  "jaguar": new Word("Jaguar", "jaguara"),
  "land": new Word("Tetama", "retama"),
  "moon": new Word("Jacy", "jacy"),
  "mother": new Word("Cy", "cy"),
  "old": new Word("", "puera"),
  "prawn": new Word("Poty", "poty"),
  "pretty": new Word("", "poranga"),
  "real": new Word("", "ete"),
  "red": new Word("", "piranga"),
  "river": new Word("Y", "hy"),
  "rock": new Word("Ita", "ita"),
  "shark": new Word("Ypero", "ypero"),
  "shrimp": new Word("Poty", "poty"),
  "small": new Word("", "mirim"),
  "snake": new Word("Boi", "mboi"),
  "star": new Word("Jacytata", "jacytata"),
  "stone": new Word("Ita", "ita"),
  "sun": new Word("Ara", "ara"),
  "tree": new Word("Ybyra", "ybyra"),
  "water": new Word("Y", "hy"),
  "white": new Word("", "tinga"),
  "yellow": new Word("", "juba"),
};

function combineWords(wordOne, wordTwo) {
  if (! ((wordOne in wordList) && (wordTwo in wordList))) {
    return "(no suggestions found)";
  };

  let convertedOne = wordList[wordOne];
  let convertedTwo = wordList[wordTwo];

  let initialWord = convertedOne.initialForm;
  let finalWord = convertedTwo.finalForm;

  if (! convertedOne.hasInitialForm() ) {
    initialWord = convertedTwo.initialForm;
    finalWord = convertedOne.finalForm;
  }; 

  return initialWord + finalWord;
};

function updateForm() {
  let wordOne = document.getElementById("word_1");
  let wordTwo = document.getElementById("word_2");

  if ((wordOne.value == "") || (wordTwo.value == "")) return;

  let result = document.getElementById("result");

  result.innerHTML = combineWords(wordOne.value, wordTwo.value);
}
</script>

<form class="input">
<input id="word_1" list="word_list" onchange="updateForm();" type="text" value="">
<input id="word_2" list="word_list" onchange="updateForm();" type="text" value="">
<datalist id="word_list"></datalist>
</form>

<script>
content = "";
for (var word in wordList) {
  content += "<option value='" + word + "'>" + word + "</option>";
};
document.getElementById("word_list").innerHTML = content;
</script>

<p id="result" class="output"></p>
