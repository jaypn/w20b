import mariadb
import dbcreds



def update_exploit(user_id,conn):
    content = input("update your content: ")
    id = input("id: ")
    cursor = conn.cursor()
    cursor.execute("UPDATE exploits SET content=?,user_id=user_id WHERE id=?",[content,id])
    conn.commit()
    if(cursor.rowcount == 1):
        print("its updated")
    else:
        print("you have no permission to update that post")    
    cursor.close()

def sign_up(conn):
    alias = input("create an alias: ")
    password = input("create a password: ")
    cursor = conn.cursor()
    #cursor.execute("INSERT INTO hackers(id, alias ,password) VALUES (?,?,?)",["",alias, password])
    cursor.execute("INSERT INTO hackers(id, alias ,password) VALUES (NULL,?,?)",[alias, password])
    conn.commit()
    print("Alias created, you can sign in")
    cursor.close()

def see_exploit(user_id,conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exploits where user_id=?",[user_id])
    exploits = cursor.fetchall()
    if(cursor.rowcount == 1):
        for exploit in exploits:
            print(exploit[1])
    cursor.close()

def see_exploits(user_id,conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cli_social_media.exploits INNER JOIN cli_social_media.hackers on cli_social_media.exploits.user_id = cli_social_media.hackers.id where user_id != ?",[user_id])
    exploits = cursor.fetchall()
    for exploit in exploits:
        print(exploit[4] +": "+exploit[1] ) 
    cursor.close()    

def add_exploit(user_id,conn):
    content = input("Please enter a new exploit: ")

    cursor = conn.cursor()
    cursor.execute("INSERT INTO exploits(content,user_id,id) VALUES(?,?,NULL)",[content,user_id])
    conn.commit()
    print("congrats u have made an exploid!")
    cursor.close()
    

conn = None
cursor = None
try:
    conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
    cursor = conn.cursor()
    alias = input("alias: ")
    password = input("password: ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hackers WHERE alias=? AND password=?", [alias,password])
    hackers = cursor.fetchall()
    if(cursor.rowcount == 1):
        user_id = hackers[0][0]
        
        while True:
            option = input("please select an option: ")
            if option == "1":
                add_exploit(user_id,conn)
            elif option == "4":
                break  
            elif option == "2":
                see_exploit(user_id,conn)
            elif option == "3":
                see_exploits(user_id,conn)
            elif option == "5":
                update_exploit(user_id,conn)              
    elif(cursor.rowcount == 0):
        sign_up(conn) 
    else:
        print("no matching data")          
except mariadb.ProgrammingError:
    print("you need lesson")
#except mariadb.OperationalError:
    #print("there's a connection error")    
#except:
    #print("this is lazy")
finally:
    if(cursor != None):
        cursor.close()
    if(conn != None):
        conn.rollback()
        conn.close()

print("we made it to the bottom")