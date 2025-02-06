mod ram;
mod screen;
mod sprite;
mod stack;

use ram::Ram;
use screen::Screen;
use stack::Stack;

#[derive(Debug)]
pub struct Chip8 {
    program_counter: u16,
    i_register: u16,
    v_registers: [u8; 16],
    ram: Ram,
    stack: Stack,
    screen: Screen,
    sound_timer: u8,
    delay_timer: u8,
}

impl Chip8 {
    pub fn new() -> Self {
        Chip8 {
            program_counter: 512,
            i_register: 0,
            v_registers: [0; 16],
            ram: Ram::new(),
            stack: Stack::new(),
            screen: Screen::new(),
            sound_timer: 0,
            delay_timer: 0,
        }
    }

    pub fn stack_push(&mut self, value: u16) {
        self.stack.push(value);
    }

    pub fn stack_pop(&mut self) -> u16 {
        self.stack.pop()
    }
}
