A lightweight QGIS plugin for detecting parcel-level spatial continuity across historical land-use maps.

Landuse Continuity is a tool compares polygon geometries from different time periods and identifies parcels that remain geometrically persistent based on an adjustable area-overlap threshold. This plugin was developed as part of a methodological exploration for historical urban infrastructure and urban health research, supporting diachronic spatial analysis of urban form.

🔴Video demo:https://www.youtube.com/watch?v=3ipKnXsKCno
🔴Installation (prototype / local use) Copy the plugin folder into your QGIS plugins directory (e.g. on Windows): C:\Users<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\grain_checker 1)Restart QGIS. 2)Enable the plugin in Plugins → Manage and Install Plugins. 3)Run Grain Checker from the toolbar/menu.

🔵What it accepts: 2 Historical landuse polygon layers

🔵Returns: True or False in the countinuity of landuse

🔵Workflow:
1)Geometry-based comparison between polygon layers
2)Adjustable continuity threshold (area overlap ratio)
3)Automatic generation of continuity attributes
4)Lightweight interface integrated into QGIS
5)Works without relying on attribute consistency between datasets
