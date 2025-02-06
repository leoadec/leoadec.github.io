const RAM_SIZE: usize = 4 * 1024;

#[derive(Debug)]
pub struct Ram {
    memory: [u8; RAM_SIZE],
}

impl Ram {
    pub fn new() -> Self {
        Ram {
            memory: [0; RAM_SIZE],
        }
    }
}
