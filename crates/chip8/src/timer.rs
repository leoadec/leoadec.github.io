#[derive(Debug)]
pub struct Timer {
    countdown: u8,
}

impl Timer {
    pub fn new() -> Self {
        Timer { countdown: 0 }
    }

    pub fn tick(&mut self) {
        if self.countdown > 0 {
            self.countdown -= 1;
        };
    }
}
