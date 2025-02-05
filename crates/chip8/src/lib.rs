pub const SCREEN_HEIGHT: usize = 32;
pub const SCREEN_WIDTH: usize = 64;

const STACK_SIZE: u8 = 16;

#[derive(Debug)]
struct Stack {
    values: [u16; STACK_SIZE as usize],
    pointer: u8,
}

impl Stack {
    fn new() -> Self {
        Stack {
            values: [0; STACK_SIZE as usize],
            pointer: 0,
        }
    }

    fn push(&mut self, value: u16) {
        if self.pointer >= (STACK_SIZE - 1) {
            panic!("Trying to push to a full stack.");
        }

        self.values[self.pointer as usize] = value;
        self.pointer += 1;
    }

    fn pop(&mut self) -> u16 {
        if self.pointer <= 0 {
            panic!("Trying to push to a full stack.");
        }

        self.pointer -= 1;

        self.values[self.pointer as usize]
    }
}

#[derive(Debug)]
pub struct Chip8 {
    program_counter: u16,
    i_register: u16,
    v_registers: [u8; 16],
    ram: [u8; 4098],
    stack: Stack,
    screen: [bool; SCREEN_HEIGHT * SCREEN_WIDTH],
    sound_timer: u8,
    delay_timer: u8,
}

impl Chip8 {
    pub fn new() -> Self {
        Chip8 {
            program_counter: 512,
            i_register: 0,
            v_registers: [0; 16],
            ram: [0; 4098],
            stack: Stack::new(),
            screen: [false; SCREEN_HEIGHT * SCREEN_WIDTH],
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
