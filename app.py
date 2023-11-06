from flask import Flask, request, render_template

app = Flask(__name__)

# ฟังก์ชันเข้ารหัส Rail Fence Cipher
def rail_fence_cipher_encrypt(plaintext, key):
     # สร้างรายการว่างๆเป็นจำนวนสายที่เท่ากับ key
    rail_fence = [''] * key

    # ตั้งค่าตัวบ่งชี้เริ่มต้นและเขาไปทางล่าง
    row = 0
    direction = 1  # 1 หมายถึงเคลื่อนที่ไปทางล่าง, -1 หมายถึงเคลื่อนที่ขึ้นข้างบน

    # เข้ารหัสข้อความ plaintext ลงในสายของ rail_fence
    for char in plaintext:
        rail_fence[row] += char

        # เมื่อรายการรอบสุดท้ายถึง key - 1, เปลี่ยนทิศทางเพื่อกลับมาขึ้น
        if row == 0:
            direction = 1
        # เมื่อรายการรอบสุดท้ายถึง 0, เปลี่ยนทิศทางเพื่อไปทางล่าง
        elif row == key - 1:
            direction = -1

        # อัพเดทตำแหน่งของรายการ
        row += direction

    # รวมข้อมูลจาก rail_fence เป็น ciphertext
    ciphertext = ''.join(rail_fence)
    return ciphertext


# ฟังก์ชันถอดรหัส Rail Fence Cipher
def rail_fence_cipher_decrypt(ciphertext, key):
    # สร้างรายการว่างเป็นของสายเพื่อเก็บข้อมูลถอดรหัส
    decrypted_text = [''] * len(ciphertext)

    # สร้างรายการว่างเป็นจำนวนสายที่เท่ากับ key
    rail_fence = [''] * key

    # ตั้งค่าตัวบ่งชี้เริ่มต้นและเขาไปทางล่าง
    row = 0
    direction = 1  # 1 หมายถึงเคลื่อนที่ไปทางล่าง, -1 หมายถึงเคลื่อนที่ขึ้นข้างบน

    # สร้างรายการของคำนามของ rail_fence โดยใช้ตัวบ่งชี้เพื่อรวม ciphertext ในแต่ละสายของ rail_fence
    for i in range(len(ciphertext)):
        rail_fence[row] += "x"  # ใส่อะไรก็ได้, จากประสิทธิภาพที่มีต่อเทนเรือราง

        # เมื่อรายการรอบสุดท้ายถึง key - 1, เปลี่ยนทิศทางเพื่อกลับมาขึ้น
        if row == 0:
            direction = 1
        # เมื่อรายการรอบสุดท้ายถึง 0, เปลี่ยนทิศทางเพื่อไปทางล่าง
        elif row == key - 1:
            direction = -1

        # อัพเดทตำแหน่งของรายการ
        row += direction

    # กำจัดรายการของคำนามที่เราสร้างขึ้น
    rail_fence = [rail.replace("x", "") for rail in rail_fence]

    # สร้างรายการเก็บข้อมูลถอดรหัสโดยใช้ตำแหน่งของข้อความ ciphertext
    rail_index = 0
    for i in range(len(ciphertext)):
        if rail_index == 0:
            direction = 1
        elif rail_index == key - 1:
            direction = -1

    # ตรวจสอบว่ารายการของ rail_fence ไม่ว่าง
        if rail_fence[rail_index]:
            decrypted_text[i] = rail_fence[rail_index][0]
            rail_fence[rail_index] = rail_fence[rail_index][1:]
        else:
            decrypted_text[i] = "x"  # ใส่อะไรก็ได้เพื่อเลี่ยง String index out of range

    rail_index += direction
    # รวมข้อมูลถอดรหัสเป็นข้อความ
    plaintext = ''.join(decrypted_text)
    return plaintext
@app.route('/', methods=['GET', 'POST'])
def chat():
    plaintext = ""
    key = ""
    ciphertext = ""
    decrypted_text = ""

    if request.method == 'POST':
        plaintext = request.form['plaintext']
        key = int(request.form['key'])
        ciphertext = rail_fence_cipher_encrypt(plaintext, key)
        decrypted_text = rail_fence_cipher_decrypt(ciphertext, key)

    return render_template('rail_fence_cipher.html', plaintext=plaintext, key=key, ciphertext=ciphertext, decrypted_text=decrypted_text)

if __name__ == '__main__':
    app.run(debug=True)