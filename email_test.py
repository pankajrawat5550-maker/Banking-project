from gmail import GMail, Message

email_id = "aditya25datascience@gmail.com"
app_pass = "pdwt jeou xnjg ctlv"

def send_openacn_ack(uemail, uname, uacn, upass):
    con = GMail(email_id, app_pass)
    sub = "Congrates😊, Account opened successfully"
    utext = f"""Hello, {uname}
Welcome to ABC Bank
Your Acc No is {uacn}
Your Pass is {upass}
Kindly change your password when you login first

Thanks
ABC Bank
Noida
"""
    msg = Message(to=uemail, subject=sub, text=utext)
    con.send(msg)

def send_otp(uemail, otp, amt):
    con = GMail(email_id, app_pass)
    sub = "OTP for fund transfer"
    utext = f"""Your OTP is {otp} to transfer amount ₹{amt}

Kindly use this OTP to complete transfer.
Please don't share with anyone else.

Thanks
ABC Bank
Noida
"""
    msg = Message(to=uemail, subject=sub, text=utext)
    con.send(msg)

def send_otp_4_pass(uemail, otp):
    con = GMail(email_id, app_pass)
    sub = "OTP for password recovery"
    utext = f"""Your OTP is {otp} to recover password.

Please don't share with anyone else.

Thanks
ABC Bank
Noida
"""
    msg = Message(to=uemail, subject=sub, text=utext)
    con.send(msg)
