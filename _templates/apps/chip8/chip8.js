import init, * as wasm from "/wasm/chip8.js"

const WIDTH = 64;
const HEIGHT = 32;
const SCALE = 10;

const canvas = document.getElementsByTagName("canvas")[0];
canvas.width = WIDTH * SCALE;
canvas.height = HEIGHT * SCALE;

const context = canvas.getContext("2d");
context.fillStyle = "black";
context.fillRect(0, 0, canvas.width, canvas.height);

async function createInput() {
    let input = document.createElement("input");
    input.setAttribute("type", "file");
    document.body.appendChild(input);

    return input;
}

async function runWasm() {
    await init();

    let inputButton = await createInput(); 

    let chip8 = new wasm.Chip8();

    function readFile (evt) {
        const file = evt.target.files[0];
        let reader = new FileReader();
        reader.onload = () => {
            chip8.load(reader.result);
            chip8.update_frame();
        };
        reader.readAsBinaryString(file);
    }

    inputButton.addEventListener("change", readFile);
}

runWasm().catch(console.error());
