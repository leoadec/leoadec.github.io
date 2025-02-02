pub struct Chip8 {
    program_counter: u16,
    i_register: u16,
    registers: [u8; 16],
    ram: [u8; 4098],
}
