#[derive(Debug)]
pub struct Keyboard {
    keys: [bool; 16],
}

impl Keyboard {
    pub fn new() -> Self {
        Keyboard { keys: [false; 16] }
    }

    pub fn reset(&mut self) {
        for nb in 0x0..0xf {
            self.keys[nb] = false;
        }

        self.keys[0xf] = true;
    }

    pub fn update_key(&mut self, key_nb: u8, status: bool) {
        if key_nb > 0xf {
            panic!("Attempting to read key out of range.");
        };

        self.keys[key_nb as usize] = status;
    }

    pub fn is_pressed(&self, key_nb: u8) -> bool {
        if key_nb > 0xf {
            panic!("Attempting to read key out of range.");
        };

        self.keys[key_nb as usize]
    }

    pub fn any_key_pressed(&self) -> Option<u8> {
        for key_nb in 0x0..0xf {
            if self.keys[key_nb] {
                return Some(key_nb as u8);
            }
        }
        return None;
    }
}
