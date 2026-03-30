// Keypad pin mapper - tests which two physical pins short when a key is pressed.
// Wiring: set pins[] to the 8 GPIOs you currently have connected to the keypad connector
// (order doesn't matter — we treat them as connector pin 1..8).
// Run, then press ONE key (e.g. A) and watch serial output.

const int pins[] = {32, 33, 25, 26, 27, 14, 23, 22}; // <- update if your 8 wires differ
const int N = sizeof(pins)/sizeof(pins[0]);
unsigned long cycleDelay = 250;

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("\n=== Keypad pin mapper ===");
  Serial.print("Pins: ");
  for (int i=0;i<N;i++) { Serial.print(i+1); Serial.print(":"); Serial.print(pins[i]); Serial.print("  "); }
  Serial.println("\nPress ONE key (e.g. A) and hold it while mapper runs.");
  Serial.println("It will drive each pin LOW in turn and read the others.");
  delay(800);
}

void loop() {
  for (int drive = 0; drive < N; drive++) {
    // set drive pin OUTPUT LOW
    for (int i=0;i<N;i++) pinMode(pins[i], INPUT_PULLUP);
    pinMode(pins[drive], OUTPUT);
    digitalWrite(pins[drive], LOW);
    delay(20);
    // read all pins
    String line = "Drive(" + String(drive+1) + ":" + String(pins[drive]) + ") -> ";
    bool foundAny = false;
    for (int j=0;j<N;j++) {
      int v = digitalRead(pins[j]); // will be 0 if connected to driven low
      line += String(pins[j]) + ":" + String(v) + " ";
      if (j != drive && v == 0) foundAny = true;
    }
    Serial.println(line);
    // If a press bridges two pins you should see another pin read 0 while drive pin is 0.
    delay(cycleDelay);
    // release drive pin
    pinMode(pins[drive], INPUT_PULLUP);
    delay(20);
  }
  Serial.println("--- cycle done. Keep pressing the key while mapper runs ---\n");
  delay(300);
}
