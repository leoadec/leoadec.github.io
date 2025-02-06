use std::env;

use chip8::Chip8;

fn main() {
    let mut args = env::args().skip(1);

    let filename = match args.next() {
        None => panic!("File name not provided."),
        Some(arg) => String::from(arg),
    };

    let mut chip8 = Chip8::new(&filename);

    chip8.tick();
}
