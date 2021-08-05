QCheckBoxStyle="""
                QCheckBox::indicator:unchecked {
                    image: url(img/cross.png);
                }
                QCheckBox::indicator:checked {
                    image: url(img/tick.png);
                }
                """


#QGRoupBox  rgb(67,145,228);



QGroupBoxStyle="""
QGroupBox {
    border: 1px solid gray;
    border-color: #FF17365D;
    margin-top: 27px;
    font-size: 25px;
    border-bottom-left-radius: 15px;
    border-bottom-right-radius: 15px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    padding: 5px 150px;
    background-color: #FF17365D;
    color: rgb(255, 255, 255);
}
"""

QGroupBoxStyle2="""
                QGroupBox {
                    background-color: qlineargradient(x1: 0.3, y1: 0.1, x2: 0.7, y2: 0.9,
                                                    stop: 0 #5ec7ff, stop: 1 #5e6dd2);
                                                    
                    border: 2px solid white;
                    border-radius: 5px;
                    margin-top: 1ex; /* leave space at the top for the title */
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left; 
                    padding: 0 30px;
                    font: 700px;
                    
                }
                """


# QPushButton
QPushButtonReceipt = """
    QPushButton {
        background-color: rgb(97,197,255);
        border-style: solid;
        border-width:5px;
        border-radius:60px;
        border-color: rgb(50,119,190);
        max-width:100px;
        max-height:120px;
        min-width:120px;
        min-height:120px;
        font: 60px;
    }
    """

QPushButton2 = """
QPushButton {
    border: 2px solid #8f8f91;
    border-radius: 6px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
    min-width: 80px;
}

QPushButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);
}
"""

#круглая
QPushButton3 = """
background-color: white;
 border-style: solid;
 border-width:1px;
 border-radius:50px;
 border-color: red;
 max-width:100px;
 max-height:100px;
 min-width:100px;
 min-height:100px;
 """


#-------------------------------------------------
BACKGROUND_COLOR = (70,140,226)  # голубой фон
TimerInnerBackGround = (232,250,128) # желтый фон на таймере
DefaultBackgroundColor = f"background-color: rgbBACKGROUND_COLOR;".replace('BACKGROUND_COLOR',str(BACKGROUND_COLOR))
DefaultFontStyle="""
    font-family: "Times";
    font-size: 27pt;
"""


QComboBoxReceipt="""
QComboBox QAbstractItemView {
  border: 1px solid grey;
  background: white;
  selection-background-color: blue;
}
QComboBox {
  background: rgb(97,197,255);
  DefaultFontStyle
}
""".replace('DefaultFontStyle',DefaultFontStyle)

QCheckBoxStyle2="""
QCheckBox {
    spacing: 10px;
    min-height: 80px; 
    DefaultFontStyle
}
QCheckBox::indicator {
    width: 30px;
    height: 30px;
}
""".replace('DefaultFontStyle',DefaultFontStyle)


HeaderStyle="""
QLabel {
    qproperty-alignment: AlignCenter;
	border: 1px solid #FF17365D;
	border-top-left-radius: 15px;
	border-top-right-radius: 15px;
	background-color: #FF17365D;
	padding: 5px 10px;
	color: rgb(255, 255, 255);
	max-height: 33px;    
    font-size: 21pt;
}
"""

BodyStyle="""
QFrame {
	border: 1px solid #FF17365D;
	border-bottom-left-radius: 15px;
	border-bottom-right-radius: 15px;
    DefaultBackgroundColor
}
""".replace('DefaultBackgroundColor',DefaultBackgroundColor)

QLabelStyle="""
QLabel {
	border: 1px solid #FF17365D;
	border-bottom-right-radius: 20px;
    border-bottom-left-radius: 0px;
    background-color: rgb(1, 255, 255);
    DefaultFontStyle
}
""".replace('DefaultFontStyle',DefaultFontStyle)

QLabelStyle2="""
QLabel {
	border: 1px solid #FF17365D;
    border-bottom-right-radius: 0px;
    border-bottom-left-radius: 0px;
    background-color: rgb(185, 200, 237);
    DefaultFontStyle
}
""".replace('DefaultFontStyle',DefaultFontStyle)

QLabelStyle3="""
QLabel#Label {
    font-family: "Times";
    font-size: 22pt;
    font-weight:bold;
    border: none;
}
"""

QLineEditStyle="""
QLineEdit {
	border: 1px solid #FF17365D;
	border-bottom-right-radius: 20px;
    background-color: rgb(135, 250, 211);
    DefaultFontStyle
}
""".replace('DefaultFontStyle',DefaultFontStyle)

QVoltageStyle="""
QLineEdit {
	border: 1px solid #FF17365D;
	border-bottom-right-radius: 20px;
    border-bottom-left-radius: 20px;
    background-color: rgb(135, 250, 211);
    max-width: 200px;
    DefaultFontStyle
}
""".replace('DefaultFontStyle',DefaultFontStyle)

QVoltageSlider = """
QSlider {
    min-height: 100px;
    max-height: 100px;
    
}
QSlider::groove:horizontal {
    background-color: rgb(135, 250, 211);
	border: 0px solid #424242; 
	height: 15px; 
	border-radius: 7px;
    
}

QSlider::handle:horizontal {
    background-color: red; 
	border: 2px solid red; 
    width: 80px; 
	height: 100px; 
	line-height: 100px; 
	margin-top: -40px; 
	margin-bottom: -40px; 
	border-radius: 40px; 
}
QSlider::handle:horizontal:hover { 
	border-radius: 40px;
}

"""


SwitchButtonStyle="""
QPushButton {
	border: 1px solid #FF17365D;
	border-bottom-right-radius: 20px;
    
    DefaultFontStyle
}
""".replace('DefaultFontStyle',DefaultFontStyle)

ButtonStartStyle="""
QPushButton#StartTestButton
{
    background-color: rgb(165,229,174);
    
    border-style: outset;
    border-width: 1px;
    border-radius: 30px;
    border-color: beige;
    font-family: "Times";
    font-size: 75pt;
}
"""
ButtonStopStyle="""
QPushButton#StartTestButton
{
    background-color: rgb(255,60,91);
    border-style: outset;
    border-width: 1px;
    border-radius: 30px;
    border-color: beige;
    font-family: "Times";
    font-size: 75pt;
}
"""
MenuButtonStyle="""
QPushButton
{
    background-color: rgb(173,173,174);   
    border-style: outset;
    border-width: 5px;
    border-radius: 10px;
    border-color: beige;
    font-family: "Times";
    font-size: 30pt;
    min-width: 300px;
}
"""

# Setup Dialog Styles (SDS_)>>
SDS_DefaultFontStyle="""
    font-family: "Times";
    font-size: 25pt;
"""
SDS_Button="""
QPushButton
{
    border-width: 5px;
    font-family: "Times";
    font-size: 30pt;
    min-width: 300px;
}
"""

SDS_GroupBox="""
QGroupBox
{
    SDS_DefaultFontStyle
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 5 5px;
    
}
""".replace('SDS_DefaultFontStyle',SDS_DefaultFontStyle)

SDS_LineEdit="""
QLineEdit
{
	border: 1px solid #FF17365D;
    max-width: 400px;
    border-width: 5px;
    border-color: palette(window);
    SDS_DefaultFontStyle
}
""".replace('SDS_DefaultFontStyle',SDS_DefaultFontStyle)

SDS_Label="""
QLabel
{
    SDS_DefaultFontStyle
}
""".replace('SDS_DefaultFontStyle',SDS_DefaultFontStyle)

SDS_ListView="""
QListView
{
    SDS_DefaultFontStyle
}
""".replace('SDS_DefaultFontStyle',SDS_DefaultFontStyle)

SDS_CheckBox="""
QCheckBox::indicator {
    width: 50px;
    height: 50px;
    
}
"""
# Setup Dialog Styles (SDS_)<<

# Service Dialog Styles (SVC_) >>
SVC_Button="""
QPushButton
{
    border-width: 5px;
    font-family: "Times";
    font-size: 30pt;
    min-width: 300px;
    DefaultBackgroundColor
}
""".replace('DefaultBackgroundColor',DefaultBackgroundColor)
# Service Dialog Styles (SVC_) <<


# Virtual keyboard >>
VK_Button="""
QPushButton
{
    DefaultFontStyle   
}
""".replace('DefaultFontStyle',DefaultFontStyle)
# Virtual keyboard <<

# Test Result >>
#https://doc.qt.io/archives/qt-4.8/stylesheet-examples.html#customizing-qscrollbar
TR_Vertical = """
QScrollBar:vertical {
     border: 2px;
     width: 120px;
     margin: 0px 0 160px 0;
     
 }
 QScrollBar::handle:vertical {
     min-width: 20px;     
 }
 QScrollBar::add-line:vertical {
    height: 75px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
    border: 2px solid gray;
    
    
 }

 QScrollBar::sub-line:vertical {
    height: 75px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
    border: 2px solid gray;
    position: absolute;
    bottom: 80px;
    
    
     
 }
 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
     width: 15px;
    height: 15px;
    background: pink;
 }

 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
     
 }
"""

TR_Horizontal = """
QScrollBar:horizontal {
    
    border: 2px;    
    height: 100px;
    margin: 0px 80px 0px 80px;
    
}

QScrollBar::handle:horizontal {
    
    min-width: 20px;
    
}

QScrollBar::add-line:horizontal {
    
    width: 75px;
    subcontrol-position: right;
    subcontrol-origin: margin;
    border: 2px solid gray;
    
    
}

QScrollBar::sub-line:horizontal {   
    width: 75px;
    subcontrol-position: left;
    subcontrol-origin: margin;
    border: 2px solid gray;

      
}

QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
    width: 15px;
    height: 15px;
    background: pink;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    
}
"""



# Test Result <<

