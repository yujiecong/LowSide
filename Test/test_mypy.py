from Source.Common.Func import OS, Shutil

OS.system(r"stubgen C:\repo\_USDQ\LowSide\Source --output C:\repo\_USDQ\LowSide\out --include-private ")
Shutil.rmtree(r"C:\repo\_USDQ\venv310\Lib\site-packages\Source")
Shutil.move(r"C:\repo\_USDQ\LowSide\out\LowSide\Source",r"C:\repo\_USDQ\venv310\Lib\site-packages\Source")