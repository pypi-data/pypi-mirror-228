แพคเกจนี้เป็นแพคเกจ Python ที่แสดงข้อมูลเกี่ยวกับ Charkkich
===========================================================

PyPi: https://pypi.org/project/mynameischarkkich/

สวัสดีจ้าาาา นี้คือแพคเกจที่แสดงข้อมูลของ Charkkich
ท่านสามารถที่จะดูเกี่ยวกับงานอดิแรกของ charkkich ได้ แสดงภาพศิลปะ Ascii

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install mynameischarkkich

วิธีใช้งานแพ็คเพจนี้
~~~~~~~~~~~~~~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

.. code:: python

   from mynameischarkkich import Charkkich

   charkkich = Charkkich() # ประกาศชื่อ class
   charkkich.show_name() # โชว์ชื่อ
   charkkich.show_hobby() # โชว์งานอดิเรก
   charkkich.about() # เกี่ยวกับฉัน
   charkkich.show_art() #โชว์ภาพศิลปะ
   charkkich.dice() #ทอยลูกเต๋า
