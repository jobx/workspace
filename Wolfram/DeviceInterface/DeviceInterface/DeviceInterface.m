(* Mathematica Package *)

(* Created by the Wolfram Workbench 30-Jun-2008 *)

BeginPackage["DeviceInterface`", {"JLink`"}]

DeviceInterface::usage = "DeviceInterface  "

GetDeviceInterfaceSymbol::usage = "GetDeviceInterfaceSymbol  "

GetDeviceInterfaceObject::usage = "GetDeviceInterfaceObject  "

GetDeviceInterfaceObject::usage = "GetDeviceInterfaceObject  "

DeviceInterfaceAddListener::usage = "DeviceInterfaceAddListener  "

DeviceInterfaceStart::usage = "DeviceInterfaceStart  "

DeviceInterfaceStart::usage = "DeviceInterfaceStart  "

DeviceInterfaceInitialize::usage = "DeviceInterfaceInitialize  "

DeviceInterfaceInitialize::usage = "DeviceInterfaceInitialize  "

DeviceInterfaceStop::usage = "DeviceInterfaceStop  "

DeviceInterfaceStop::usage = "DeviceInterfaceStop  "

DeviceInterfaceTerminate::usage = "DeviceInterfaceTerminate  "

DeviceInterfaceTerminate::usage = "DeviceInterfaceTerminate  "

Capture::usage = "Capture  "

DeviceInterfaceObject::usage = "DeviceInterfaceObject  "



Begin["`Private`"]
(* Implementation of the package *)



installArgs = Sequence[]

(*
installArgs = LinkConnect["jlink"]
*)

InstallJava[installArgs];

DeviceInterface[ str_, type_] :=
	Module[ {obj, sym},
		obj = JavaNew[ str];
		With[ {s = sym},
			DeviceInterfaceObject[ obj, type, Hold[s]]]
	]

GetDeviceInterfaceSymbol[ DeviceInterfaceObject[ obj_, type_, sym_]] :=
	sym
	
GetDeviceInterfaceObject[ DeviceInterfaceObject[ obj_, type_, sym_]] :=
	obj
	
DeviceInterfaceAddListener[ DeviceInterfaceObject[ obj_, type_, sym_], func_] :=
	obj@addListener[ ToString[ func, InputForm]]

DeviceInterfaceStart[ DeviceInterfaceObject[ obj_, type_, sym_]] :=
	obj@startDevice[]
	
DeviceInterfaceInitialize[ DeviceInterfaceObject[ obj_, type_, sym_]] :=
	obj@initializeDevice[]
	
DeviceInterfaceStop[ DeviceInterfaceObject[ obj_, type_, sym_]] :=
	obj@stopDevice[]
	
DeviceInterfaceTerminate[ DeviceInterfaceObject[ obj_, type_, sym_]] :=
	obj@terminateDevice[]
	
Capture[ DeviceInterfaceObject[ obj_, type_, Hold[sym_]]] :=
		sym



End[]

EndPackage[]

