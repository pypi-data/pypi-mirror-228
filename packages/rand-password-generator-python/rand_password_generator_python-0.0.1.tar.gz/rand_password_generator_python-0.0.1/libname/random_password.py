def PassWord_Gen():
    import random
    import string
    
    no_upch = int(input("No of uppercase characters: "))
    no_lowch = int(input("No of lowercase characters: "))
    no_n = int(input("No of digits: "))
    no_s = int(input("No of special characters: "))

    s_l = []

    for i in range(0, no_upch):
        upch = random.choice(string.ascii_uppercase)
        s_l.append(upch)

    for i in range(0, no_lowch):
        loch = random.choice(string.ascii_lowercase)
        s_l.append(loch)

    for i in range(0, no_n):
        dig = random.choice(string.digits)
        s_l.append(dig)    

    for i in range(0, no_s):
        spch = random.choice(string.punctuation)
        s_l.append(spch)

    random.shuffle(s_l)

    m_password = ''.join(s_l)
    return m_password
