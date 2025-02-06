#[derive(Clone, Copy, Debug)]
pub struct Pixel(pub bool);

pub struct Sprite {
    pixels: Vec<Pixel>,
    height: u8,
}

impl Sprite {
    pub fn from_bytes(bytes: &[u8]) {
        let mut pixels: Vec<Pixel> = Vec::with_capacity(8 * bytes.len());
        for row in 0..bytes.len() {
            let mut byte = bytes[row];
            for column in 0..8 {
                pixels[row * 8 + column] = match byte & 1 {
                    0 => Pixel(false),
                    1 => Pixel(true),
                    _ => panic!("Unreachable code."),
                };
                byte = byte >> 1;
            }
        }
    }
}
