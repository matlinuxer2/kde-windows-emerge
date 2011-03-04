; kdeglobals.nsi
;(c)2009-2011, Intevation GmbH
;Authors:
; Andre Heinecke aheinecke@intevation.de
;
; This program is free software; you can redistribute it and/or modify
; it under the terms of the GNU General Public License version 2,
; or, at your option, any later version as published by the Free
; Software Foundation
;
; This program is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
;
; You should have received a copy of the GNU General Public License
; along with this program; if not, write to the Free Software
; Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
;
;--------------------------------
; This script writes a kdeglobalsrc as the default configuration for the
; Package

    FileOpen $1 "$INSTDIR\share\config\kdeglobals" "w"
    FileWrite $1 '[Locale] $\r$\n'
    FileWrite $1 'Country=$(T_kdeglobalsCountryCode) $\r$\n'
    FileWrite $1 'Language=$(T_kdeglobalsLanguageCode) $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[General] $\r$\n'
    FileWrite $1 'font=Tahoma  $\r$\n'
    FileWrite $1 'menuFont=Tahoma $\r$\n'
    FileWrite $1 'ColorScheme=ghost $\r$\n'
    FileWrite $1 'shadeSortColumn=true $\r$\n'
    FileWrite $1 'widgetStyle=windowsvista $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[ColorEffects:Disabled] $\r$\n'
    FileWrite $1 'Color=56,56,56 $\r$\n'
    FileWrite $1 'ColorAmount=0.1 $\r$\n'
    FileWrite $1 'ColorEffect=2 $\r$\n'
    FileWrite $1 'ContrastAmount=0.65 $\r$\n'
    FileWrite $1 'ContrastEffect=1 $\r$\n'
    FileWrite $1 'IntensityAmount=0.1 $\r$\n'
    FileWrite $1 'IntensityEffect=2 $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[ColorEffects:Inactive] $\r$\n'
    FileWrite $1 'ChangeSelectionColor=true $\r$\n'
    FileWrite $1 'Color=112,111,110 $\r$\n'
    FileWrite $1 'ColorAmount=-0.9 $\r$\n'
    FileWrite $1 'ColorEffect=0 $\r$\n'
    FileWrite $1 'ContrastAmount=0.1 $\r$\n'
    FileWrite $1 'ContrastEffect=-2 $\r$\n'
    FileWrite $1 'Enable=false $\r$\n'
    FileWrite $1 'IntensityAmount=0 $\r$\n'
    FileWrite $1 'IntensityEffect=0 $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[Colors:Button] $\r$\n'
    FileWrite $1 'BackgroundAlternate=88,88,88 $\r$\n'
    FileWrite $1 'BackgroundNormal=207,204,201 $\r$\n'
    FileWrite $1 'DecorationFocus=58,167,221 $\r$\n'
    FileWrite $1 'DecorationHover=110,214,255 $\r$\n'
    FileWrite $1 'ForegroundActive=255,128,224 $\r$\n'
    FileWrite $1 'ForegroundInactive=137,136,135 $\r$\n'
    FileWrite $1 'ForegroundLink=0,87,174 $\r$\n'
    FileWrite $1 'ForegroundNegative=191,3,3 $\r$\n'
    FileWrite $1 'ForegroundNeutral=176,128,0 $\r$\n'
    FileWrite $1 'ForegroundNormal=27,25,24 $\r$\n'
    FileWrite $1 'ForegroundPositive=0,110,40 $\r$\n'
    FileWrite $1 'ForegroundVisited=100,74,155 $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[Colors:Selection] $\r$\n'
    FileWrite $1 'BackgroundAlternate=128,128,128 $\r$\n'
    FileWrite $1 'BackgroundNormal=65,139,212 $\r$\n'
    FileWrite $1 'DecorationFocus=88,88,88 $\r$\n'
    FileWrite $1 'DecorationHover=88,88,88 $\r$\n'
    FileWrite $1 'ForegroundActive=255,128,224 $\r$\n'
    FileWrite $1 'ForegroundInactive=165,193,228 $\r$\n'
    FileWrite $1 'ForegroundLink=0,49,110 $\r$\n'
    FileWrite $1 'ForegroundNegative=156,14,14 $\r$\n'
    FileWrite $1 'ForegroundNeutral=255,221,0 $\r$\n'
    FileWrite $1 'ForegroundNormal=255,255,255 $\r$\n'
    FileWrite $1 'ForegroundPositive=128,255,128 $\r$\n'
    FileWrite $1 'ForegroundVisited=69,40,134 $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[Colors:Tooltip] $\r$\n'
    FileWrite $1 'BackgroundAlternate=195,195,195 $\r$\n'
    FileWrite $1 'BackgroundNormal=48,48,48 $\r$\n'
    FileWrite $1 'DecorationFocus=58,167,221 $\r$\n'
    FileWrite $1 'DecorationHover=110,214,255 $\r$\n'
    FileWrite $1 'ForegroundActive=255,128,224 $\r$\n'
    FileWrite $1 'ForegroundInactive=137,136,135 $\r$\n'
    FileWrite $1 'ForegroundLink=0,87,174 $\r$\n'
    FileWrite $1 'ForegroundNegative=191,3,3 $\r$\n'
    FileWrite $1 'ForegroundNeutral=176,128,0 $\r$\n'
    FileWrite $1 'ForegroundNormal=255,255,255 $\r$\n'
    FileWrite $1 'ForegroundPositive=0,110,40 $\r$\n'
    FileWrite $1 'ForegroundVisited=100,74,155 $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[Colors:View] $\r$\n'
    FileWrite $1 'BackgroundAlternate=220,220,220 $\r$\n'
    FileWrite $1 'BackgroundNormal=255,255,255 $\r$\n'
    FileWrite $1 'DecorationFocus=88,88,88 $\r$\n'
    FileWrite $1 'DecorationHover=160,160,160 $\r$\n'
    FileWrite $1 'ForegroundActive=255,128,224 $\r$\n'
    FileWrite $1 'ForegroundInactive=137,136,135 $\r$\n'
    FileWrite $1 'ForegroundLink=0,87,174 $\r$\n'
    FileWrite $1 'ForegroundNegative=191,3,3 $\r$\n'
    FileWrite $1 'ForegroundNeutral=176,128,0 $\r$\n'
    FileWrite $1 'ForegroundNormal=24,22,21 $\r$\n'
    FileWrite $1 'ForegroundPositive=0,110,40 $\r$\n'
    FileWrite $1 'ForegroundVisited=100,74,155 $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[Colors:Window] $\r$\n'
    FileWrite $1 'BackgroundAlternate=195,195,195 $\r$\n'
    FileWrite $1 'BackgroundNormal=255,255,255 $\r$\n'
    FileWrite $1 'DecorationFocus=128,128,128 $\r$\n'
    FileWrite $1 'DecorationHover=88,88,88 $\r$\n'
    FileWrite $1 'ForegroundActive=255,128,224 $\r$\n'
    FileWrite $1 'ForegroundInactive=137,136,135 $\r$\n'
    FileWrite $1 'ForegroundLink=0,87,174 $\r$\n'
    FileWrite $1 'ForegroundNegative=191,3,3 $\r$\n'
    FileWrite $1 'ForegroundNeutral=176,128,0 $\r$\n'
    FileWrite $1 'ForegroundNormal=27,25,24 $\r$\n'
    FileWrite $1 'ForegroundPositive=0,110,40 $\r$\n'
    FileWrite $1 'ForegroundVisited=100,74,155 $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[General] $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[KDE] $\r$\n'
    FileWrite $1 'ShowIconsOnPushButtons=true $\r$\n'
    FileWrite $1 'contrast=6 $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[KDE-Global GUI Settings] $\r$\n'
    FileWrite $1 'GraphicEffectsLevel=6 $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[Toolbar style] $\r$\n'
    FileWrite $1 'ToolButtonStyle=TextBesideIcon $\r$\n'
    FileWrite $1 'ToolButtonStyleOtherToolbars=TextBesideIcon $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[WM] $\r$\n'
    FileWrite $1 'activeBackground=48,174,232 $\r$\n'
    FileWrite $1 'activeForeground=255,255,255 $\r$\n'
    FileWrite $1 'inactiveBackground=224,223,222 $\r$\n'
    FileWrite $1 'inactiveForeground=75,71,67 $\r$\n'

    FileClose $1