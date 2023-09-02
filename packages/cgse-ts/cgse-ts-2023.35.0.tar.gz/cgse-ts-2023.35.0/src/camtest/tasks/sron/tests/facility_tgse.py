from pathlib import Path
from time                                   import time, sleep

from egse.state                             import GlobalState
from egse.hk                                import get_housekeeping
from egse.system                            import EPOCH_1958_1970

from camtest import execute
from camtest import building_block

from gui_executor.exec import exec_ui

UI_MODULE_DISPLAY_NAME = "9 — Facility TGSE"

ICON_PATH = Path(__file__).parent.parent.resolve() / "icons"

PREFIXES = ["GSRON_AG34972_0_T", "GSRON_AG34972_1_T", "GSRON_AG34970_0_T", "GSRON_AG34970_1_T"]



@exec_ui(display_name="TGSE Find PT1000s",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def tgse_sensor_check():

    execute(sron_tgse_sensor_check,
            description="Validating all facility temperature sensors")

@exec_ui(display_name="TGSE Find PT1000 Heater pairs",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def tgse_sensor_heater_check():
    
    execute(sron_tgse_sensor_heater_check,
            description="Validating all facility temperature sensor and heater pairs")

@exec_ui(display_name="TGSE Check PID control loops",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def tgse_pid_check():
    
    execute(sron_tgse_pid_check,
            description="Validating all facility PID control loop")

class pt1000_heater:
    def __init__(self, htr_idx, htr_chnl, daq, daq_chnl):
        self.htr_idx    = htr_idx
        self.htr_chnl   = htr_chnl
        self.daq        = daq
        self.daq_chnl   = daq_chnl
        self.correct    = False
   
@building_block
def sron_tgse_sensor_check():

    # Retrieve list op DAQs and Channels from setup
    setup = GlobalState.load_setup()
    
    ag34972_0_setup = setup.gse.agilent34972_0
    ag34972_1_setup = setup.gse.agilent34972_1
    ag34970_1_setup = setup.gse.agilent34970_1
    
    ag34972_0_channels = ag34972_0_setup.two_wire + ag34972_0_setup.four_wire + ag34972_0_setup.thermocouples
    ag34972_1_channels = ag34972_1_setup.two_wire + ag34972_1_setup.four_wire + ag34972_1_setup.thermocouples
    ag34970_1_channels = ag34970_1_setup.two_wire + ag34970_1_setup.four_wire + ag34970_1_setup.thermocouples
    
    error = {}
    
    AG34972_0_PATH = "GSRON_AG34972_0_T"
    AG34972_1_PATH = "GSRON_AG34972_1_T"
    AG34970_1_PATH = "GSRON_AG34970_1_T"
    
    
    # Retrieve Latest HK value for all of these channels   
    for channel in ag34972_0_channels:
        try:
            timestamp, value = get_housekeeping(AG34972_0_PATH + f"{channel}")
            
            # Make sure they are not too old
            if time() - (timestamp - EPOCH_1958_1970) > 60:
                error[AG34972_0_PATH + f"{channel}"] = value
                continue

            # Is value within range 45 - -180
            if not -180 <= float(value) <= 45:
                error[AG34972_0_PATH + f"{channel}"] = value
        except Exception as ex:
            print(f"Skipping AG34972 0 Channel {channel}: {ex}")
        
        
        
    for channel in ag34972_1_channels:
        try:
            timestamp, value = get_housekeeping(AG34972_1_PATH + f"{channel}")
            
            if time() - (timestamp - EPOCH_1958_1970) > 60:
                error[AG34972_1_PATH + f"{channel}"] = value
                continue
            
            if not -180 <= float(value) <= 45:
                error[AG34972_1_PATH + f"{channel}"] = value 
        except Exception as ex:
            print(f"Skipping AG34972 1 Channel {channel}: {ex}")
        
    for channel in ag34970_1_channels:
        try:
            timestamp, value = get_housekeeping(AG34970_1_PATH + f"{channel}")
            
            if time() - (timestamp - EPOCH_1958_1970) > 60:
                error[AG34970_1_PATH + f"{channel}"] = value
                continue
            
            if not -180 <= float(value) <= 45:
                error[AG34970_1_PATH + f"{channel}"] = value 
        except Exception as ex:
            print(f"Skipping AG34972 0 Channel {channel}: {ex}")
            
            
    # Return all channels that do not have values within the given range and their values
    for metric, value in error.items():
        print(f"HK Metric: {metric}, Value: {value}")

@building_block
def sron_tgse_sensor_heater_check():
    try:
        heaters = GlobalState.setup.gse.beaglebone_heater.device
    except:
        raise Exception("Could not connect to proxy")
    
    def roc_housekeeping(daq, daq_chnl):
        try:
            timestamp, values = get_housekeeping(hk_name=PREFIXES[daq] + f"{daq_chnl}", time_window=30)
        except Exception as ex:
            print(f"Could not find HK: {ex}")
            raise ex
        
        deltaY = float(values[-1]) - float(values[0])
        deltaX = float(timestamp[-1]) - float(timestamp[0])
        roc    = deltaY / deltaX

        if time() - (float(timestamp[-1]) - EPOCH_1958_1970) > 60:
            raise Exception("Data too old")

        return float(roc)
    
    # Retrieve heater configuration from setup
    setup = GlobalState.load_setup()
    heater_config = setup.gse.spid.configuration.heaters
    
    pt1000_heater_list = []
    
    # Generate a list of all pairs based with heaters in ascending order
    for name, configurations in heater_config.items():
        
        for config in configurations:
            pt1000_heater_list.append(pt1000_heater(config[3], config[4], config[1], config[2]))

    pt1000_heater_list.sort(key=lambda x: x.htr_idx)

    
    print("Starting evaluation loop....")
    for pair in pt1000_heater_list:
        try:
            correct = True
            print(f"Turning on Heater {pair.htr_idx + 1} {chr(65+pair.htr_chnl)}")
            heaters.set_duty_cycle(pair.htr_idx, pair.htr_chnl, 5000)
            heaters.set_enable(pair.htr_idx, pair.htr_chnl, True)
            
            start_time = time()
            
            print(f"Current RoC: {roc_housekeeping(pair.daq, pair.daq_chnl)}")
            
            print(f"Waiting for a change on: {PREFIXES[pair.daq]}{pair.daq_chnl}")
            
            while not roc_housekeeping(pair.daq, pair.daq_chnl) > 0.0001:
                print(f"Current RoC: {roc_housekeeping(pair.daq, pair.daq_chnl)}, time left: {60 - (time() - start_time)}", end='\r')
                if time() - start_time > 60:
                    print("No change detected on {PREFIXES[pair.daq]}{pair.daq_chnl}")
                    correct = False
                    break
                sleep(1)
            
            print(f"Heater pair is {correct}")
            
            pair.correct = correct

        except Exception as ex:
            print(f"Skipped PID channel : {ex}")
        finally:
            print(f"Turning off Heater {pair.htr_idx + 1} {chr(65+pair.htr_chnl)}")
            heaters.set_enable(pair.htr_idx, pair.htr_chnl, False)
    
    for pair in pt1000_heater_list:
        print(f"Heater {pair.htr_idx + 1} {chr(65+pair.htr_chnl)}, {PREFIXES[pair.daq]}{pair.daq_chnl} {pair.correct}")

@building_block        
def sron_tgse_pid_check():
    
    pid = GlobalState.setup.gse.spid.device
    
    setup    = GlobalState.load_setup()
    heaters  = setup.gse.spid.configuration.heaters
    
    pid_list = {}
    
    for name, configurations in heaters.items():
        pid_list[name] = []
        for config in configurations:
            pid_list[name].append(config)
    
    correct = {}

    # Turn on PID to 25C
    for name, config in pid_list.items():
        for parameter in config:
            pid.set_temperature(parameter[0], 25)
            pid.enable(True)
            start_time = time()
        
            print(f"Turning on heater {parameter[3]} channel {parameter[4]} to test PID loop {parameter[0]} on PT1000 {PREFIXES[parameter[1]]}{parameter[2]}")
            
            while True:
                timestamp, value = get_housekeeping(f"{PREFIXES[parameter[1]]}{parameter[2]}")
            
                if float(value) >= 24.9:
                    print(f"PID channel {parameter[0]}: Correct")
                    correct[parameter[0]] = True
                    break
                elif (time() - start_time) > 300:
                    print(f"PID channel {parameter[0]}: Timeout, check if correct")
                    correct[parameter[0]] = False
                    break
                
                sleep(10)
                    
            print(f"Turning off heater {parameter[3]} channel {parameter[4]} from test PID loop {parameter[0]} on PT1000 {PREFIXES[parameter[1]]}{parameter[2]}")
            pid.set_temperature(parameter[0], 0)
            pid.enable(False)
            
    for idx, item in enumerate(correct):
        print(f"PID channel {idx} is: {'Correct' if item else 'Incorrect'}")