import pyvisa

rm = pyvisa.ResourceManager()

# List of COM ports to try (excluding the ones you know are other devices)
# ASRL11 is your Arduino shutter, ASRL19 is your PM100
ports_to_try = ['ASRL12::INSTR', 'ASRL13::INSTR', 'ASRL14::INSTR', 
                'ASRL15::INSTR', 'ASRL16::INSTR', 'ASRL17::INSTR', 
                'ASRL18::INSTR', 'ASRL1::INSTR']

for port in ports_to_try:
    try:
        print(f"\nTrying {port}...")
        piezo = rm.open_resource(port)
        piezo.write_termination = '\r'
        piezo.read_termination = '\r'
        piezo.baud_rate = 19200
        piezo.timeout = 1000
        
        # Try to get firmware version (command from your colleague's code)
        response = piezo.query('ver')
        print(f"SUCCESS on {port}!")
        print(f"Response: {response}")
        piezo.close()
        break
    except Exception as e:
        print(f"Failed on {port}: {e}")
        try:
            piezo.close()
        except:
            pass