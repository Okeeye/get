import smbus
import time

class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        try:
            data = self.bus.read_word_data(self.address, 0)
            lower_data_byte = data >> 8
            upper_data_byte = data & 0xFF
            number = (upper_data_byte << 6) | (lower_data_byte >> 2)
            
            if self.verbose:
                print(f"Принятые данные: {data}, Старший байт: {upper_data_byte:x}, Младший байт: {lower_data_byte:x}, Число: {number}")
            
            return number
        except Exception as e:
            print(f"Ошибка I2C: {e}")
            return 0

    def get_voltage(self):
        # MCP3021 — 10-битный АЦП (0..1023)
        number = self.get_number()
        voltage = (number / 1023.0) * self.dynamic_range
        return voltage

if __name__ == "__main__":
    adc = None
    try:
        # Укажите здесь напряжение, измеренное мультиметром (например, 5.0 или 3.3)
        adc = MCP3021(dynamic_range=5.0) 
        
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.2f} В")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nИзмерения остановлены пользователем")
        
    finally:
        if adc:
            adc.deinit()
        print("Шина I2C освобождена")