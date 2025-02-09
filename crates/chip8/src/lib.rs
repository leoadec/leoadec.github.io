use std::fs::File;
use std::io::Read;
use std::str;
use std::time;

use js_sys::Uint8Array;
use rand::random;
use wasm_bindgen::prelude::*;

mod keyboard;
mod ram;
mod screen;
pub mod sprite;
mod stack;
mod timer;

use keyboard::Keyboard;
use ram::Ram;
use screen::Screen;
use stack::Stack;
use timer::{Beeper, Timer};

#[wasm_bindgen]
extern "C" {
    // Use `js_namespace` here to bind `console.log(..)` instead of just
    // `log(..)`
    #[wasm_bindgen(js_namespace = console)]
    pub fn log(s: &str);
}

#[derive(Debug)]
#[wasm_bindgen]
pub struct Chip8 {
    i_register: u16,
    v_registers: [u8; 16],
    ram: Ram,
    stack: Stack,
    screen: Screen,
    sound_timer: Timer<Beeper>,
    delay_timer: Timer<Beeper>,
    keyboard: Keyboard,
}

#[wasm_bindgen]
impl Chip8 {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Chip8 {
            i_register: 0,
            v_registers: [0; 16],
            ram: Ram::new(),
            stack: Stack::new(),
            screen: Screen::new(),
            sound_timer: Timer::<Beeper>::new(),
            delay_timer: Timer::<Beeper>::new(),
            keyboard: Keyboard::new(),
        }
    }

    #[wasm_bindgen]
    pub fn load(&mut self, data: Uint8Array) {
        self.load_original(data.to_vec());
    }

    pub fn load_original(&mut self, buffer: Vec<u8>) {
        self.ram.load(&buffer);
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
        if (0x000f & op) != 0 {
            panic!("Unrecognized operation.");
        }

        let register_1 = ((0x0f00 & op) >> 8) as usize;
        let register_2 = ((0x00f0 & op) >> 4) as usize;

        if self.v_registers[register_1] == self.v_registers[register_2] {
            self.ram.next();
        }
    }

    fn if_register_does_not_match_register(&mut self, op: u16) {
        if (0x000f & op) != 0 {
            panic!("Unrecognized operation.");
        }

        let register_1 = ((0x0f00 & op) >> 8) as usize;
        let register_2 = ((0x00f0 & op) >> 4) as usize;

        if self.v_registers[register_1] != self.v_registers[register_2] {
            self.ram.next();
        }
    }

    fn assign_to_v_register(&mut self, op: u16) {
        log("Assigning value to v regsiter.");
        let literal = 0x00ff & op as u8;
        let register_nb = ((0x0f00 & op) >> 8) as usize;
        log(&literal.to_string());
        log(&register_nb.to_string());

        self.v_registers[register_nb] = literal;
    }

    fn assign_to_i_register(&mut self, op: u16) {
        log("Assigning value to i register.");
        let literal = 0x0fff & op as u16;
        log(&literal.to_string());

        self.i_register = literal;
    }

    fn add_to_v_register(&mut self, op: u16) {
        let literal = 0x00ff & op as u8;
        let register_nb = ((0x0f00 & op) >> 8) as usize;

        self.v_registers[register_nb] = self.v_registers[register_nb].wrapping_add(literal);
    }

    fn rand(&mut self, op: u16) {
        let literal = 0x00ff & op as u8;
        let register_nb = ((0x0f00 & op) >> 8) as usize;

        let rnd: u8 = random();

        self.v_registers[register_nb] = rnd & literal;
    }

    fn draw_sprite(&mut self, op: u16) {
        let register_x = ((0x0f00 & op) >> 8) as usize;
        let register_y = ((0x00f0 & op) >> 4) as usize;
        let rows = (op & 0x000f) as usize;

        if rows == 0 {
            panic!("Trying to create a sprite with zero pixels.");
        }

        let pos_x = self.v_registers[register_x] as usize;
        let pos_y = self.v_registers[register_y] as usize;

        log("Drawing at this point:");
        log(&pos_x.to_string());
        log(&pos_y.to_string());

        let sprite = self.ram.get_sprite(self.i_register as usize, rows);
        let flipped = self.screen.draw_sprite(&sprite, (pos_x, pos_y));

        if flipped {
            self.v_registers[0xf] = 1;
        } else {
            self.v_registers[0xf] = 0;
        }
    }

    fn handle_bitwise_ops(&mut self, op: u16) {
        let trailing_nb = 0x000f & op as u8;

        let register_1 = ((0x0f00 & op) >> 8) as usize;
        let register_2 = ((0x00f0 & op) >> 4) as usize;

        let value_1 = self.v_registers[register_1];
        let value_2 = self.v_registers[register_2];

        match trailing_nb {
            0x0 => self.v_registers[register_1] = value_2,
            0x1 => self.v_registers[register_1] |= value_2,
            0x2 => self.v_registers[register_1] &= value_2,
            0x3 => self.v_registers[register_1] ^= value_2,
            0x4 => {
                let (result, of) = self.v_registers[register_1].overflowing_add(value_2);
                self.v_registers[0xf] = if of { 1 } else { 0 };
                self.v_registers[register_1] = result;
            }
            0x5 => {
                let (result, uf) = self.v_registers[register_1].overflowing_sub(value_2);
                self.v_registers[0xf] = if uf { 0 } else { 0 };
                self.v_registers[register_1] = result;
            }
            0x7 => {
                let (result, uf) = self.v_registers[register_2].overflowing_sub(value_1);
                self.v_registers[0xf] = if uf { 0 } else { 0 };
                self.v_registers[register_2] = result;
            }
            0x6 => {
                self.v_registers[0xf] = value_1 & 1;
                self.v_registers[register_1] >>= 1;
            }
            0xe => {
                self.v_registers[0xf] = (value_1 >> 7) & 1;
                self.v_registers[register_1] <<= 1;
            }
            _ => panic!("Unrecognized operation."),
        }
    }

    fn handle_key_press(&mut self, op: u16) {
        let trailing_byte = 0x00ff & op as u8;

        let invert = match trailing_byte {
            0x9e => true,
            0xa1 => false,
            _ => panic!("Unrecognized key press instruction."),
        };

        let register_nb = (0x0f00 & op) >> 8 as u8;
        let key = self.v_registers[register_nb as usize];

        let condition = self.keyboard.is_pressed(key) ^ invert;

        if condition {
            self.ram.next();
        };
    }

    fn handle_timer_ops(&mut self, op: u16) {
        let trailing_byte = 0x00ff & op as u8;

        let register_nb = ((0x0f00 & op) >> 8) as usize;
        let value = self.v_registers[register_nb];

        match trailing_byte {
            0x07 => {
                self.v_registers[register_nb] = self.delay_timer.get_countdown();
            }
            0x0a => match self.keyboard.any_key_pressed() {
                Some(key_nb) => self.v_registers[register_nb] = key_nb,
                None => self.ram.back(),
            },
            0x15 => {
                self.delay_timer
                    .set_countdown(self.v_registers[register_nb]);
            }
            0x18 => {
                self.sound_timer
                    .set_countdown(self.v_registers[register_nb]);
            }
            0x1e => {
                self.i_register = self.i_register.wrapping_add(value as u16);
            }
            0x29 => {
                self.i_register = 5 * value as u16;
            }
            0x33 => {
                self.ram
                    .write_byte(self.i_register, (value as f32 / 100.0).floor() as u8);
                self.ram.write_byte(
                    self.i_register + 1,
                    ((value as f32 / 10.0) % 10.0).floor() as u8,
                );
                self.ram.write_byte(self.i_register + 2, (value % 10) as u8);
            }
            0x55 => {
                for nb in 0..=register_nb {
                    self.ram
                        .write_byte(self.i_register + nb as u16, self.v_registers[nb]);
                }
            }
            0x65 => {
                for nb in 0..=register_nb {
                    self.i_register = self.ram.read_byte(self.i_register + nb as u16) as u16;
                }
            }
            _ => panic!("Unrecognized operation."),
        }
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
            0xc000..=0xcfff => self.rand(op),
            0xd000..=0xdfff => self.draw_sprite(op),
            0x8000..=0x8ffe => self.handle_bitwise_ops(op),
            0xe09e..=0xefa1 => self.handle_key_press(op),
            0xf007..=0xff65 => self.handle_timer_ops(op),
            _ => {
                panic!("Unrecognized operation.");
            }
        }
    }

    #[wasm_bindgen]
    pub fn tick(&mut self) {
        let op = self.ram.next();
        self.run_op(op);
    }

    #[wasm_bindgen]
    pub fn update_frame(&mut self) -> String {
        self.sound_timer.tick();
        self.delay_timer.tick();

        self.screen.print()
    }

    #[wasm_bindgen]
    pub fn run(&mut self) {
        loop {
            for _ in 0..10 {
                self.tick();
            }
            self.sound_timer.tick();
            self.delay_timer.tick();
            self.screen.print();
            self.keyboard.reset();
        }
    }
}
