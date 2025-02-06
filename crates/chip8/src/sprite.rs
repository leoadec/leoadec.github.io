#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Pixel(pub bool);

#[derive(Debug)]
pub struct Sprite {
    pixels: Vec<Pixel>,
    height: u8,
}

impl Sprite {
    pub fn from_bytes(bytes: &[u8]) -> Self {
        let height = bytes.len();
        let mut pixels: Vec<Pixel> = Vec::new();
        for row in 0..height {
            let byte = bytes[row];
            for column in 0..8 {
                let pixel = match (byte >> column) & 1 {
                    0 => Pixel(false),
                    1 => Pixel(true),
                    _ => panic!("Unreachable code."),
                };
                pixels.push(pixel);
            }
        }
        Sprite {
            pixels: pixels,
            height: height as u8,
        }
    }

    pub fn get_pixel(&self, x: usize, y: usize) -> Pixel {
        let pos = x + 8 * y;

        if pos >= 8 * self.height as usize {
            panic!("Attempting to read beyond the size of the Sprite.");
        };

        self.pixels[pos]
    }

    pub fn get_height(&self) -> usize {
        self.height as usize
    }
}
