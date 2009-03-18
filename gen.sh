#!/bin/sh

PYUIC=`which pyuic4`

if [ ! -x "$PYUIC" ]; then 
	PYUIC="/opt/local/Library/Frameworks/Python.framework/Versions/2.5/bin/pyuic4";	
fi
	
$PYUIC MainWindow.ui > Ui_MainWindow.py