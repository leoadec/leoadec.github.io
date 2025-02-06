use std::env;
use std::fs::File;
use std::io::Read;

use chip8::Chip8;

fn main() {
    let mut args = env::args().skip(1);

    let filename = match args.next() {
        None => panic!("File name not provided."),
        Some(arg) => String::from(arg),
    };

    let file = File::open(&filename);

    let mut buffer = Vec::new();

    match file {
        Err(_) => panic!("Could not read file {filename}."),
        Ok(mut f) => f.read(&mut buffer).expect("Could not read file."),
    };

    let mut chip8 = Chip8::new();

    chip8.tick();
}
