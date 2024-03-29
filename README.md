# autoCombind
สำหรับรวมไฟล์งาน

## Installation
```bash
pip3 install -r requirements.txt
```

## Exec
```bash
python3 autoCombind.py
```

## description

เป็นโปรแกรมที่ผมเขียนเพื่อแก้ปัญหางานในที่ทำงานเก่า โดยใช้ภาษา python เป็นงานเกี่ยวกับหนังสือ ทีนี้ปัญหาคือ เวลาลูกค้าส่งไฟล์มาจะเป็นไฟล์แยกเพื่อให้เรามารวมไฟล์ให้ ก่อนจะออกมาปริ้นเป็นเล่มเราก็ต้องมานั่งจัดไฟล์เอง ซึ่งนี่แหละปัญหา เวลาเราจัดไฟล์อาจจัดผิดได้ คำว่ามนุษย์ไม่แม่นยำและผิดพลาดอยู่บ่อยๆ และอีกอย่างคือ ถ้ามีงานมาแบบนี้อีกเราก็ต้องมานั่งจัดแบบเดิมซ้ำๆ ทำให้เสียเวลาในการทำและแก้งานอีก

### โปรแกรมนี้แก้ปัญหายังไง?
งานนี้เวลาลูกค้าส่งงานมาจะเป็นไฟล์ pdf แยกๆกันมา เป็นไฟล์ดังนี้
* ปกหนังสือ
* หน้าคั่นแต่ละบท
* สารบัญ
* เนื้อหาในแต่ละบท
#### ทีนี้ถ้าผมจะจัดแบบทำมือโดยไม่มีโปรแกรม ผมก็ต้องมานั่งยัดหน้าแต่ละหน้าเอง และสิ่งที่ต้องระวังเวลาจัดไฟล์เองคือ
* หน้าคั่นแต่ละบทต้องเป็นกระดาษสี เพราะงั้น ต้องคอยจดเลขหน้าไว้ใส่ตอนสั่งเครื่องว่าให้แทรกกระดาษสีหน้าไหน
* เข้าคู่หน้าขาวเวลาจบบท เพราะกระดาษมันมีสองหน้า เวลาขึ้นบทใหม่ถ้าเนื้อหน้ามันไม่เข้าคู่ ก็ต้องมานั่งยัดหน้าขาว

## options
ที่จริงแล้วตัวนี้มันเอารวมไฟล์เฉยๆก็ได้ ไม่จำเป็นต้องเป็นไปตามตัวอย่างงานที่พูดมา
* **หน้าคั่นบท** กรณีนี้ถ้ามีหน้าคั่นบทมันจะแทรกตัวไปด้านหน้าไฟล์แต่ละบท
* **แทรกหน้าขาวถ้าไม่มีคู่** ตามชื่อเลย ถ้ามีบทไหนที่ไม่เข้าคู่ก็จะแทรกหน้าขาวในแต่ละบท  หรือถ้ามีหน้าคั่นบทด้วยก็จะแทรกขาวหลังคั่นบทด้วย
* **เข้ารหัส** อันนี้ไว้สำหรับล๊อคไฟล์ได้ เวลาเปิดก็ต้องใส่รหัส

## screenshot
![screenshot](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjB0W0IKC-qh_8wcvsasjj3XTWWbm5LG2ZXVgnQ-g-nZWr-0uH0EVQPBsy64pQe0rMbJKmpGQIqJFj2uakOsWDIsq1LRQmCS2hsvOeJm8ezrDrD0ZJO6S8104UTO3XlZhpt7AZcOciVSSUWbQ6tOKFvruV-qryipqGObZkgfZGY1TFn9Kj4eLZmfpNW/s1948/Screenshot%202566-05-15%20at%2023.58.35.png)

## ref
[อ่านเพิ่มเติม](https://blog.9krit.dev/p/pdf.html)
