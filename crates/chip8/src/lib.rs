use std::thread;
use std::time;

mod ram;
mod screen;
pub mod sprite;
mod stack;
mod timer;

use ram::Ram;
use screen::Screen;
use sprite::Sprite;
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
        let address = self.stack.pop();
        self.ram.goto(address);
    }

    fn jump(&mut self, op: u16) {
        let address = 0x0fff & op;
        self.ram.goto(address);
    }

    fn jump_plus_register(&mut self, op: u16) {
        let address = 0x0fff & op;

        self.ram.goto(address + self.v_registers[0] as u16);
    }

    fn call_subroutine(&mut self, op: u16) {
        let address = 0x0fff & op;
        self.stack.push(self.ram.get_current_counter());
        self.ram.goto(address);
    }

    fn if_register_matches_literal(&mut self, op: u16) {
        let literal = 0x00ff & op as u8;
        let register_nb = ((0x0f00 & op) >> 8) as usize;

        if self.v_registers[register_nb as usize] == literal {
            self.ram.next();
        }
    }

    fn if_register_does_not_match_literal(&mut self, op: u16) {
        let literal = 0x00ff & op as u8;
        let register_nb = ((0x0f00 & op) >> 8) as usize;

        if self.v_registers[register_nb as usize] != literal {
            self.ram.next();
        }
    }

    fn if_register_matches_register(&mut self, op: u16) {
        if ((0x000f & op) != 0) {
            panic!("Unrecognized operation.");
        }

        let register_1 = ((0x0f00 & op) >> 8) as usize;
        let register_2 = ((0x00f0 & op) >> 4) as usize;

        if self.v_registers[register_1] == self.v_registers[register_2] {
            self.ram.next();
        }
    }

    fn if_register_does_not_match_register(&mut self, op: u16) {
        if ((0x000f & op) != 0) {
            panic!("Unrecognized operation.");
        }

        let register_1 = ((0x0f00 & op) >> 8) as usize;
        let register_2 = ((0x00f0 & op) >> 4) as usize;

        if self.v_registers[register_1] != self.v_registers[register_2] {
            self.ram.next();
        }
    }

    fn assign_to_v_register(&mut self, op: u16) {
        let literal = 0x00ff & op as u8;
        let register_nb = ((0x0f00 & op) >> 8) as usize;

        self.v_registers[register_nb] = literal;
    }

    fn assign_to_i_register(&mut self, op: u16) {
        let literal = 0x0fff & op as u16;

        self.i_register = literal;
    }

    fn add_to_v_register(&mut self, op: u16) {
        let literal = 0x00ff & op as u8;
        let register_nb = ((0x0f00 & op) >> 8) as usize;

        self.v_registers[register_nb] = self.v_registers[register_nb].wrapping_add(literal);
    }

    fn assign_from_v_register(&mut self, op: u16) {
        if ((0x000f & op) != 0) {
            panic!("Unrecognized operation.");
        }

        let register_1 = ((0x0f00 & op) >> 8) as usize;
        let register_2 = ((0x00f0 & op) >> 4) as usize;

        self.v_registers[register_1] = self.v_registers[register_2];
    }

    fn draw_sprite(&mut self, op: u16) {
        let register_x = (op & 0x0f00 >> 8) as usize;
        let register_y = (op & 0x00f0 >> 4) as usize;
        let rows = (op & 0x000f) as usize;

        if rows == 0 {
            panic!("Trying to create a sprite with zero pixels.");
        }

        let pos_x = self.v_registers[register_x] as usize;
        let pos_y = self.v_registers[register_y] as usize;

        let sprite = self.ram.get_sprite(self.i_register as usize, rows);
        self.screen.draw_sprite(&sprite, (pos_x, pos_y));
    }

    fn run_op(&mut self, op: u16) {
        match op {
            0x0000 => (),
            0x00e0 => self.screen.clear(),
            0x00ee => self.return_from_subroutine(),
            0x2000..=0x2fff => self.call_subroutine(op),
            0x1000..=0x1fff => self.jump(op),
            0xb000..=0xbfff => self.jump_plus_register(op),
            0x3000..=0x3fff => self.if_register_matches_literal(op),
            0x4000..=0x4fff => self.if_register_does_not_match_literal(op),
            0x5000..=0x5fff => self.if_register_matches_register(op),
            0x9000..=0x9fff => self.if_register_does_not_match_register(op),
            0x6000..=0x6fff => self.assign_to_v_register(op),
            0xa000..=0xafff => self.assign_to_i_register(op),
            0x7000..=0x7fff => self.add_to_v_register(op),
            0x8000..=0x8fff => self.assign_from_v_register(op),
            0xd000..=0xdfff => self.draw_sprite(op),
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
