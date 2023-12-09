IfWinNotExist, LIVE Show - by NimaNzri
{
    SetWorkingDir, ComfyUI\custom_nodes\comfyui-popup_preview\window\
    IfNotExist, venv
	{
        Run, setup.bat
    }
	Else
	{
		Run, venv\Scripts\python.exe popup_window.py
	}

}
ExitApp