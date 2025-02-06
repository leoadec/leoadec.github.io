use chip8::Chip8;

fn main() {
    let mut chip8 = Chip8::new();

    chip8.stack_push(3);
    print!("{}", chip8.stack_pop());

    chip8.tick();
}
