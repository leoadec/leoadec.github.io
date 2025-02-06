#[derive(Clone, Copy, Debug)]
pub struct Pixel(pub bool);

pub struct Sprite {
    pixels: Vec<Pixel>,
    height: u8,
}

impl Sprite {
    pub fn from_bytes(bytes: &[u8]) -> Self {
        let height = bytes.len();
        let mut pixels: Vec<Pixel> = Vec::with_capacity(8 * height);
        for row in 0..height {
            let mut byte = bytes[row];
            for column in 0..8 {
                pixels[row * 8 + column] = match byte & 1 {
                    0 => Pixel(false),
                    1 => Pixel(true),
                    _ => panic!("Unreachable code."),
                };
                byte = byte >> 1;
            }
        };
        Sprite{ pixels: pixels, height: height as u8 }
    }
}
