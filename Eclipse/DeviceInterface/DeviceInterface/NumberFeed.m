

BeginPackage[ "DeviceInterface`NumberFeed`", {"DeviceInterface`", "JLink`"}]

NumberFunction::usage = "NumberFunction  "

NumberDevice::usage = "NumberDevice  "

NumberDeviceSetUpper::usage = "NumberDeviceSetUpper  "

NumberDeviceSetLower::usage = "NumberDeviceSetLower  " 



Begin["`Private`"]



NumberFunction[ Hold[sym_]][ obj_] :=
	Module[ {},
		If[ !ListQ[ sym], sym = {}];
		If[ Length[ sym] > 100, sym = Drop[ sym, 1]];
		sym = Append[ sym, JavaObjectToExpression[obj]];
	]



NumberDevice[] := 
	Module[ {dev, sym},
		dev = DeviceInterface[ 
			"com.wolfram.numberfeed.NumberFeed", NumberDevice];
		sym = GetDeviceInterfaceSymbol[ dev];
		DeviceInterfaceAddListener[ dev, NumberFunction[ sym]];
		dev
	]
	

NumberDeviceSetUpper[ dev_, val_]:=
	GetDeviceInterfaceObject[ dev][ setUpper[ val]]
	
NumberDeviceSetLower[ dev_, val_]:=
	GetDeviceInterfaceObject[ dev][ setLower[ val]]
	
	
End[]

EndPackage[]

