pub const SCREEN_HEIGHT: usize = 32;
pub const SCREEN_WIDTH: usize = 64;

#[derive(Debug)]
pub struct Chip8 {
    program_counter: u16,
    i_register: u16,
    v_registers: [u8; 16],
    ram: [u8; 4098],
    stack_pointer: u8,
    stack: [u16; 16],
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
            stack_pointer: 0,
            stack: [0; 16],
            screen: [false; SCREEN_HEIGHT * SCREEN_WIDTH],
            sound_timer: 0,
            delay_timer: 0,
        }
    }
}
