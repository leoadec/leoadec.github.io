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

function printScreen(input) {
    for (let i=0; i < input.length; i += 1) {
        let column = i % WIDTH;
        let row = Math.floor(i / WIDTH);
        let color = "white";
        if (input.charAt(i) != 0) color = "black";
        context.fillStyle = color;
        context.fillRect(column * SCALE, row * SCALE, SCALE - 1, SCALE - 1);
    }
}

async function mainLoop(chip8) {
    let is_true = true;
    while(is_true) {
        for (let j=0; j<10; j += 1) {
            let op = chip8.tick();
        }
        let frame_state = chip8.update_frame();
        printScreen(frame_state);
        await new Promise((r) => setTimeout(r, 30));
    }
}

async function runWasm() {
    await init();

    let inputButton = await createInput(); 

    let chip8 = new wasm.Chip8();

    document.addEventListener(
        "keydown", function(evt) {
            chip8.handle_keys(evt.key, true);
        }
    )
    document.addEventListener(
        "keyup", function(evt) {
            chip8.handle_keys(evt.key, false);
        }
    )

    function readFile (evt) {
        const file = evt.target.files[0];
        let reader = new FileReader();
        reader.onload = () => {
            let buffer = reader.result;
            const u8array = new Uint8Array(buffer);
            chip8.load(u8array);
            mainLoop(chip8);
        };
        reader.readAsArrayBuffer(file);
    }

    inputButton.addEventListener("change", readFile);
}

runWasm()
