use std::io::{stdout, Write};

use crate::sprite::{Pixel, Sprite};

pub const SCREEN_HEIGHT: usize = 32;
pub const SCREEN_WIDTH: usize = 64;

#[derive(Debug)]
pub struct Screen {
    pixels: [Pixel; SCREEN_WIDTH * SCREEN_HEIGHT],
}

impl Screen {
    pub fn new() -> Self {
        Screen {
            pixels: [Pixel(false); SCREEN_WIDTH * SCREEN_HEIGHT],
        }
    }

    pub fn clear(&mut self) {
        self.pixels = [Pixel(false); SCREEN_WIDTH * SCREEN_HEIGHT];
    }

    pub fn draw_sprite(&mut self, sprite: &Sprite, offset: (usize, usize)) {
        let height = sprite.get_height();

        for row in 0..height {
            for column in 0..8 {
                let x = (offset.0 + column) % SCREEN_WIDTH;
                let y = (offset.1 + row) % SCREEN_HEIGHT;
                self.pixels[x + y * SCREEN_WIDTH] = sprite.get_pixel(column, row);
            }
        }
    }

    pub fn print(&self) {
        let mut out = stdout();

        out.write(&[0x1b, 0x5b, 0x32, 0x4a]);
        for y in 0..SCREEN_HEIGHT {
            for x in 0..SCREEN_WIDTH {
                match self.pixels[x + SCREEN_WIDTH * y] {
                    Pixel(false) => {
                        out.write(&[0x2e]);
                    }
                    Pixel(true) => {
                        out.write(&[0x23]);
                    }
                }
            }
            stdout().write(&[0x0a]);
        }
    }
}
