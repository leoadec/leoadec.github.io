pub trait TimedAction {
    fn execute(&self);
}

#[derive(Debug)]
pub struct Beeper;

impl TimedAction for Beeper {
    fn execute(&self) {
        println!("BEEP!");
    }
}

#[derive(Debug)]
pub struct Timer<T: TimedAction> {
    countdown: u8,
    timed_action: T,
}

impl Timer<Beeper> {
    pub fn new() -> Self {
        Timer::<Beeper> {
            countdown: 0,
            timed_action: Beeper {},
        }
    }
}

impl<T: TimedAction> Timer<T> {
    pub fn tick(&mut self) {
        if self.countdown == 1 {
            self.timed_action.execute();
        }

        if self.countdown > 0 {
            self.countdown -= 1;
        };
    }

    pub fn set_countdown(&mut self, value: u8) {
        self.countdown = value;
    }

    pub fn get_countdown(&self) -> u8 {
        self.countdown
    }
}
