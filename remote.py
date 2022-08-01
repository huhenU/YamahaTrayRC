import requests
import configparser
from infi.systray import SysTrayIcon

config = configparser.ConfigParser()
config.read('config.ini')

standby = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><System><Power_Control><Power>Standby</Power></Power_Control></System></YAMAHA_AV>'
wakeup = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><System><Power_Control><Power>On</Power></Power_Control></System></YAMAHA_AV>'

togglemute = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Mute>On/Off</Mute></Volume></Main_Zone></YAMAHA_AV>'
volpreset1 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Lvl><Val>' + config['PRESETS']['volpreset1'] + '</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume></Main_Zone></YAMAHA_AV>'
volpreset2 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Lvl><Val>' + config['PRESETS']['volpreset2'] + '</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume></Main_Zone></YAMAHA_AV>'
volpreset3 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Lvl><Val>' + config['PRESETS']['volpreset3'] + '</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume></Main_Zone></YAMAHA_AV>'
volpreset4 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Lvl><Val>' + config['PRESETS']['volpreset4'] + '</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume></Main_Zone></YAMAHA_AV>'


netradio = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Input><Input_Sel>' + config['PRESETS']['inpreset1'] + '</Input_Sel></Input></Main_Zone></YAMAHA_AV>'
EQ = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Input><Input_Sel>' + config['PRESETS']['inpreset2'] + '</Input_Sel></Input></Main_Zone></YAMAHA_AV>'
inpreset3 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Input><Input_Sel>' + config['PRESETS']['inpreset3'] + '</Input_Sel></Input></Main_Zone></YAMAHA_AV>'
inpreset4 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Input><Input_Sel>' + config['PRESETS']['inpreset4'] + '</Input_Sel></Input></Main_Zone></YAMAHA_AV>'

sleep0 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>Off</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'
sleep30 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>30 min</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'
sleep60 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>60 min</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'
sleep90 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>90 min</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'
sleep120 = '<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>120 min</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'


def trayAction(action):

    if action == 'wakeup':
        with requests.Session() as session:
            r = session.post('http://' + config['INFO']['ip'] + '/YamahaRemoteControl/ctrl', data='<?xml version="1.0" encoding="utf-8"?><YAMAHA_AV cmd="GET"><System><Power_Control><Power>GetParam</Power></Power_Control></System></YAMAHA_AV>', headers={"Content-Type": "application/json; charset=UTF-8"})
            if(r.text) == '<YAMAHA_AV rsp="GET" RC="0"><System><Power_Control><Power>Standby</Power></Power_Control></System></YAMAHA_AV>':
                r = session.post('http://' + config['INFO']['IP'] + '/YamahaRemoteControl/ctrl', data=wakeup,
                                 headers={"Content-Type": "application/json; charset=UTF-8"})
            else:
                r = session.post('http://' + config['INFO']['IP'] + '/YamahaRemoteControl/ctrl', data=standby,
                                 headers={"Content-Type": "application/json; charset=UTF-8"})


    with requests.Session() as session:
        r = session.post('http://' + config['INFO']['IP'] + '/YamahaRemoteControl/ctrl', data=action,
                         headers={"Content-Type": "application/json; charset=UTF-8"})


menu_options = (("Power", None, lambda x: trayAction('wakeup')),

               ("Toggle Mute", None, lambda x: trayAction(togglemute)),
               ("Output Volume", None, ((config['PRESETS']['volpreset1'][:3] +'dB', None, lambda x: trayAction(volpreset1)),
                                        (config['PRESETS']['volpreset2'][:3] +'dB', None, lambda x: trayAction(volpreset2)),
                                        (config['PRESETS']['volpreset3'][:3] +'dB', None, lambda x: trayAction(volpreset3)),
                                        (config['PRESETS']['volpreset4'][:3] +'dB', None, lambda x: trayAction(volpreset4)),
                                       )),

               ("Select Input", None, ((config['PRESETS']['inpreset1'], None, lambda x: trayAction(netradio)),
                                        (config['PRESETS']['inpreset2'], None, lambda x: trayAction(EQ)),
                                        (config['PRESETS']['inpreset3'], None, lambda x: trayAction(inpreset3)),
                                        (config['PRESETS']['inpreset4'], None, lambda x: trayAction(inpreset4)),
                                       )),

               ("Sleep Timer", None, (('Off', None, lambda x: trayAction(sleep0)),
                                      ('30 min', None, lambda x: trayAction(sleep30)),
                                      ('60 min', None, lambda x: trayAction(sleep60)),
                                      ('90 min', None, lambda x: trayAction(sleep90)),
                                      ('120 min', None, lambda x: trayAction(sleep120)),
                                      )))

systray = SysTrayIcon("icon.ico", "AV Controller", menu_options)
systray.start()
