import serial
import sys

# Tentukan port serial yang digunakan (ubah sesuai dengan port Anda)
arduino_port = '/dev/cu.usbserial-140'
baud_rate = 9600

# Inisialisasi komunikasi serial
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

def get_data(data_type):
    if data_type not in ['temp', 'hum']:
        raise ValueError("Invalid data type. Use 'temp' or 'hum'.")

    while True:
        try:
            # Membaca data dari serial
            serial_data = ser.readline().decode().strip()
            
            if serial_data:
                # Split data menjadi temperature dan humidity
                data_parts = serial_data.split(',')
                
                # Parse data
                temperature = float(data_parts[0].split(':')[1])
                humidity = float(data_parts[1].split(':')[1])
                
                # Mengembalikan data sesuai dengan permintaan (temp/hum)
                if data_type == 'temp':
                    return temperature
                elif data_type == 'hum':
                    return humidity
        except (IndexError, ValueError) as e:
            # Jika terjadi error parsing data, lanjutkan loop
            print(f"Error parsing data: {e}")
            continue

# Contoh penggunaan
if __name__ == "__main__":
    while True:
        command = input("Masukkan 'temp' untuk temperatur, 'hum' untuk kelembaban, atau 'exit' untuk keluar: ").strip().lower()
        
        if command in ['temp', 'hum']:
            data = get_data(command)
            print(f"{command.upper()}: {data}")
        
        elif command == 'exit':
            print("Program dihentikan.")
            ser.close()  # Menutup koneksi serial sebelum keluar
            sys.exit()   # Menghentikan program
        
        else:
            print("Input tidak valid, coba lagi.")
