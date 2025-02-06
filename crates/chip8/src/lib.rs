use std::thread;
use std::time;

mod ram;
mod screen;
mod sprite;
mod stack;
mod timer;

use ram::Ram;
use screen::Screen;
use stack::Stack;
use timer::{Beeper, Timer};

#[derive(Debug)]
pub struct Chip8 {
    i_register: u16,
    v_registers: [u8; 16],
    ram: Ram,
    stack: Stack,
    screen: Screen,
    sound_timer: Timer<Beeper>,
    delay_timer: Timer<Beeper>,
}

impl Chip8 {
    pub fn new() -> Self {
        Chip8 {
            i_register: 0,
            v_registers: [0; 16],
            ram: Ram::new(),
            stack: Stack::new(),
            screen: Screen::new(),
            sound_timer: Timer::<Beeper>::new(),
            delay_timer: Timer::<Beeper>::new(),
        }
    }

    pub fn load(&mut self, buffer: &[u8]) {
        self.ram.load(buffer);
    }

    fn return_from_subroutine(&mut self) {
        self.ram.goto(self.stack.pop());
    }

    fn run_op(&mut self, op: u16) {
        match op {
            0x0000 => (),
            0x00e0 => self.screen.clear(),
            0x00ee => self.return_from_subroutine(),
            _ => (),
        }
    }

    fn tick(&mut self) {
        let op = self.ram.next();
        self.run_op(op);

        self.sound_timer.tick();
        self.delay_timer.tick();
    }

    pub fn run(&mut self) {
        loop {
            self.tick();
            thread::sleep(time::Duration::from_millis(30));
            self.screen.print();
        }
    }
}
