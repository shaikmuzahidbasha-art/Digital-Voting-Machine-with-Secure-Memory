class LcdApi:
    LCD_CLR = 0x01
    LCD_HOME = 0x02

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns