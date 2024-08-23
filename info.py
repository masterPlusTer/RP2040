import machine
import uos
import gc
import utime

# Obtener información de la memoria
def memory_info():
    return {
        'free_memory': gc.mem_free(),
        'total_memory': gc.mem_alloc() + gc.mem_free()
    }

# Obtener información de la memoria flash
def flash_info():
    return {
        'flash_size': 2048 * 1024  # Tamaño típico de flash de 2MB
    }

# Obtener información del reloj
def clock_info():
    return {
        'cpu_frequency': machine.freq()  # Frecuencia del CPU en Hz
    }

# Obtener temperatura del chip
def temperature_info():
    adc = machine.ADC(4)  # El canal de ADC 4 está conectado al sensor de temperatura interno
    raw_temp = adc.read_u16()
    temperature = 27 - (raw_temp / 65535 * 3.3 - 0.706) / 0.001721
    return {'temperature_celsius': temperature}

# Leer voltaje de entrada
def read_vsys():
    adc = machine.ADC(3)  # El canal 3 está conectado al pin Vsys
    voltage = adc.read_u16() * (3.3 / 65535) * 2  # El divisor de voltaje es 2
    return {'voltage_vsys': voltage}

# Obtener tiempo de ejecución
def uptime_info():
    return {'uptime_seconds': utime.ticks_ms() / 1000}

# Obtener información de RTC
def rtc_info():
    rtc = machine.RTC()
    datetime = rtc.datetime()
    return {
        'rtc_year': datetime[0],
        'rtc_month': datetime[1],
        'rtc_day': datetime[2],
        'rtc_hour': datetime[4],
        'rtc_minute': datetime[5],
        'rtc_second': datetime[6],
        'rtc_datetime': f"{datetime[0]}-{datetime[1]:02d}-{datetime[2]:02d} {datetime[4]:02d}:{datetime[5]:02d}:{datetime[6]:02d}"
    }

# Obtener información del firmware del chip RP2040
def rp2040_firmware_info():
    return {'rp2040_firmware': 'MicroPython v1.23.0'}

# Obtener información de la batería (si aplica)
def battery_info():
    return {'battery_level': 'No disponible'}  # Reemplaza con un sensor real si es necesario

# Obtener información de interrupciones (si aplica)
def interrupt_info():
    return {'interrupt_count': 0}  # Implementar conteo real si es necesario

# Obtener información del sistema de archivos
def filesystem_info():
    fs_info = uos.statvfs('/')
    total_size = fs_info[0] * fs_info[1]  # Tamaño total del sistema de archivos
    free_size = fs_info[0] * fs_info[3]   # Espacio libre en el sistema de archivos
    return {
        'fs_total': total_size,
        'fs_free': free_size
    }

# Obtener información del chip
def chip_info():
    return {'chip_id': 'RP2040'}

# Obtener información del estado de los pines
def pin_info():
    pins = [machine.Pin(i) for i in range(28)]  # Suponiendo que estás utilizando los 28 pines GPIO
    pin_states = {f'GPIO{i}': pin.value() for i, pin in enumerate(pins)}
    return pin_states

# Obtener el uso de almacenamiento por directorio
def storage_usage_info():
    files = uos.listdir('/')
    return {'number_of_files': len(files)}

# Obtener información adicional del RTC
def rtc_extended_info():
    rtc = machine.RTC()
    datetime = rtc.datetime()
    # Nota: el cálculo del día del año puede variar, este es un cálculo simple
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_of_year = sum(days_in_months[:datetime[1]-1]) + datetime[2]
    return {
        'rtc_weekday': datetime[3],  # Día de la semana
        'rtc_day_of_year': day_of_year  # Día del año
    }

# Obtener información general del sistema
def system_info():
    info = {
        'board': uos.uname().machine,
        'version': uos.uname().version,
        'frequency': machine.freq(),
        'memory': memory_info(),
        'flash': flash_info(),
        'temperature': temperature_info(),
        'voltage': read_vsys(),
        'uptime': uptime_info(),
        'rtc': rtc_info(),
        'rp2040_firmware': rp2040_firmware_info(),
        'battery': battery_info(),
        'interrupt': interrupt_info(),
        'filesystem': filesystem_info(),
        'chip': chip_info(),
        'pins': pin_info(),
        'storage_usage': storage_usage_info(),
        'rtc_extended': rtc_extended_info()
    }
    return info

# Imprimir información del sistema
def print_system_info_extended():
    info = system_info()
    
    print("Sistema Raspberry Pi Pico:")
    print(f"Placa: {info['board']}")
    print(f"Versión de MicroPython: {info['version']}")
    print(f"Frecuencia del CPU: {info['frequency']} Hz")
    
    print("Información de memoria:")
    print(f"Memoria libre: {info['memory']['free_memory']} bytes")
    print(f"Memoria total: {info['memory']['total_memory']} bytes")
    
    print("Información de la memoria flash:")
    print(f"Tamaño de flash: {info['flash']['flash_size']} bytes")
    
    print("Información de temperatura:")
    print(f"Temperatura: {info['temperature']['temperature_celsius']:.2f} °C")
    
    print("Voltaje de entrada:")
    print(f"Voltaje Vsys: {info['voltage']['voltage_vsys']:.2f} V")
    
    print("Tiempo de ejecución:")
    print(f"Uptime: {info['uptime']['uptime_seconds']:.2f} segundos")
    
    print("RTC:")
    print(f"Fecha y hora: {info['rtc']['rtc_datetime']}")
    print(f"Año: {info['rtc']['rtc_year']}")
    print(f"Mes: {info['rtc']['rtc_month']}")
    print(f"Día: {info['rtc']['rtc_day']}")
    print(f"Hora: {info['rtc']['rtc_hour']}")
    print(f"Minuto: {info['rtc']['rtc_minute']}")
    print(f"Segundo: {info['rtc']['rtc_second']}")
    print(f"Día de la semana: {info['rtc_extended']['rtc_weekday']}")
    print(f"Día del año: {info['rtc_extended']['rtc_day_of_year']}")
    
    print("Firmware del RP2040:")
    print(f"Firmware RP2040: {info['rp2040_firmware']}")
    
    print("Información de la batería:")
    print(f"Nivel de batería: {info['battery']['battery_level']}")
    
    print("Información de interrupciones:")
    print(f"Conteo de interrupciones: {info['interrupt']['interrupt_count']}")
    
    print("Sistema de archivos:")
    print(f"Tamaño total del FS: {info['filesystem']['fs_total']} bytes")
    print(f"Espacio libre en el FS: {info['filesystem']['fs_free']} bytes")
    
    print("Información del chip:")
    print(f"Chip ID: {info['chip']['chip_id']}")
    
    print("Información de los pines:")
    for pin, state in info['pins'].items():
        print(f"{pin}: {state}")
    
    print("Uso de almacenamiento por directorio:")
    print(f"Número de archivos: {info['storage_usage']['number_of_files']}")

# Ejecutar la impresión de información extendida del sistema
print_system_info_extended()

