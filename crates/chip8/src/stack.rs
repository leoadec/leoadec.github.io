const STACK_SIZE: u8 = 16;

#[derive(Debug)]
pub struct Stack {
    values: [u16; STACK_SIZE as usize],
    pointer: u8,
}

impl Stack {
    pub fn new() -> Self {
        Stack {
            values: [0; STACK_SIZE as usize],
            pointer: 0,
        }
    }

    pub fn push(&mut self, value: u16) {
        if self.pointer >= (STACK_SIZE - 1) {
            panic!("Trying to push to a full stack.");
        }

        self.values[self.pointer as usize] = value;
        self.pointer += 1;
    }

    pub fn pop(&mut self) -> u16 {
        if self.pointer <= 0 {
            panic!("Trying to read from an empty stack.");
        }

        self.pointer -= 1;

        self.values[self.pointer as usize]
    }
}
