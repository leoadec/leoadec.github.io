const RAM_SIZE: usize = 4 * 1024;

#[derive(Debug)]
pub struct Ram {
    program_counter: u8,
    memory: [u8; RAM_SIZE],
}

impl Ram {
    pub fn new() -> Self {
        Ram {
            memory: [0; RAM_SIZE],
            program_counter: 0,
        }
    }

    pub fn fetch(&mut self) -> u16 {
        if (self.program_counter as usize) >= (RAM_SIZE - 1) {
            panic!("Attempt to read beyond the size of the RAM.");
        };

        let first_byte = self.memory[self.program_counter as usize] as u16;
        let second_byte = self.memory[self.program_counter as usize + 1] as u16;

        self.program_counter += 2;

        (first_byte << 8) | second_byte
    }
}
