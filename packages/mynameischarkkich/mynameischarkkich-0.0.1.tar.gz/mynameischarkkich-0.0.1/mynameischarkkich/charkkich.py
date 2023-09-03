class Charkkich :
    """
    คลาส Charkkich เป็นข้อมูลที่เกี่ยวข้องกับ Charkkich
    ประกอบด้วย ชื่อฉัน
    งานอดิเรกของฉัน

    Example
    ------------------------
    charkkich = Charkkich()
    charkkich.show_name()
    charkkich.show_hobby()
    charkkich.about()
    charkkich.show_art()
    ------------------------
    """
    def __init__(self):
        self.name = "Charkkich"
        self.hobby = "Learn Python"

    def show_name(self):
        print(f"สวัสดี ฉันชื่อ {self.name}")

    def show_hobby(self):
        print(f"งานอดิเรกของฉันคือ {self.hobby}")

    def about(self):
        text = """
        ----------------------------------------------------------------
        สวัสดี ฉันชื่อ 'charkkich' ฉันอยากเรียนรู้เกี่ยวกับสิ่งใหม่ๆ อยากเขียนโปรแกรมเก่งๆ
        ----------------------------------------------------------------"""
        print(text)

    def show_art(self):
        text = """
                                ______                     
        _________        .---"""      """---.              
        :______.-':      :  .--------------.  :             
        | ______  |      | :                : |             
        |:______B:|      | |  Little Error: | |             
        |:______B:|      | |                | |             
        |:______B:|      | |  Power not     | |             
        |         |      | |  found.        | |             
        |:_____:  |      | |                | |             
        |    ==   |      | :                : |             
        |       O |      :  '--------------'  :             
        |       o |      :'---...______...---'              
        |       o |-._.-i__//'             \\._              
        |'-.____o_|   '-.   '-...______...-'  `-._          
        :_________:      `.____________________   `-.___.-.   Credit : Marcin Glinski
                        .'.eeeeeeeeeeeeeeeeee.'.      :___:
                       .'.eeeeeeeeeeeeeeeeeeeeee.'.         
                    :____________________________:
                    
        """
        print(text)

if __name__ == "__main__" :
    charkkich = Charkkich()
    charkkich.show_name()
    charkkich.show_hobby()
    charkkich.about()
    charkkich.show_art()

