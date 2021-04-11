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
                    background-color: qlineargradient(x1: 0.3, y1: 0.1, x2: 0.7, y2: 0.9,
                                                    stop: 0 #5ec7ff, stop: 1 #5e6dd2);
                                                    
                    border: 2px solid white;
                    border-radius: 5px;
                    margin-top: 1ex; /* leave space at the top for the title */
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center; /* position at the top center */
                    padding: 0 3px;
                    font: 30px;
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 1,
                                                    stop: 0 #FF0ECE, stop: 1 #FFFFFF);
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