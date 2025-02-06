const RAM_SIZE: usize = 4 * 1024;
const FIRST_INSTRUCTION: u16 = 512;

#[derive(Debug)]
pub struct Ram {
    program_counter: u16,
    memory: [u8; RAM_SIZE],
}

impl Ram {
    pub fn new() -> Self {
        Ram {
            memory: [0; RAM_SIZE],
            program_counter: FIRST_INSTRUCTION,
        }
    }

    pub fn goto(&mut self, position: u16) {
        self.program_counter = position;
    }

    pub fn get_current_counter(&self) -> u16 {
        self.program_counter
    }

    pub fn load(&mut self, buffer: &[u8]) {
        let last_instruction = FIRST_INSTRUCTION as usize + buffer.len();

        if last_instruction > RAM_SIZE {
            panic!("Program size is too long.");
        };

        self.memory[FIRST_INSTRUCTION as usize..last_instruction].copy_from_slice(buffer);
    }

    pub fn next(&mut self) -> u16 {
        if (self.program_counter as usize) >= (RAM_SIZE - 1) {
            panic!("Attempt to read beyond the size of the RAM.");
        };

        let first_byte = self.memory[self.program_counter as usize] as u16;
        let second_byte = self.memory[self.program_counter as usize + 1] as u16;

        self.program_counter += 2;

        dbg!(self.program_counter, first_byte, second_byte);

        (first_byte << 8) | second_byte
    }
}
