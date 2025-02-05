pub const SCREEN_HEIGHT: usize = 32;
pub const SCREEN_WIDTH: usize = 64;

#[derive(Debug)]
pub struct Screen {
    pixels: [bool; SCREEN_WIDTH * SCREEN_HEIGHT],
}

impl Screen {
    pub fn new() -> Self {
        Screen {
            pixels: [false; SCREEN_WIDTH * SCREEN_HEIGHT],
        }
    }
}
